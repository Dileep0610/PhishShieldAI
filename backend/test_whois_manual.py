import time
from services.whois_service import WHOISService
import whois
from unittest.mock import patch

def run_tests():
    service = WHOISService()

    print("--- TEST A: Valid Domain ---")
    res_a = service.get_domain_info("https://example.com")
    print("Result:", res_a)

    print("\n--- TEST B: Unavailable Domain ---")
    # Using random nonexistent domain, should fail whois lookup
    res_b = service.get_domain_info("https://thisdomainshouldnotexist1234567890abc.com")
    print("Result:", res_b)

    print("\n--- TEST C: Port Handling ---")
    # Using example.com again, should hit cache or work correctly without breaking on port
    res_c = service.get_domain_info("https://example.com:443/path")
    print("Result:", res_c)
    assert res_c["domain"] == "example.com"

    print("\n--- TEST D: Timeout Mock ---")
    # Simulate a blocking call that throws an exception (which is what native timeout does internally usually, or simulating it natively)
    def slow_whois(*args, **kwargs):
        time.sleep(0.5)
        raise Exception("Mocked timeout error")

    start = time.time()
    with patch("whois.whois", side_effect=slow_whois):
        # We need a new domain to avoid cache hit
        res_d = service.get_domain_info("https://timeout-test.com")
    elapsed = time.time() - start
    print(f"Elapsed: {elapsed:.2f}s")
    print("Result:", res_d)

if __name__ == "__main__":
    run_tests()
