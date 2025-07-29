#!/usr/bin/env python3
"""
Test script to verify the improved request type mapping for Close Account requests
"""

# Test the improved request type mapping logic for close account
def test_close_account_mapping():
    """Test the request type mapping for 'Close/deactivate/cancel my College Board account'"""
    
    # Simulate the 5th record's request type
    request_type_from_excel = "Close/deactivate/cancel my College Board account"
    print(f"🎯 Testing request type: '{request_type_from_excel}'")
    
    # Define the improved request type mappings (including new close account mappings)
    request_type_mappings = {
        # Delete data variants
        'request to delete my data': ['delete', 'removal', 'erase', 'remove'],
        'delete my data': ['delete', 'removal', 'erase', 'remove'],
        
        # Parent/CC information specific (exact match priority)
        'remove my parent\'s cc information': ['cc information', 'parent', 'credit card'],
        
        # Copy data variants  
        'request a copy of my data': ['copy', 'access', 'download', 'portability'],
        'copy of my data': ['copy', 'access', 'download', 'portability'],
        
        # Correct data variants
        'correct my data': ['correct', 'rectify', 'update', 'modify'],
        
        # Object to processing variants
        'opt out of search': ['opt out', 'search', 'withdraw consent'],
        
        # Close/deactivate account variants
        'close/deactivate/cancel my college board account': ['close', 'deactivate', 'cancel', 'account'],
        'close my college board account': ['close', 'deactivate', 'cancel', 'account'],
        'deactivate my college board account': ['close', 'deactivate', 'cancel', 'account'],
        'cancel my college board account': ['close', 'deactivate', 'cancel', 'account'],
        'close account': ['close', 'deactivate', 'cancel', 'account'],
        'deactivate account': ['close', 'deactivate', 'cancel', 'account'],
        'cancel account': ['close', 'deactivate', 'cancel', 'account']
    }
    
    # STEP 1: First try EXACT TEXT MATCHING (priority)
    search_keywords = []
    request_type_lower = request_type_from_excel.lower()
    exact_match_found = False
    
    print("\n🔍 STEP 1: Checking for exact phrase matches...")
    for key, keywords in request_type_mappings.items():
        if key in request_type_lower:
            search_keywords = keywords
            exact_match_found = True
            print(f"✅ Found exact mapping for '{request_type_from_excel}' -> keywords: {keywords}")
            break
    
    # STEP 2: If no exact mapping found, try KEYWORD-BASED MATCHING (fallback)
    if not search_keywords:
        print(f"\n⚠️ No exact mapping found for '{request_type_from_excel}', trying keyword-based matching...")
        
        if 'close' in request_type_lower or 'deactivate' in request_type_lower or 'cancel' in request_type_lower:
            search_keywords = ['close', 'deactivate', 'cancel', 'account']
            print(f"🔍 Using close/deactivate/cancel keywords: {search_keywords}")
        else:
            search_keywords = ['copy', 'access', 'download', 'portability']
            print(f"⚠️ No specific mapping found for '{request_type_from_excel}', defaulting to copy/access keywords")
    
    print(f"\n🔍 Final search keywords: {search_keywords}")
    
    # Simulate what form options might be available (from your description)
    available_form_options = [
        "Request a copy of my data",
        "Opt out of Search", 
        "Remove my parent's cc information",
        "Request to delete my data",
        "Close/deactivate/cancel my College Board account",
        "Request to correct my data"
    ]
    
    print(f"\n📋 Available form options:")
    for i, option in enumerate(available_form_options, 1):
        print(f"  {i}. {option}")
    
    # Test EXACT MATCHING first (improved logic)
    print(f"\n🎯 STEP 1: Testing exact match for: '{request_type_from_excel}'")
    exact_match_found = False
    for option in available_form_options:
        if request_type_from_excel.lower() in option.lower() or option.lower() in request_type_from_excel.lower():
            print(f"🎯 Found EXACT MATCH: '{option}'")
            print(f"✅ WOULD SELECT: '{option}' (EXACT MATCH)")
            exact_match_found = True
            break
    
    if not exact_match_found:
        # Test keyword matching (fallback)
        print(f"\n🔍 STEP 2: No exact match found, testing keyword-based matching...")
        for keyword in search_keywords:
            for option in available_form_options:
                if keyword.lower() in option.lower():
                    print(f"🔍 Found keyword match for '{keyword}': '{option}'")
                    print(f"⚠️  WOULD SELECT: '{option}' (keyword: '{keyword}')")
                    break
            else:
                continue
            break
    
    print(f"\n" + "="*80)
    print("📊 CONCLUSION:")
    print("="*80)
    
    if exact_match_found:
        print("✅ SUCCESS: The logic would correctly select the exact match!")
        print("   'Close/deactivate/cancel my College Board account' → 'Close/deactivate/cancel my College Board account'")
    else:
        print("⚠️  The exact match logic didn't work as expected.")
        print("   This means the form option text might be slightly different.")
        print("   The script would fall back to keyword matching.")
    
    # Test sub-options logic
    print(f"\n" + "="*80)
    print("📊 SUB-OPTIONS TEST:")
    print("="*80)
    
    # Test different Excel scenarios for close account sub-options
    test_scenarios = [
        {
            'name': 'Both Student and Educator',
            'close_student': 'Student account (if any)',
            'close_educator': 'Educator data (if any)'
        },
        {
            'name': 'Only Student',
            'close_student': 'Student account (if any)',
            'close_educator': ''
        },
        {
            'name': 'Only Educator',
            'close_student': '',
            'close_educator': 'Educator data (if any)'
        },
        {
            'name': 'Neither (empty Excel)',
            'close_student': '',
            'close_educator': ''
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n🧪 Testing scenario: {scenario['name']}")
        print(f"   Excel close_student: '{scenario['close_student']}'")
        print(f"   Excel close_educator: '{scenario['close_educator']}'")
        
        def should_select_option(excel_value):
            if excel_value is None:
                return False
            excel_str = str(excel_value).strip()
            if excel_str.lower() in ['nan', '', 'none', 'no', 'false', '0', 'n']:
                return False
            if excel_str.lower() in ['yes', 'true', '1', 'y']:
                return True
            if any(keyword in excel_str.lower() for keyword in ['account', 'student', 'educator']):
                return True
            return len(excel_str) > 0
        
        student_should_select = should_select_option(scenario['close_student'])
        educator_should_select = should_select_option(scenario['close_educator'])
        
        print(f"   🎓 Student account: {'SELECT' if student_should_select else 'SKIP'}")
        print(f"   👨‍🏫 Educator account: {'SELECT' if educator_should_select else 'SKIP'}")
        print(f"   📊 Total to select: {sum([student_should_select, educator_should_select])}")

if __name__ == "__main__":
    test_close_account_mapping()
