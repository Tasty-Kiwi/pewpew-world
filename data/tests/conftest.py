import pytest


@pytest.fixture
def mock_logger(mocker):
    """Mock loguru logger to avoid side effects in tests."""
    logger_mock = mocker.patch("modules.github_data.logger")
    logger_mock.info = mocker.Mock()
    logger_mock.success = mocker.Mock()
    logger_mock.error = mocker.Mock()
    return logger_mock
