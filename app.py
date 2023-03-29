#importing libraries
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'   # Configuring the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   
db = SQLAlchemy(app)   # Initializing the database

class Task(db.Model):
    """
    A class representing each task in Kanban Board.

    ---------------------------
    Attributes:
        id (int): Unique identifier for the task.
        title (str): The title(name) of the task
        status(str): The status of a task (To do, In Progress, Complete)
    Methods:
        __repr__(): Returns a string representation of the Task object.
    """
    __tablename__ = "Kanban"   
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(100))
    status = db.Column(db.String(20))

    def __repr__(self):
        return f'Task{self.id}: {self.title}'

@app.route('/')
# Retrieving all the tasks from the database
# and rendering the HTML template with the task list
def index():
    task_list = Task.query.all()   
    return render_template("kanban.html", task_list=task_list)  

@app.route("/add", methods=["POST"])
def add():
    #Retrieving the title and status of the task from the form
    title = request.form.get("title")   
    column = request.form.get("column")   
    
    #Checking the status of the task
    if column == "To Do":   
        status = "To Do"
    elif column == "In Progress":
        status = "In Progress"
    else:
        status = "Complete"

    # Creating a new task object with the given title and status   
    new_todo = Task(title=title, status=status)

    # Adding the new task to the database session  
    db.session.add(new_todo)   
    db.session.commit()   

     # Redirecting the user to the homepage
    return redirect(url_for("index"))  

@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    # Retrieving the task with the given ID from the database
    todo = Task.query.get(todo_id) 

    # Deleting the task from the database session  
    db.session.delete(todo)   
    db.session.commit()   

     # Redirecting the user to the homepage
    return redirect(url_for("index"))  

@app.route("/update/<int:id>/<status>", methods=["POST"])
def update(id, status):
    # Retrieving the task with the given ID from the database
    task = Task.query.get(id)   

    # Updating the status of the task
    if status == "To Do":
        task.status = "In Progress"   
    elif status == "In Progress":
        task.status = "Complete"
    
    # Committing the changes to the database
    db.session.commit()   

    # Redirecting the user to the homepage
    return redirect(url_for("index"))   

if __name__ == '__main__':
    with app.app_context():
        db.create_all()   
    try:
        app.run(debug=True, port=5001)  
    except SystemExit:
        pass
