from extractors.html_extractor import HTMLExtractor

extractor = HTMLExtractor()

url = "https://google.com"

soup = extractor.fetch_html(url)

# STEP 5
print("MissingTitle :", extractor.extract_title(soup))

# STEP 7
print("Iframe :", extractor.extract_iframe(soup))

# STEP 9
print("InsecureForms :", extractor.extract_insecure_forms(soup))

print(
    "PctExtHyperlinks:",
    extractor.extract_external_hyperlinks(
        soup,
        url
    )
)
print(
    "PctExtResourceUrls :",
    extractor.extract_external_resources(soup, url)
)

form_features = extractor.extract_form_features(soup, url)

print("\nForm Features")

for key, value in form_features.items():
    print(f"{key}: {value}")


print("\nAdvanced HTML Features")

print(
    "ExtFavicon:",
    extractor.extract_external_favicon(soup, url)
)

print(
    "ExtMetaScriptLinkRT:",
    extractor.extract_meta_script_link_rt(soup, url)
)

print(
    "PctNullSelfRedirectHyperlinks:",
    extractor.extract_null_redirect_links(soup)
)

print(
    "FrequentDomainNameMismatch:",
    extractor.extract_domain_mismatch(soup, url)
)
