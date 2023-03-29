from src.app import Task, app, db
import unittest
from flask import Flask

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.client = app.test_client()
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()
    
    #testing whether the homepage load through the status code
    def test_home_page(self):
        with app.app_context():
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)

    #functions to add task in a column
    def add(self, title, column):
        with app.app_context():
            return self.client.post('/add', data={'title': title, 'column': column}, follow_redirects=True)
    
    #function to delete task in a column
    def delete(self, id):
        with app.app_context():
            return self.client.post(f'/delete/{id}', follow_redirects=True)
     
    #function to check whether a task is added in each column
    def test_add_task(self):
        # Test adding function with "To Do" column
        with app.app_context():
            response = self.add(title='Task Test 1', column='To Do')
            test_todo = db.session.query(Task).filter_by(title='Task Test 1').first()
            self.assertEqual(response.status_code, 200)  
            self.assertEqual(test_todo.title, 'Task Test 1')
            self.assertEqual(test_todo.status, 'To Do')
        
        # Test adding function with "In Progress" column
        with app.app_context():
            response = self.add(title='Task Test 2', column='In Progress')
            test_inprogress = db.session.query(Task).filter_by(title='Task Test 2').first()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(test_inprogress.title, 'Task Test 2')
            self.assertEqual(test_inprogress.status, 'In Progress')
        
        # Test adding function  with "Complete" column
        with app.app_context():
            response = self.add(title='Task Test 3', column='Complete')
            test_complete = db.session.query(Task).filter_by(title='Task Test 3').first()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(test_complete.title, 'Task Test 3')
            self.assertEqual(test_complete.status, 'Complete')

    #function to check whether a task is updated 
    def test_update_task(self):
        with app.app_context():
            #adding a task to prepare for update
            response = self.client.post(
                "/add",data={"title": "Task Test 4", "column": "To Do"},follow_redirects=True)
            taskchange = db.session.query(Task).filter_by(title='Task Test 4').first()
            taskchangeId = taskchange.id
            self.assertEqual(taskchange.status, "To Do")

            # test task moving from to do column -> in progress
            response = self.client.post(
                f"/update/{taskchangeId}/To Do", follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            test_todo = db.session.query(Task).filter_by(id=taskchangeId).first()
            self.assertEqual(test_todo.title, "Task Test 4")
            self.assertEqual(test_todo.status, "In Progress")

            # test task moving to in progress -> complete
            response = self.client.post(
                f"/update/{taskchangeId}/In Progress", follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)

            test_inprogress = db.session.query(Task).filter_by(id=taskchangeId).first()
            self.assertEqual(test_inprogress.title, "Task Test 4")
            self.assertEqual(test_inprogress.status, "Complete")


    #function to check for deletion of tasks in each column
    def test_delete_task(self):
        with app.app_context():
            # creating a task to prepare for deletion
            response = self.add(title="Task Test 5", column="Complete")
            task_delete_1 = db.session.query(Task).filter_by(title='Task Test 5').first()
            task_delete_Id1 = task_delete_1.id

            # delete a task
            response = self.delete(id=task_delete_Id1)
            test_delete_1= db.session.query(Task).filter_by(title='Task Test 5').first()
            test_deleteID_1= db.session.query(Task).filter_by(id=task_delete_Id1).first()
            self.assertIsNone(test_delete_1)
            self.assertIsNone(test_deleteID_1)

            response = self.add(title="Task Test 6", column="In Progress")
            task_delete_2 = db.session.query(Task).filter_by(title='Task Test 6').first()
            task_deleteId2 = task_delete_2.id

            # delete a task
            response = self.delete(id=task_deleteId2)
            test_delete_2= db.session.query(Task).filter_by(title='Task Test 6').first()
            test_deleteID2= db.session.query(Task).filter_by(id=task_deleteId2).first()
            self.assertIsNone(test_delete_2)
            self.assertIsNone(test_deleteID2)

            response = self.add(title="Task Test 7", column="Complete")
            task_delete_3 = db.session.query(Task).filter_by(title='Task Test 7').first()
            task_deleteId3 = task_delete_3.id

            # delete a task
            response = self.delete(id=task_deleteId3)
            test_delete_3= db.session.query(Task).filter_by(title='Task Test 7').first()
            test_deleteId3= db.session.query(Task).filter_by(id=task_deleteId3).first()
            self.assertIsNone(test_delete_3)
            self.assertIsNone(test_deleteId3)

    