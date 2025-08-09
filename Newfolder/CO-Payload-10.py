# Colorado Payload #10 - Alternative Test Data for Ethan Rodriguez
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
            "firstNm": "Ethan",
            "lastNm": "Rodriguez",
            "genderTxt": "",
            "middleInitial": "D",
            "studentSearchOptInInd": "N",
            "birthDt": "2004-08-30",
            "hsGradDt": "2022-05-28",
            "incomingAdminDt": None,
            "aiCd": "012345",
            "educationLevelCd": None,
            "preferredFirstNm": "",
            "sundayTestTakerInd": "N",
            "deceasedInd": "N",
            "activeInd": "Y"
        },
        "homeAddress": {
            "streetAddr1": "8765 Valley Vista Way",
            "streetAddr2": "",
            "streetAddr3": "",
            "urbanization": "",
            "city": "Westminster",
            "zip5": "80031",
            "zip4": "1357",
            "stateCd": "CO",
            "carrierRt": "",
            "regionFipsCd": "",
            "province": "",
            "intlPostalCode": "",
            "countyFipsCd": "",
            "countryIsoCd": "US"
        },
        "personalEmail": {
            "emailAddress": "ethan.rodriguez@mailinator.com"
        },
        "homePhone": {
            "ndc": "303",
            "cc": "1",
            "local": "5554680",
            "prefInd": "Y",
            "intlPhone": None,
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 1
        },
        "altPhone": {
            "ndc": None,
            "cc": "39",
            "local": None,
            "prefInd": "U",
            "intlPhone": "312345678",
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 2
        },
        "personParent": {
            "firstNm": "Patricia",
            "lastNm": "Rodriguez",
            "emailAddr": "patricia.rodriguez@mailinator.com",
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
    print("Colorado Payload #10 - Ethan Rodriguez:")
    print(json.dumps(payload, indent=2))
