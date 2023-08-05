import os
import unittest
from ipaddress import ip_address
from reverseip import Client
from reverseip import ParameterError, ApiAuthError


class TestClient(unittest.TestCase):
    """
    Final integration tests without mocks.

    Active API_KEY is required.
    """
    def test_get_correct_data(self):
        client = Client(os.getenv("API_KEY"))

        result = client.data('8.8.8.8')
        assert result.current_page == '0'

    def test_get_second_page(self):
        client = Client(os.getenv("API_KEY"))
        result = client.data('8.8.8.8')
        last_domain = result.result[-1].name
        result = client.data('8.8.8.8', start_from=last_domain)
        assert result.current_page == last_domain

    def test_get_raw_data(self):
        client = Client(os.getenv("API_KEY"))
        raw = client.raw_data(ip_address('1.1.1.1'), output_format='xml')
        assert raw.startswith('<?xml')

    def test_get_auth_error(self):
        client = Client('at_00000000000000000000000000000')
        self.assertRaises(ApiAuthError, client.data, '1.1.1.1')
        try:
            client.data('1.1.1.1')
        except ApiAuthError as error:
            parsed = error.parsed_message
            assert parsed.code == 403

    def test_get_parameter_error(self):
        client = Client(os.getenv('API_KEY'))
        self.assertRaises(ParameterError, client.data, 'incorrect.ip')

    def test_pagination(self):
        client = Client(os.getenv('API_KEY'))
        response = client.data('8.8.8.8')
        counter = 0
        while response.has_next:
            counter += 1
            response = client.next_page('8.8.8.8', response)
            if counter > 1:
                break

        assert counter > 0

    def test_pagination2(self):
        client = Client(os.getenv('API_KEY'))
        counter = 0
        p_page = '-1'
        for r in client.iterate_over('1.1.1.1'):
            assert p_page != r.current_page
            counter += 1
            if counter > 2:
                break

        assert counter > 0


if __name__ == '__main__':
    unittest.main()
