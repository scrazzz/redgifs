"""
This example shows how you can use a proxy if your
country blocks redgifs.com.

This is similiar even if you're using async code.
"""

import redgifs

api = redgifs.API(
    proxy='https://myproxy.com:6969',
    # If your proxy server requires auth
    proxy_auth=redgifs.ProxyAuth('myusername', 'mypasswd')
)

api.search('agent')
