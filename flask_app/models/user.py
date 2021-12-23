from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
from flask import flash
import re
from flask_app.models import character

EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

#same fields must exist here as in database
class User:
    def __init__(self, data):
        self.id=data['id']
        self.username=data['username']
        self.email=data['email']
        self.password=data['password']
        self.created_at= data['created_at']
        self.updated_at=data['updated_at']


    @classmethod
    def get_all(cls):
        #enter relevant query
        query= "Select * FROM blank;"
        results=connectToMySQL(DB).query_db(query)
        
        #convert results from mySQL into a list of class objects
        # blank=[]
        #for blank in results:  blank.append(cls(blank))
        #return blank

        #dont forget to add this into server.py

    @classmethod
    def create_user(cls,data):
        query="INSERT INTO users (username,email,password) VALUES (%(username)s,%(email)s,%(password)s);"
        results=connectToMySQL(DB).query_db(query,data)
        return results

    @classmethod
    def get_by_username(cls,data):
        query="SELECT * FROM users WHERE username= %(username)s;"
        result=connectToMySQL(DB).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])

    @classmethod
    def get_all_list(cls,data):
        query="SELECT * FROM users LEFT JOIN trackers ON users.id=user_id LEFT JOIN characters ON characters.id=character_id WHERE username=%(username)s;"
        results=connectToMySQL(DB).query_db(query,data)
        if results:
            this_user=cls(results[0])
            this_user.chars=[]
            for row in results:
                char_data={
                    'id':row['characters.id'],
                    'name':row['name'],
                    'vision':row['vision'],
                    'weapon':row['weapon'],
                    'rarity':row['rarity'],
                    'nation':row['nation']
                }
                this_user.chars.append(character.Character(char_data))
            return this_user
    @classmethod
    def get_tracker(cls,data):
        query="SELECT * FROM trackers WHERE user_id=%(uid)s AND character_id=%(cid)s;"
        results=connectToMySQL(DB).query_db(query,data)
        if results:
            return results
        else:
            return False
    
         
    @staticmethod
    def validate_users(user):
        is_valid=True
        query="SELECT username, email FROM users;"
        results=connectToMySQL(DB).query_db(query)
        for result in results:
            if result['username']==user['username']:
                flash('Taken username', 'register')
                is_valid= False
            if result['email']==user['email']:
                flash('Taken email', 'register')
        if len(user['username'])<2:
            flash('Input valid username', 'register')
            is_valid= False
        if len(user['password'])<8:
            flash('Input valid password', 'register')
            is_valid= False
        if user['password'] != user['passwordconfirm']:
            flash('Password no match', 'register')
            is_valid= False
        if not EMAIL_REGEX.match(user['email']):
            flash('Input valid email', 'register')
            is_valid= False
        return is_valid


