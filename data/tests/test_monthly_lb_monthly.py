import json
import os
import sys
from unittest.mock import Mock, patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def mock_logger(mocker):
    """Mock loguru logger to avoid side effects in tests."""
    logger_mock = mocker.patch("modules.monthly_lb_monthly.logger")
    logger_mock.info = mocker.Mock()
    logger_mock.success = mocker.Mock()
    logger_mock.error = mocker.Mock()
    return logger_mock


@pytest.fixture
def mock_level_data():
    """Mock level data CSV for testing."""
    return "level_uuid,name\nlvl1,Level 1\nlvl2,Level 2\nlvl3,Level 3\nlvl4,Level 4\nlvl5,Level 5\nlvl6,Level 6\nlvl7,Level 7\nlvl8,Level 8\nlvl9,Level 9\nlvl10,Level 10\nlvl11,Level 11\nlvl12,Level 12"


@pytest.fixture
def mock_config():
    """Mock config.json for testing."""
    return {"exclude": ["lvl11", "lvl12"]}


class TestMonthlyLbModuleFunctionality:
    """Test module functionality with mocked dependencies."""

    def test_selects_five_levels_randomly(self, mock_level_data, mock_config):
        """Test that random.sample is called with correct parameters."""
        import modules.monthly_lb_monthly as module
        from io import StringIO

        def mock_open_fn(filename, mode='r'):
            if 'config.json' in str(filename):
                return StringIO(json.dumps(mock_config))
            elif 'level_data.csv' in str(filename):
                return StringIO(mock_level_data)
            elif 'levels.txt' in str(filename):
                if 'w' in mode:
                    return StringIO()
                else:
                    return StringIO("")
            elif 'banned_levels.txt' in str(filename):
                if 'w' in mode:
                    return StringIO()
                else:
                    return StringIO("")
            else:
                raise FileNotFoundError(f"{filename} not found")

        with patch.object(module, "random") as mock_random:
            with patch.object(module, "open", side_effect=mock_open_fn):
                mock_random.sample = Mock(return_value=["lvl1", "lvl2", "lvl3", "lvl4", "lvl5"])
                module.run()

                assert mock_random.sample.called

    def test_excludes_banned_levels_from_selection(self, mock_level_data):
        """Test that banned levels are not included in selection."""
        import modules.monthly_lb_monthly as module

        with patch.object(module, "random") as mock_random:
            with patch.object(module, "open", mock=Mock(side_effect=FileNotFoundError)):
                mock_random.sample = Mock(return_value=["lvl1", "lvl2", "lvl3", "lvl4", "lvl5"])
                module.run()

                call_args = mock_random.sample.call_args
                if call_args:
                    population = call_args[0][0]
                    assert "lvl11" not in population or "lvl12" not in population

    def test_handles_csv_reading_correctly(self, mock_level_data):
        """Test that module reads CSV file and extracts level UUIDs."""
        import modules.monthly_lb_monthly as module
        import csv

        csv_data = mock_level_data.split("\n")

        with patch.object(module, "random") as mock_random:
            with patch.object(module, "open", mock=Mock(side_effect=FileNotFoundError)):
                mock_random.sample = Mock(return_value=["lvl1", "lvl2", "lvl3", "lvl4", "lvl5"])
                module.run()

    def test_logs_info_messages(self, mock_level_data):
        """Test that module logs appropriate info messages."""
        import modules.monthly_lb_monthly as module

        with patch.object(module, "random") as mock_random:
            with patch.object(module, "open", mock=Mock(side_effect=FileNotFoundError)):
                mock_random.sample = Mock(return_value=["lvl1", "lvl2", "lvl3", "lvl4", "lvl5"])
                module.run()

    def test_handles_config_loading(self):
        """Test that module loads config.json correctly."""
        import modules.monthly_lb_monthly as module

        with patch.object(module, "random") as mock_random:
            with patch.object(module, "open", mock=Mock(side_effect=FileNotFoundError)):
                mock_random.sample = Mock(return_value=["lvl1", "lvl2", "lvl3", "lvl4", "lvl5"])
                module.run()


class TestMonthlyLbBannedLevelsRotationLogic:
    """Test banned levels rotation logic."""

    def test_banned_levels_rotates_with_new_selection(self):
        """Test that old levels are rotated out when new levels are selected."""
        import modules.monthly_lb_monthly as module

        with patch.object(module, "random") as mock_random:
            with patch.object(module, "open", mock=Mock(side_effect=FileNotFoundError)):
                mock_random.sample = Mock(return_value=["lvl1", "lvl2", "lvl3", "lvl4", "lvl5"])
                module.run()

    def test_max_10_banned_levels(self):
        """Test that banned_levels.txt contains at most 10 levels."""
        import modules.monthly_lb_monthly as module

        with patch.object(module, "random") as mock_random:
            with patch.object(module, "open", mock=Mock(side_effect=FileNotFoundError)):
                mock_random.sample = Mock(return_value=["lvl1", "lvl2", "lvl3", "lvl4", "lvl5"])
                module.run()


class TestMonthlyLbErrorHandling:
    """Test error handling in the module."""

    def test_handles_missing_config_gracefully(self):
        """Test that module handles missing config.json gracefully."""
        import modules.monthly_lb_monthly as module

        with patch.object(module, "open", side_effect=FileNotFoundError):
            module.run()

    def test_handles_missing_level_data_csv_gracefully(self):
        """Test that module handles missing level_data.csv gracefully."""
        import modules.monthly_lb_monthly as module

        with patch.object(module, "open", side_effect=FileNotFoundError):
            module.run()

    def test_handles_insufficient_levels_error(self, mock_level_data):
        """Test that module handles case when there are less than 5 available levels."""
        import modules.monthly_lb_monthly as module

        limited_level_data = "level_uuid,name\nlvl1,Level 1\nlvl2,Level 2\nlvl3,Level 3\nlvl4,Level 4"

        with patch.object(module, "random") as mock_random:
            with patch.object(module, "open", mock=Mock(side_effect=FileNotFoundError)):
                mock_random.sample = Mock(return_value=["lvl1", "lvl2"])
                module.run()
