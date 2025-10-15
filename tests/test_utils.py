from unittest.mock import patch, MagicMock, AsyncMock

import httpx
import pytest
import requests

from rv16_lib.utils import call_srv_sync, call_srv_async


@pytest.mark.asyncio
async def test_call_srv_async_success():
    """
    Tests that call_srv_async returns a response on a successful call.
    """
    test_method = "POST"
    test_url = "http://test-server/api/endpoint"
    test_payload = {"key": "value"}
    test_timeout = 5

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ok"}
    mock_response.raise_for_status.return_value = None

    with patch('rv16_lib.utils.httpx.AsyncClient.request', return_value=mock_response) as mock_async_client:
        response = await call_srv_async(method=test_method, url=test_url, json=test_payload, timeout=test_timeout)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    mock_async_client.assert_called_once_with(method=test_method, url=test_url, json=test_payload, timeout=test_timeout)



@pytest.mark.asyncio
async def test_call_srv_async_http_error():
    """
    Tests that call_srv_async raises HTTPStatusError on a 500 server error.
    """
    test_method = "POST"
    test_url = "http://test-server/api/endpoint"

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Server Error", request=MagicMock(), response=mock_response
    )

    with patch('rv16_lib.utils.httpx.AsyncClient.request', return_value=mock_response):
        with pytest.raises(httpx.HTTPStatusError):
            await call_srv_async(method=test_method, url=test_url)


@pytest.mark.asyncio
async def test_call_srv_async_request_error():
    """
    Tests that call_srv_async raises RequestError on a connection issue.
    """
    test_method = "POST"
    test_url = "http://test-server/api/endpoint"

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = httpx.ConnectError("Connection failed", request=MagicMock())

    with patch('rv16_lib.utils.httpx.AsyncClient.request', return_value=mock_response):
        with pytest.raises(httpx.RequestError):
            await call_srv_async(method=test_method, url=test_url)



def test_call_srv_sync_success():
    """
    Tests that call_srv_async returns a response on a successful call.
    """
    test_method = "POST"
    test_url = "http://test-server/api/endpoint"
    test_payload = {"key": "value"}
    test_timeout = 5

    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "ok"}

    with patch('rv16_lib.utils.requests.request', return_value=mock_response) as mock_sync_client:
        response = call_srv_sync(method=test_method, url=test_url, json=test_payload, timeout=test_timeout)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    mock_sync_client.assert_called_once_with(method=test_method, url=test_url, json=test_payload, timeout=test_timeout)


def test_call_srv_sync_returns_error_response():
    """
    Tests that call_srv_sync returns the response object for HTTP error status codes.
    """
    test_method = "POST"
    test_url = "http://test-server/api/endpoint"

    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 404

    with patch('rv16_lib.utils.requests.request', return_value=mock_response):
        response = call_srv_sync(method=test_method, url=test_url)

    assert response.status_code == 404

def test_call_srv_sync_request_exception():
    """
    Tests that call_srv_sync raises RequestException on a connection issue.
    """
    test_method = "POST"
    test_url = "http://test-server/api/endpoint"

    with patch('rv16_lib.utils.requests.request', side_effect=requests.exceptions.ConnectionError) as mock_request:
        with pytest.raises(requests.exceptions.RequestException):
            call_srv_sync(method=test_method, url=test_url)
        mock_request.assert_called_once_with(method=test_method, url=test_url)