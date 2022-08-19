
from flask import render_template, redirect, session, request, flash
from flask_app import app

#Importacion del modelo de Message
from flask_app.models.messages import Message

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return redirect('/')
    
    #Guardar el mensaje
    Message.save(request.form)
    return redirect('/wall')

@app.route('/eliminar/mensaje/<int:id>')
def eliminar_mensaje(id):
    formulario = {"id": id}
    Message.eliminate(formulario)
    return redirect('/wall')