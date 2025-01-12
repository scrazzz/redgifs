"""
This example shows how you can use a proxy if your country blocks redgifs.com
"""

import redgifs

api = redgifs.API(
    proxy='https://myproxy.com:6969',
    # If your proxy server requires auth
    proxy_auth=redgifs.ProxyAuth('myusername', 'mypasswd')
)
api.login()
api.search('agent')
