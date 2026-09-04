import time
import requests
from unittest.mock import patch, Mock
from services.virustotal_service import VirusTotalService

def run_tests():
    service = VirusTotalService()
    # Mock API key so service doesn't throw ValueError
    service.api_key = "mock-key"

    print("--- TEST A: Existing analysis already available ---")
    def mock_req_a(method, url, **kwargs):
        resp = Mock()
        resp.status_code = 200
        resp.json = lambda: {"data": {"attributes": {"last_analysis_stats": {"malicious": 1, "suspicious": 2, "harmless": 3, "undetected": 4}}}}
        return resp

    with patch("requests.request", side_effect=mock_req_a):
        res = service.analyze("http://example.com")
        print("Result A:", res)

    print("\n--- TEST B: 404 then POST then completed polling ---")
    call_count = [0]
    def mock_req_b(method, url, **kwargs):
        resp = Mock()
        if method == "GET" and "analyses" not in url:
            resp.status_code = 404
            resp.raise_for_status = Mock(side_effect=requests.HTTPError(response=resp))
        elif method == "POST":
            resp.status_code = 200
            resp.json = lambda: {"data": {"id": "mock_id"}}
            resp.raise_for_status = Mock()
        else:
            call_count[0] += 1
            resp.status_code = 200
            resp.raise_for_status = Mock()
            if call_count[0] == 1:
                resp.json = lambda: {"data": {"attributes": {"status": "queued"}}}
            else:
                resp.json = lambda: {"data": {"attributes": {"status": "completed", "stats": {"malicious": 5, "suspicious": 0, "harmless": 90, "undetected": 5}}}}
        return resp

    with patch("requests.request", side_effect=mock_req_b):
        with patch("time.sleep", return_value=None):
            res = service.analyze("http://example-b.com")
            print("Result B:", res)

    print("\n--- TEST C: Analysis remains queued (Incomplete) ---")
    def mock_req_c(method, url, **kwargs):
        resp = Mock()
        if method == "GET" and "analyses" not in url:
            resp.status_code = 404
            resp.raise_for_status = Mock(side_effect=requests.HTTPError(response=resp))
        elif method == "POST":
            resp.status_code = 200
            resp.json = lambda: {"data": {"id": "mock_id"}}
            resp.raise_for_status = Mock()
        else:
            resp.status_code = 200
            resp.raise_for_status = Mock()
            resp.json = lambda: {"data": {"attributes": {"status": "queued"}}}
        return resp

    with patch("requests.request", side_effect=mock_req_c):
        with patch("time.sleep", return_value=None):
            res = service.analyze("http://example-c.com")
            print("Result C:", res)

    print("\n--- TEST D: HTTP 429 (Rate limit with Retry-After) ---")
    call_count_d = [0]
    def mock_req_d(method, url, **kwargs):
        resp = Mock()
        if call_count_d[0] == 0:
            call_count_d[0] += 1
            resp.status_code = 429
            resp.headers = {"Retry-After": "1"}
            resp.raise_for_status = Mock(side_effect=requests.HTTPError(response=resp))
        else:
            resp.status_code = 200
            resp.raise_for_status = Mock()
            resp.json = lambda: {"data": {"attributes": {"last_analysis_stats": {"malicious": 9, "suspicious": 9, "harmless": 9, "undetected": 9}}}}
        return resp

    with patch("requests.request", side_effect=mock_req_d):
        with patch("time.sleep", return_value=None):
            res = service.analyze("http://example-d.com")
            print("Result D:", res)

    print("\n--- TEST E: HTTP 429 without Retry-After ---")
    call_count_e = [0]
    def mock_req_e(method, url, **kwargs):
        resp = Mock()
        if call_count_e[0] == 0:
            call_count_e[0] += 1
            resp.status_code = 429
            resp.headers = {}
            resp.raise_for_status = Mock(side_effect=requests.HTTPError(response=resp))
        else:
            resp.status_code = 200
            resp.raise_for_status = Mock()
            resp.json = lambda: {"data": {"attributes": {"last_analysis_stats": {"malicious": 8, "suspicious": 8, "harmless": 8, "undetected": 8}}}}
        return resp

    with patch("requests.request", side_effect=mock_req_e):
        with patch("time.sleep", return_value=None):
            res = service.analyze("http://example-e.com")
            print("Result E:", res)

    print("\n--- TEST F: 500 server error ---")
    def mock_req_f(method, url, **kwargs):
        resp = Mock()
        resp.status_code = 500
        resp.raise_for_status = Mock(side_effect=requests.HTTPError(response=resp))
        return resp

    with patch("requests.request", side_effect=mock_req_f):
        res = service.analyze("http://example-f.com")
        print("Result F:", res)

    print("\n--- TEST G: Request timeout ---")
    def mock_req_g(method, url, **kwargs):
        raise requests.Timeout("Mocked timeout")

    with patch("requests.request", side_effect=mock_req_g):
        res = service.analyze("http://example-g.com")
        print("Result G:", res)

    print("\n--- TEST H: Malformed response ---")
    def mock_req_h(method, url, **kwargs):
        resp = Mock()
        resp.status_code = 200
        resp.raise_for_status = Mock()
        resp.json = lambda: {"unexpected": "json structure"}
        return resp

    with patch("requests.request", side_effect=mock_req_h):
        res = service.analyze("http://example-h.com")
        print("Result H:", res)

if __name__ == "__main__":
    run_tests()
