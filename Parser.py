import re
import typing
from typing import List, Dict, Any
import sys

class NaturalLanguageParser:
    def __init__(self):
        self.variables: Dict[str, int] = {}
        self.collections: Dict[str, List[str]] = {}
        
        self.rules = [
            {
                'pattern': r'There once was a (\w+) named (\w+)',
                'type': 'declaration',
                'transform': self.handle_declaration
            },
            {
                'pattern': r'(\w+) had (\d+) (\w+)',
                'type': 'assignment',
                'transform': self.handle_assignment
            },
            {
                'pattern': r'(\w+) (earned|gained|found|lost|spent) (\d+) (\w+)',
                'type': 'modification',
                'transform': self.handle_modification
            },
            {
                'pattern': r'Bards told the tale of (\w+)',
                'type': 'output',
                'transform': self.handle_output
            },
            {
                'pattern': r'(?:He|She) formed a party with ([\w\s,]+(?:, and \w+)?)',
                'type': 'party_formation',
                'transform': self.handle_party_formation
            },
            {
                'pattern': r'For each (\w+) in the (\w+), (?:they|he|she) gained (\d+) (\w+)',
                'type': 'iteration',
                'transform': self.handle_iteration
            },
            {
                'pattern': r'If (\w+) was pure, (?:he|she) could complete the quest',
                'type': 'purity_condition',
                'transform': self.handle_purity_condition
            },
            {
                'pattern': r'If (?:he|she) defeats the demon king, the quest is complete',
                'type': 'boolean_output',
                'transform': self.handle_boolean_output
            },
        ]

    def parse(self, code: str) -> str:
        statements = [s.strip() for s in code.split('.') if s.strip()]
        
        transformed_code = []
        
        for statement in statements:
            matched = False
            for rule in self.rules:
                match = re.match(rule['pattern'], statement)
                if match:
                    result = rule['transform'](*match.groups())
                    if result:
                        transformed_code.append(result)
                        matched = True
                        break
            
            if not matched:
                print(f"Warning: Could not parse statement: {statement}")
        
        return '\n'.join(transformed_code)

    def handle_declaration(self, character_type: str, var_name: str) -> str:
        return f"{var_name} = 0"

    def handle_assignment(self, var_name: str, value: str, unit: str) -> str:
        self.variables[var_name] = int(value)
        return f"{var_name} = {value}"
    
    def handle_purity_condition(self, var_name: str) -> str:
        return f"quest_complete = {var_name} <= 0"

    def handle_boolean_output(self) -> str:
        return f"""if quest_complete:
    print("Quest completed!")
else:
    print("Quest incomplete. The hero is not pure.")"""

    def handle_modification(self, var_name: str, operation: str, amount: str, unit: str) -> str:
        amount = int(amount)
        if operation in ['earned', 'gained', 'found']:
            return f"{var_name} += {amount}"
        elif operation in ['lost', 'spent']:
            return f"{var_name} -= {amount}"

    def handle_output(self, var_name: str) -> str:
        return f"print({var_name})"

    def handle_party_formation(self, members_str: str) -> str:
        members = [member.strip() for member in re.split(r',\s*| and ', members_str)]
        party_name = 'party'
        self.collections[party_name] = members
        return f"{party_name} = {members}"

    def handle_iteration(self, member_name: str, collection_name: str, amount: str, unit: str) -> str:
        amount = int(amount)
        return f"""for {member_name} in {collection_name}:
    Vars += {amount}"""

def main(input_file: str):
    try:
        with open(input_file, 'r') as file:
            scenarios = file.read()
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
        return
    except IOError:
        print(f"Error: Could not read file {input_file}")
        return

    parser = NaturalLanguageParser()

    print("Original 'Story':")
    print(scenarios.strip())
    print("\nTranslated Code:")
    
    transformed_code = parser.parse(scenarios)
    print(transformed_code)
    
    print("\nCode Output:")
    local_namespace = {}
    
    exec(transformed_code, {}, local_namespace)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Need a 'Story' to read through. Add it after 'Parser.py'.")
        sys.exit(1)

    input_file = sys.argv[1]
    main(input_file)
