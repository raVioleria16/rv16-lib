from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from rv16_lib.exceptions import RV16Exception
from rv16_lib.configuration_manager import ConfigurationManagerProxyException
from rv16_lib.configuration_manager import ConfigurationManagerProxy


class TestConfigurationManagerProxy:

    @pytest.fixture
    def config_manager_proxy(self):
        """Fixture to create a ConfigurationManagerProxy instance for tests."""
        return ConfigurationManagerProxy()

    def test_init(self, config_manager_proxy):
        """Test the initialization of ConfigurationManagerProxy."""
        assert config_manager_proxy.hostname == "srv-configuration-manager"
        assert config_manager_proxy.port == 8000
        assert config_manager_proxy._register_path == "/register-service"
        assert config_manager_proxy._get_path == "/get-service-configuration"


    def test_register_successfully(self, config_manager_proxy):
        """Test the register method of ConfigurationManagerProxy."""

        mock_request_payload = MagicMock()
        mock_request_payload.model_dump.return_value = {"service_name": "test-service"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok"}

        with patch("rv16_lib.configuration_manager.call_srv_sync", return_value=mock_response) as mock_call_srv_sync:
            response = config_manager_proxy.register(mock_request_payload)

            mock_call_srv_sync.assert_called_once()
            assert response == {"status": "ok"}

    def test_register_failure(self, config_manager_proxy):
        """Test the register method of ConfigurationManagerProxy when registration fails."""

        mock_request_payload = MagicMock()
        mock_request_payload.model_dump.return_value = {"service_name": "test-service"}

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        with patch("rv16_lib.configuration_manager.call_srv_sync", return_value=mock_response) as mock_call_srv_sync:
            with pytest.raises(ConfigurationManagerProxyException) as exc_info:
                config_manager_proxy.register(mock_request_payload)

            mock_call_srv_sync.assert_called_once()
            assert exc_info.value.status_code == 500
            assert exc_info.value.message == "Internal Server Error"

    def test_register_exception(self, config_manager_proxy):
        """Test the register method of ConfigurationManagerProxy when call_srv_sync raises an exception."""

        mock_request_payload = MagicMock()
        mock_request_payload.model_dump.return_value = {"service_name": "test-service"}

        with patch("rv16_lib.configuration_manager.call_srv_sync", side_effect=RV16Exception(500, "Network Error")) as mock_call_srv_sync:
            with pytest.raises(RV16Exception) as exc_info:
                config_manager_proxy.register(mock_request_payload)

            mock_call_srv_sync.assert_called_once()
            assert exc_info.value.status_code == 500
            assert str(exc_info.value.message) == "Network Error"


    def test_get_successfully_without_output_type(self, config_manager_proxy):
        """Test the get method successfully returns a dict when no output_type is provided."""
        mock_request_payload = MagicMock()
        mock_request_payload.model_dump.return_value = {"service_name": "test-service"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"config_key": "config_value"}

        with patch("rv16_lib.configuration_manager.call_srv_sync", return_value=mock_response) as mock_call_srv_sync:
            response = config_manager_proxy.get(mock_request_payload)

            mock_call_srv_sync.assert_called_once()
            assert response == {"config_key": "config_value"}


    def test_get_successfully_with_output_type(self, config_manager_proxy):
        """Test the get method successfully returns a Pydantic model when output_type is provided."""
        class TestConfig(BaseModel):
            config_key: str

        mock_request_payload = MagicMock()
        mock_request_payload.model_dump.return_value = {"service_name": "test-service"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"config_key": "config_value"}

        with patch("rv16_lib.configuration_manager.call_srv_sync", return_value=mock_response) as mock_call_srv_sync:
            response = config_manager_proxy.get(mock_request_payload, output_type=TestConfig)

            mock_call_srv_sync.assert_called_once()
            assert isinstance(response, TestConfig)
            assert response.config_key == "config_value"

    def test_get_failure(self, config_manager_proxy):
        """Test the get method when the request fails."""
        mock_request_payload = MagicMock()
        mock_request_payload.model_dump.return_value = {"service_name": "test-service"}

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"detail": "Bad Request"}

        with patch("rv16_lib.configuration_manager.call_srv_sync", return_value=mock_response) as mock_call_srv_sync:
            with pytest.raises(ConfigurationManagerProxyException) as exc_info:
                config_manager_proxy.get(mock_request_payload)

            mock_call_srv_sync.assert_called_once()
            assert exc_info.value.status_code == 500
            assert exc_info.value.message == "Failed to send request: {'detail': 'Bad Request'}"

    def test_get_exception(self, config_manager_proxy):
        """Test the get method when call_srv_sync raises an exception."""
        mock_request_payload = MagicMock()
        mock_request_payload.model_dump.return_value = {"service_name": "test-service"}

        with patch("rv16_lib.configuration_manager.call_srv_sync", side_effect=RV16Exception(500, "Network Error")) as mock_call_srv_sync:
            with pytest.raises(RV16Exception) as exc_info:
                config_manager_proxy.get(mock_request_payload)

            mock_call_srv_sync.assert_called_once()
            assert exc_info.value.status_code == 500
            assert str(exc_info.value.message) == "Network Error"
