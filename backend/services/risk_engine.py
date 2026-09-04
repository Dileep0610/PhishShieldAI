class RiskEngine:

    def calculate(
        self,
        prediction,
        confidence,
        whois,
        ssl,
        redirect,
        virustotal
    ):

        # -------------------------------------------------
        # TRUE RISK SCORE
        # 0   = Very Safe
        # 100 = Very High Risk
        # -------------------------------------------------

        risk = 0.0

        # -------------------------------------------------
        # ML MODEL
        # -------------------------------------------------
        #
        # prediction:
        # 0 = Legitimate
        # 1 = Phishing
        #
        # The model prediction gets the strongest weight.
        # -------------------------------------------------

        if prediction == 1:

            if confidence >= 90:
                risk += 55

            elif confidence >= 80:
                risk += 50

            elif confidence >= 70:
                risk += 45

            elif confidence >= 60:
                risk += 35

            else:
                risk += 25

        else:

            if confidence >= 95:
                risk += 0

            elif confidence >= 90:
                risk += 3

            elif confidence >= 80:
                risk += 7

            elif confidence >= 70:
                risk += 12

            else:
                risk += 18

        # -------------------------------------------------
        # WHOIS / DOMAIN AGE
        # -------------------------------------------------

        age = whois.get("domain_age_days")

        if age is not None:

            if age < 30:
                risk += 15

            elif age < 90:
                risk += 12

            elif age < 365:
                risk += 8

            elif age < 365 * 2:
                risk += 4

            elif age < 365 * 5:
                risk += 1

            else:
                risk += 0

        else:

            # Missing WHOIS information should be a
            # moderate signal, not an automatic phishing signal.
            risk += 5

        # -------------------------------------------------
        # SSL
        # -------------------------------------------------

        ssl_error = ssl.get("error", "")

        if ssl.get("ssl_valid") is True:
            risk += 0
        elif "HTTP URL" in ssl_error:
            risk += 0
        elif "CERTIFICATE_VERIFY_FAILED" in ssl_error or "certificate has expired" in ssl_error:
            risk += 15
        else:
            # Generic unavailability or socket error
            risk += 5

        # -------------------------------------------------
        # REDIRECTS
        # -------------------------------------------------

        redirect_risk = 0.0
        redirects = redirect.get("redirect_count", 0)

        if redirects == 1:
            redirect_risk += 1
        elif redirects > 1 and redirects <= 3:
            redirect_risk += 5
        elif redirects > 3:
            redirect_risk += 12

        if redirect.get("domain_changed"):
            redirect_risk += 8

        if redirect.get("protocol_changed"):
            redirect_risk += 10

        if redirect.get("uses_shortener"):
            redirect_risk += 8

        # Cap redirect risk at 30 combined
        risk += min(redirect_risk, 30.0)

        # -------------------------------------------------
        # VIRUSTOTAL
        # -------------------------------------------------

        vt_error = virustotal.get("error")

        if not vt_error:
            malicious = int(virustotal.get("malicious", 0) or 0)
            suspicious = int(virustotal.get("suspicious", 0) or 0)
            harmless = int(virustotal.get("harmless", 0) or 0)
            undetected = int(virustotal.get("undetected", 0) or 0)

            total_engines = malicious + suspicious + harmless + undetected

            if total_engines > 0:
                vt_risk = 0.0
                malicious_ratio = malicious / total_engines

                if malicious >= 10 or malicious_ratio >= 0.20:
                    vt_risk += 30
                elif malicious >= 5 or malicious_ratio >= 0.10:
                    vt_risk += 25
                elif malicious >= 3 or malicious_ratio >= 0.05:
                    vt_risk += 18
                elif malicious >= 2 or malicious_ratio >= 0.03:
                    vt_risk += 12
                elif malicious == 1:
                    vt_risk += 5

                if suspicious >= 5:
                    vt_risk += 12
                elif suspicious >= 2:
                    vt_risk += 8
                elif suspicious == 1:
                    vt_risk += 4

                risk += min(vt_risk, 30.0)

        # -------------------------------------------------
        # CAP SCORE
        # -------------------------------------------------

        risk = max(0, min(risk, 100))

        return round(risk, 2)