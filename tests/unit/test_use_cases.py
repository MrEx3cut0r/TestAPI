import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from src.application.use_cases.get_all_prices_uc import GetAllPricesUseCase
from src.application.use_cases.get_last_price_uc import GetLastPriceUseCase
from src.application.use_cases.get_prices_by_date_uc import GetPricesByDateUseCase
from src.domain.entities.price import Price
from src.domain.exceptions.domain_exceptions import InvalidTickerException


class TestGetAllPricesUseCase:    
    @pytest.mark.asyncio
    async def test_execute_success(self):
        mock_repository = AsyncMock()
        mock_repository.get_all.return_value = [
            Price(ticker="btc_usd", price=45000.50, timestamp=1700000000),
            Price(ticker="btc_usd", price=45100.75, timestamp=1700000100),
        ]
        
        use_case = GetAllPricesUseCase(mock_repository)
        
        result = await use_case.execute("btc_usd")
        
        assert len(result) == 2
        assert result[0].ticker == "btc_usd"
        assert result[0].price == 45000.50
        mock_repository.get_all.assert_called_once_with("btc_usd")
    
    @pytest.mark.asyncio
    async def test_execute_invalid_ticker(self):
        mock_repository = AsyncMock()
        use_case = GetAllPricesUseCase(mock_repository)
        
        with pytest.raises(InvalidTickerException):
            await use_case.execute("invalid_ticker")
        
        mock_repository.get_all.assert_not_called()


class TestGetLastPriceUseCase:    
    @pytest.mark.asyncio
    async def test_execute_success(self):
        mock_repository = AsyncMock()
        mock_repository.get_last.return_value = Price(
            ticker="btc_usd",
            price=45000.50,
            timestamp=1700000000
        )
        
        use_case = GetLastPriceUseCase(mock_repository)
        result = await use_case.execute("btc_usd")
        
        assert result is not None
        assert result.ticker == "btc_usd"
        assert result.price == 45000.50
        mock_repository.get_last.assert_called_once_with("btc_usd")
    
    @pytest.mark.asyncio
    async def test_execute_no_price_found(self):
        mock_repository = AsyncMock()
        mock_repository.get_last.return_value = None
        
        use_case = GetLastPriceUseCase(mock_repository)
        result = await use_case.execute("btc_usd")
        
        assert result is None


class TestGetPricesByDateUseCase:    
    @pytest.mark.asyncio
    async def test_execute_success(self):
        mock_repository = AsyncMock()
        mock_repository.get_by_date_range.return_value = [
            Price(ticker="btc_usd", price=45000.50, timestamp=1700000000),
        ]
        
        use_case = GetPricesByDateUseCase(mock_repository)
        
        start_date = datetime(2023, 11, 15)
        end_date = datetime(2023, 11, 16)
        
        result = await use_case.execute("btc_usd", start_date, end_date)
        
        assert len(result) == 1
        mock_repository.get_by_date_range.assert_called_once_with(
            "btc_usd", start_date, end_date
        )
    
    @pytest.mark.asyncio
    async def test_execute_invalid_dates(self):
        mock_repository = AsyncMock()
        use_case = GetPricesByDateUseCase(mock_repository)
        
        start_date = datetime(2023, 11, 16)
        end_date = datetime(2023, 11, 15)
        
        with pytest.raises(ValueError):
            await use_case.execute("btc_usd", start_date, end_date)
        
        mock_repository.get_by_date_range.assert_not_called()