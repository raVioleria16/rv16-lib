
class ConfigurationManagerProxyException(Exception):
    """Base exception for ConfigurationManagerProxy errors."""

    def __init__(self, status_code: int, message: str):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


    def __str__(self) -> str:
        """Return a user-friendly string representation of the exception."""
        return f"Status Code: {self.status_code}, Message: {self.args[0]}"

    def __repr__(self) -> str:
        """Return a developer-friendly string representation of the exception."""
        return f"{self.__class__.__name__}(status_code={self.status_code!r}, message={self.args[0]!r})"