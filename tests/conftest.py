"""Pytest configuration and fixtures for gridline OCR tests."""
import pytest


def pytest_addoption(parser):
    """Add custom command-line options."""
    parser.addoption(
        "--save-profiles",
        action="store_true",
        default=False,
        help="Save projection profiles when running tests"
    )


@pytest.fixture
def save_profiles(request):
    """Fixture to provide the save_profiles parameter from command-line."""
    return request.config.getoption("--save-profiles")
