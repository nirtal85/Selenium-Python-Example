from types import SimpleNamespace

import pytest

from tests import conftest as test_config


class StopChromeStartup(Exception):
    """Stop setup after inspecting Chrome options."""


@pytest.mark.devRun
def test_chrome_setup_uses_installed_browser_version(monkeypatch: pytest.MonkeyPatch) -> None:
    captured_options = {}

    def stop_chrome_startup(*, options):
        captured_options["options"] = options
        raise StopChromeStartup

    monkeypatch.setattr(test_config.webdriver, "Chrome", stop_chrome_startup)
    item = SimpleNamespace(
        config=SimpleNamespace(
            getoption=lambda option: {
                "driver": "chrome_headless",
                "base_url": "https://example.test",
            }[option]
        ),
        fspath=SimpleNamespace(purebasename="login_test"),
        name="test_sanity",
    )

    with pytest.raises(StopChromeStartup):
        test_config.pytest_runtest_setup(item)

    assert "browserVersion" not in captured_options["options"].capabilities


@pytest.mark.devRun
def test_exception_hook_ignores_failure_before_driver_creation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delattr(test_config, "driver", raising=False)

    result = test_config.pytest_exception_interact(SimpleNamespace(funcargs={}))

    assert result is None


@pytest.mark.devRun
def test_exception_hook_ignores_missing_session_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(test_config, "driver", object(), raising=False)

    result = test_config.pytest_exception_interact(SimpleNamespace(funcargs={}))

    assert result is None


@pytest.mark.devRun
def test_teardown_ignores_missing_driver(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(test_config, "driver", None, raising=False)

    result = test_config.pytest_runtest_teardown()

    assert result is None


@pytest.mark.devRun
def test_chrome_startup_failure_is_not_masked_by_stale_driver(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(test_config, "driver", object(), raising=False)

    def fail_chrome_startup(*, options):
        raise StopChromeStartup

    monkeypatch.setattr(test_config.webdriver, "Chrome", fail_chrome_startup)
    item = SimpleNamespace(
        config=SimpleNamespace(
            getoption=lambda option: {
                "driver": "chrome_headless",
                "base_url": "https://example.test",
            }[option]
        ),
        fspath=SimpleNamespace(purebasename="login_test"),
        name="test_sanity",
    )

    with pytest.raises(StopChromeStartup):
        test_config.pytest_runtest_setup(item)

    result = test_config.pytest_exception_interact(SimpleNamespace(funcargs={}))

    assert result is None
