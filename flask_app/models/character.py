from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
from flask import flash
import re

#same fields must exist here as in database
class Character:
    def __init__(self, data):
        self.id=data['id']
        self.name=data['name']
        self.vision=data['vision']
        self.weapon=data['weapon']
        self.nation=data['nation']
        self.rarity=data['rarity']

    @classmethod
    def get_all(cls):
        #enter relevant query
        query= "Select * FROM characters ORDER BY rarity DESC, name ASC;"
        results=connectToMySQL(DB).query_db(query)
        print('GET ALLResults---------------',results)
        return results

    @classmethod
    def get_one(cls,data):
        query= "Select * FROM characters WHERE name=%(name)s;"
        results=connectToMySQL(DB).query_db(query,data)
        return results[0]


    @classmethod
    def delete_all_characters(cls):
        #enter relevant query
        query= "DELETE FROM characters;"
        results=connectToMySQL(DB).query_db(query)
        print('Results---------------',results)
        return results
        
    @classmethod
    def recompile(cls,data):
        query="INSERT INTO characters (name,vision,weapon,nation,rarity) VALUES (%(name)s,%(vision)s,%(weapon)s,%(nation)s,%(rarity)s);"
        results=connectToMySQL(DB).query_db(query,data)
        return results
        
    @classmethod
    def add_to_list(cls,data):
        query="INSERT INTO trackers (user_id,character_id) VALUES (%(uid)s,%(cid)s);"
        results=connectToMySQL(DB).query_db(query,data)
        return results

    @classmethod
    def ascension(cls,data):
        query="SELECT * FROM ascensions WHERE character_id=%(cid)s ORDER BY ascensions.rank ASC;"
        results=connectToMySQL(DB).query_db(query,data)
        return results
        
    @classmethod
    def ascension_change(cls,data):
        query="INSERT INTO ascensions(ascensions.rank,level,mora,mat1,mat1cost,mat2,mat2cost,mat3,mat3cost,mat4,mat4cost,character_id) VALUES(%(rank)s,%(level)s,%(mora)s,%(mat1)s,%(mat1cost)s,%(mat2)s,%(mat2cost)s,%(mat3)s,%(mat3cost)s,%(mat4)s,%(mat4cost)s,%(character_id)s);"
        results=connectToMySQL(DB).query_db(query,data)
        return results

    @classmethod
    def delete_from_tracker(cls,data):
        query="DELETE FROM trackers WHERE user_id=%(uid)s AND character_id=%(cid)s"
        results=connectToMySQL(DB).query_db(query,data)
        return results


    @classmethod
    def livesearch(cls,data): 
        print(data)
        query="SELECT name FROM characters WHERE characters.name LIKE '%(search)s%';"
        results=connectToMySQL(DB).query_db(query,data)
        print("TESTING>>>>>>>",results)
        matches=[]
        for match in results:
            matches.append(match)
        print("Matches>>>>>>>>>>",matches)
        return matches