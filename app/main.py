from sqlalchemy import create_engine,String,CHAR,Text,Column,Boolean,Integer,DateTime,ForeignKey
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

DATABASE_URL = ""

engine = create_engine(DATABASE_URL,echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = "Users"
    id = Column('user_id',Integer,primary_key=True)
    user_name = Column("users",String)
    email = Column('Emails', String,unique=True)
    is_active = Column("is_active", Boolean)
    
    post = relationship("Post")
    def __init__(self,id,user_name,email,is_active):
        self.id = id
        self.user_name = user_name
        self.email = email
        self.is_active = is_active
        
    def __repr__(self):
        return f"{self.id} -> {self.user_name} -> {self.email} -> {self.is_active}"
    
    
class Post(Base):
    __tablename__= "Post"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey('users.id'))
    def __repr__(self):
        return f"{self.id} ,{self.title}, {self.author_id}"

Base.metadata.create_all(engine)
Session = sessionmaker()
session = Session(bind=engine)



def Create_User(id,user_name,email, is_active=False):
    new_user = User(id=id,user_name=user_name,email=email,is_active=is_active)
    session.add(new_user)
    session.commit()
    return new_user


def get_all_users():
    return session.query(User).all()

def get_user_by_name(user_name):
    return session.query(User).filter(User.user_name == user_name).first()

def get_active_users():
    return session.query(User).filter(User.is_active==True).all()


def get_post_by_user(user_id):
    return session.query(Post).filter(Post.author_id == user_id).all()


# Update & modifying reocrds 

def update_username(user_id,username):