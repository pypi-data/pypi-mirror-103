from json import loads, JSONDecodeError
import re
from ipaddress import ip_address, IPv4Address

from .net.http import ApiRequester
from .models.response import Result
from .exceptions.error import ParameterError, EmptyApiKeyError, \
    UnparsableApiResponseError, CannotRetrieveNextPageError


class Client:
    __default_url = "https://reverse-ip.whoisxmlapi.com/api/v1"
    __parsable_format = 'json'
    _api_requester: ApiRequester or None
    _api_key: str

    _re_api_key = re.compile(r'^at_[a-z0-9]{29}$', re.IGNORECASE)
    _re_output_format = re.compile(r'^(json)|(xml)$', re.IGNORECASE)

    def __init__(self, api_key: str, **kwargs):
        """
        :param api_key: str: Your API key.
        :param base_url: str: (optional) API endpoint URL.
        :param timeout: float: (optional) API call timeout in seconds
        """
        self._api_key = ''

        self.api_key = api_key

        if 'base_url' not in kwargs:
            kwargs['base_url'] = Client.__default_url
        self.api_requester = ApiRequester(**kwargs)

    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, value: str):
        self._api_key = Client._validate_api_key(value)

    @property
    def api_requester(self) -> ApiRequester or None:
        return self._api_requester

    @api_requester.setter
    def api_requester(self, value: ApiRequester):
        self._api_requester = value

    @property
    def base_url(self) -> str:
        return self._api_requester.base_url

    @base_url.setter
    def base_url(self, value: str or None):
        if value is None:
            self._api_requester.base_url = Client.__default_url
        else:
            self._api_requester.base_url = value

    @property
    def timeout(self) -> float:
        return self._api_requester.timeout

    @timeout.setter
    def timeout(self, value: float):
        self._api_requester.timeout = value

    def data(self, ip: str or IPv4Address, **kwargs) -> Result:
        """
        Get parsed whois data from the API

        :param: ip - str|IPv4Address - the domain name
        :param: start_from (optional) :str: Last domain names of the cur. page
        :return: Result
        :raises:
        - base class is reverseip.exceptions.ReverseIpApiError
          - EmptyApiKeyError
          - ResponseError -- response contains an error message
          - ApiAuthError -- Server returned 401, 402 or 403 HTTP code
          - BadRequestError - Server returned 400 or 422 HTTP code
          - HttpApiError -- HTTP code >= 300 and not equal to above codes from
          - UnparsableApiResponseError -- the response couldn't be parsed
          - ParameterError -- invalid parameter's value
        - ConnectionError
        """

        kwargs['output_format'] = Client.__parsable_format

        response = self.raw_data(ip, **kwargs)
        try:
            parsed = loads(str(response))
            if 'result' in parsed:
                return Result(parsed)
            raise UnparsableApiResponseError(
                "Could not find the correct root element.", None)
        except JSONDecodeError as error:
            raise UnparsableApiResponseError("Could not parse API response", error)

    def next_page(self, ip: str or IPv4Address, current_page: Result) -> Result:
        """

        :param ip: :str/IPv4Address:
        :param current_page: :Result: instance
        :return: :Result:
        :raises CannotRetrieveNextPage:
        """

        if current_page is not None:
            if current_page.size > 0:
                return self.data(ip, start_from=current_page.result[-1].name)

        raise CannotRetrieveNextPageError("Unable to retrieve next page for given parameters")

    def iterate_over(self, ip: str or IPv4Address):
        r = self.data(ip)
        yield r
        while r.has_next:
            r = self.next_page(ip, r)
            yield r

    def raw_data(self, ip: str or IPv4Address, **kwargs) -> str:
        """
        Get parsed whois data from the API
        :param ip: - :str|IPv4Address: - the domain name
        :param start_from: (optional) :str: Last domain names of the current page.
        :param output_format: - (optional) :str: 'json' or 'xml'
        :return: str
        :raises
        - base class is reverseip.exceptions.ReverseIpApiError
          - ResponseError -- response contains an error message
          - ApiAuthError -- Server returned 401, 402 or 403 HTTP code
          - BadRequestError - Server returned 400 or 422 HTTP code
          - HttpApiError -- HTTP code >= 300 and not equal to above codes
          - ParameterError -- invalid parameter's value
        - ConnectionError
        """
        if self.api_key == '':
            raise EmptyApiKeyError('')

        ip = Client._validate_ip(ip)

        if 'start_from' in kwargs:
            start_from = Client._validate_domain_name(kwargs['start_from'])
        else:
            start_from = "0"

        if 'output_format' in kwargs:
            output_format = Client._validate_output_format(
                kwargs['output_format'])
        else:
            output_format = Client.__parsable_format

        return self._api_requester.get_data(
            self.api_key, ip, start_from, output_format)

    @staticmethod
    def _validate_api_key(api_key):
        if Client._re_api_key.search(
                str(api_key)
        ) is not None:
            return str(api_key)
        else:
            raise ParameterError("Invalid API key format.")

    @staticmethod
    def _validate_ip(ip):
        ipv4 = None
        try:
            if isinstance(ip, IPv4Address):
                return str(ip)
            ipv4 = ip_address(ip)
            if isinstance(ipv4, IPv4Address):
                return str(ipv4)
        except ValueError:
            pass
        if ipv4 is None:
            raise ParameterError('Invalid IPv4 value.')

    @staticmethod
    def _validate_domain_name(domain):
        if domain is not None and len(str(domain)) > 0:
            return domain
        raise ParameterError('Invalid domain name.')

    @staticmethod
    def _validate_output_format(_format):
        if Client._re_output_format.search(str(_format)):
            return str(_format)
        else:
            raise ParameterError(
                "Output format should be either JSON or XML.")
