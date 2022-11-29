from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.controllers import users
from flask_app.models.magazine import Magazine
from flask_app.controllers import magazines

@app.route('/addMagazine')
def addMagazine():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        return render_template("addMagazine.html",loggedUser= user)
    return redirect('/')

@app.route('/newMagazine', methods=['POST'])
def newMagazine():
    if Magazine.validate_magazine(request.form):
        data = { 
            "title" : request.form["title"], 
            "description" : request.form["description"], 
            'user_id': session['user_id']
            }
        print(data)
        Magazine.saveMagazine(data)
        return redirect("/dashboard")
    return redirect('/addMagazine')

@app.route('/show_magazine/<int:id>')
def show_magazine(id):
    if 'user_id' in session:
        data = {
        "id":id
        }
        return render_template('show_magazine.html', creator = Magazine.get_creator(data), magazine=Magazine.get_by_id(data), allSubscribers = Magazine.getAllSubscribers(data))
    return redirect('/')

@app.route('/favorite/<int:id>')
def addFavorite(id):
    if 'user_id' in session:
        data = {
            'magazine_id': id,
            'user_id': session['user_id']
        }
        Magazine.addFavorite(data)
        return redirect(request.referrer)    
    return redirect('/')

@app.route('/unfavorite/<int:id>')
def removeFavorite(id):
    if 'user_id' in session:
        data = {
            'magazine_id': id,
            'user_id': session['user_id']
        }
        Magazine.removeFavorite(data)
        return redirect(request.referrer)
    return redirect('/')

@app.route('/delete/<int:id>')
def destroyMagazine(id):
    if 'user_id' in session:
        data = {
            'magazine_id': id,
        }
        magazine = Magazine.get_magazine_by_id(data)
        if session['user_id']==magazine['user_id']:
            Magazine.deleteAllSubscribers(data)
            Magazine.destroyMagazine(data)
            return redirect(request.referrer)
        return redirect(request.referrer)
    return redirect('/')