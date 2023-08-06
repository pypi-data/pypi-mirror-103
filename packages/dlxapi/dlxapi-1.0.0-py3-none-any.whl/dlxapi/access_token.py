import requests

from dlxapi.constants import base_url
from dlxapi.from_json import FromJson


def get_access_token(client_id, client_secret, api_instance_url=None, grant_type='client_credentials'):
    if api_instance_url is None:
        api_instance_url = base_url
    auth_url = api_instance_url + "/oauth/token?grant_type=client_credentials"

    response = requests.post(auth_url, auth=(client_id, client_secret),
                            data={"grant_type": grant_type, "client_id": client_id, "client_secret": client_secret})

    return FromJson(response.content).access_token

