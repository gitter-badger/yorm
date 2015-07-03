# pylint: disable=W0201

from unittest import mock

from yorm.utilities import attr
from yorm.converters import Float
from yorm.base.mappable import Mappable

from . import strip


@attr(value=Float)
class SampleManuallyMapped(Mappable):

    """Sample class that is manually mapped."""

    def __init__(self, value=0):
        self.value = value


@mock.patch('yorm.settings.fake', True)
class TestManualInheritance:

    def setup_method(self, _):
        self.sample = SampleManuallyMapped()

    def test_mapping(self):
        assert strip("""
        value: 0.0
        """) == self.sample.yorm_mapper.text

        self.sample.value = 42
        assert strip("""
        value: 42.0
        """) == self.sample.yorm_mapper.text
