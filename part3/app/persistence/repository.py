from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[str(obj.id)] = obj
        return obj

    def get(self, obj_id):
        return self._storage.get(str(obj_id))

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            return obj
        return None

    def delete(self, obj_id):
        if str(obj_id) in self._storage:
            del self._storage[str(obj_id)]
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name, None) == attr_value), None)


class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model
        from app import db
        self.db = db

    def add(self, obj):
        self.db.session.add(obj)
        self.db.session.commit()
        return obj

    def get(self, obj_id):
        return self.db.session.get(self.model, str(obj_id))

    def get_all(self):
        return self.db.session.query(self.model).all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            self.db.session.commit()
            return obj
        return None

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            self.db.session.delete(obj)
            self.db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        return self.db.session.query(self.model).filter(getattr(self.model, attr_name) == attr_value).first()
