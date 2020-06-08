from flask_restful import Resource,reqparse
from models.Conti import ContiModel
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional
from sqlalchemy_continuum import make_versioned
from db import db


class Continuum_(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('lname',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def get(self, con_name):
        conti = ContiModel.find_by_name(con_name)
        try :
            if conti:
                return conti.json()
        except Exception as e:
            return {"message": "Record not found'{}'".format(e)}, 404
    def put(self, con_name):
        data = self.parser.parse_args()
        conti=ContiModel.find_by_name(con_name)
        if conti:
            conti.lname = data['lname']
            conti.save_to_db()
            
        else :
            return "error"
        return conti.json()
    @classmethod
    def delete(cls, con_name):
        conti = ContiModel.find_by_name(con_name)
        if conti:
            conti.delete_from_db()
            return {'message': 'Record deleted'}
        else :
            return {"Message":"Record Not FOUND"}

    def post(self, con_name):
        db.create_all()
        db.session.commit()
        data = self.parser.parse_args()
        conti = ContiModel(con_name,**data)
        try:
            conti.save_to_db()
        except Exception as e:
            return {"message": "An error occurred creating the Record.'{}'".format(e)}, 500
        return conti.json(), 201



class ContiList(Resource):
    @classmethod
    def get(cls):
        return {'conti': [conti.json() for conti in ContiModel.find_all()]}
