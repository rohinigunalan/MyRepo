# Colorado Payload #6 - Alternative Test Data for Daniel Wilson
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
            "firstNm": "Daniel",
            "lastNm": "Wilson",
            "genderTxt": "",
            "middleInitial": "A",
            "studentSearchOptInInd": "N",
            "birthDt": "2005-07-15",
            "hsGradDt": "2023-05-25",
            "incomingAdminDt": None,
            "aiCd": "567890",
            "educationLevelCd": None,
            "preferredFirstNm": "",
            "sundayTestTakerInd": "N",
            "deceasedInd": "N",
            "activeInd": "Y"
        },
        "homeAddress": {
            "streetAddr1": "3456 Mountain View Circle",
            "streetAddr2": "Building C",
            "streetAddr3": "",
            "urbanization": "",
            "city": "Pueblo",
            "zip5": "81001",
            "zip4": "5432",
            "stateCd": "CO",
            "carrierRt": "",
            "regionFipsCd": "",
            "province": "",
            "intlPostalCode": "",
            "countyFipsCd": "",
            "countryIsoCd": "US"
        },
        "personalEmail": {
            "emailAddress": "daniel.wilson@mailinator.com"
        },
        "homePhone": {
            "ndc": "719",
            "cc": "1",
            "local": "5552345",
            "prefInd": "Y",
            "intlPhone": None,
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 1
        },
        "altPhone": {
            "ndc": None,
            "cc": "52",
            "local": None,
            "prefInd": "U",
            "intlPhone": "5512345678",
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 2
        },
        "personParent": {
            "firstNm": "Linda",
            "lastNm": "Wilson",
            "emailAddr": "linda.wilson@mailinator.com",
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
    print("Colorado Payload #6 - Daniel Wilson:")
    print(json.dumps(payload, indent=2))
