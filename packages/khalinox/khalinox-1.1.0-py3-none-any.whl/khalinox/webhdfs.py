"""pythonic hdfs client
"""
import requests

# from hdfs import InsecureClient,Client
import hdfs
from khalinox import config, utils
from urllib.parse import urljoin

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _webhdfs_url(knox_url: str, path="gateway/default/webhdfs/v1") -> str:
    # return "https://obitedhs-vcs001.equant.com:8443/gateway/default/webhdfs/v1"
    return urljoin(knox_url, path)


def hdfs_client(myconfig: config.Config) -> hdfs.InsecureClient:
    # context to use with knox simple user/password auth
    session = requests.Session()
    session.verify = myconfig.verify
    # https://docs.python-requests.org/en/master/user/advanced/#session-objects
    session.auth = (myconfig.user, utils.decrypt(myconfig._key, myconfig.password))
    return hdfs.InsecureClient(url=_webhdfs_url(myconfig.knox_url), session=session)
