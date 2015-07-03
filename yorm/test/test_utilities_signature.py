# pylint:disable=W0621,R,C

import pytest

from yorm import utilities


class SampleWithMagicMethods:

    """Sample class with magic methods implemented."""

    def __init__(self):
        self.values = []

    def __setattr__(self, name, value):
        self.values.append(('__setattr__', name, value))
        super().__setattr__(self, name, value)


@pytest.fixture
def unmapped():
    return SampleWithMagicMethods()


@pytest.yield_fixture
def mapped():
    import yorm
    yorm.settings.fake = True
    yield utilities.sync(SampleWithMagicMethods(), "sample.yml")
    yorm.settings.fake = False


class TestSyncObjectMaintainsSignature:

    def test_repr(self, unmapped, mapped):
        assert repr(unmapped) == repr(mapped)

    def test_doc(self, unmapped, mapped):
        assert unmapped.__doc__ == mapped.__doc__

    def test_class_name(self, unmapped, mapped):
        assert unmapped.__class__.__name__ == mapped.__class__.__name__

    def test_instance(self, unmapped, mapped):
        assert isinstance(mapped, unmapped.__class__)

    def test_magic_methods(self, mapped):
        setattr(mapped, 'value', 42)
        assert mapped.values == [('__setattr__', 'value', 42)]
