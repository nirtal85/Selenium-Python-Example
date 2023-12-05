import pytest

from tests.base_test import BaseTest


@pytest.mark.skip(reason="Example only")
class TestDependencyExample(BaseTest):
    """Test suite for demonstrating test dependencies in the same class.

    This class defines a test suite with four test cases, illustrating the use
    of test dependencies using the pytest-dependency plugin.

    Test cases:
    - test_a: Placeholder test function with the dependency name "a".
    - test_b: Placeholder test function with the dependency name "a".
    - test_c: Placeholder test function with the dependency name "c" and depends on "b".
    - test_d: Placeholder test function with the dependency name "d" and depends on "b" and "c".
    """

    @pytest.mark.dependency(name="a")
    def test_a(self):
        pass

    @pytest.mark.dependency(name="b")
    def test_b(self):
        assert False

    @pytest.mark.dependency(name="c", depends=["b"])
    def test_c(self):
        pass

    @pytest.mark.dependency(name="d", depends=["b", "c"])
    def test_d(self):
        pass
