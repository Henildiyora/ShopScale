from sqlalchemy import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from src.core.config import settings

class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass

class DatabaseSessionManager:
    """
    Singleton-like wrapper for SQLAlchemy Async Engine.
    
    Optimized to maintain a single engine instance and generate
    sessions on demand.
    """
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, host: str):
        """Initializes the async engine."""
        self._engine = create_async_engine(host, echo=False)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._engine, expire_on_commit=False
        )

    async def close(self):
        """Closes the engine connection gracefully."""
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

    async def get_session(self) -> AsyncSession:
        """dependency to provide a database session."""
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")
        
        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

# Global Instance
sessionmanager = DatabaseSessionManager()

# Dependency Injection for FastAPI
async def get_db():
    async for session in sessionmanager.get_session():
        yield session



# Explanation:
"""pydantic-settings (Config):
Logic: Instead of doing os.getenv("DB_URL") everywhere, we define a class Settings. Pydantic automatically reads the system environment.
Optimization: We instantiate it once (settings = Settings()). This is efficient because we only read the file system once at startup.

DatabaseSessionManager (OOP & Async):
Logic: We wrapped the database engine in a class. The init method starts the connection pool, and get_session gives a temporary connection to a request.
Optimization: We use asyncpg. Standard psycopg2 is synchronous (blocking). asyncpg allows our Auth service to handle thousands of login requests concurrently while waiting for the database to reply.
"yield session": This is a Python generator. It opens the session, pauses while the API route runs, and then automatically closes the session (in the finally block) even if the code crashes. This prevents memory leaks.
"""