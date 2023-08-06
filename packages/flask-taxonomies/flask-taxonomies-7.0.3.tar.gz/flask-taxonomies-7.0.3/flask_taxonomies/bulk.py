from collections import namedtuple, defaultdict
from typing import Iterable, List

from sqlalchemy import or_, cast
from sqlalchemy.orm import joinedload

from flask_taxonomies.api import TaxonomyTerm
from flask_taxonomies.api import TermStatusEnum
from flask_taxonomies.fields import PrefixPostfixQuery, LQueryArray

from sqlalchemy.dialects.postgresql import array, dialect

class TermWithPriority:
    def __init__(self, term: TaxonomyTerm, priority: int):
        self.term = term
        self.priority = priority

    def __repr__(self):
        return f'{self.term}[{self.priority}]'


class CriterionResult:
    def __init__(self, criterion, terms: List[TermWithPriority]):
        self.criterion = criterion
        self.terms = terms

    def __repr__(self):
        return f'{self.criterion}{repr(self.terms)}'


class SingleQueryResult:
    def __init__(self, d, results: List[CriterionResult]):
        self.d = d
        self.results = results

    def __repr__(self):
        return repr(self.results)

    def __str__(self):
        return repr(self.results)

def bulk_taxonomy_query(
        db,
        taxonomy_code,
        query_data,
        query_function,
        query_combining_function,
        result_preprocess_function,
        result_match_function
) -> List[SingleQueryResult]:
    """
    Selects taxonomy terms by multiple search criteria.

    It works the following way:

      1. query_data is an array of query data (for example, oai-pmh records). Items in this array are
         called 'd'
         Each 'd' is converted to an array of query criteria via the query_function function.
      2. An array of array of query criteria is passed to the query_combining_function that
         creates db query, using TaxonomyTerm class
      3. TaxonomyTerm query selecting terms matching the created query and their ancestors
         is executed on the database.
      4. The resulting terms are split into "all_terms" and "leaf_terms" dictionaries and both
         are passed to the result_preprocess_function. The function returns a context filled
         with (somehow) preprocessed terms
      5. For each 'd', the result_match_function is called with 'd',
         list of criteria from #1 and context. The function must return
         an instance of SingleQueryResult
      6. A list of these (in the same order as input data) is returned

    :param taxonomy_code:       the taxonomy code
    :param query_data:          array of query criteria
    :param query_function:      function converting query criterium to DB query
    :param result_preprocess_function:      function for preprocessing terms from DB
    :param result_match_function:   function that matches pre-processed terms query criteria
    :return:
    """
    call_context = {}
    all_terms = db.session.query(TaxonomyTerm.id, TaxonomyTerm.parent_id).filter(
        TaxonomyTerm.taxonomy_code == taxonomy_code,
        TaxonomyTerm.status == TermStatusEnum.alive
    )
    terms = all_terms
    d_with_criteria = [
        (d, tuple(query_function(d))) for d in query_data
    ]
    terms = terms.filter(
        query_combining_function(
            [d[1] for d in d_with_criteria],
            call_context
        )
    )
    terms = terms.cte('cte', recursive=True)

    ancestors = all_terms.join(terms, TaxonomyTerm.id == terms.c.parent_id)

    recursive_q = terms.union(ancestors)
    q = db.session.query(recursive_q)
    ids = [x[0] for x in q]
    terms = {
        t.id: t for t in
        db.session
            .query(TaxonomyTerm)
            .options(joinedload(TaxonomyTerm.taxonomy, innerjoin=True))
            .filter(TaxonomyTerm.id.in_(ids))
    }
    parent_terms = set(t.parent_id for t in terms.values())
    leaf_terms = {
        k: v for k, v in terms.items() if k not in parent_terms
    }
    ctx = result_preprocess_function(leaf_terms, terms, call_context)
    for d in d_with_criteria:
        yield result_match_function(d[0], d[1], ctx)


def slug_taxonomy_query(
        db,
        taxonomy_code,
        slug_function,
        data
):
    def combining_function(queries, call_context):
        regexs = []
        for qs in queries:
            for q in qs:
                regexs.append(q.to_db())
                if q.prefix:
                    call_context['prefix'] = True
                if q.postfix:
                    call_context['postfix'] = True
        return TaxonomyTerm.slug.op('?')(cast(regexs, LQueryArray))

    def result_preprocess_function(leaf_terms, terms, call_context):
        ctx = defaultdict(list)
        for lt in terms.values():
            slug = lt.slug.split('/')

            if call_context.get('prefix'):
                for i in range(1, len(slug) + 1):
                    ctx[PrefixPostfixQuery('/'.join(slug[:i]), prefix=True)].append(
                        TermWithPriority(lt, len(slug) - i)
                    )

            if call_context.get('postfix'):
                for i in range(0, len(slug)):
                    ctx[PrefixPostfixQuery('/'.join(slug[i:]), postfix=True)].append(
                        TermWithPriority(lt, i)
                    )

                if call_context.get('prefix'):
                    for i in range(len(slug)):
                        for j in range(i + 1, len(slug)):
                            ctx[PrefixPostfixQuery('/'.join(slug[i:j]), prefix=True, postfix=True)].append(
                                TermWithPriority(lt, len(slug) - (j - i))
                            )
        return ctx

    def result_match_function(d, criteria, ctx):
        ret = []
        for q in criteria:
            found = ctx.get(q)
            if found:
                found.sort(key=lambda x: x.priority)
                ret.append(
                    CriterionResult(q, found)
                )
        return SingleQueryResult(d, ret)

    for res in bulk_taxonomy_query(
            db,
            taxonomy_code,
            data,
            slug_function,
            combining_function,
            result_preprocess_function,
            result_match_function):
        yield res


ExtraField = namedtuple('ExtraField', 'field_array, priority, single_value')


def get_json_path(q, path):
    for p in path:
        q = q.op('->')(p)
    return q


def title_taxonomy_query(
        db,
        taxonomy_code,
        fields: Iterable[ExtraField],
        title_function,
        data,
        full_path_required=True
):
    """

    :param db:
    :param taxonomy_code:
    :param fields:
    :param title_function:  A function returning for each 'd' a list of title terms.
      Each title term is a path of titles (from the root of the taxonomy). For example,
      if 'd' is :
      ```
        {
            orgunits: [
                ['uct', 'dpt of anorganic chemistry'],
                ['university of chemistry and technology', 'department of anorganic chemistry']
            ]
        }
      ```
      the result of the title function would be a generator returning:
      ```
        ['uct', 'dpt of anorganic chemistry'],
        ['university of chemistry and technology', 'department of anorganic chemistry']
      ```
    :param data: a list of records
    :param full_path_required if True, the output of the title function must be a path
           from the root, if False the path may not start in the root
    :return:
    """

    def combining_function(queries, call_context):
        or_query = []
        for fld in fields:
            # get only the values matching the end of the query
            values = list(set([q[-1] for qs in queries for q in qs]))

            if fld.single_value:
                # return fld->
                query_term = get_json_path(
                    TaxonomyTerm.extra_data,
                    fld.field_array[:-1]
                ).op('->>')(fld.field_array[-1]).in_(tuple(values))
            else:
                query_term = get_json_path(
                    TaxonomyTerm.extra_data,
                    fld.field_array
                ).op('?|')(array(values))
            or_query.append(query_term)
        return or_(*or_query)

    def deep_get(d, flds):
        for fld in flds:
            d = d.get(fld)
            if not d:
                break
        return d

    def result_preprocess_function(leaf_terms, terms, call_context):
        candidates = namedtuple('candidates', 'titles, leaf_terms') \
            (defaultdict(list), leaf_terms)
        for t in terms.values():
            for fld in fields:
                n = deep_get(t.extra_data, fld.field_array)
                if n:
                    for nn in [n] if fld.single_value else n:
                        candidates.titles[(nn, t.level)].append((t, fld.priority))
                        if not full_path_required:
                            candidates.titles[nn].append((t, fld.priority))
        return candidates

    def result_match_function(d, criteria, ctx):
        possibilities = None
        criteria_results = []
        for criterion in criteria:
            for level, title in reversed(list(enumerate(criterion))):
                if full_path_required:
                    found = ctx.titles.get((title, level), [])
                else:
                    found = ctx.titles.get(title, [])
                if possibilities is None:
                    possibilities = [
                        ([x[0]], x[1]) for x in found
                    ]
                else:
                    found = {
                        x[0].id: x for x in found
                    }
                    filtered_possibilities = []
                    for p in possibilities:
                        if p[0][0].parent_id in found:
                            f = found[p[0][0].parent_id]
                            filtered_possibilities.append((
                                [
                                    f[0],
                                    *p[0]
                                ],
                                f[1] + p[1]
                            ))
                    possibilities = filtered_possibilities
            possibilities.sort(key=lambda x: x[1])
            criteria_results.append(CriterionResult(
                criterion, [
                    TermWithPriority(x[0][-1], x[1]) for x in possibilities
                ]
            ))
        return SingleQueryResult(d, criteria_results)

    return bulk_taxonomy_query(
        db,
        taxonomy_code,
        data,
        title_function,
        combining_function,
        result_preprocess_function,
        result_match_function
    )
