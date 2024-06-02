import requests
import asyncio


import requests
import urllib3
import ssl


# IDK why but works
class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.set_ciphers("DEFAULT")
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)


def request_new_tst(url: str):
    session = requests.Session()
    session.mount('https://', TLSAdapter())
    response = session.get(url, verify=False)
    return response.content


async def download(url: str):
    loop = asyncio.get_event_loop()
    
    return (await loop.run_in_executor(
        None,
        request_new_tst,
        url
    ))


async def writeData(raw: bytes, target: str):
    with open(target, 'wb') as f:
        f.write(raw)
