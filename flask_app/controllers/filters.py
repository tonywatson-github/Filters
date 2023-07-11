from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.filter import Filter
from flask_app import app


@app.route('/filtersomething')
def filtersomething():
    if 'idd' not in session:
        return redirect ('/logout')
    data = {
        "id": session['idd'],
    }
    return render_template('/filter.html', user = User.one(data))


@app.route('/filter',methods=['POST'])
def filter():
    if 'idd' not in session:
        return redirect ('/logout')
    if not Filter.valid(request.form):
        return redirect('/filtersomething')
    data = {
        "type": request.form['type'],
        "reason": request.form['reason'],
        'user_id': session['idd']
    }
    Filter.save(data)
    return redirect("/dashboard")


@app.route('/edit/<int:id>')
def edit(id):
    if 'idd' not in session:
        return redirect ('/logout')
    data = {'id': id}
    user_data = {'id': session['idd']}
    return render_template("/edit.html", filter= Filter.one(data), user = User.one(user_data))

@app.route('/update',methods=['POST'])
def update():
    if 'idd' not in session:
        return redirect ('/logout')
    if not Filter.valid(request.form):
        return redirect('/filtersomething')
    data = {
        'type':request.form['type'],
        'reason':request.form['reason'],
        'id': request.form['id']}
    Filter.update(data)
    return redirect("/dashboard")

@app.route('/details/<int:id>')
def show(id):
    if 'idd' not in session:
        return redirect ('/logout')
    data = {'id': id}
    user_data = {'id': session['idd']}
    return render_template("/details.html", filter= Filter.one(data), user = User.one(user_data))

@app.route('/myfilters')
def my():
    if 'idd' not in session:
        return redirect ('/logout')
    data = {'id': session['idd']}
    return render_template("/my.html", user = User.one_with_many(data))

@app.route('/delete/<int:id>')
def delete(id):
    if 'idd' not in session:
        return redirect ('/logout')
    data = {'id': id}
    Filter.delete(data)
    return redirect("/dashboard")






