from bs4 import BeautifulSoup
html_pos_1 = """<html><body><a href="https://example.com" onmouseover="window.status='https://fake.example.com'">Login</a></body></html>"""
soup = BeautifulSoup(html_pos_1, "lxml")
for a in soup.find_all('a'):
    print(repr(a))
    print(repr(a.get('onmouseover')))
    print(type(a.get('onmouseover')))
    
print("=======")
html_pos_2 = """<html><body><script>window.open('https://example.com');</script></body></html>"""
soup2 = BeautifulSoup(html_pos_2, "lxml")
for s in soup2.find_all('script'):
    print(repr(s))
    print(repr(s.string))
    
print("=======")
html_pos_3 = """<html><body oncontextmenu="return false;"></body></html>"""
soup3 = BeautifulSoup(html_pos_3, "lxml")
for t in soup3.find_all(True):
    print(t.name, repr(t.get('oncontextmenu')))
