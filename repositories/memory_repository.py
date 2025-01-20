import chromadb
from typing import List
from entities import ShortTermMemory
from entities import LongTermMemory


class MemoryRepository():
    def __init__(self):
        self.client = chromadb.Client()
    
    def add_short_term_memory(self, user_id: str, conversation_id: str, memory: ShortTermMemory):
        try:
            collection = self.client.get_collection(f"{user_id}-{conversation_id}")
        except Exception as e:
            collection = self.client.create_collection(f"{user_id}-{conversation_id}")
        try:
            collection.add(
                documents=[str(memory.model_dump_json())],
                ids=[memory.id]
            )
        except Exception as e:
            print(e)

    def get_short_term_memory(self, user_id: str, conversation_id: str) -> List[ShortTermMemory]:
        try:
            collection = self.client.get_collection(f"{user_id}-{conversation_id}")
            documents = collection.get(include=["documents"])["documents"]
            return [ShortTermMemory.parse_raw(memory) for memory in documents]
        except Exception as e:
            print(e)
            return []
    
    def add_long_term_memory(self, user_id: str, memory: LongTermMemory):
        try:
            collection = self.client.get_collection(f"{user_id}")
        except Exception as e:
            collection = self.client.create_collection(f"{user_id}")
        try:
            collection.add(
                documents=[str(memory.model_dump_json())],
                ids=[memory.id]
            )
        except Exception as e:
            print(e)

    def query_long_term_memory(self, user_id: str, query: str, top_k: int = 10) -> List[LongTermMemory]:
        try:
            collection = self.client.get_collection(f"{user_id}")
            documents = collection.query(
                query_texts=[query],
                n_results=top_k
            )["documents"][0]
            return [LongTermMemory.parse_raw(memory) for memory in documents]
        except Exception as e:
            print(e)
            return []
