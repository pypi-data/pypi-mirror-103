import unittest
from json import loads
from reverseip import Result, ErrorMessage


_json_response_ok = '''{
   "result": [
      {
         "name": "cms.dlcra.rec1.net",
         "first_seen": "1530901800",
         "last_visit": "1530901800"
      },
      {
         "name": "crpa.rec1.net",
         "first_seen": "1530905127",
         "last_visit": "1530905127"
      },
      {
         "name": "dlcra.org",
         "first_seen": "1530487091",
         "last_visit": "1531103210"
      },
      {
         "name": "dlcra.rec1.net",
         "first_seen": "1530907559",
         "last_visit": "1530907559"
      },
      {
         "name": "gojmba.com",
         "first_seen": "1530497143",
         "last_visit": "1531114542"
      }
   ],
   "current_page": "0",
   "size": 5
}'''

_json_response_error = '''{
    "code": 403,
    "messages": "Access restricted. Check credits balance or enter the correct API key."
}'''


class TestModel(unittest.TestCase):

    def test_response_parsing(self):
        response = loads(_json_response_ok)
        parsed = Result(response)
        assert parsed.current_page == '0'
        assert parsed.size == 5
        assert len(parsed.result) == 5
        assert parsed.has_next is False

        record = parsed.result[0]
        assert record.name == 'cms.dlcra.rec1.net'
        assert record.first_seen == '1530901800'
        assert record.last_visit == '1530901800'

        record1 = parsed.result[1]
        assert record1.name == 'crpa.rec1.net'
        assert record1.first_seen == '1530905127'
        assert record1.last_visit == '1530905127'

    def test_error_parsing(self):
        error = loads(_json_response_error)
        parsed_error = ErrorMessage(error)
        assert parsed_error.code == 403
        assert parsed_error.message == 'Access restricted. Check credits balance or enter the correct API key.'
