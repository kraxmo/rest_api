#todoserver\app.py

import json
import functools

from flask import (
    Flask,
    make_response,
    request,
)

from .store import(
    BadSummaryError,
    TaskStore, 
)

class TodoserverApp(Flask):
    def init_db(self, engine_spec):
        self.store = TaskStore(engine_spec)

    def erase_all_test_data(self):
        assert self.testing # if true, TEST MODE; otherwise PROD MODE *BOMB*
        self.store._delete_all_tasks()

app = TodoserverApp(__name__)

def validate_summary(view):
    @functools.wraps(view)  # retain __name__ value from caller
    def wrapper(*args, **kwargs):
        try:
            return view(*args, **kwargs)
        except BadSummaryError:
            result = {
                "error": "Summary must be under 120 chars, without newlines"
            }
            return make_response(json.dumps(result), 400)
    
    return wrapper

@app.route("/tasks/", methods=["GET"])
def get_all_tasks():
    tasks = app.store.get_all_tasks()
    return make_response(json.dumps(tasks), 200)

@app.route("/tasks/", methods=["POST"])
@validate_summary
def create_task():
    payload = request.get_json(force=True)
    #return make_response(json.dumps(payload))
    task_id = app.store.create_task(
        summary = payload["summary"],
        description = payload["description"],
    )
    task_info = {"id": task_id}
    return make_response(json.dumps(task_info), 201)

@app.route("/tasks/<int:task_id>/", methods = ["PUT"])
@validate_summary
def modify_task(task_id):
    payload = request.get_json(force=True)
    modified = app.store.modify_task(
        task_id = task_id,
        summary = payload["summary"],
        description = payload["description"]
    )
    if modified:
        return ""

    return make_response("", 404)
    
@app.route("/tasks/<int:task_id>/")
def task_details(task_id):
    task_info = app.store.task_details(task_id)
    if task_info is None: # no value retured by get
        return make_response("", 404) # make API response 404 per requirement
    
    return json.dumps(task_info)

@app.route("/tasks/<int:task_id>/", methods = ["DELETE"])
def delete_task(task_id):
    deleted = app.store.delete_task(task_id)
    if deleted:
        return ""
    
    return make_response("", 404)
