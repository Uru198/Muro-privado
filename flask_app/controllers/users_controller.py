
from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.messages import Message

#Importacion del modelo
from flask_app.models.users import User


#Importacion Bcrypt

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrate', methods=["POST"])
def registrate():
    #validar la informacion ingresada
    if not User.valida_usuario(request.form):
        return redirect('/')
  

    pwd = bcrypt.generate_password_hash(request.form['password']) #Encriptamos el password del usuario

    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

  #request.form = FORMULARIO HTML
    id = User.save(formulario) #recibo el identificador de mi nuevo usuario
    
    session['user_id'] = id
    
    
    return redirect('/wall')

@app.route('/login', methods=['POST'])
def login():
    #verificar si el email existe
    #request
    user = User.get_by_email(request.form) #Recibimos una instancia de usuario o false
    
    if not user:
        flash('E-mail no encontrado', 'login')
        return redirect('/')
    
    print(request.form["password"])
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password incorrecto', 'login')
        return redirect('/')
    
    session['user_id'] = user.id
    
    return redirect('/wall')



    
@app.route('/wall')
def wall():
    if 'user_id' not in session:
        return redirect('/')
    
    formulario ={
        'id': session['user_id'] 
    }
    
    user = User.get_by_id(formulario) #ususario que inicio sesion
    
    users = User.get_all()
    
    messages = Message.get_user_messages(formulario) #regresa una lista de todos los mensajes de la persona que inicio sesion
    
    return render_template('wall.html', user=user, users=users, messages=messages, amount=len(messages))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


