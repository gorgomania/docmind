from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def check_password(cls, value: str) -> str:
        if not (any(ch.isdigit() for ch in value) and (any(ch.isalpha() for ch in value))):
            raise ValueError("Password must contain numbers and letters")
        return value


class UserRead(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attribures=True)
