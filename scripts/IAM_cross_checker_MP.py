## This is an AI-generated Python script, which will identify which actions in a iam-dangerous-actions file, match all the IAM Roles in the results folder.
##
## Usage: python3 IAM_cross_checker_MP.py <iam-dangerous-actions-list.txt> <results-folder> <output-file.txt>
##
## Example: python3 IAM_cross_checker_MP.py iam-actions-HT-risk.txt results output-all-dangerous-roles.txt 
##    
## This script might need to be adjusted for PROD environments, it is currently for testing and PoC purposes. 


import os
import json
import fnmatch
import sys
import re

def normalize_action(action):
    """Normalize action names by converting to lowercase and stripping quotes"""
    return action.lower().strip('",')

def extract_statements(data):
    """Extract policy statements from various AWS policy formats"""
    statements = []
    
    if isinstance(data, dict):
        if "Statement" in data:
            stmt = data["Statement"]
            if isinstance(stmt, list):
                statements.extend(stmt)
            elif isinstance(stmt, dict):
                statements.append(stmt)
        elif "Effect" in data and "Action" in data:
            statements.append(data)
    
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and "Effect" in item and "Action" in item:
                statements.append(item)
    
    return statements

def main():
    if len(sys.argv) != 4:
        print("Usage: python iam_matcher.py <actions_file> <policies_dir> <output_file>")
        sys.exit(1)
    
    actions_file = sys.argv[1]
    policies_dir = sys.argv[2]
    output_file = sys.argv[3]
    
    # Read input actions
    try:
        raw_actions = []
        action_names = []
        with open(actions_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("//"):
                    continue  # Ignore comments and empty lines
                if ":" in line:
                    # Extract action name before the first colon, remove quotes and whitespace
                    match = re.match(r'["\']?([a-zA-Z0-9\-]+:[a-zA-Z0-9\-]+)["\']?', line)
                    if match:
                        action_name = match.group(1).lower()
                        action_names.append(action_name)
                        raw_actions.append(line)
        print(f"Loaded {len(raw_actions)} actions from {actions_file}")
    except Exception as e:
        print(f"Error reading actions file: {e}")
        sys.exit(1)
    
    # Validate directory
    if not os.path.isdir(policies_dir):
        print(f"Error: {policies_dir} is not a valid directory")
        sys.exit(1)
    
    # Process policies
    role_actions = {}
    files_processed = 0

    for filename in os.listdir(policies_dir):
        filepath = os.path.join(policies_dir, filename)
        if not os.path.isfile(filepath) or not filename.lower().endswith(('.json', '.txt')):
            continue
            
        try:
            with open(filepath) as f:
                data = json.load(f)
            files_processed += 1
        except Exception as e:
            print(f"Warning: Could not parse {filename} ({e})")
            continue
        
        # Get role name from filename (without extension)
        role_name = os.path.splitext(filename)[0]

        print(f"Processing IAM Role: {role_name}")  # <-- Added message

        role_actions[role_name] = set()
        
        # Extract statements from different policy formats
        statements = extract_statements(data)
        if not statements:
            continue
        
        # Process each statement
        for stmt in statements:
            if not isinstance(stmt, dict) or stmt.get("Effect") != "Allow":
                continue
                
            actions = stmt.get("Action", [])
            if isinstance(actions, str):
                actions = [actions]
            if not isinstance(actions, list):
                continue
            
            # Process each action pattern in the statement
            for pattern in actions:
                if not isinstance(pattern, str):
                    continue
                
                # Normalize pattern for case-insensitive matching
                pattern_norm = normalize_action(pattern)
                
                # Check against all input actions
                for idx, action in enumerate(raw_actions):
                    action_name = action_names[idx]
                    
                    # Handle wildcards in patterns
                    if fnmatch.fnmatch(action_name, pattern_norm):
                        role_actions[role_name].add(action)
    
    # Generate output file with requested format
    with open(output_file, 'w') as f:
        first_role = True
        
        for role_name, actions in sorted(role_actions.items()):
            if not actions:
                continue  # Skip roles with no matches
                
            if not first_role:
                # Add separator between roles
                f.write("\n" + "-" * 50 + "\n\n")
            else:
                first_role = False
                
            # Write role name header
            f.write(f"Role: {role_name}\n\n")
            
            # Write each action on a separate line
            for action in sorted(actions):
                f.write(f"  {action}\n")
    
    print(f"Report generated: {output_file}")
    print(f"Roles processed: {files_processed}")
    print(f"Roles with matching dangerous-iam-actions: {sum(1 for v in role_actions.values() if v)}")

if __name__ == "__main__":
    main()