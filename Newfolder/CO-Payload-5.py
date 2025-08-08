# Colorado Payload #5 - Alternative Test Data for Emily Johnson
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
            "firstNm": "Emily",
            "lastNm": "Johnson",
            "genderTxt": "",
            "middleInitial": "R",
            "studentSearchOptInInd": "N",
            "birthDt": "2004-11-03",
            "hsGradDt": "2022-06-10",
            "incomingAdminDt": None,
            "aiCd": "234567",
            "educationLevelCd": None,
            "preferredFirstNm": "",
            "sundayTestTakerInd": "N",
            "deceasedInd": "N",
            "activeInd": "Y"
        },
        "homeAddress": {
            "streetAddr1": "789 Cherry Lane",
            "streetAddr2": "Suite 5A",
            "streetAddr3": "",
            "urbanization": "",
            "city": "Boulder",
            "zip5": "80302",
            "zip4": "9876",
            "stateCd": "CO",
            "carrierRt": "",
            "regionFipsCd": "",
            "province": "",
            "intlPostalCode": "",
            "countyFipsCd": "",
            "countryIsoCd": "US"
        },
        "personalEmail": {
            "emailAddress": "emily.johnson@mailinator.com"
        },
        "homePhone": {
            "ndc": "303",
            "cc": "1",
            "local": "5557890",
            "prefInd": "Y",
            "intlPhone": None,
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 1
        },
        "altPhone": {
            "ndc": None,
            "cc": "49",
            "local": None,
            "prefInd": "U",
            "intlPhone": "30123456789",
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 2
        },
        "personParent": {
            "firstNm": "Robert",
            "lastNm": "Johnson",
            "emailAddr": "robert.johnson@mailinator.com",
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
    print("Colorado Payload #5 - Emily Johnson:")
    print(json.dumps(payload, indent=2))
