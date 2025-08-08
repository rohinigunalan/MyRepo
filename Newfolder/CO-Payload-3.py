# Colorado Payload #3 - Alternative Test Data for Sarah Martinez
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
            "firstNm": "Sarah",
            "lastNm": "Martinez",
            "genderTxt": "",
            "middleInitial": "E",
            "studentSearchOptInInd": "N",
            "birthDt": "2005-09-12",
            "hsGradDt": "2023-06-15",
            "incomingAdminDt": None,
            "aiCd": "789012",
            "educationLevelCd": None,
            "preferredFirstNm": "",
            "sundayTestTakerInd": "N",
            "deceasedInd": "N",
            "activeInd": "Y"
        },
        "homeAddress": {
            "streetAddr1": "2847 Maple Avenue",
            "streetAddr2": "Unit 12B",
            "streetAddr3": "",
            "urbanization": "",
            "city": "Colorado Springs",
            "zip5": "80918",
            "zip4": "7321",
            "stateCd": "CO",
            "carrierRt": "",
            "regionFipsCd": "",
            "province": "",
            "intlPostalCode": "",
            "countyFipsCd": "",
            "countryIsoCd": "US"
        },
        "personalEmail": {
            "emailAddress": "sarah.martinez@mailinator.com"
        },
        "homePhone": {
            "ndc": "719",
            "cc": "1",
            "local": "5554567",
            "prefInd": "Y",
            "intlPhone": None,
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 1
        },
        "altPhone": {
            "ndc": None,
            "cc": "33",
            "local": None,
            "prefInd": "U",
            "intlPhone": "6123456789",
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 2
        },
        "personParent": {
            "firstNm": "Maria",
            "lastNm": "Martinez",
            "emailAddr": "maria.martinez@mailinator.com",
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
    print("Colorado Payload #3 - Sarah Martinez:")
    print(json.dumps(payload, indent=2))
