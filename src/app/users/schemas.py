from typing import Optional
from uuid import UUID

from app.common.enums import UserRoleEnum
from app.common.schemas import BaseSchema


class UserSignupSchema(BaseSchema):
    username: str
    email: Optional[str]
    fullname: Optional[str]
    password: str
    role: Optional[UserRoleEnum] = UserRoleEnum.USER


class UserSchema(BaseSchema):
    uuid: UUID
    username: str
    email: Optional[str]
    fullname: Optional[str]
    role: UserRoleEnum
    is_active: bool


class UserSigninSchema(BaseSchema):
    username: str
    password: Optional[str]


class TokenSchema(BaseSchema):
    access_token: str
    token_type: str


class TokenPayload(BaseSchema):
    uuid: str
    username: str
    role: UserRoleEnum
    is_active: bool
