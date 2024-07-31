This project creates an API web service using Flask and SQLAlchemy

act.bat
set path=c:\Users\jkraxberger\pyproj\pp\repox\lib;%path%
set PYTHONPATH=C:\Users\jkraxberger\pyproj\pp\repox\lib
%~dp0venv\Scripts\activate

dact.bat
%~dp0\venv\Scripts\deactivate

To start the environment:
1. act <Enter>
2. todoserver tasks.db
3. use curl tasks below to test out the API

To list all tasks:

curl http://127.0.0.1:5000/tasks/

To list a specific task:

curl http://127.0.0.1:5000/tasks/#/

where # = task_id

To add a new task:

curl -d "{\"subject\":\"Get milk\", \"description\":\"hi\"}" -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/tasks/

To modify an existing task:

curl -X PUT -d "{\"summary\":\"Get almond milk\", \"description\":\"Chocolate flavor\"}" http://127.0.0.1:5000/tasks/1/

To delete an existing task:

curl -X DELETE -d "{\"summary\":\"Get almond milk\", \"description\":\"Chocolate flavor\"}" http://127.0.0.1:5000/tasks/1/

NOTE: to show the status code at any time, include the -I parameter in each curl call
