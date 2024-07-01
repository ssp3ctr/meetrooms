from typing import List, Dict, Any
from app.db.database import db
from app.utils.rule_evaluator import RuleEvaluator

class RuleService:
    def __init__(self):
        self.collection = db['rules']

    async def process_service_data(self, service_data: Dict[str, Any]) -> List[str]:
        json_keys = list(service_data.keys())
        pipeline = [
            {'$unwind': {'path': '$rules'}},
            {'$unwind': {'path': '$rules.rules', 'preserveNullAndEmptyArrays': True}},
            {'$unwind': {'path': '$rules.rules.rules', 'preserveNullAndEmptyArrays': True}},
            {'$unwind': {'path': '$rules.rules.rules.rules', 'preserveNullAndEmptyArrays': True}},
            {'$unwind': {'path': '$rules.rules.rules.rules.rules', 'preserveNullAndEmptyArrays': True}},
            {'$project': {'property': {
                '$cond': {
                    'if': {'$eq': ['$rules.element_type', 'rule']},
                    'then': '$rules.property',
                    'else': {
                        '$cond': {
                            'if': {'$eq': ['$rules.rules.element_type', 'rule']},
                            'then': '$rules.rules.property',
                            'else': {
                                '$cond': {
                                    'if': {'$eq': ['$rules.rules.rules.element_type', 'rule']},
                                    'then': '$rules.rules.rules.property',
                                    'else': None
                                }
                            }
                        }
                    }
                }
            }}},
            {'$group': {'_id': '$_id', 'fields': {'$addToSet': '$property'}}},
            {'$match': {'$expr': {'$setIsSubset': ['$fields', json_keys]}}},
            {'$lookup': {'from': 'rules', 'localField': '_id', 'foreignField': '_id', 'as': 'fullDocument'}},
            {'$replaceRoot': {'newRoot': {'$arrayElemAt': ['$fullDocument', 0]}}}
        ]
        
        filtered_documents = await self.collection.aggregate(pipeline).to_list(None)
        evaluator = RuleEvaluator()
        valid_documents = await evaluator.process_documents(filtered_documents, service_data)
        valid_document_ids = [str(doc['_id']) for doc in valid_documents]
        return valid_document_ids
