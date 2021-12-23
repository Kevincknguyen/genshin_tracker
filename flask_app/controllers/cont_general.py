from flask import render_template, request, redirect, session, flash, jsonify
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.user import User
from flask_app.models.character import Character
from flask_app import DB
import requests
import os

# from flask_app.models.FILE_NAME import CLASS_NAME

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    response=requests.get("https://api.genshin.dev/characters/")
    list=response.json()
    totalcharacters=Character.get_all()
    return render_template('home.html', list=list, totalcharacters=totalcharacters) 

@app.route('/login')
def login():
    if 'user_id' not in session:
        return render_template('login.html') 
    else:
        return redirect ('/profile')

@app.post('/login/confirm')
def loginconfirm():
    data= {"username":request.form["username"]}
    user_in_db= User.get_by_username(data)
    if not user_in_db:
        flash("Invalid username/password (user)", "login")
        return redirect('/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash ("Invalid Email/Password (password)", "login")
        return redirect ('/login')
    session ['user_id']= user_in_db.id
    session['username']=user_in_db.username
    return redirect (f'/profile/{user_in_db.username}') 


@app.route('/register')
def register():
    if 'user_id' in session:
        return redirect ('/profile')
    return render_template('register.html') 

@app.post('/register/confirm')
def registerconfirm():
    if not User.validate_users(request.form):
        return redirect('/register')
    pw_hash= bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data={
        "username": request.form['username'],
        "email": request.form['email'],
        "password": pw_hash
    }
    User.create_user(data)
    return redirect('/login') 


@app.route('/characters/<name>')
def characters(name):
    response=requests.get(f"https://api.genshin.dev/characters/{name}")
    win=response.json()
    print('win>>>>>>>>>>>>>>>>>>>>>>>>>>>',win)
    data={
        'name':name
    }
    char=Character.get_one(data)
    print('char>>>>>>>>>>>>>>>>>>>>>>>>>>>',char)
    if 'user_id' in session:
        data={
            'uid':session['user_id'],
            'cid':char['id']
        }
        inTracker=User.get_tracker(data)
    else:
        inTracker=False
    ascension=Character.ascension({'cid':char['id']})
    print('ASCENSION>>>>>>>>>>>>',ascension)
    return render_template('characters.html', name=name, win=win, char=char, inTracker=inTracker, ascension=ascension) 

@app.route('/add/<name>/<int:id>')
def add_to_list(id,name):
    data={
        "uid":session['user_id'],
        "cid":id,
    }
    Character.add_to_list(data)
    return redirect (f'/characters/{name}')

@app.route('/delete/<name>/<int:id>')
def delete_from_tracker(id,name):
    data={
        "uid":session['user_id'],
        "cid":id,
    }
    Character.delete_from_tracker(data)
    return redirect (f'/characters/{name}')


@app.route('/items')
def items():
    return render_template('items.html') 


@app.route('/materials')
def materials():
    return render_template('materials.html') 


@app.route('/profile/<username>')
def profile(username):
    char=User.get_all_list({"username":username})
    return render_template('profile.html', char=char) 

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')




@app.post('/search')
def livesearch():
    data={
        'search':request.form['search']
    }

    query="SELECT name FROM characters WHERE characters.name LIKE 'a%';"
    results=connectToMySQL(DB).query_db(query)
    print(results)
    
    matches=Character.livesearch(data)
    return jsonify(matches=matches)


# ADMIN DUTIES>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect ('/')
    if 'user_id' in session:
        if session['user_id'] !=1:
                return redirect ('/')
    check=requests.get("https://api.genshin.dev/characters")
    print('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',check.json())
    Character.get_all()
    return render_template('admin.html') 

@app.route('/admin/recompile')
def recompile():
    check=requests.get("https://api.genshin.dev/characters")
    compare=Character.get_all()
    print('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',check.json())
    for item in check.json():
        print('++++++++++++',item)
        if item in compare:
            print("here!")
        else:
            print("not!")
            add=requests.get(f"https://api.genshin.dev/characters/{item}")
            data={
                'name':item,
                'vision': add.json()['vision'],
                'weapon': add.json()['weapon'],
                'nation':add.json()['nation'],
                'rarity': add.json()['rarity']
            }
            print(data)
            Character.recompile(data)
    return redirect ('/admin') 

@app.route('/delete')
def deleteall():
    Character.delete_all_characters()
    return redirect('/admin')

@app.post('/characters/<name>/<int:id>/ascension')
def update_insert_ascension(name,id):
    print("hello")
    data={
        "rank":request.form['rank'],
        "level":request.form['level'],
        'mora':request.form['mora'],
        'mat1':request.form['mat1'],
        'mat1cost':request.form['mat1cost'],
        'mat2':request.form['mat2'],
        'mat2cost':request.form['mat2cost'],
        'mat3':request.form['mat3'],
        'mat3cost':request.form['mat3cost'],
        'mat4':request.form['mat4'],
        'mat4cost':request.form['mat4cost'],
        'character_id':id
    }
    Character.ascension_change(data)
    return redirect (f'/characters/{name}')