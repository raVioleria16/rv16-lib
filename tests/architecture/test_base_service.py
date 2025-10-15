import pytest
from unittest.mock import Mock, patch, MagicMock

from starlette import status

from rv16_lib.architecture.base_service import BaseService
from rv16_lib.exceptions import RV16Exception


class TestBaseService:

    @pytest.fixture
    def base_service(self):
        """Fixture to create a BaseService instance for tests."""
        service = BaseService()
        service.service_name = "test_service"
        return service

    def test_init(self):
        """Test the initialization of BaseService."""
        service = BaseService()
        assert service.service_name is None
        assert service.providers == {}

    def test_register_service(self, base_service):
        """Test the service registration process."""
        mock_cm_proxy = MagicMock()
        mock_cm_proxy.register.return_value = {"status": "ok"}
        provider = "test_provider"
        configuration = {"key": "value"}

        with patch('rv16_lib.architecture.base_service.ServiceRegistrationRequest'):

            response = base_service.register_service(mock_cm_proxy, provider, configuration)
            mock_cm_proxy.register.assert_called_once()

            assert response == {"status": "ok"}


    def test_initialize_service(self, base_service):
        """Test that initialize_service raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            base_service.initialize_service()

    def test_get_provider_success(self, base_service):
        """Test successfully retrieving a supported provider."""
        mock_provider = Mock()
        provider_name = "supported_provider"
        base_service.providers[provider_name] = mock_provider

        provider = base_service.get_provider(provider_name)

        assert provider == mock_provider

    def test_get_provider_not_supported(self, base_service):
        """Test that getting an unsupported provider raises an RV16Exception."""
        provider_name = "unsupported_provider"

        with pytest.raises(RV16Exception) as exc_info:
            base_service.get_provider(provider_name)

        assert exc_info.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert exc_info.value.message == f"Provider {provider_name} not supported."