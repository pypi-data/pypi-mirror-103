import pkg_resources
import sys

if sys.version_info < (3, 5):
    raise EnvironmentError("Python 3.5 or above is required")

from platone.packages.platone_account import Account  # noqa: E402
from platone.main import Web3  # noqa: E402
from platone.providers.rpc import (  # noqa: E402
    HTTPProvider,
)
from platone.providers.eth_tester import (  # noqa: E402
    EthereumTesterProvider,
)
from platone.providers.tester import (  # noqa: E402
    TestRPCProvider,
)
from platone.providers.ipc import (  # noqa: E402
    IPCProvider,
)
from platone.providers.websocket import (  # noqa: E402
    WebsocketProvider,
)

try:
    __version__ = pkg_resources.get_distribution("platone").version
except:
    __version__ = '0.13.1.'

__all__ = [
    "__version__",
    "Web3",
    "HTTPProvider",
    "IPCProvider",
    "WebsocketProvider",
    "TestRPCProvider",
    "EthereumTesterProvider",
    "Account",
]
