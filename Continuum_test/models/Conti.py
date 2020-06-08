from sqlalchemy_continuum import make_versioned, version_class, parent_class
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from flask_continuum import VersioningMixin
import psycopg2
from flask_sqlalchemy_session import flask_scoped_session
from flask import jsonify
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

from db import db

make_versioned(user_cls=None)



class ContiModel(db.Model,VersioningMixin):
    __versioned__ = {}
    __tablename__ = 'test_db'
    

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    con_name = db.Column(db.Unicode(255))
    lname = db.Column(db.Unicode(80))
    sa.orm.configure_mappers()

    def __init__(self,con_name,lname):
        self.con_name=con_name
        self.lname = lname
   

    def json(self):
        return{
            'id':self.id,
            'name':self.con_name,
            'Login_Name':self.lname
        }
    
    @classmethod 
    def find_by_name(cls,con_name):
        return cls.query.filter_by(con_name=con_name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    def save_to_db(self) :
        db.session.add(self)
        db.session.commit()


