from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB Client
client = MongoClient('localhost', 27017)
# MongoDB Database
db = client['flask_database']
# Collection in that database
todos = db.todos


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form.get('content')
        degree = request.form.get('degree')
        if content and degree:  # Ensure that neither field is empty
            todos.insert_one({'content': content, 'degree': degree})
        return redirect(url_for('index'))

    all_todos = todos.find()  # Fetch all todos to display
    return render_template('index.html', todos=all_todos)


@app.post("/<id>/delete/")


def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)  # Server restarts automatically on code changes
