# todoserver\store.py

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)    
    summary = Column(String)
    description = Column(String)

MAX_SUMMARY_LENGTH = 119
class BadSummaryError(Exception):
    pass

def validate_summary(summary):
    if len(summary) > MAX_SUMMARY_LENGTH or "\n" in summary:
        raise BadSummaryError
    
class TaskStore():
    def __init__(self, engine_spec):
        self.engine = create_engine(engine_spec)
        Base.metadata.create_all(self.engine) # creates table if not exist
        self.Session = sessionmaker(bind=self.engine)
    
    def get_all_tasks(self):
        return [{"id": task.id, "summary": task.summary, "description": task.description} 
            for task in self.Session().query(Task).all()]
    
    def create_task(self, summary, description):
        validate_summary(summary)
        session = self.Session()
        task = Task(
            summary = summary,
            description = description
        )
        session.add(task)
        session.commit()
        return task.id
    
    def modify_task(self, task_id, summary, description):
        validate_summary(summary)
        session = self.Session()
        #task = session.query(Task).get(task_id)        # SQLAlchemy 1.x
        task = session.get(Task, task_id)               # SQLAlchemy 2.0
        if task is None:
            modified = False
        else:
            modified = True
            task.summary = summary
            task.description = description
            session.add(task)
            session.commit()
        
        return modified
    
    def task_details(self, task_id):
        #task = self.Session().query(Task).get(task_id) # SQLAlchemy 1.x
        task = self.Session().get(Task, task_id)        # SQLAlchemy 2.0
        if task is None: # if no value is returned by get (returns None if no value)
            return None
        
        return {
            "id": task.id,
            "summary": task.summary,
            "description": task.description,
        }   # return a dictionary
        
    def delete_task(self, task_id):
        session = self.Session()
        #task = session.query(Task).get(task_id)        # SQLAlchemy 1.x
        task = session.get(Task, task_id)               # SQLAlchemy 2.0
        if task is None:
            deleted = False
        else:
            deleted = True
            session.delete(task)
            session.commit()
            
        return deleted
    
    def _delete_all_tasks(self):
        session = self.Session()
        session.query(Task).delete()
        session.commit()
        
