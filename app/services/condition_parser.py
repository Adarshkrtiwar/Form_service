import re
from typing import Dict, Any

class ConditionParser:
    @staticmethod
    def evaluate(condition: str, data: Dict[str, Any]) -> bool:
        if not condition:
            return True

        # Handle simple comparisons
        comparison_pattern = r'\$\.([a-zA-Z0-9_.]+)\s*(==|!=)\s*[\'"]?([a-zA-Z0-9_]+)[\'"]?'
        matches = re.findall(comparison_pattern, condition)
        
        for path, op, value in matches:
            current = data
            try:
                for part in path.split('.'):
                    current = current[part]
            except KeyError:
                return False
            
            current_str = str(current)
            if op == '==' and current_str != value:
                return False
            elif op == '!=' and current_str == value:
                return False
        
        # Handle AND/OR logic
        if ' and ' in condition.lower():
            parts = [part.strip() for part in condition.lower().split(' and ')]
            return all(ConditionParser.evaluate(part, data) for part in parts)
        elif ' or ' in condition.lower():
            parts = [part.strip() for part in condition.lower().split(' or ')]
            return any(ConditionParser.evaluate(part, data) for part in parts)
        
        return True