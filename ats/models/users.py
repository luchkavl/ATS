from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    admin: bool


class RegisterUser(User):
    password: str


class UserToDB(User):
    hashed_password: str
