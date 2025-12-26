import json
import os
import sys
from unittest.mock import Mock, patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def mock_csv_data():
    """Simple mock CSV data for testing."""
    return {
        "account_data.csv": "account_id,name\n1,TestUser\n2,AnotherUser",
        "level_data.csv": "level_id,name\n1,Easy\n2,Hard",
        "score_data.csv": "score_id,value\n1,100\n2,200",
    }


class TestGithubDataDirectoryCreation:
    """Test that directories are created if they don't exist."""

    def test_creates_github_data_directory(self, mock_csv_data):
        """Test that data/data/github_data directory is created."""

        def mock_get(url):
            filename = url.split("/")[-1]
            mock_response = Mock()
            mock_response.content = mock_csv_data[filename].encode()
            mock_response.raise_for_status = Mock()
            return mock_response

        with patch("requests.get", side_effect=mock_get):
            import importlib

            from modules import github_data

            importlib.reload(github_data)
            github_data.run()

        from modules import github_data

        importlib.reload(github_data)
        data_dir = os.path.dirname(os.path.dirname(github_data.__file__))
        github_data_dir = os.path.join(data_dir, "data", "github_data")

        assert os.path.exists(github_data_dir)
        assert os.path.isdir(github_data_dir)

        for filename in mock_csv_data.keys():
            os.remove(os.path.join(github_data_dir, filename))
        os.remove(os.path.join(github_data_dir, "metadata.json"))


class TestGithubDataFileCreation:
    """Test that CSV files and metadata.json are created correctly."""

    def test_creates_three_csv_files(self, mock_csv_data):
        """Test that all three CSV files are created."""

        def mock_get(url):
            filename = url.split("/")[-1]
            mock_response = Mock()
            mock_response.content = mock_csv_data[filename].encode()
            mock_response.raise_for_status = Mock()
            return mock_response

        with patch("requests.get", side_effect=mock_get):
            import importlib

            from modules import github_data

            importlib.reload(github_data)
            github_data.run()

        from modules import github_data

        importlib.reload(github_data)
        data_dir = os.path.dirname(os.path.dirname(github_data.__file__))
        github_data_dir = os.path.join(data_dir, "data", "github_data")

        csv_files = [
            "account_data.csv",
            "level_data.csv",
            "score_data.csv",
        ]

        for filename in csv_files:
            filepath = os.path.join(github_data_dir, filename)
            assert os.path.exists(filepath), f"{filename} was not created"
            assert os.path.isfile(filepath)
            os.remove(filepath)

        os.remove(os.path.join(github_data_dir, "metadata.json"))

    def test_creates_metadata_json(self, mock_csv_data):
        """Test that metadata.json is created."""

        def mock_get(url):
            filename = url.split("/")[-1]
            mock_response = Mock()
            mock_response.content = mock_csv_data[filename].encode()
            mock_response.raise_for_status = Mock()
            return mock_response

        with patch("requests.get", side_effect=mock_get):
            import importlib

            from modules import github_data

            importlib.reload(github_data)
            github_data.run()

        from modules import github_data

        importlib.reload(github_data)
        data_dir = os.path.dirname(os.path.dirname(github_data.__file__))
        github_data_dir = os.path.join(data_dir, "data", "github_data")
        metadata_file = os.path.join(github_data_dir, "metadata.json")

        assert os.path.exists(metadata_file)
        assert os.path.isfile(metadata_file)

        for filename in mock_csv_data.keys():
            os.remove(os.path.join(github_data_dir, filename))
        os.remove(metadata_file)


class TestGithubDataMetadataContent:
    """Test that metadata.json contains correct timestamp."""

    def test_metadata_has_timestamp(self, mock_csv_data):
        """Test that metadata.json contains a timestamp."""

        def mock_get(url):
            filename = url.split("/")[-1]
            mock_response = Mock()
            mock_response.content = mock_csv_data[filename].encode()
            mock_response.raise_for_status = Mock()
            return mock_response

        with patch("requests.get", side_effect=mock_get):
            import importlib

            from modules import github_data

            importlib.reload(github_data)
            github_data.run()

        from modules import github_data

        importlib.reload(github_data)
        data_dir = os.path.dirname(os.path.dirname(github_data.__file__))
        github_data_dir = os.path.join(data_dir, "data", "github_data")
        metadata_file = os.path.join(github_data_dir, "metadata.json")

        with open(metadata_file, "r") as f:
            metadata = json.load(f)

        assert "timestamp" in metadata
        assert isinstance(metadata["timestamp"], float)

        for filename in mock_csv_data.keys():
            os.remove(os.path.join(github_data_dir, filename))
        os.remove(metadata_file)

    def test_metadata_only_has_timestamp(self, mock_csv_data):
        """Test that metadata.json only contains timestamp field."""

        def mock_get(url):
            filename = url.split("/")[-1]
            mock_response = Mock()
            mock_response.content = mock_csv_data[filename].encode()
            mock_response.raise_for_status = Mock()
            return mock_response

        with patch("requests.get", side_effect=mock_get):
            import importlib

            from modules import github_data

            importlib.reload(github_data)
            github_data.run()

        from modules import github_data

        importlib.reload(github_data)
        data_dir = os.path.dirname(os.path.dirname(github_data.__file__))
        github_data_dir = os.path.join(data_dir, "data", "github_data")
        metadata_file = os.path.join(github_data_dir, "metadata.json")

        with open(metadata_file, "r") as f:
            metadata = json.load(f)

        assert list(metadata.keys()) == ["timestamp"]

        for filename in mock_csv_data.keys():
            os.remove(os.path.join(github_data_dir, filename))
        os.remove(metadata_file)


class TestGithubDataCSVContent:
    """Test that CSV files contain correct data."""

    def test_csv_files_have_correct_data(self, mock_csv_data):
        """Test that CSV files contain the mock data."""

        def mock_get(url):
            filename = url.split("/")[-1]
            mock_response = Mock()
            mock_response.content = mock_csv_data[filename].encode()
            mock_response.raise_for_status = Mock()
            return mock_response

        with patch("requests.get", side_effect=mock_get):
            import importlib

            from modules import github_data

            importlib.reload(github_data)
            github_data.run()

        from modules import github_data

        importlib.reload(github_data)
        data_dir = os.path.dirname(os.path.dirname(github_data.__file__))
        github_data_dir = os.path.join(data_dir, "data", "github_data")

        for filename, expected_content in mock_csv_data.items():
            filepath = os.path.join(github_data_dir, filename)
            with open(filepath, "r") as f:
                actual_content = f.read()

            assert actual_content == expected_content, f"{filename} content mismatch"
            os.remove(filepath)

        os.remove(os.path.join(github_data_dir, "metadata.json"))

    def test_account_data_csv_structure(self, mock_csv_data):
        """Test that account_data.csv has correct structure."""

        def mock_get(url):
            filename = url.split("/")[-1]
            mock_response = Mock()
            mock_response.content = mock_csv_data[filename].encode()
            mock_response.raise_for_status = Mock()
            return mock_response

        with patch("requests.get", side_effect=mock_get):
            import importlib

            from modules import github_data

            importlib.reload(github_data)
            github_data.run()

        from modules import github_data

        importlib.reload(github_data)
        data_dir = os.path.dirname(os.path.dirname(github_data.__file__))
        github_data_dir = os.path.join(data_dir, "data", "github_data")
        csv_file = os.path.join(github_data_dir, "account_data.csv")

        with open(csv_file, "r") as f:
            lines = f.readlines()

        assert len(lines) == 3
        assert lines[0].strip() == "account_id,name"
        assert "TestUser" in lines[1]
        assert "AnotherUser" in lines[2]

        for filename in mock_csv_data.keys():
            os.remove(os.path.join(github_data_dir, filename))
        os.remove(os.path.join(github_data_dir, "metadata.json"))

    def test_level_data_csv_structure(self, mock_csv_data):
        """Test that level_data.csv has correct structure."""

        def mock_get(url):
            filename = url.split("/")[-1]
            mock_response = Mock()
            mock_response.content = mock_csv_data[filename].encode()
            mock_response.raise_for_status = Mock()
            return mock_response

        with patch("requests.get", side_effect=mock_get):
            import importlib

            from modules import github_data

            importlib.reload(github_data)
            github_data.run()

        from modules import github_data

        importlib.reload(github_data)
        data_dir = os.path.dirname(os.path.dirname(github_data.__file__))
        github_data_dir = os.path.join(data_dir, "data", "github_data")
        csv_file = os.path.join(github_data_dir, "level_data.csv")

        with open(csv_file, "r") as f:
            lines = f.readlines()

        assert len(lines) == 3
        assert lines[0].strip() == "level_id,name"
        assert "Easy" in lines[1]
        assert "Hard" in lines[2]

        for filename in mock_csv_data.keys():
            os.remove(os.path.join(github_data_dir, filename))
        os.remove(os.path.join(github_data_dir, "metadata.json"))

    def test_score_data_csv_structure(self, mock_csv_data):
        """Test that score_data.csv has correct structure."""

        def mock_get(url):
            filename = url.split("/")[-1]
            mock_response = Mock()
            mock_response.content = mock_csv_data[filename].encode()
            mock_response.raise_for_status = Mock()
            return mock_response

        with patch("requests.get", side_effect=mock_get):
            import importlib

            from modules import github_data

            importlib.reload(github_data)
            github_data.run()

        from modules import github_data

        importlib.reload(github_data)
        data_dir = os.path.dirname(os.path.dirname(github_data.__file__))
        github_data_dir = os.path.join(data_dir, "data", "github_data")
        csv_file = os.path.join(github_data_dir, "score_data.csv")

        with open(csv_file, "r") as f:
            lines = f.readlines()

        assert len(lines) == 3
        assert lines[0].strip() == "score_id,value"
        assert "100" in lines[1]
        assert "200" in lines[2]

        for filename in mock_csv_data.keys():
            os.remove(os.path.join(github_data_dir, filename))
        os.remove(os.path.join(github_data_dir, "metadata.json"))
