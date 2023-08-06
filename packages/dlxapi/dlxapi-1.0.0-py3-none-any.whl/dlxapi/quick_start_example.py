import dlxapi
from dlxapi.constants import base_url
from dlxapi.access_token import get_access_token
from dlxapi import Configuration


def dlx_api():
    configuration = Configuration()
    configuration.access_token = get_access_token()
    configuration.host = base_url

    api_instance = dlxapi.PortfoliosApi(dlxapi.ApiClient(configuration))
    portfolios = api_instance.get_portfolios()

    return portfolios


if __name__ == '__main__':
    dlx_api()
