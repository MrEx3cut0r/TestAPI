from typing import Generator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.session import db_manager
from src.infrastructure.database.repositories.price_repository_impl import PriceRepositoryImpl
from src.infrastructure.external.deribit_client import DeribitClient
from src.application.use_cases.get_all_prices_uc import GetAllPricesUseCase
from src.application.use_cases.get_last_price_uc import GetLastPriceUseCase
from src.application.use_cases.get_prices_by_date_uc import GetPricesByDateUseCase
from src.application.use_cases.fetch_market_prices_uc import FetchMarketPricesUseCase
from src.infrastructure.config.settings import settings


async def get_db_session() -> Generator[AsyncSession, None, None]:
    async for session in db_manager.get_session():
        yield session


def get_price_repository(
    session: AsyncSession = Depends(get_db_session)
) -> PriceRepositoryImpl:
    return PriceRepositoryImpl(session)


def get_deribit_client() -> DeribitClient:
    return DeribitClient(settings.DERIBIT_API_URL)


def get_all_prices_use_case(
    repository: PriceRepositoryImpl = Depends(get_price_repository)
) -> GetAllPricesUseCase:

    return GetAllPricesUseCase(repository)


def get_last_price_use_case(
    repository: PriceRepositoryImpl = Depends(get_price_repository)
) -> GetLastPriceUseCase:
    return GetLastPriceUseCase(repository)


def get_prices_by_date_use_case(
    repository: PriceRepositoryImpl = Depends(get_price_repository)
) -> GetPricesByDateUseCase:
    return GetPricesByDateUseCase(repository)


def get_fetch_market_prices_use_case(
    client: DeribitClient = Depends(get_deribit_client),
    repository: PriceRepositoryImpl = Depends(get_price_repository)
) -> FetchMarketPricesUseCase:
    return FetchMarketPricesUseCase(client, repository)