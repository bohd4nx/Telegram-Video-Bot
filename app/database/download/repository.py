from sqlalchemy.ext.asyncio import AsyncSession

from app.database.download.model import Download
from app.database.download.schemas import DownloadCreate


async def add_download(session: AsyncSession, dto: DownloadCreate) -> None:
    session.add(Download(user_id=dto.user_id, content_type=dto.content_type, content_id=dto.content_id))
    await session.commit()
