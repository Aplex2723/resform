from typing import AsyncGenerator, List
import os
from dotenv import load_dotenv

from fastapi import Depends
from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

load_dotenv()
# DATABASE_URL = "sqlite+aiosqlite:///./test.db"
DBNAME = os.getenv('DB_NAME')
DBHOST = os.getenv('DB_HOST')
DBPASSWORD = os.getenv('DB_PASSWORD')
DBUSER = os.getenv('DB_USER')
DATABASE_URL = f"mysql+aiomysql://{DBUSER}:{DBPASSWORD}@{DBHOST}/{DBNAME}"
print(DATABASE_URL)



class Base(DeclarativeBase):
    pass


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )
    credits = Column(Integer, default=25)
        # Relación uno a muchos con Suscripciones
    subscriptions = relationship("Subscription", back_populates="user")


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    credits_monthly = Column(Integer, default=25)
    credits_anual = Column(Integer)

    # Relación uno a muchos con Suscripciones
    subscriptions = relationship("Subscription", back_populates="plan")

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), ForeignKey("user.id"))
    plan_id = Column(Integer, ForeignKey("plans.id"))
    start_date = Column(DateTime, server_default=func.now())
    end_date = Column(DateTime)

    # Definir una propiedad calculada para el tipo de suscripción
    @property
    def tipo(self):
        if (self.end_date - self.start_date).days >= 365:
            return "anual"
        else:
            return "mensual"

    # Relaciones con User y Plan
    user = relationship("User", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")

# class AvailableCredits(Base):
#     __tablename__ = "credits_available"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(String(255), ForeignKey("user.id"))
#     plan_id = Column(Integer, ForeignKey("plans.id"))
#     credits_available  = Column(Integer)

#     # Relaciones con User y Plan
#     user = relationship("User", back_populates="credits")
#     plan = relationship("Plan", back_populates="credits")

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = async_session_maker()
    try:
        yield db
    finally:
        await db.close()
