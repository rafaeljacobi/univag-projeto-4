from flask_sqlalchemy import SQLAlchemy
import os.path

db = SQLAlchemy()

def create_database(app):
    with app.app_context():
        db.create_all()

def clear_database(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        
def db_file_path():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file_dir = os.path.join(base_dir, "instance/database.db")
    return file_dir

# Classe para um CRUD genérico
class CRUD:
    def __init__(self, model_class):
        self.model_class = model_class
        self.Session = db.session

    def create(self, data):
        instance = self.model_class(**data)
        self.Session.add(instance)
        self.Session.commit()
        self.Session.refresh(instance)
        return instance

    def find(self, att, value):
        att_dynamic = getattr(self.model_class, att)
        result = self.model_class.query.filter(att_dynamic == value).first()
        return result

    def find_all(self, **kwargs):
        filters = []
        for att, value in kwargs.items():
            att_dynamic = getattr(self.model_class, att)
            filters.append(att_dynamic == value)
        result = self.model_class.query.filter(*filters)
        return result

    def get_all(self):
        return self.Session.query(self.model_class).all()

    def get_by_id(self, id):
        return self.Session.query(self.model_class).get(id)

    def update(self, id, data):
        instance = self.Session.query(self.model_class).get(id)
        if instance:
            for field, value in data.items():
                setattr(instance, field, value)
            self.Session.commit()
            return instance
        else:
            print(f">>> Object with ID {id} not found")

    def delete(self, id):
        instance = self.Session.query(self.model_class).get(id)
        if instance:
            self.Session.delete(instance)
            self.Session.commit()
        else:
            print(f">>> Object with ID {id} not found")
            
    def delete_all(self):
        query = self.model_class.query.delete()
        self.Session.commit()