from typing import List, Dict, Any

class Rule:
    def __init__(self, element_type: str, rules: List[Dict[str, Any]] = None, property: str = None, equality_type: str = None, value: Any = None):
        self.element_type = element_type
        self.rules = rules or []
        self.property = property
        self.equality_type = equality_type
        self.value = value
