from datetime import datetime
from typing import List
from fastapi import APIRouter, Query, HTTPException, Depends
from src.application.dtos.price_dto import PriceDTO
from src.application.use_cases.get_all_prices_uc import GetAllPricesUseCase
from src.application.use_cases.get_last_price_uc import GetLastPriceUseCase
from src.application.use_cases.get_prices_by_date_uc import GetPricesByDateUseCase
from src.presentation.models.price_schemas import PriceResponse, PriceListResponse, ErrorResponse
from src.presentation.models.request_schemas import DateFilterRequest
from src.presentation.api.dependencies import (
    get_all_prices_use_case,
    get_last_price_use_case,
    get_prices_by_date_use_case,
)
from src.domain.exceptions.domain_exceptions import (
    InvalidTickerException,
    PriceNotFoundException
)

router = APIRouter(prefix="/prices", tags=["prices"])

@router.get(
    "/",
    response_model=PriceListResponse,
    summary="Получить все цены по тикеру",
    responses={
        400: {"model": ErrorResponse, "description": "Неверный запрос"},
        404: {"model": ErrorResponse, "description": "Цены не найдены"}
    }
)
async def get_all_prices(
    ticker: str = Query(..., description="Тикер валютной пары (btc_usd или eth_usd)"),
    use_case: GetAllPricesUseCase = Depends(get_all_prices_use_case)
):
    try:
        prices_dto = await use_case.execute(ticker)
        
        if not prices_dto:
            raise HTTPException(
                status_code=404,
                detail=f"No prices found for ticker: {ticker}"
            )
        
        prices_response = [
            PriceResponse(
                id=price_dto.id,
                ticker=price_dto.ticker,
                value=price_dto.price, 
                timestamp=price_dto.timestamp,
                datetime=datetime.fromtimestamp(price_dto.timestamp)
            ) for price_dto in prices_dto
        ]
        
        return PriceListResponse(
            ticker=ticker,
            prices=prices_response,
            count=len(prices_response)
        )
        
    except InvalidTickerException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.get(
    "/last",
    response_model=PriceResponse,
    summary="Получить последнюю цену по тикеру",
    responses={
        400: {"model": ErrorResponse, "description": "Неверный запрос"},
        404: {"model": ErrorResponse, "description": "Цена не найдена"}
    }
)
async def get_last_price(
    ticker: str = Query(..., description="Тикер валютной пары (btc_usd или eth_usd)"),
    use_case: GetLastPriceUseCase = Depends(get_last_price_use_case)
):
    try:
        price_dto = await use_case.execute(ticker)
        
        if not price_dto:
            raise HTTPException(
                status_code=404,
                detail=f"No prices found for ticker: {ticker}"
            )
        
        return PriceResponse.from_dto(price_dto)
        
    except InvalidTickerException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get(
    "/by-date",
    response_model=PriceListResponse,
    summary="Получить цены по тикеру с фильтром по дате",
    responses={
        400: {"model": ErrorResponse, "description": "Неверный запрос"},
        404: {"model": ErrorResponse, "description": "Цены не найдены"}
    }
)
async def get_prices_by_date(
    ticker: str = Query(..., description="Тикер валютной пары (btc_usd или eth_usd)"),
    start_date: datetime = Query(..., description="Начальная дата (YYYY-MM-DDTHH:MM:SS)"),
    end_date: datetime = Query(..., description="Конечная дата (YYYY-MM-DDTHH:MM:SS)"),
    use_case: GetPricesByDateUseCase = Depends(get_prices_by_date_use_case)
):
    try:
        if start_date > end_date:
            raise HTTPException(
                status_code=400,
                detail="start_date cannot be greater than end_date"
            )
        
        prices_dto = await use_case.execute(ticker, start_date, end_date)
        
        if not prices_dto:
            raise HTTPException(
                status_code=404,
                detail=f"No prices found for ticker {ticker} in date range "
                      f"{start_date} to {end_date}"
            )
        
        prices_response = [
            PriceResponse.from_dto(price_dto) for price_dto in prices_dto
        ]
        
        return PriceListResponse(
            ticker=ticker,
            prices=prices_response,
            count=len(prices_response)
        )
        
    except InvalidTickerException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get(
    "/supported-tickers",
    summary="Получить список поддерживаемых тикеров",
    response_model=List[str]
)
async def get_supported_tickers():
    from src.domain.value_objects.currency import CurrencyPair
    return CurrencyPair.list()