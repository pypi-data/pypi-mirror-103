import sqlalchemy as sa
from sqlalchemy import types
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import ColumnElement
from sqlalchemy.sql.elements import Grouping
from sqlalchemy.sql.operators import custom_op
from sqlalchemy_utils import LtreeType


def postgresql_process_path_string(value):
    return value.replace('/', '.').replace('-', '_').lower()


class PrefixPostfixQuery:
    def __init__(self, path, prefix=False, postfix=False):
        self.path = path.lower()
        self.prefix = prefix
        self.postfix = postfix

    def to_db(self):
        ret = postgresql_process_path_string(self.path)
        if self.prefix:
            ret += '.*'
        if self.postfix:
            ret = '*.' + ret
        return ret

    def __hash__(self):
        return hash((self.path, self.prefix, self.postfix))

    def __eq__(self, other):
        return other and \
               self.path == other.path and \
               self.prefix == other.prefix and \
               self.postfix == other.postfix

    def __repr__(self):
        return self.to_db()


class Ancestor(ColumnElement):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs


class Descendant(ColumnElement):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs


# postgresql ltree does not allow for hyphens in path, so need to change them to _
class PostgresSlugType(LtreeType):
    class comparator_factory(types.Concatenable.Comparator):
        def ancestor_of(self, other):
            return Ancestor(self, other)

        def descendant_of(self, other):
            return Descendant(self, other)

    def bind_processor(self, dialect):
        def process(value):
            if value:
                if isinstance(value, str):
                    return postgresql_process_path_string(value)
                elif isinstance(value, PrefixPostfixQuery):
                    return value.convert()
                elif isinstance(value, (list, tuple)):
                    return tuple(
                        [process(x) for x in value]
                    )
                else:
                    raise ValueError(f'Do not know how to convert value {value} to slug')
            else:
                return None

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return self._coerce(value)

        return process

    def literal_processor(self, dialect):
        def process(value):
            value = value.replace('/', '.').replace("'", "''").replace('-', '_')
            return "'%s'" % value

        return process

    __visit_name__ = 'LTREE'

    def _coerce(self, value):
        if value:
            return value.replace('.', '/').replace('_', '-')


ESCAPE_CHAR = '\x01'  # as low as possible, \x00 is handled incorrectly in sqlite3


class SlugType(types.TypeDecorator):
    impl = sa.UnicodeText()

    class Comparator(sa.UnicodeText.Comparator):
        def ancestor_of(self, other):
            return Ancestor(self, other)

        def descendant_of(self, other):
            return Descendant(self, other)

        def reverse_op(self, opstring, precedence=0, is_comparison=False, return_type=None):
            operator = custom_op(opstring, precedence, is_comparison, return_type)

            def against(other):
                return operator(self, other, reverse=True)

            return against

    comparator_factory = Comparator

    def process_bind_param(self, value, dialect):
        if value is not None:
            return value.replace('/', ESCAPE_CHAR)

    def process_result_value(self, value, dialect):
        if value is not None:
            return value.replace(ESCAPE_CHAR, '/')


@compiles(Descendant)
def compile_descendant(element, compiler, **kw):
    expr = Grouping(element.lhs.op('like')(element.rhs + ESCAPE_CHAR + '%').op('or')(element.lhs.op('=')(element.rhs)))
    return compiler.visit_grouping(expr)


@compiles(Descendant, 'postgresql')
def compile_descendant(element, compiler, **kw):
    lhs = element.lhs
    rhs = element.rhs
    if isinstance(rhs, str):
        rhs = rhs.replace('/', '.').replace('-', '_')
    expr = Grouping(lhs.op('<@')(rhs))
    return compiler.visit_grouping(expr)


@compiles(Ancestor)
def compile_ancestor(element, compiler, **kw):
    expr = Grouping(element.lhs.op('||')(ESCAPE_CHAR + '%').reverse_op('like')(element.rhs).op('or')(
        element.lhs.op('=')(element.rhs)
    ))
    return compiler.visit_grouping(expr)


@compiles(Ancestor, 'postgresql')
def compile_ancestor(element, compiler, **kw):
    lhs = element.lhs
    rhs = element.rhs
    if isinstance(rhs, str):
        rhs = rhs.replace('/', '.').replace('-', '_')
    expr = Grouping(lhs.op('@>')(rhs))
    return compiler.visit_grouping(expr)


@compiles(sa.UnicodeText, 'postgresql')
@compiles(sa.UnicodeText, 'postgresql')
def compile_slug(element, compiler, **kw):
    if 'type_expression' in kw:
        column = kw['type_expression']
        try:
            if isinstance(column.type.impl, SlugType):
                return 'LTREE'
        except:
            pass
    return compiler.visit_unicode(element, **kw)


class LQueryArray(types.UserDefinedType):
    def get_col_spec(self, **kw):
        return 'lquery[]'