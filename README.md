# CS162 Kanban Board Assignment (Trinh Nguyen)

Demo of the app: https://www.loom.com/share/82ce24bb97db40ccb8f924e4df62fda3

## Functionalities
The app displays a Kanban board which have 3 columns representing the tasks status.
- To do
- In progress
- Complete

The users can:
- Add tasks to any columns
- Update the task (moving the task to next column)
- Delete a task

## Project Structures
```bash
cs162-kanban/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── instance/
│   │   └── db.sqlite
│   ├── static/
│   │   └── styles.css
│   └── templates/
│       └── kanban.html
└── test/
    ├── __init__.py
    └── testing.py
```


## Run the app
### MacOS
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cd src
python3 app.py
```
It will be running on http://127.0.0.1:5001
## Run unit test 
```bash
python -m unittest test.testing
```
