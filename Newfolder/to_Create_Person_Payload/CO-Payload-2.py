# Colorado Payload #2 - Alternative Test Data
payload = {
    "studentInfoManagerRequest": {
        "requestName": "createPersonInfo",
        "channel": {
            "type": "C",
            # "aiCd":"343705",
            # "aiSourceCd":"CC"
            "orgId" :"0"
        },
        "personInfo": {
            "matchInd": "Y",
            "genderCd": "M",
            "firstNm": "Alexander",
            "lastNm": "Thompson",
            "genderTxt":"",
            "middleInitial": "J",
            "studentSearchOptInInd": "N",
            "birthDt": "2006-03-22",
            "hsGradDt": "2024-05-20",
            "incomingAdminDt": null,
            "aiCd": "456789",
            "educationLevelCd": null,
            "preferredFirstNm": "",
            "sundayTestTakerInd": "N",
            "deceasedInd": "N",
            "activeInd": "Y"
        },
        "homeAddress": {
            "streetAddr1": "1562 Pine Ridge Drive",
            "streetAddr2": "Apartment 304",
            "streetAddr3": "",
            "urbanization": "",
            "city": "Denver",
            "zip5": "80203",
            "zip4": "4578",
            "stateCd": "CO",
            "carrierRt": "",
            "regionFipsCd": "",
            "province": "",
            "intlPostalCode": "",
            "countyFipsCd": "",
            "countryIsoCd": "US"
        },
        "personalEmail": {
            "emailAddress": "alexander.thompson@mailinator.com"
        },
        "homePhone": {
            "ndc": "303",
            "cc": "1",
            "local": "5558923",
            "prefInd": "Y",
            "intlPhone": null,
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 1
        },
        "altPhone": {
            "ndc": null,
            "cc": "44",
            "local": null,
            "prefInd": "U",
            "intlPhone": "7789654123",
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 2
        },
        "personParent": {
            "firstNm": "David",
            "lastNm": "Thompson",
            "emailAddr": "david.thompson@mailinator.com",
            "newsletterSubscriptionInd": "Y",
            "ccSelectedInd": "Y"
        },
        "callerAppId": 303,
        "aiDomainCd":"SAT"
    }
}
