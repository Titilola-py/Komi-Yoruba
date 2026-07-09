from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRegisterRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr
    username: str = Field(min_length=3, max_length=64)
    display_name: str = Field(min_length=1, max_length=128)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.lower() if isinstance(value, str) else value

    @field_validator("username", mode="before")
    @classmethod
    def normalize_username(cls, value: str) -> str:
        if isinstance(value, str):
            value = value.lower()
        return value

    @field_validator("username", mode="after")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not value.replace("_", "").replace("-", "").isalnum():
            raise ValueError("username can only contain letters, numbers, underscores, or hyphens")
        return value


class UserRegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    display_name: str
    is_active: bool


class UserLoginRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.lower() if isinstance(value, str) else value


class TokenResponse(BaseModel):
    """Response containing JWT access token after successful login."""

    access_token: str
    token_type: str = "bearer"
