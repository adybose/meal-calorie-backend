import pytest
from unittest.mock import patch, MagicMock


def test_get_calories_success(client, mocker):
    # Mock the USDA API responses
    mock_search_response = MagicMock()
    mock_search_response.status_code = 200
    mock_search_response.json.return_value = {
        "foods": [
            {
                "description": "Apple, raw",
                "fdcId": 12345
            }
        ]
    }
    mock_details_response = MagicMock()
    mock_details_response.status_code = 200
    mock_details_response.json.return_value = {
        "servingSize": 100,
        "servingSizeUnit": "g",
        "householdServingFullText": "1 medium apple",
        "foodNutrients": [
            {
                "nutrient": {"id": 1008, "name": "Energy", "unitName": "kcal"},
                "amount": 52.0
            }
        ]
    }

    def mock_get(url, params=None):
        if "search" in url:
            return mock_search_response
        elif "food" in url:
            return mock_details_response
        return MagicMock(status_code=404)

    mocker.patch("requests.get", side_effect=mock_get)
    request_data = {
        "dish_name": "Apple",
        "mode": "servings",
        "servings": 1.0
    }
    response = client.post("/get-calories", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["dish_name"] == "Apple"
    assert "total_nutrients" in data
    assert len(data["total_nutrients"]) > 0


def test_get_calories_invalid_servings(client, mocker):
    request_data = {
        "dish_name": "Apple",
        "mode": "servings",
        "servings": 0
    }
    response = client.post("/get-calories", json=request_data)
    assert response.status_code == 400
    assert "Invalid servings" in response.json()["detail"]


def test_get_calories_no_foods_found(client, mocker):
    # Mock empty foods response
    mock_search_response = MagicMock()
    mock_search_response.status_code = 200
    mock_search_response.json.return_value = {
        "foods": []
    }
    mocker.patch("requests.get", return_value=mock_search_response)
    request_data = {
        "dish_name": "NonexistentFood",
        "mode": "servings",
        "servings": 1.0
    }
    response = client.post("/get-calories", json=request_data)
    assert response.status_code == 404
    assert "Dish not found" in response.json()["detail"]


def test_get_calories_usda_api_error(client, mocker):
    # Mock API error
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mocker.patch("requests.get", return_value=mock_response)
    request_data = {
        "dish_name": "Apple",
        "mode": "servings",
        "servings": 1.0
    }
    response = client.post("/get-calories", json=request_data)
    assert response.status_code == 500
    assert "USDA API error" in response.json()["detail"]


def test_get_calories_details_api_error(client, mocker):
    # Mock search success but details failure
    mock_search_response = MagicMock()
    mock_search_response.status_code = 200
    mock_search_response.json.return_value = {
        "foods": [
            {
                "description": "Apple, raw",
                "fdcId": 12345
            }
        ]
    }
    mock_details_response = MagicMock()
    mock_details_response.status_code = 404

    def mock_get(url, params=None):
        if "search" in url:
            return mock_search_response
        elif "food" in url:
            return mock_details_response
        return MagicMock(status_code=404)

    mocker.patch("requests.get", side_effect=mock_get)
    request_data = {
        "dish_name": "Apple",
        "mode": "servings",
        "servings": 1.0
    }
    response = client.post("/get-calories", json=request_data)
    assert response.status_code == 500
    assert "USDA details API error" in response.json()["detail"]


def test_get_calories_grams_mode(client, mocker):
    # Mock the USDA API responses
    mock_search_response = MagicMock()
    mock_search_response.status_code = 200
    mock_search_response.json.return_value = {
        "foods": [
            {
                "description": "Apple, raw",
                "fdcId": 12345
            }
        ]
    }
    mock_details_response = MagicMock()
    mock_details_response.status_code = 200
    mock_details_response.json.return_value = {
        "servingSize": 100,
        "servingSizeUnit": "g",
        "householdServingFullText": "1 medium apple",
        "foodNutrients": [
            {
                "nutrient": {"id": 1008, "name": "Energy", "unitName": "kcal"},
                "amount": 52.0
            }
        ]
    }

    def mock_get(url, params=None):
        if "search" in url:
            return mock_search_response
        elif "food" in url:
            return mock_details_response
        return MagicMock(status_code=404)

    mocker.patch("requests.get", side_effect=mock_get)
    request_data = {
        "dish_name": "Apple",
        "mode": "grams",
        "servings": 200.0  # 200 grams
    }
    response = client.post("/get-calories", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "grams"
    assert data["amount"] == 200.0


def test_get_calories_no_nutrients(client, mocker):
    # Mock responses with no nutrients
    mock_search_response = MagicMock()
    mock_search_response.status_code = 200
    mock_search_response.json.return_value = {
        "foods": [
            {
                "description": "Test Food",
                "fdcId": 12345
            }
        ]
    }
    mock_details_response = MagicMock()
    mock_details_response.status_code = 200
    mock_details_response.json.return_value = {
        "servingSize": 100,
        "servingSizeUnit": "g",
        "householdServingFullText": "1 serving",
        "foodNutrients": []  # No nutrients
    }

    def mock_get(url, params=None):
        if "search" in url:
            return mock_search_response
        elif "food" in url:
            return mock_details_response
        return MagicMock(status_code=404)

    mocker.patch("requests.get", side_effect=mock_get)
    request_data = {
        "dish_name": "Test Food",
        "mode": "servings",
        "servings": 1.0
    }
    response = client.post("/get-calories", json=request_data)
    assert response.status_code == 404
    assert "No nutrient data available" in response.json()["detail"]


def test_get_calories_no_suitable_match(client, mocker):
    # Mock search response with foods that don't match well
    mock_search_response = MagicMock()
    mock_search_response.status_code = 200
    mock_search_response.json.return_value = {
        "foods": [
            {"description": "Rice paper", "fdcId": 12345}
        ]
    }
    mocker.patch("requests.get", return_value=mock_search_response)
    request_data = {
        "dish_name": "Paper Plane",  # Non-existent or poor match
        "mode": "servings",
        "servings": 1.0
    }
    response = client.post("/get-calories", json=request_data)
    assert response.status_code == 404
    assert "Dish not found" in response.json()["detail"]


def test_get_calories_invalid_request_data(client, mocker):
    # Missing required fields
    request_data = {
        "dish_name": "Apple"
        # Missing mode and servings
    }
    response = client.post("/get-calories", json=request_data)
    assert response.status_code == 422  # Validation error
