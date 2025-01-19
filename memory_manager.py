from collections import deque
import time

class MemoryManager:
    def __init__(self, max_memories=1000, ttl=3600):  # 最多1000条记忆，生存时间1小时
        self.memories = deque(maxlen=max_memories)
        self.ttl = ttl

    def add_memory(self, content, importance=False):
        self.memories.append({
            'content': content,
            'timestamp': time.time(),
            'importance': importance
        })

    def get_relevant_memories(self, query):
        current_time = time.time()
        relevant = []
        for memory in self.memories:
            if current_time - memory['timestamp'] > self.ttl and not memory['importance']:
                continue
            if query.lower() in memory['content'].lower():
                relevant.append(memory['content'])
        return relevant

memory_manager = MemoryManager()
