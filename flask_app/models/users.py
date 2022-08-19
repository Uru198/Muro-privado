

from flask_app.config.mysqlconnection import connectToMySQL

import re #importando Expresiones regulares
#Expresion Regular de Email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')




from flask import flash

class User:
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        
    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('muro_privado').query_db(query, formulario)
        #registrado
        #result = 5
        return result
    
    @staticmethod
    def valida_usuario(formulario):
         
        # formulario = { DICCIONARIO
        #    first_name = "Elena",
        #    last_name = "De troya",
        #    email = "elena@coding.com",
        #    password = "123",
        #    confirm_password = "234",
        #}
        
      
        # validar que el nombre tenga al menos 3 caracteres
        if len(formulario['first_name']) < 3:
            flash("Nombre debe de tener almenos 3 caracteres", "registro")
            es_valido = False
            
        if len(formulario['last_name']) < 3:
            flash("Apellido debe de tener almenos 3 caracteres", "registro")
            es_valido = False
            
    
        #verificar que el email tenga el formato correcto - EXPRESIONES REGULARES
        if not EMAIL_REGEX.match(formulario['email']):
            flash("E-mail invalido", "registro")
            es_valido = False
            
        #Password con al menos 6 caracteres
        if len(formulario['password']) < 6:
            flash("contraseña debe tener al menos 6 caracteres", "registro")
            es_valido = False
            
            
        #consultar si ya existe ese correo electronico
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('muro_privado').query_db(query, formulario)
        if len(result) >= 1:
            flash("E-mail registrado previamente", "registro")
            es_valido = False
            
            
        return True
        
        
    @classmethod
    def get_by_email(cls, formulario):
        # formulario = {
        #   email: elena@cd.com
        #   password: 123
        #}
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('muro_privado').query_db(query, formulario)# los SELECT regresan una lista
        if len(result) < 1: #No existe registro con ese correo
            return False
        else:
            user = cls(result[0])
            return user
    
    @classmethod
    def get_by_id(cls, formulario):
        #formulario = {id : 4}
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('muro_privado').query_db(query, formulario)# recibimos una lista
        user = cls(result[0]) #creamos una instancia de usuario
        return user
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL('muro_privado').query_db(query)#Regresa una lista de diccionarios
        users = []
        for us in results:
            users.append(cls(us))#1 - cls(us) creando una instancia de user. 2- esa instancia la agrego a la lista de 
            
        return users        
    

        