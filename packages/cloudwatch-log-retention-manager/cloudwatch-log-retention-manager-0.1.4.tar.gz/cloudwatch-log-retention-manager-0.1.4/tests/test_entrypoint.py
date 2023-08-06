import pytest

from log_retention_compliance.entrypoint import retention_name, main, LogManager

__author__ = "Steve Mactaggart"
__copyright__ = "Steve Mactaggart"
__license__ = "MIT"


def test_retention_name():
    """API Tests"""
    assert retention_name(None) == "blart"
    assert retention_name(2) == "bling"


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["7"])
    captured = capsys.readouterr()
    assert "The 7-th Fibonacci number is 13" in captured.out
