from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Filter:
    def __init__( self , data ):
        self.id = data['id']
        self.type = data['type']
        self.reason = data['reason']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        
    @classmethod
    def all(cls):
        query = "SELECT * FROM filters;"
        results = connectToMySQL('user').query_db(query)
        filters = []
        for filter in results:
            filters.append(cls(filter))
        return filters
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO filters (type, reason, user_id) VALUES(%(type)s, %(reason)s, %(user_id)s)"
        return connectToMySQL('user').query_db(query, data)
    
    @classmethod
    def one(cls, id):
        query  = "SELECT * FROM filters WHERE id = %(id)s;"
        results = connectToMySQL('user').query_db(query, id)
        
        return cls(results[0])
    
    @classmethod
    def update(cls,data):
        query = """UPDATE filters 
               SET type=%(type)s,reason=%(reason)s, updated_at =NOW()
                WHERE (id = %(id)s);"""
        return connectToMySQL('user').query_db(query,data) 

    @classmethod
    def delete(cls, id):
        query  = "DELETE FROM filters WHERE id = %(id)s;"
        return connectToMySQL('user').query_db(query, id)

    @staticmethod
    def valid(filter):
        valid=True
        if len(filter['type']) < 3:
            flash("Type of Filter must be at least 3 char","filter")
            valid=False
        if len(filter['reason']) < 10:
            flash("Usage must be at least 10 char","filter")
            valid=False
        return valid
    
    
