#EJECUTA nuestra aplicación
from flask_app import app

#Importando mi controlador
from flask_app.controllers import users_controller, messages_controller

#pipenv install flask pymysql flask-bcrypt
#pipenv shell
#py server.py
#pipenv --rm Para eliminar algun ambiente virtual con un error

if __name__=="__main__":
    app.run(debug=True)
