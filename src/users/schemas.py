from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator
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


class UserUpdate(BaseSchemaModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=50)
    last_name: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=120)


class UserPublic(BaseSchemaModel):
    id: int
    profile_image: str | None
    first_name: str
    last_name: str
    full_name: str


class UserUpdatePassword(BaseSchemaModel):
    password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)
    new_confirm_password: str = Field(min_length=8)

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.new_password != self.new_confirm_password:
            raise ValueError("New passwords do not match")
        return self


class UserPrivate(UserPublic):
    email: EmailStr


class Message(BaseModel):
    message: str
