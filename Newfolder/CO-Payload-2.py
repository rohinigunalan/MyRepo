# Colorado Payload #2 - Alternative Test Data for Alexander Thompson
payload = {
    "studentInfoManagerRequest": {
        "requestName": "createPersonInfo",
        "channel": {
            "type": "C",
            # "aiCd":"343705",
            # "aiSourceCd":"CC"
            "orgId": "0"
        },
        "requestId": "67890-ABCDE",  # Changed from original
        "personInfo": {
            "givenName": "Alexander",    # Changed from Emma
            "familyName": "Thompson",    # Changed from Rodriguez  
            "middleName": "James",       # Changed from Marie
            "email": "alexander.thompson@gmail.com",  # Changed email
            "locale": "en_US",
            "dateBirth": "2000-03-15",   # Changed birth date
            "genderCd": "M",             # Changed to Male
            "incomingAdminDt": None,     # Using Python None instead of null
            "adminEducDt": "2018-05-20", # Changed date
            "educationLevelCd": None,    # Using Python None instead of null
            "demographicInfos": [
                {
                    "stateCd": "CO",
                    "ethnicityRace": [
                        {
                            "majorEthnicitySubgroupCd": "5"  # Changed ethnicity
                        }
                    ]
                }
            ]
        },
        "address": {
            "countrySubdivisionCd": "CO",
            "addressLine1": "456 Oak Street",      # Changed address
            "addressLine2": "Apartment 201",       # Changed apt
            "cityName": "Boulder",                 # Changed city
            "postalCd": "80301",                   # Changed zip
            "countryCd": "US"
        },
        "phones": [
            {
                "phoneTypeCd": "M",
                "intlPhone": None,    # Using Python None instead of null
                "phoneNumber": {
                    "countryCode": "1",
                    "ndc": None,      # Using Python None instead of null
                    "subscriber": "3035551234",  # Changed phone
                    "local": None,    # Using Python None instead of null
                    "ext": ""
                }
            }
        ]
    }
}

# Usage example:
if __name__ == "__main__":
    import json
    print("Colorado Payload #2 - Alexander Thompson:")
    print(json.dumps(payload, indent=2))
