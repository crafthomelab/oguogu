import pytest

@pytest.fixture
def given_repository(local_database_container):
    return local_database_container.repository()



def test_get_challenge(given_repository):
    challenge = given_repository.get_challenge("123")
    assert challenge is not None
