# Colorado Payload #7 - Alternative Test Data for Jessica Garcia
payload = {
    "studentInfoManagerRequest": {
        "requestName": "createPersonInfo",
        "channel": {
            "type": "C",
            # "aiCd":"343705",
            # "aiSourceCd":"CC"
            "orgId": "0"
        },
        "personInfo": {
            "matchInd": "Y",
            "genderCd": "F",
            "firstNm": "Jessica",
            "lastNm": "Garcia",
            "genderTxt": "",
            "middleInitial": "L",
            "studentSearchOptInInd": "N",
            "birthDt": "2006-12-08",
            "hsGradDt": "2024-12-15",
            "incomingAdminDt": None,
            "aiCd": "678901",
            "educationLevelCd": None,
            "preferredFirstNm": "",
            "sundayTestTakerInd": "N",
            "deceasedInd": "N",
            "activeInd": "Y"
        },
        "homeAddress": {
            "streetAddr1": "9821 Sunset Ridge Road",
            "streetAddr2": "Apt 7B",
            "streetAddr3": "",
            "urbanization": "",
            "city": "Aurora",
            "zip5": "80012",
            "zip4": "3456",
            "stateCd": "CO",
            "carrierRt": "",
            "regionFipsCd": "",
            "province": "",
            "intlPostalCode": "",
            "countyFipsCd": "",
            "countryIsoCd": "US"
        },
        "personalEmail": {
            "emailAddress": "jessica.garcia@mailinator.com"
        },
        "homePhone": {
            "ndc": "303",
            "cc": "1",
            "local": "5556789",
            "prefInd": "Y",
            "intlPhone": None,
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 1
        },
        "altPhone": {
            "ndc": None,
            "cc": "34",
            "local": None,
            "prefInd": "U",
            "intlPhone": "91234567890",
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 2
        },
        "personParent": {
            "firstNm": "Carlos",
            "lastNm": "Garcia",
            "emailAddr": "carlos.garcia@mailinator.com",
            "newsletterSubscriptionInd": "Y",
            "ccSelectedInd": "Y"
        },
        "callerAppId": 303,
        "aiDomainCd": "SAT"
    }
}

# Usage example:
if __name__ == "__main__":
    import json
    print("Colorado Payload #7 - Jessica Garcia:")
    print(json.dumps(payload, indent=2))
