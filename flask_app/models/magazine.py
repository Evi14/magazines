from flask_app.config.mysqlconnection import connectToMySQL
# import re
from flask import render_template, redirect, request, session, flash
from flask_app.models import user

db_name = 'login_register'
class Magazine:

    def __init__(self, data):
        #data['emri i kolones si ne tab e db']
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        
        self.users_who_favorited = []

    @classmethod
    def saveMagazine(cls,data):
        # %(emri i te dhenes si tek dict i data)s
        query = "INSERT INTO magazines (title, description, created_at, updated_at, user_id) VALUES (%(title)s, %(description)s, NOW(), NOW(), %(user_id)s );"
        return connectToMySQL(db_name).query_db(query, data)
    # magazine info
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM magazines LEFT JOIN favorites ON magazines.id = favorites.magazine_id LEFT JOIN users ON users.id = favorites.user_id WHERE magazines.id = %(id)s;"
        results = connectToMySQL(db_name).query_db(query,data)
        magazine = (results[0])
        # print(magazine)
        return magazine

    @classmethod
    def addFavorite(cls, data):
        query= 'INSERT INTO favorites (magazine_id, user_id) VALUES ( %(magazine_id)s, %(user_id)s );'
        return connectToMySQL(db_name).query_db(query, data)

    @classmethod
    def removeFavorite(cls, data):
        query= 'DELETE FROM favorites WHERE magazine_id = %(magazine_id)s and user_id = %(user_id)s;'
        return connectToMySQL(db_name).query_db(query, data)

    @classmethod
    def get_creator(cls,data):
        query = "select u.first_name from users u join magazines m on u.id = m.user_id where m.id = %(id)s;"
        results = connectToMySQL(db_name).query_db(query,data)
        magazine = (results[0])
        return magazine
        
    @classmethod
    def getAllSubscribers(cls, data):
        query= 'SELECT * FROM magazines LEFT JOIN favorites ON magazines.id = favorites.magazine_id LEFT JOIN users ON users.id = favorites.user_id WHERE magazines.id = %(id)s;'
        results =  connectToMySQL(db_name).query_db(query, data)
        subscribers= []
        for row in results:
            subscribers.append(row)
        print(subscribers)
        return subscribers
        
    @classmethod
    def destroyMagazine(cls, data):
        query= 'DELETE FROM magazines WHERE magazines.id = %(magazine_id)s;'
        return connectToMySQL(db_name).query_db(query, data)

    @classmethod
    def deleteAllSubscribers(cls, data):
        query= 'DELETE FROM favorites WHERE favorites.magazine_id = %(magazine_id)s;'
        return connectToMySQL(db_name).query_db(query, data)
    
    @classmethod
    def get_magazine_by_id(cls, data):
        query= 'SELECT * FROM magazines WHERE magazines.id = %(magazine_id)s;'
        results = connectToMySQL(db_name).query_db(query, data)
        return results[0]
    
    @classmethod
    def get_subscribersNo(cls, data):
        query= 'SELECT count(*), title FROM magazines JOIN favorites ON magazines.id = favorites.magazine_id LEFT JOIN users ON users.id = favorites.user_id group by magazine_id;'
        results = connectToMySQL(db_name).query_db(query, data)
        return results[0]

    @staticmethod
    def validate_magazine(magazine):
        is_valid = True
        if len(magazine['title']) < 2:
            flash("Magazine title must be at least 2 characters.", 'title')
            is_valid = False
        if len(magazine['description']) < 10:
            flash("Magazine description must be at least 10 characters.", 'description')
            is_valid = False
        return is_valid

