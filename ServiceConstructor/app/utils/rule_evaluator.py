from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

class RuleEvaluator:
    def check_condition(self, field_value, equality_type, value):
        if equality_type == ">":
            return field_value > value
        elif equality_type == "<":
            return field_value < value
        elif equality_type == "=":
            return field_value == value
        elif equality_type == "like":
            return value in field_value
        else:
            return False

    def evaluate_rules(self, rules, data):
        for rule in rules:
            element_type = rule.get('element_type')
            if element_type == 'Group_AND':
                if not all(self.evaluate_rules([sub_rule], data) for sub_rule in rule['rules']):
                    return False
            elif element_type == 'Group_OR':
                if not any(self.evaluate_rules([sub_rule], data) for sub_rule in rule['rules']):
                    return False
            elif element_type == 'Group_NOT':
                if any(self.evaluate_rules([sub_rule], data) for sub_rule in rule['rules']):
                    return False
            elif element_type == 'rule':
                property_name = rule.get('property')
                if property_name in data:
                    if not self.check_condition(data[property_name], rule['equality_type'], rule['value']):
                        return False
                else:
                    return False
        return True

    async def process_documents(self, documents, data):
        valid_documents = []
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.evaluate_rules, doc.get('rules', []), data): doc for doc in documents}
            for future in as_completed(futures):
                doc = futures[future]
                if future.result():
                    valid_documents.append(doc)
        return valid_documents
