from sqlalchemy import Integer, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url="sqlite+aiosqlite:///database/db.sqlite3", echo=False)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

