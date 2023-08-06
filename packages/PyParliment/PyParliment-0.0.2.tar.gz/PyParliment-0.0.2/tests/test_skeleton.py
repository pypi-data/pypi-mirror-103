# print(help("modules"))

from pyparliment.members.location import find

__author__ = "George Sykes"
__copyright__ = "George Sykes"
__license__ = "MIT"


def test_find():
    """API Tests"""
    test_data = find.search("")
    assert "int64" not in test_data.dtypes
    assert len(test_data) == 650
