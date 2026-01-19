import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from src.presentation.main import app


class TestPricesAPI:    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_get_supported_tickers(self, client):
        response = client.get("/api/v1/prices/supported-tickers")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert "btc_usd" in data
        assert "eth_usd" in data
    
    def test_get_all_prices_invalid_ticker(self, client):
        response = client.get("/api/v1/prices/?ticker=invalid")
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
    
    def test_get_prices_by_date_invalid_params(self, client):
        response = client.get(
            "/api/v1/prices/by-date",
            params={
                "ticker": "invalid",
                "start_date": "2023-11-15T00:00:00",
                "end_date": "2023-11-16T00:00:00"
            }
        )
        
        assert response.status_code == 400
        
        response = client.get(
            "/api/v1/prices/by-date",
            params={
                "ticker": "btc_usd",
                "start_date": "2023-11-16T00:00:00",
                "end_date": "2023-11-15T00:00:00"
            }
        )
        
        assert response.status_code == 400
    
    def test_health_endpoint(self, client):
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_root_endpoint(self, client):
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data