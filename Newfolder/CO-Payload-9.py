# Colorado Payload #9 - Alternative Test Data for Sophia Anderson
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
            "firstNm": "Sophia",
            "lastNm": "Anderson",
            "genderTxt": "",
            "middleInitial": "M",
            "studentSearchOptInInd": "N",
            "birthDt": "2005-02-14",
            "hsGradDt": "2023-05-18",
            "incomingAdminDt": None,
            "aiCd": "901234",
            "educationLevelCd": None,
            "preferredFirstNm": "",
            "sundayTestTakerInd": "N",
            "deceasedInd": "N",
            "activeInd": "Y"
        },
        "homeAddress": {
            "streetAddr1": "1234 Mountain Sky Drive",
            "streetAddr2": "Penthouse 20",
            "streetAddr3": "",
            "urbanization": "",
            "city": "Thornton",
            "zip5": "80241",
            "zip4": "2468",
            "stateCd": "CO",
            "carrierRt": "",
            "regionFipsCd": "",
            "province": "",
            "intlPostalCode": "",
            "countyFipsCd": "",
            "countryIsoCd": "US"
        },
        "personalEmail": {
            "emailAddress": "sophia.anderson@mailinator.com"
        },
        "homePhone": {
            "ndc": "303",
            "cc": "1",
            "local": "5559876",
            "prefInd": "Y",
            "intlPhone": None,
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 1
        },
        "altPhone": {
            "ndc": None,
            "cc": "47",
            "local": None,
            "prefInd": "U",
            "intlPhone": "91234567",
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 2
        },
        "personParent": {
            "firstNm": "Katherine",
            "lastNm": "Anderson",
            "emailAddr": "katherine.anderson@mailinator.com",
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
    print("Colorado Payload #9 - Sophia Anderson:")
    print(json.dumps(payload, indent=2))
