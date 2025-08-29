## This AI-generated Python script identifies which actions in a iam-dangerous-actions file, match the allowed IAM actions in any IAM policy.
##
## We dont need to remove the "" and "," from the IAM actions file, as the script will handle that for us.
## 
## Usage: python3 IAM_cross_checker_SP.py <iam-dangerous-actions-risk-list.txt> <IAM_policy-file.txt>
##
## Example: python3 IAM_cross_checker_SP.py iam-actions-all-risks.txt dangerous-iam-policy.json
##    
## This script might need to be adjusted for PROD environments, it is currently for testing and PoC purposes. 


import json
import sys
import re

def clean_permission(s):
    """Normalize permission strings for matching (lowercase, no extra spaces/quotes)"""
    s = re.sub(r'^[\s,"\']+|[\s,"\']+$', '', s)
    return re.sub(r'\s*:\s*', ':', s).lower()

def find_matching_permissions(permissions_file, policy_file):
    # Store original permissions and their cleaned versions
    original_permissions = []
    cleaned_permissions = []
    
    with open(permissions_file, 'r') as f:
        for line in f:
            stripped_line = line.strip()
            if (not stripped_line or 
                stripped_line.startswith('#') or 
                stripped_line.upper() == 'EOF'):
                continue
            original_permissions.append(stripped_line)
            cleaned_permissions.append(clean_permission(stripped_line))
    
    print(f"\n🔍 Loaded {len(original_permissions)} permissions:")
    for i, perm in enumerate(original_permissions[:10], 1):
        print(f"  {i:2d}. {perm}")
    if len(original_permissions) > 10:
        print(f"  ... and {len(original_permissions)-10} more")

    # Read policy
    with open(policy_file, 'r') as f:
        policy = json.load(f)
    
    # Extract ALLOW statements
    allow_patterns = []
    for stmt in policy.get('Statement', []):
        if stmt.get('Effect', '').lower() != 'allow':
            continue
        actions = stmt.get('Action', [])
        if isinstance(actions, str):
            allow_patterns.append(clean_permission(actions))
        else:
            allow_patterns.extend(clean_permission(a) for a in actions if isinstance(a, str))
    
    print(f"\n📜 Policy patterns:")
    for i, pattern in enumerate(allow_patterns, 1):
        print(f"  {i:2d}. {pattern}")

    # Custom matcher
    def is_match(permission, pattern):
        if pattern == "*": 
            return True
        service, _, pattern_action = pattern.partition(':')
        perm_service, _, perm_action = permission.partition(':')
        
        if service != perm_service:
            return False
        if pattern_action == "*": 
            return True
        regex_pattern = pattern_action.replace('*', '.*') + '$'
        return bool(re.match(regex_pattern, perm_action))

    # Match permissions using cleaned versions but store originals
    matched = []
    for idx, perm in enumerate(cleaned_permissions):
        for pattern in allow_patterns:
            if is_match(perm, pattern):
                matched.append(original_permissions[idx])
                break
    
    return matched

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 IAM_cross_checker_SP.py <iam-dangerous-actions-list.txt> <IAM_policy-file.txt>")
        sys.exit(1)
    
    permissions_file = sys.argv[1]
    policy_file = sys.argv[2]
    output_file = "matched_permissions_SP.txt"  # Default output filename
    
    print("="*60)
    print("AWS Permission Checker (Enhanced)")
    print("="*60)
    
    matches = find_matching_permissions(permissions_file, policy_file)
    
    # Write all matched permissions to file in their original format
    with open(output_file, 'w') as f:
        for match in matches:
            f.write(match + '\n')
       
    print("\n" + "="*60)
    print(f"💡 RESULT: {len(matches)} matches found")
    for i, match in enumerate(matches[:20], 1):
        print(f"  ✅ {match}")
    if len(matches) > 20:
        print(f"  ... and {len(matches)-20} more")
    print("="*60)

    print(f"\n💾 Saved {len(matches)} matched permissions to: {output_file}")