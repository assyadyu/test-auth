import sqlalchemy as sa

from app.common.enums import UserRoleEnum
from app.db.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    username = sa.Column(sa.String(20), nullable=False, unique=True)
    hashed_password = sa.Column(sa.LargeBinary, nullable=False)
    fullname = sa.Column(sa.String(30), nullable=True)
    email = sa.Column(sa.String(100), nullable=True, unique=True)
    is_active = sa.Column(sa.Boolean(), default=True)
    role = sa.Column(sa.Enum(UserRoleEnum), nullable=False, default=UserRoleEnum.USER.value)
