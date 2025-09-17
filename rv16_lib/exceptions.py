class RV16Exception(Exception):
    """
    A base exception class for the RV16 system.

    This class includes a status_code and a message to provide more context
    for the error. It inherits from Python's built-in `Exception` class.

    Attributes:
        status_code (int): A numerical status code representing the type of error.
        message (str): A human-readable message describing the error.
    """

    def __init__(self, status_code: int, message: str):
        """
        Initializes the RV16Exception with a status code and a message.

        Args:
            status_code (int): The status code for the exception.
            message (str): The error message.
        """
        super().__init__(message)  # Call the base class constructor
        self.status_code = status_code
        self.message = message

    def __str__(self) -> str:
        """
        Returns a string representation of the exception.
        """
        return f"RV16Exception: [Status Code: {self.status_code}] {self.message}"