2025-07-16T21:39:00.711Z	06b6bec6-c682-4b40-b49a-040c2b1b97c7	INFO	Hyperloop message created. Publishing 
{
    "header": {
        "version": "1.0.0",
        "event": {
            "category": "compliance",
            "name": "data-subject-rights-delete-notification",
            "type": "data",
            "version": "1.1.0",
            "origin": "cb",
            "timestamp": "2025-07-16T21:39:00.711Z"
        },
        "cb": {
            "env": "qa"
        }
    },
    "body": {
        "requestId": "ekul1278",
        "confirmationDueDate": 1727534693,
        "detail": {
            "channels": [
                "consumer"
            ],
            "scopes": [
                "student",
                "parent",
                "educator"
            ],
            "requestDetails": {
                "formInput": {
                    "requester": {
                        "parentFirstName": "",
                        "parentLastName": "",
                        "parentEmail": ""
                    },
                    "subject": {
                        "firstName": "Gerlyn",
                        "lastName": "Figueroa",
                        "emailAddress": "testdsremail@cbreston.org",
                        "alternateEmail": [
                            "zzikyepez@epsilon.cbreston.org",
                            "test@cb.org"
                        ],
                        "residentialAddress": {
                            "StreetAddress": "4435 W Avalon Ave",
                            "State": "California",
                            "Country": "United States",
                            "PostalCode": "93722",
                            "City": "Fresno"
                        },
                        "birthdate": "09/22/2007",
                        "phoneNumber": "800-867-5309",
                        "studentSchoolName": "N/A",
                        "studentGraduationYear": "2023",
                        "educatorSchoolAffiliation": "N/A"
                    }
                },
                "enrichment": {
                    "students": {
                        "200062692": {
                            "PersonId": "200062692",
                            "CatapultId": "us-east-1:8e07129e-af2f-cc96-eb8a-c6cada9676f6"
                        },
                        "200758264": {
                            "PersonId": "200758264",
                            "CatapultId": "us-east-1:8e07129e-af56-c221-bb4b-a0bfcacd8ffb"
                        }
                    },
                    "professionals": {
                        "11111": {
                            "ProfessionalId": "11111",
                            "Username": "joesmithatcenterville",
                            "ProfessionalAccountId": "546789"
                        },
                        "54678": {
                            "ProfessionalId": "54678",
                            "Username": "joesmithatcenterville",
                            "ProfessionalAccountId": "78712"
                        }
                    }
                }
            }
        }
    }
}