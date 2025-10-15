import pytest
from rv16_lib.storage.database_connector import DatabaseConnector, DatabaseElement


def test_abstract_class_cannot_be_instantiated():
    """
    Verifies that DatabaseConnector itself cannot be instantiated
    because it has unimplemented abstract methods, which is the
    core purpose of an ABC.
    """
    with pytest.raises(TypeError) as excinfo:
        # Attempting to instantiate an ABC with abstract methods should fail
        DatabaseConnector()

    assert "Can't instantiate abstract class DatabaseConnector with abstract methods" in str(excinfo.value)


def test_partial_implementation_fails_instantiation():
    """
    Tests that a subclass failing to implement *all* abstract methods
    also inherits the 'abstract' status and cannot be instantiated.
    """

    # Define a subclass that only implements 'insert_one'
    class PartialConnector(DatabaseConnector):
        def insert_one(self, *args, **kwargs) -> None:
            pass  # Only implements one method

    with pytest.raises(TypeError) as excinfo:
        PartialConnector()

    error_message = str(excinfo.value)
    assert "abstract methods" in error_message
    assert "delete" in error_message
    assert "update" in error_message
    assert "find" in error_message
    assert "insert_one" not in error_message  # Should not be listed as it was implemented





def test_fully_implemented_subclass_can_be_instantiated_and_used():
    """
    Verifies that the full implementation satisfies the ABC contract,
    allowing instantiation and method calls.
    """

    class MockConnector(DatabaseConnector):
        """
        A concrete implementation that fulfills the contract. Used here to
        verify the contract is fully implementable.
        """

        def insert_one(self, *args, **kwargs) -> dict:
            return {"status": "mock_inserted"}

        def delete(self, *args, **kwargs) -> dict:
            return {"count": 1}

        def update(self, *args, **kwargs) -> dict:
            return {"status": "mock_updated"}

        def find(self, *args, **kwargs) -> list:
            return [{"id": 1, "data": "A"}, {"id": 2, "data": "B"}]

    try:
        # Instantiation should succeed without raising TypeError
        connector = MockConnector()
        assert isinstance(connector, DatabaseConnector)

        # Test methods for basic execution and expected mock return types
        assert connector.insert_one() == {"status": "mock_inserted"}
        assert connector.delete() == {"count": 1}
        assert connector.update() == {"status": "mock_updated"}
        assert isinstance(connector.find(), list)
        assert len(connector.find()) == 2

    except TypeError:
        # If instantiation fails here, the test should fail
        pytest.fail("MockConnector failed to instantiate. The contract was not fully met.")
