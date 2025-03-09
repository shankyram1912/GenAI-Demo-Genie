customerprofile_response = {
    "customer_fname": "Shanky",
    "customer_postpaidmobile": "60000002",
    "customer_billingacct": "1247891"    
}

balances_response = {
    "mobile": "60000002",
    "data":[
            {
                "type": "High Speed Data",
                "remaining": 2.7,
                "units": "GB",
                "expiry": "01-May-2025",
                "is_expiring_soon": False
            },
            {
                "type": "Japan Roaming Data",
                "remaining": 12,
                "units": "GB",
                "expiry": "15-Apr-2025",
                "is_expiring_soon": True
            }          
    ], 
    "voice": {
        "type": "Local Voice",
        "remaining": 20,
        "units": "mins",
        "expiry": "01-May-2025",
        "is_expiring_soon": False
    },
    "sms": {
        "type": "Local SMS",
        "remaining": 251,
        "units": "mins",
        "expiry": "01-May-2025",
        "is_expiring_soon": False
    }
}

plans_response = {
    "basicplan": {
        "plan_name": "Postpaid Lite Plan @ 200 PHP",
        "can_expire": False
    },
    "dataplans": [
        {
            "plan_name": "Monthly Add On High Speed Data Package 5 GB @ 120 PHP",
            "can_expire": True,
            "expiry_date": "01-May-2025",
            "is_expiring_soon": False
        }        
    ],
    "roamingplans": [
        {
            "plan_name": "Japan 30 Day Plan @ 1000 PHP",
            "can_expire": True,
            "expiry_date": "15-Apr-2025",
            "is_expiring_soon": True
        }
    ]
}

bundles_response = {
    "bundledetails": [
        {
            "bundle_name": "IPhone 13, 2 Year Contract",
            "bundle_expiry_date": "01-Mar-2026",
            "monthly_emi": "1200 PHP",
            "number_pending_emi_payments": "12",
            "last_emi_status": "OVERDUE",
            "emi_due_date": "01-Mar-2025"

        }
    ] 
}