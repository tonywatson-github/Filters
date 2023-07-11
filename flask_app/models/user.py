from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.filter import Filter
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first = data['first']
        self.last = data['last']
        self.email = data['email']
        self.passw = data['passw']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.filters = []

    @classmethod
    def all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('user').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first, last, email, passw) VALUES(%(first)s, %(last)s, %(email)s, %(passw)s)"
        return connectToMySQL('user').query_db(query, data)
    
    @classmethod
    def one(cls, id):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('user').query_db(query, id)
        return cls(results[0])
    
    @classmethod
    def one_with_many(cls, id):
        query  = "SELECT * FROM users LEFT JOIN filters ON filters.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL('user').query_db(query, id)
        user = cls(results[0])
        for row in results:
            filters_data = {
            'id': row['filters.id'],
            'type': row['type'],
            'reason': row['reason'],
            'created_at': row['filters.created_at'],
            'updated_at': row['filters.updated_at'],
            'user_id': row['user_id']
            }
            user.filters.append(Filter(filters_data))
        return user
    
    @classmethod
    def emai(cls, emai):
        query  = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('user').query_db(query, emai)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def valid(user):
        valid=True
        query  = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('user').query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken!","register")
            valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Bad email format.", "register")
            valid=False
        if len(user['first']) < 3:
            flash("First Name must be at least 3 char","register")
            valid=False
        if len(user['last']) < 3:
            flash("Last Name must be at least 3 char","register")
            valid=False
        if len(user['passw']) < 8:
            flash("Password must be at least 8 char","register")
            valid=False
        if user['passw'] != user['con']:
            flash("Passwords don't match!","register")
            valid=False
            
        return valid

    
    
    
    
    
    
    
    
    
    
    
    
    #    @classmethod
    #    def update(cls,data):
      #      query = """UPDATE users 
       #             SET first=%(first)s,last=%(last)s, 
         #           WHERE (id = %(id)s);"""
         #   return connectToMySQL('user').query_db(query,data) 

   # @classmethod
   # def delete(cls, id):
     #   query  = "DELETE FROM users WHERE id = %(id)s;"
      #  data = {"id": id}
     #   return connectToMySQL('user').query_db(query, data)