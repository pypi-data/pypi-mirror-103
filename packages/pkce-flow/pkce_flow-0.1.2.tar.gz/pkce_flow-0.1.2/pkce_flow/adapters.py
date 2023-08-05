from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

exponential_backoff_retry = Retry(
    total=5,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["GET", "POST"],
    backoff_factor=1,
)

exponential_backoff_adapter = HTTPAdapter(max_retries=exponential_backoff_retry)
