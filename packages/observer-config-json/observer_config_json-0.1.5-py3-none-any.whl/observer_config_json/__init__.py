
from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:  # package is not installed
    __version__ = None
from .cli import OBSERVER_CONFIG_JSON

__all__ = [OBSERVER_CONFIG_JSON]