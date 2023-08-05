import uuid

from mjooln.core.seed import Seed, re
from mjooln.core.glass import Glass


class IdentityError(Exception):
    pass


class Identity(str, Seed, Glass):
    """ UUID string generator with convenience functions

    Inherits str, and is therefore an immutable string, with a fixed format
    as illustrated below.

    Examples::

        Identity()
            'BD8E446D_3EB9_4396_8173_FA1CF146203C'

        Identity.is_in('Has BD8E446D_3EB9_4396_8173_FA1CF146203C within')
            True

        Identity.find_one('Has BD8E446D_3EB9_4396_8173_FA1CF146203C within')
            'BD8E446D_3EB9_4396_8173_FA1CF146203C'

    """

    REGEX = r'[0-9A-F]{8}\_[0-9A-F]{4}\_[0-9A-F]{4}\_[0-9A-F]{4}' \
            r'\_[0-9A-F]{12}'

    REGEX_CLASSIC = r'[0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}' \
                    r'\-[0-9a-f]{12}'
    REGEX_COMPACT = r'[0-9a-f]{32}'
    LENGTH = 36

    @classmethod
    def from_seed(cls, str_: str):
        return cls(str_)

    @classmethod
    def is_classic(cls, str_: str):
        if len(str_) != 36:
            return False
        _regex_exact = rf'^{cls.REGEX_CLASSIC}$'
        return re.compile(_regex_exact).match(str_) is not None

    @classmethod
    def from_classic(cls, str_: str):
        str_ = str_.replace('-', '_').upper()
        return cls(str_)

    @classmethod
    def is_compact(cls, str_: str):
        if len(str_) != 32:
            return False
        _regex_exact = rf'^{cls.REGEX_COMPACT}$'
        return re.compile(_regex_exact).match(str_) is not None

    @classmethod
    def from_compact(cls, str_: str):
        str_ = '_'.join([
            str_[:8],
            str_[8:12],
            str_[12:16],
            str_[16:20],
            str_[20:]
        ]).upper()
        return cls(str_)

    @classmethod
    def elf(cls, str_):
        if isinstance(str_, Identity):
            return str_
        elif isinstance(str_, str):
            if cls.is_seed(str_):
                return cls(str_)
            elif cls.is_classic(str_):
                return cls.from_classic(str_)
            elif cls.is_compact(str_):
                return cls.from_compact(str_)
            elif cls.is_classic(str_.lower()):
                return cls.from_classic(str_.lower())
            elif cls.is_compact(str_.lower()):
                return cls.from_compact(str_.lower())

            # Try to find one or more identities in string
            ids = cls.find_seeds(str_)
            if len(ids) > 0:
                # If found, return the first
                return ids[0]
        raise IdentityError(
            f'This useless excuse for a string has no soul, '
            f'and hence no identity: \'{str_}\''
        )

    def __new__(cls,
                identity: str = None):
        if not identity:
            identity = str(uuid.uuid4()).replace('-', '_').upper()
        elif not cls.is_seed(identity):
            raise IdentityError(f'String is not valid identity: {identity}')
        instance = super().__new__(cls, identity)
        return instance

    def __repr__(self):
        return f'Identity(\'{self}\')'

    def classic(self):
        return str(self).replace('_', '-').lower()

    def compact(self):
        return str(self).replace('_', '').lower()
