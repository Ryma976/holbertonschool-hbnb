import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """تحديث وقت التعديل عند حفظ البيانات"""
        self.updated_at = datetime.now()

    def update(self, data):
        """تحديث الخصائص ديناميكياً"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
