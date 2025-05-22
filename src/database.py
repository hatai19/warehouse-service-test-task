from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

postgres_url = f"postgresql+asyncpg://postgres:postgres@db:5432/postgres"

async_engine = create_async_engine(postgres_url)
async_session = async_sessionmaker(async_engine)