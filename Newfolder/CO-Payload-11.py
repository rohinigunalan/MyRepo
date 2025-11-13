# Colorado Payload #11 - Test Data for 13-year-old Student
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
            "lastNm": "Martinez",
            "genderTxt": "",
            "middleInitial": "A",
            "studentSearchOptInInd": "N",
            "birthDt": "2012-03-15",  # 13 years old (born March 15, 2012)
            "hsGradDt": "2030-06-15",  # Expected graduation in 2030
            "incomingAdminDt": None,
            "aiCd": "013579",
            "educationLevelCd": None,
            "preferredFirstNm": "",
            "sundayTestTakerInd": "N",
            "deceasedInd": "N",
            "activeInd": "Y"
        },
        "homeAddress": {
            "streetAddr1": "2468 Pine Ridge Circle",
            "streetAddr2": "Apt 7B",
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
            "emailAddress": "sophia.martinez13@mailinator.com"
        },
        "homePhone": {
            "ndc": "720",
            "cc": "1",
            "local": "5551357",
            "prefInd": "Y",
            "intlPhone": None,
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 1
        },
        "altPhone": {
            "ndc": None,
            "cc": "44",
            "local": None,
            "prefInd": "U",
            "intlPhone": "7890123456",
            "txtMsgAllowInd": "Y",
            "deviceTypeCd": 2
        },
        "personParent": {
            "firstNm": "Maria",
            "lastNm": "Martinez",
            "emailAddr": "maria.martinez.parent@mailinator.com",
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
    print("Colorado Payload #11 - Sophia Martinez (Age 13):")
    print(json.dumps(payload, indent=2))
    print(f"\nStudent Details:")
    print(f"Name: {payload['studentInfoManagerRequest']['personInfo']['firstNm']} {payload['studentInfoManagerRequest']['personInfo']['lastNm']}")
    print(f"Birth Date: {payload['studentInfoManagerRequest']['personInfo']['birthDt']} (Age 13)")
    print(f"Expected Graduation: {payload['studentInfoManagerRequest']['personInfo']['hsGradDt']}")
    print(f"Location: {payload['studentInfoManagerRequest']['homeAddress']['city']}, {payload['studentInfoManagerRequest']['homeAddress']['stateCd']}")
    print(f"Parent: {payload['studentInfoManagerRequest']['personParent']['firstNm']} {payload['studentInfoManagerRequest']['personParent']['lastNm']}")
    
    # Excel Format Data
    print(f"\n" + "="*80)
    print("📊 EXCEL FORMAT DATA:")
    print("="*80)
    
    # Extract data for Excel format
    person_info = payload['studentInfoManagerRequest']['personInfo']
    home_address = payload['studentInfoManagerRequest']['homeAddress']
    email_info = payload['studentInfoManagerRequest']['personalEmail']
    parent_info = payload['studentInfoManagerRequest']['personParent']
    
    print("\n📋 Column Headers:")
    headers = "Email Address\tFirst_Name\tLast_Name\tbirthDate\tphone\tcountry\tstateOrProvince\tpostalCode\tcity\tstreetAddress\tstudentSchoolName\tstudentGraduationYear\teducatorSchoolAffiliation\tRequest type to select\tparentFirstName\tparentLastName\tparentEmail"
    print(headers)
    
    print("\n📝 Data Row:")
    excel_data = f"{email_info['emailAddress']}\t{person_info['firstNm']}\t{person_info['lastNm']}\t{person_info['birthDt'].replace('-', '/')}\t720{payload['studentInfoManagerRequest']['homePhone']['local']}\tUnited States\tColorado\t{home_address['zip5']}\t{home_address['city']}\t{home_address['streetAddr1']}, {home_address['streetAddr2']}\tThornton Middle School\t2030\tN/A\tClose/deactivate/cancel my College Board account\t{parent_info['firstNm']}\t{parent_info['lastNm']}\t{parent_info['emailAddr']}"
    print(excel_data)
    
    print("\n📊 Ready for Excel Copy-Paste:")
    print("Headers and data are tab-separated - copy and paste directly into Excel!")
    print("="*80)
