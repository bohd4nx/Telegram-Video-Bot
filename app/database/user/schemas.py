from pydantic import BaseModel


class UserCreate(BaseModel):
    user_id: int
    username: str | None = None
