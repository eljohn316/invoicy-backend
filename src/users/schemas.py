from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.alias_generators import to_camel


class BaseSchemaModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_by_name=True,
        serialize_by_alias=True,
        alias_generator=to_camel,
    )


class Token(BaseSchemaModel):
    access_token: str
    token_type: str


class UserBase(BaseSchemaModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserPublic(BaseSchemaModel):
    id: int
    profile_image: str | None
    first_name: str
    last_name: str
    full_name: str


class UserPrivate(UserPublic):
    email: EmailStr


class UserUpdate(BaseSchemaModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=50)
    last_name: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=120)
    profile_image: str | None = Field(default=None, min_length=1, max_length=200)
