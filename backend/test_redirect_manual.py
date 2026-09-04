import time
from unittest.mock import patch, Mock
from services.redirect_service import RedirectService

def run_tests():
    service = RedirectService()

    print("--- SSRF DIRECT TESTS ---")
    ssrf_urls = [
        "http://127.0.0.1/",
        "http://localhost/",
        "http://10.0.0.1/",
        "http://192.168.1.1/",
        "http://[::1]/"
    ]
    for url in ssrf_urls:
        res = service.analyze(url)
        print(f"{url} -> redirect_count: {res['redirect_count']}, final_url: {res['final_url']}")

    print("\n--- REDIRECT TO PRIVATE ADDRESS ---")
    def mock_requests_get(url, **kwargs):
        resp = Mock()
        resp.close = Mock()
        if url == "https://public.example/":
            resp.status_code = 302
            resp.headers = {"Location": "http://127.0.0.1/"}
        else:
            resp.status_code = 200
            resp.headers = {}
        return resp
        
    with patch("requests.get", side_effect=mock_requests_get):
        res = service.analyze("https://public.example/")
        print("Redirect to private chain:", res['redirect_chain'])
        print("Final URL:", res['final_url'])

    print("\n--- MAX REDIRECT TEST ---")
    def mock_requests_get_max(url, **kwargs):
        resp = Mock()
        resp.close = Mock()
        if url.endswith("/"):
            url = url[:-1]
        try:
            num = int(url.split("/")[-1])
        except ValueError:
            num = 0
            
        resp.status_code = 302
        resp.headers = {"Location": f"https://mock.example/{num+1}"}
        return resp

    with patch.object(service, '_is_safe_url', return_value=True):
        with patch("requests.get", side_effect=mock_requests_get_max):
            res = service.analyze("https://mock.example/0")
            print("Max redirects followed:", res['redirect_count'])
            print("Redirect chain length:", len(res['redirect_chain']))
            print("Final URL:", res['final_url'])

    print("\n--- REDIRECT LOOP TEST ---")
    def mock_requests_get_loop(url, **kwargs):
        resp = Mock()
        resp.close = Mock()
        if "a" in url:
            resp.status_code = 302
            resp.headers = {"Location": "https://mock.example/b"}
        else:
            resp.status_code = 302
            resp.headers = {"Location": "https://mock.example/a"}
        return resp

    with patch.object(service, '_is_safe_url', return_value=True):
        with patch("requests.get", side_effect=mock_requests_get_loop):
            res = service.analyze("https://mock.example/a")
            print("Loop test redirect count:", res['redirect_count'])
            print("Loop chain:", res['redirect_chain'])

    print("\n--- PUBLIC SITE REGRESSION ---")
    for url in ["https://www.google.com", "https://www.python.org", "http://example.com"]:
        res = service.analyze(url)
        print(f"{url} -> count: {res['redirect_count']}, final: {res['final_url']}")

if __name__ == "__main__":
    run_tests()
