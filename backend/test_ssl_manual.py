import time
from services.ssl_service import SSLService
from unittest.mock import patch

def run_tests():
    service = SSLService()

    print("--- TEST A: Valid HTTPS ---")
    res_a = service.get_ssl_info("https://example.com")
    print("Result:", res_a)

    print("\n--- TEST B: HTTP URL ---")
    res_b = service.get_ssl_info("http://example.com")
    print("Result:", res_b)

    print("\n--- TEST C: Explicit HTTPS port ---")
    res_c = service.get_ssl_info("https://example.com:443/path")
    print("Result:", res_c)

    print("\n--- TEST D: Invalid domain ---")
    res_d = service.get_ssl_info("https://thisdomainshouldnotexist123456789.com")
    print("Result:", res_d)

    print("\n--- TEST E: Timeout mock ---")
    def slow_connect(*args, **kwargs):
        time.sleep(0.1)
        raise TimeoutError("Mocked socket timeout")
        
    with patch("socket.create_connection", side_effect=slow_connect):
        res_e = service.get_ssl_info("https://example.com")
        print("Result:", res_e)

    print("\n--- TEST F: Certificate Validation (expired.badssl.com) ---")
    res_f = service.get_ssl_info("https://expired.badssl.com")
    print("Result:", res_f)

if __name__ == "__main__":
    run_tests()
