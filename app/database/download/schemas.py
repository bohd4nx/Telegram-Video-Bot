from pydantic import BaseModel


class DownloadCreate(BaseModel):
    user_id: int
    content_type: str
    content_id: str | None = None
