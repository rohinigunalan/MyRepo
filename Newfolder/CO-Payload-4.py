# Colorado Payload #4 - Alternative Test Data for Michael Chen
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
            "genderCd": "M",
            "firstNm": "Michael",
            "lastNm": "Chen",
            "genderTxt": "",
            "middleInitial": "W",
            "studentSearchOptInInd": "N",
            "birthDt": "2007-01-28",
            "hsGradDt": "2025-05-30",
            "incomingAdminDt": None,
            "aiCd": "345678",
            "educationLevelCd": None,
            "preferredFirstNm": "",
            "sundayTestTakerInd": "N",
            "deceasedInd": "N",
            "activeInd": "Y"
        },
        "homeAddress": {
            "streetAddr1": "4521 Oakwood Boulevard",
            "streetAddr2": "",
            "streetAddr3": "",
            "urbanization": "",
            "city": "Fort Collins",
            "zip5": "80525",
            "zip4": "1234",
            "stateCd": "CO",
            "carrierRt": "",
            "regionFipsCd": "",
            "province": "",
            "intlPostalCode": "",
            "countyFipsCd": "",
            "countryIsoCd": "US"
        },
        "personalEmail": {
            "emailAddress": "michael.chen@mailinator.com"
        },
        "homePhone": {
            "ndc": "970",
            "cc": "1",
            "local": "5553421",
            "prefInd": "Y",
            "intlPhone": None,
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 1
        },
        "altPhone": {
            "ndc": None,
            "cc": "86",
            "local": None,
            "prefInd": "U",
            "intlPhone": "13812345678",
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 2
        },
        "personParent": {
            "firstNm": "Jennifer",
            "lastNm": "Chen",
            "emailAddr": "jennifer.chen@mailinator.com",
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
    print("Colorado Payload #4 - Michael Chen:")
    print(json.dumps(payload, indent=2))
