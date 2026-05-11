"""Shared fixtures for provider tests."""

import pytest
from pytest_mock import MockerFixture
from tenacity import wait_none

from prollm.providers.base import BaseProvider


@pytest.fixture(autouse=True)
def _disable_retry_wait(mocker: MockerFixture) -> None:
    """Replace tenacity's exponential backoff with no-wait so retries don't sleep.

    The retry decorator lives on ``BaseProvider.complete`` and
    ``BaseProvider.acomplete``, so every provider inherits the same retry
    machinery. We patch both wait policies once here for every provider test.

    Args:
        mocker: pytest-mock fixture used to swap the wait policy.
    """
    mocker.patch.object(BaseProvider.complete.retry, "wait", wait_none())
    mocker.patch.object(BaseProvider.acomplete.retry, "wait", wait_none())
