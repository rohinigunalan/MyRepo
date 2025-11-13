# Colorado Payload #8 - Alternative Test Data for Ryan Taylor
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
            "firstNm": "Ryan",
            "lastNm": "Taylor",
            "genderTxt": "",
            "middleInitial": "B",
            "studentSearchOptInInd": "N",
            "birthDt": "2003-04-25",
            "hsGradDt": "2021-06-03",
            "incomingAdminDt": None,
            "aiCd": "890123",
            "educationLevelCd": None,
            "preferredFirstNm": "",
            "sundayTestTakerInd": "N",
            "deceasedInd": "N",
            "activeInd": "Y"
        },
        "homeAddress": {
            "streetAddr1": "567 Aspen Creek Lane",
            "streetAddr2": "Unit 15",
            "streetAddr3": "",
            "urbanization": "",
            "city": "Lakewood",
            "zip5": "80226",
            "zip4": "7890",
            "stateCd": "CO",
            "carrierRt": "",
            "regionFipsCd": "",
            "province": "",
            "intlPostalCode": "",
            "countyFipsCd": "",
            "countryIsoCd": "US"
        },
        "personalEmail": {
            "emailAddress": "ryan.taylor@mailinator.com"
        },
        "homePhone": {
            "ndc": "303",
            "cc": "1",
            "local": "5551357",
            "prefInd": "Y",
            "intlPhone": None,
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 1
        },
        "altPhone": {
            "ndc": None,
            "cc": "61",
            "local": None,
            "prefInd": "U",
            "intlPhone": "412345678",
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 2
        },
        "personParent": {
            "firstNm": "Michelle",
            "lastNm": "Taylor",
            "emailAddr": "michelle.taylor@mailinator.com",
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
    print("Colorado Payload #8 - Ryan Taylor:")
    print(json.dumps(payload, indent=2))
