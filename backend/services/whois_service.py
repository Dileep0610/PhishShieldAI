import whois
from urllib.parse import urlparse
from datetime import datetime
import time


class WHOISService:

    def __init__(self):

        # domain -> (timestamp, result)
        self.cache = {}

        # Cache validity (1 hour)
        self.cache_duration = 3600

    def get_domain_info(self, url):

        domain = urlparse(url).netloc.split(":")[0]

        # -------------------------
        # Check Cache
        # -------------------------
        if domain in self.cache:

            timestamp, result = self.cache[domain]

            if time.time() - timestamp < self.cache_duration:

                print(f"WHOIS Cache Hit : {domain}")

                return result

        try:

            data = whois.whois(domain, timeout=8)

            creation = data.creation_date
            expiration = data.expiration_date

            if isinstance(creation, list):
                creation = creation[0]

            if isinstance(expiration, list):
                expiration = expiration[0]

            # Remove timezone information
            if creation and creation.tzinfo is not None:
                creation = creation.replace(tzinfo=None)

            if expiration and expiration.tzinfo is not None:
                expiration = expiration.replace(tzinfo=None)

            age = None

            if creation:
                age = (datetime.now() - creation).days

            result = {

                "domain": domain,

                "registrar": data.registrar,

                "creation_date": str(creation),

                "expiration_date": str(expiration),

                "domain_age_days": age
            }

            # Save to cache
            self.cache[domain] = (
                time.time(),
                result
            )

            return result

        except Exception:

            result = {

                "domain": None,

                "registrar": None,

                "creation_date": None,

                "expiration_date": None,

                "domain_age_days": None
            }

            self.cache[domain] = (
                time.time(),
                result
            )

            return result