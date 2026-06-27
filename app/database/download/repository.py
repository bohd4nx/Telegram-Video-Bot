from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.download.model import Download
from app.database.download.schemas import DownloadCreate


async def add_download(session: AsyncSession, dto: DownloadCreate) -> None:
    session.add(Download(user_id=dto.user_id, content_type=dto.content_type, content_id=dto.content_id))
    await session.commit()


async def count_url_downloads_today(session: AsyncSession, user_id: int) -> int:
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    result = await session.execute(
        select(func.count())
        .select_from(Download)
        .where(
            Download.user_id == user_id,
            Download.content_type != "video_file",
            Download.created_at >= today,
        )
    )
    return result.scalar_one()
