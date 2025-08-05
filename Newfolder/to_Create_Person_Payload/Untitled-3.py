{
    "header": {
        "version": "1.0.0",
        "event": {
            "category": "compliance",
            "name": "data-subject-rights-information-notification",
            "type": "data",
            "version": "1.1.0",
            "origin": "cb",
            "timestamp": "2025-07-14T21:12:57.289Z"
        },
        "cb": {
            "env": "qa"
        }
    },
    "body": {
        "requestId": "palm888",
        "detail": {
            "channels": [
                "institutional"
            ],
            "scopes": [
                "parent"
            ],
            "requestDetails": {
                "formInput": {
                    "requester": {
                        "parentFirstName": "",
                        "parentLastName": "",
                        "parentEmail": ""
                    },
                    "subject": {
                        "firstName": "firstName",
                        "lastName": "lastName",
                        "emailAddress": "notifyIntTest@cb.com",
                        "alternateEmail": [
                            "intTestAlt@cb.com"
                        ],
                        "residentialAddress": {},
                        "birthdate": "09/09/1970",
                        "phoneNumber": "800-867-5309",
                        "studentGraduationYear": "",
                        "educatorSchoolAffiliation": ""
                    }
                },
                "enrichment": {
                    "students": [],
                    "professionals": []
                }
            }
        }
    }
}