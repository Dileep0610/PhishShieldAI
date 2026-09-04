from bs4 import BeautifulSoup
from extractors.html_extractor import HTMLExtractor
from services.feature_pipeline import FeaturePipeline
import pandas as pd
import joblib

def run_tests():
    extractor = HTMLExtractor()
    pipeline = FeaturePipeline()
    
    print("\n--- Test 1/2: FakeLinkInStatusBar ---")
    html_pos_1 = """<html><body><a href="https://example.com" onmouseover="window.status='https://fake.example.com'">Login</a></body></html>"""
    html_neg_1 = """<html><body><a href="https://example.com">Login</a></body></html>"""
    
    soup_pos = BeautifulSoup(html_pos_1, "lxml")
    f_pos = extractor.extract_form_features(soup_pos, "https://example.com")
    print("FakeLinkInStatusBar POS:", f_pos.get("FakeLinkInStatusBar"))

    soup_neg = BeautifulSoup(html_neg_1, "lxml")
    f_neg = extractor.extract_form_features(soup_neg, "https://example.com")
    print("FakeLinkInStatusBar NEG:", f_neg.get("FakeLinkInStatusBar"))

    print("\n--- Test 3/4: PopUpWindow ---")
    html_pos_2 = """<html><body><script>window.open('https://example.com');</script></body></html>"""
    html_neg_2 = """<html><body><script>console.log('hi');</script></body></html>"""
    
    soup_pos = BeautifulSoup(html_pos_2, "lxml")
    f_pos = extractor.extract_form_features(soup_pos, "https://example.com")
    print("PopUpWindow POS:", f_pos.get("PopUpWindow"))
    
    soup_neg = BeautifulSoup(html_neg_2, "lxml")
    f_neg = extractor.extract_form_features(soup_neg, "https://example.com")
    print("PopUpWindow NEG:", f_neg.get("PopUpWindow"))
    
    print("\n--- Test 5/6: RightClickDisabled ---")
    html_pos_3 = """<html><body oncontextmenu="return false;"></body></html>"""
    html_neg_3 = """<html><body>Hello</body></html>"""
    
    soup_pos = BeautifulSoup(html_pos_3, "lxml")
    f_pos = extractor.extract_form_features(soup_pos, "https://example.com")
    print("RightClickDisabled POS:", f_pos.get("RightClickDisabled"))
    
    soup_neg = BeautifulSoup(html_neg_3, "lxml")
    f_neg = extractor.extract_form_features(soup_neg, "https://example.com")
    print("RightClickDisabled NEG:", f_neg.get("RightClickDisabled"))
    
    print("\n--- Test 7: Real webpage extraction ---")
    soup_real = extractor.fetch_html("https://example.com")
    f_real = extractor.extract_form_features(soup_real, "https://example.com")
    print("Real page FakeLinkInStatusBar:", f_real.get("FakeLinkInStatusBar"))
    print("Real page PopUpWindow:", f_real.get("PopUpWindow"))
    print("Real page RightClickDisabled:", f_real.get("RightClickDisabled"))
    
    print("\n--- Test 8/9/10: FeaturePipeline integration & Feature contract & RT safety ---")
    df = pipeline.build_vector("https://example.com")
    print("Feature count:", df.shape[1])
    print("Exact 47 features match:", list(df.columns) == pipeline.feature_names)
    print("RT features safety (e.g. PctExtResourceUrlsRT is NaN):", pd.isna(df["PctExtResourceUrlsRT"].iloc[0]))
    
if __name__ == '__main__':
    run_tests()
