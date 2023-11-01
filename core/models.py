from typing import Optional, Union, Dict, List, Any

from django.db import models
from django.utils.functional import cached_property

models.Model


class TokenUser:
    """
    A dummy user class modeled after django.contrib.auth.models.AnonymousUser.
    Used in conjunction with the `JWTStatelessUserAuthentication` backend to
    implement single sign-on functionality across services which share the same
    secret key.  `JWTStatelessUserAuthentication` will return an instance of this
    class instead of a `User` model instance.  Instances of this class act as
    stateless user objects which are backed by validated tokens.
    """

    # User is always active since Simple JWT will never issue a token for an
    # inactive user
    is_active = True

    def __init__(self, token: Dict[str, Any]) -> None:
        self.token = token

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self)

    def __str__(self):
        return "%s object (%s)" % (self.__class__.__name__, self.pk)

    @cached_property
    def id(self) -> Union[int, str]:
        return self.token["user_id"]

    @cached_property
    def pk(self) -> Union[int, str]:
        return self.id

    @cached_property
    def username(self) -> str:
        return self.token.get("username", "")

    @cached_property
    def is_staff(self) -> bool:
        return self.token.get("is_staff", False)

    @cached_property
    def is_superuser(self) -> bool:
        return self.token.get("is_superuser", False)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TokenUser):
            return NotImplemented
        return self.id == other.id

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.id)

    def save(self) -> None:
        raise NotImplementedError("Token users have no DB representation")

    def delete(self) -> None:
        raise NotImplementedError("Token users have no DB representation")

    def set_password(self, raw_password: str) -> None:
        raise NotImplementedError("Token users have no DB representation")

    def check_password(self, raw_password: str) -> None:
        raise NotImplementedError("Token users have no DB representation")

    @property
    def groups(self) -> None:
        return None

    @property
    def user_permissions(self) -> None:
        return None

    def get_group_permissions(self, obj: Optional[object] = None) -> set:
        return set()

    def get_all_permissions(self, obj: Optional[object] = None) -> set:
        return set()

    def has_perm(self, perm: str, obj: Optional[object] = None) -> bool:
        return False

    def has_perms(self, perm_list: List[str], obj: Optional[object] = None) -> bool:
        return False

    def has_module_perms(self, module: str) -> bool:
        return False

    @property
    def is_anonymous(self) -> bool:
        return False

    @property
    def is_authenticated(self) -> bool:
        return True

    def get_username(self) -> str:
        return self.username

    # def __getattr__(self, attr: str) -> Optional[Any]:
    #     """This acts as a backup attribute getter for custom claims defined in Token serializers."""
    #     return self.token.get(attr, None)
