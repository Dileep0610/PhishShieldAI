import time
from urllib.parse import urlparse

import requests


class RedirectService:

    # =========================================================
    # Known URL shortening services
    # =========================================================

    SHORTENER_DOMAINS = {

        "bit.ly",
        "tinyurl.com",
        "t.co",
        "goo.gl",
        "ow.ly",
        "is.gd",
        "buff.ly",
        "cutt.ly",
        "rb.gy",
        "shorturl.at",
        "tiny.cc",
        "lnkd.in",
        "s.id",
        "rebrand.ly",
        "trib.al",
        "soo.gd",
        "v.gd",
        "bl.ink",
        "snip.ly"
    }

    # =========================================================
    # Constructor
    # =========================================================

    def __init__(self):

        self.timeout = 8

        self.max_redirects = 10

    # =========================================================
    # SSRF Protection
    # =========================================================

    def _is_safe_url(self, url):
        try:
            import socket
            import ipaddress
            domain = urlparse(url).hostname
            if not domain:
                return False
                
            try:
                ip = ipaddress.ip_address(domain)
                if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved or ip.is_unspecified:
                    return False
            except ValueError:
                pass
                
            addrinfo = socket.getaddrinfo(domain, None)
            for info in addrinfo:
                ip_str = info[4][0]
                ip = ipaddress.ip_address(ip_str)
                if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved or ip.is_unspecified:
                    return False
            return True
        except Exception:
            return False

    # =========================================================
    # Normalize domain
    # =========================================================

    def _normalize_domain(self, url):

        try:

            parsed = urlparse(url)

            domain = (
                parsed.netloc
                .lower()
                .split(":")[0]
            )

            if domain.startswith("www."):

                domain = domain[4:]

            return domain

        except Exception:

            return ""

    # =========================================================
    # Shortener detection
    # =========================================================

    def _is_shortener(self, url):

        domain = self._normalize_domain(url)

        if not domain:

            return False

        return (
            domain in self.SHORTENER_DOMAINS
        )

    # =========================================================
    # Analyze URL
    # =========================================================

    def analyze(self, url):

        start_time = time.perf_counter()

        result = {

            "redirected": False,

            "redirect_count": 0,

            "final_url": url,

            "redirect_chain": [url],

            "protocol_changed": False,

            "domain_changed": False,

            "uses_shortener": self._is_shortener(url)
        }

        try:

            # =================================================
            # Manual Redirect Loop with SSRF Protection
            # =================================================

            chain = [url]
            final_url = url
            redirect_count = 0

            while redirect_count <= self.max_redirects:
                if not self._is_safe_url(final_url):
                    break

                response = requests.get(
                    final_url,
                    allow_redirects=False,
                    timeout=self.timeout,
                    stream=True,
                    headers={
                        "User-Agent":
                        "Mozilla/5.0 "
                        "(Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 "
                        "(KHTML, like Gecko) "
                        "Chrome/131.0 Safari/537.36"
                    }
                )
                response.close()

                if response.status_code in (301, 302, 303, 307, 308):
                    location = response.headers.get("Location")
                    if location:
                        from urllib.parse import urljoin
                        next_url = urljoin(final_url, location)
                        if next_url in chain:
                            break
                        chain.append(next_url)
                        final_url = next_url
                        redirect_count += 1
                        if redirect_count > self.max_redirects:
                            break
                    else:
                        break
                else:
                    break

            cleaned_chain = []
            for item in chain:
                if item not in cleaned_chain:
                    cleaned_chain.append(item)

            # =================================================
            # Redirect count
            # =================================================

            # Limit count strictly to max_redirects for reporting
            redirect_count = min(redirect_count, self.max_redirects)

            result["redirected"] = (
                redirect_count > 0
            )

            result["redirect_count"] = (
                redirect_count
            )

            result["final_url"] = final_url

            result["redirect_chain"] = (
                cleaned_chain
            )

            # =================================================
            # Compare original and final URL
            # =================================================

            original_parsed = urlparse(url)

            final_parsed = urlparse(final_url)

            # -------------------------------------------------
            # Protocol changed
            # -------------------------------------------------

            result["protocol_changed"] = (
                original_parsed.scheme.lower()
                != final_parsed.scheme.lower()
            )

            # -------------------------------------------------
            # Domain changed
            # -------------------------------------------------

            original_domain = (
                self._normalize_domain(url)
            )

            final_domain = (
                self._normalize_domain(final_url)
            )

            result["domain_changed"] = (
                original_domain != final_domain
            )

            # =================================================
            # Shortener detection
            # =================================================
            #
            # IMPORTANT:
            #
            # A normal redirect such as:
            #
            # microsoft.com
            #       ↓
            # microsoft.com/en-in
            #
            # is NOT a shortener.
            #
            # We only mark a URL as shortened when the
            # ORIGINAL URL belongs to a known shortening
            # service.
            # =================================================

            result["uses_shortener"] = (
                self._is_shortener(url)
            )

        except requests.RequestException as e:

            print(
                f"Redirect analysis failed: {e}"
            )

        except Exception as e:

            print(
                f"Unexpected redirect error: {e}"
            )

        # =====================================================
        # Processing time
        # =====================================================

        processing_time = round(
            (time.perf_counter() - start_time)
            * 1000,
            2
        )

        result["processing_time_ms"] = (
            processing_time
        )

        return result