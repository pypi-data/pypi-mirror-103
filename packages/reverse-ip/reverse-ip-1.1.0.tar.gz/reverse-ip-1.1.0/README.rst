.. image:: https://img.shields.io/badge/License-MIT-green.svg
    :alt: reverse-ip-py license
    :target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/pypi/v/reverse-ip.svg
    :alt: reverse-ip-py release
    :target: https://pypi.org/project/reverse-ip

.. image:: https://github.com/whois-api-llc/reverse-ip-py/workflows/Build/badge.svg
    :alt: reverse-ip-py build
    :target: https://github.com/whois-api-llc/reverse-ip-py/actions

========
Overview
========

The client library for
`Reverse IP/DNS API <https://reverse-ip.whoisxmlapi.com/>`_
in Python language.

The minimum Python version is 3.6.

Installation
============
::

    pip install reverse-ip

Examples
========

Full API documentation available `here <https://reverse-ip.whoisxmlapi.com/api/documentation/making-requests>`_

Create a new client
-------------------

::

    from reverseip import *

    client = Client('Your API key')

Make basic requests
-------------------

::

    # Get parsed records as a model instance.
    result = client.data('8.8.8.8')
    print(result.size)
    for record in result.result:
        print("Domain: {}, visited: {}".format(
                record.name, record.last_visit))

    # Get raw API response
    resp_str = client.raw_data('1.1.1.1')

Advanced usage
-------------------
Pagination


::

    for response in client.iterate_over('1.1.1.1'):
        # Working with the current page
        print(response.size)
        for record in response.result:
            print(record.name)


    # Alternative way
    try:
        response = client.data('1.1.1.1')
        # processing
        # ...
        while response.has_next:
            response = client.next_page('1.1.1.1', response)
            # processing
            # ...
    except ReverseIpApiError as error:
        print(error.message)


Get raw data in XML

::

    raw = client.raw_data('1.1.1.1', output_format='xml')
    print(raw)
