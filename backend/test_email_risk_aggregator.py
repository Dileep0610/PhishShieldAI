from services.email_risk_aggregator import aggregate_email_risk

def run_aggregator_tests():
    print("--- CHECKPOINT 14 UNIT TESTS ---")
    
    # Test 1
    # Legitimate email, No URLs -> Safe
    res1 = aggregate_email_risk("Legitimate", -0.5, [])
    print(f"Test 1: {res1['overall_risk_level']} (Expected: Safe)")
    
    # Test 2
    # Phishing email, No URLs -> High Risk
    res2 = aggregate_email_risk("Phishing", 0.5, [])
    print(f"Test 2: {res2['overall_risk_level']} (Expected: High Risk)")

    # Test 3
    # Legitimate email, Safe URL -> Safe
    res3 = aggregate_email_risk("Legitimate", -0.5, [{"risk_level": "Safe"}])
    print(f"Test 3: {res3['overall_risk_level']} (Expected: Safe)")

    # Test 4
    # Legitimate email, Suspicious URL -> Suspicious
    res4 = aggregate_email_risk("Legitimate", -0.5, [{"risk_level": "Suspicious"}])
    print(f"Test 4: {res4['overall_risk_level']} (Expected: Suspicious)")

    # Test 5
    # Legitimate email, High Risk URL -> High Risk
    res5 = aggregate_email_risk("Legitimate", -0.5, [{"risk_level": "High Risk"}])
    print(f"Test 5: {res5['overall_risk_level']} (Expected: High Risk)")

    # Test 6
    # Phishing email, Safe URL -> High Risk
    res6 = aggregate_email_risk("Phishing", 0.5, [{"risk_level": "Safe"}])
    print(f"Test 6: {res6['overall_risk_level']} (Expected: High Risk)")

    # Test 7
    # Phishing email, High Risk URL -> Very High Risk (highest severity)
    res7 = aggregate_email_risk("Phishing", 0.5, [{"risk_level": "High Risk"}])
    print(f"Test 7: {res7['overall_risk_level']} (Expected: Very High Risk)")

    # Test 8
    # Multiple URLs: Safe, Safe, High Risk -> High Risk
    res8 = aggregate_email_risk("Legitimate", -0.5, [
        {"risk_level": "Safe"},
        {"risk_level": "Safe"},
        {"risk_level": "High Risk"}
    ])
    print(f"Test 8: {res8['overall_risk_level']} (Expected: High Risk)")

    # Test 9
    # Multiple URLs: Safe, Suspicious -> Suspicious
    res9 = aggregate_email_risk("Legitimate", -0.5, [
        {"risk_level": "Safe"},
        {"risk_level": "Suspicious"}
    ])
    print(f"Test 9: {res9['overall_risk_level']} (Expected: Suspicious)")

    # Test 10
    # URL analysis failure (Error risk level) -> Email result still returned (Safe for Legitimate)
    res10 = aggregate_email_risk("Legitimate", -0.5, [{"risk_level": "Error"}])
    print(f"Test 10: {res10['overall_risk_level']} (Expected: Safe)")

if __name__ == "__main__":
    run_aggregator_tests()
