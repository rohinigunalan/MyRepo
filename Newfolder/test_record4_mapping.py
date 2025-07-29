#!/usr/bin/env python3
"""
Test script to verify the improved request type mapping for Record 4
"""

# Test the improved request type mapping logic
def test_request_type_mapping():
    """Test the request type mapping for 'Remove my parent's cc information'"""
    
    # Simulate the 4th record's request type
    request_type_from_excel = "Remove my parent's cc information"
    print(f"🎯 Testing request type: '{request_type_from_excel}'")
    
    # Define the improved request type mappings
    request_type_mappings = {
        # Delete data variants
        'request to delete my data': ['delete', 'removal', 'erase', 'remove'],
        'delete my data': ['delete', 'removal', 'erase', 'remove'],
        'delete data': ['delete', 'removal', 'erase', 'remove'],
        'remove my data': ['delete', 'removal', 'erase', 'remove'],
        'erase my data': ['delete', 'removal', 'erase', 'remove'],
        
        # Parent/CC information specific (exact match priority)
        'remove my parent\'s cc information': ['cc information', 'parent', 'credit card'],
        'remove my parents cc information': ['cc information', 'parent', 'credit card'],
        'remove parent cc information': ['cc information', 'parent', 'credit card'],
        'remove my parent\'s credit card information': ['cc information', 'parent', 'credit card'],
        
        # Copy data variants  
        'request a copy of my data': ['copy', 'access', 'download', 'portability'],
        'copy of my data': ['copy', 'access', 'download', 'portability'],
        'copy my data': ['copy', 'access', 'download', 'portability'],
        'access my data': ['copy', 'access', 'download', 'portability'],
        'download my data': ['copy', 'access', 'download', 'portability'],
        
        # Correct data variants
        'correct my data': ['correct', 'rectify', 'update', 'modify'],
        'update my data': ['correct', 'rectify', 'update', 'modify'],
        'modify my data': ['correct', 'rectify', 'update', 'modify'],
        'rectify my data': ['correct', 'rectify', 'update', 'modify'],
        
        # Restrict processing variants
        'restrict processing': ['restrict', 'limit', 'stop processing'],
        'limit processing': ['restrict', 'limit', 'stop processing'],
        'stop processing my data': ['restrict', 'limit', 'stop processing'],
        
        # Object to processing variants
        'object to processing': ['object', 'opt out', 'withdraw consent'],
        'opt out': ['object', 'opt out', 'withdraw consent'],
        'opt out of search': ['opt out', 'search', 'withdraw consent'],
        'withdraw consent': ['object', 'opt out', 'withdraw consent']
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
        
        # Special handling for specific cases that might be mismatched
        if 'cc information' in request_type_lower or 'credit card' in request_type_lower:
            # This might be a specific request type, let's try to find exact match first
            search_keywords = ['cc information', 'credit card', 'parent', 'remove']
            print(f"🎯 Detected CC/credit card request, using specific keywords: {search_keywords}")
        elif 'parent' in request_type_lower and 'information' in request_type_lower:
            # Parent information removal - might be its own category
            search_keywords = ['parent', 'information', 'remove', 'cc']
            print(f"🎯 Detected parent information request, using specific keywords: {search_keywords}")
        elif 'delete' in request_type_lower or 'remove' in request_type_lower or 'erase' in request_type_lower:
            search_keywords = ['delete', 'removal', 'erase', 'remove']
            print(f"🔍 Using delete/remove keywords: {search_keywords}")
        elif 'copy' in request_type_lower or 'access' in request_type_lower or 'download' in request_type_lower:
            search_keywords = ['copy', 'access', 'download', 'portability']
            print(f"🔍 Using copy/access keywords: {search_keywords}")
        elif 'correct' in request_type_lower or 'update' in request_type_lower or 'modify' in request_type_lower:
            search_keywords = ['correct', 'rectify', 'update', 'modify']
            print(f"🔍 Using correct/update keywords: {search_keywords}")
        elif 'restrict' in request_type_lower or 'limit' in request_type_lower:
            search_keywords = ['restrict', 'limit', 'stop processing']
            print(f"🔍 Using restrict/limit keywords: {search_keywords}")
        elif 'object' in request_type_lower or 'opt out' in request_type_lower:
            search_keywords = ['object', 'opt out', 'withdraw consent']
            print(f"🔍 Using object/opt-out keywords: {search_keywords}")
        else:
            # Default to copy if nothing matches
            search_keywords = ['copy', 'access', 'download', 'portability']
            print(f"⚠️ No specific mapping found for '{request_type_from_excel}', defaulting to copy/access keywords")
    
    print(f"\n🔍 Final search keywords: {search_keywords}")
    
    # Simulate what form options might be available (from your screenshot)
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
    
    # Test EXACT MATCHING first (new improved logic)
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
        print("✅ SUCCESS: The improved logic would now correctly select the exact match!")
        print("   'Remove my parent's cc information' → 'Remove my parent's cc information'")
        print("   (Instead of incorrectly mapping to 'Request to delete my data')")
    else:
        print("⚠️  The exact match logic didn't work as expected.")
        print("   This means the form option text might be slightly different.")
        print("   The script would fall back to keyword matching.")

if __name__ == "__main__":
    test_request_type_mapping()
