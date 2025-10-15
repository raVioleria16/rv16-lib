import pytest
from unittest.mock import Mock, patch, MagicMock

from rv16_lib.architecture.base_service_connector import BaseServiceConnector, BaseServiceConfig


class TestBaseServiceConfig:
    """
    Test suite for the BaseServiceConfig Pydantic model.
    """

    def test_base_service_config_valid_data(self):
        """
        Tests successful creation of BaseServiceConfig with valid data.
        """
        config_data = {
            "provider": "google",
            "hostname": "api.google.com"
        }
        config = BaseServiceConfig(**config_data)

        assert config.provider == "google"
        assert config.hostname == "api.google.com"
        assert isinstance(config, BaseServiceConfig)

    @pytest.mark.parametrize("provider, hostname", [
        ("my_provider", "localhost:8080")
    ])
    def test_base_service_config_valid_inputs(self, provider, hostname):
        """
        Tests successful creation with various valid string combinations.
        """
        config = BaseServiceConfig(provider=provider, hostname=hostname)

        assert config.provider == provider
        assert config.hostname == hostname

    @pytest.mark.parametrize("missing_field", [
        "provider",
        "hostname"
    ])
    def test_missing_required_field(self, missing_field):
        """
        Tests that a ValueError (ValidationError) is raised when a required field is missing.
        """
        data = {
            "provider": "test_provider",
            "hostname": "test_hostname"
        }
        del data[missing_field]

        with pytest.raises(ValueError) as excinfo:
            BaseServiceConfig(**data)

        assert missing_field in str(excinfo.value)
        assert "Field required" in str(excinfo.value)

    @pytest.mark.parametrize("field, invalid_value", [
        ("provider", 12345),
        ("provider", [1, 2, 3]),
        ("provider", None),
        ("hostname", 12345),
        ("hostname", [1, 2, 3]),
        ("hostname", None),
    ])
    def test_invalid_data_type(self, field, invalid_value):
        """
        Tests that a ValueError (ValidationError) is raised when fields have the wrong data type.
        """
        data = {
            "provider": "default_provider",
            "hostname": "default_hostname"
        }
        data[field] = invalid_value

        with pytest.raises(ValueError) as excinfo:
            BaseServiceConfig(**data)

        assert field in str(excinfo.value)
        assert "validation error" in str(excinfo.value)


class TestBaseServiceConnector:
    """
    Test suite for the BaseServiceConnector class.
    """

    @pytest.fixture
    def mock_config(self):
        """
        Provides a mock config object for testing.
        """
        config = MagicMock(spec=BaseServiceConfig)
        config.provider = "test_provider"
        config.hostname = "test_hostname"
        return config

    @pytest.fixture
    def mock_configuration_type(self):
        class MockConfigurationType(MagicMock):
            key: str
        return MockConfigurationType()

    @pytest.fixture
    def connector(self, mock_config):
        """
        Provides an instance of BaseServiceConnector with a mock config.
        """
        return BaseServiceConnector(config=mock_config)

    def test_init(self, connector, mock_config):
        """
        Tests the initialization of the BaseServiceConnector.
        """
        assert connector.url is None
        assert connector.connection is None
        assert connector.config == mock_config
        assert connector.provider == "test_provider"
        assert connector.srv_name == "test_hostname"

    @pytest.mark.parametrize("output_type", [
        dict,
        None,
        mock_configuration_type
    ])
    def test_setup_connections(self, connector, output_type):
        """
        Tests the setup_connections method.
        """
        cm_proxy_result = {"key": "value"}
        cm_provider = "test_cm_provider"
        mock_cm_proxy_instance = MagicMock()
        mock_cm_proxy_instance.get.return_value = cm_proxy_result

        with patch(
            'rv16_lib.architecture.base_service_connector.CMConfigurationRequest'
        ) as mock_cm_request:

            connector.setup_connections(
                cm_proxy=mock_cm_proxy_instance,
                cm_provider=cm_provider,
                output_type=output_type
            )

            # Verify CMConfigurationRequest was called correctly
            mock_cm_request.assert_called_once_with(
                service=connector.srv_name,
                provider=cm_provider
            )

            # Verify cm_proxy.get was called with the created request instance
            mock_cm_proxy_instance.get.assert_called_once_with(
                payload=mock_cm_request.return_value,
                output_type=output_type
            )

        # Verify the connection attribute is set
        assert connector.connection == {"key": "value"}
