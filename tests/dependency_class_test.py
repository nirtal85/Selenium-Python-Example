import pytest

from tests.base_test import BaseTest


@pytest.mark.skip(reason="Example only")
@pytest.mark.dependency(name="e", depends=["TestDependencyExample::b"])
class TestDependencyExample(BaseTest):
    """Test suite for demonstrating test dependencies between different
    classes."""

    def test_e(self):
        """
        Placeholder test function with the dependency name "e" and depends on "TestDependencyExample::b".

        This test case is designed for demonstration purposes only.
        """
