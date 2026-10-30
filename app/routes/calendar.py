from flask import Blueprint, request, session
from datetime import datetime
from app.extensions import db
from app.models import FarmTask
from app.utils.errors import api_response, bad_request, unauthorized, not_found

calendar_bp = Blueprint('calendar', __name__, url_prefix='/api/tasks')

@calendar_bp.route('', methods=['GET'])
def get_tasks():
    user_id = session.get('user_id')
    if not user_id:
        return unauthorized()

    status = request.args.get('status')
    query = FarmTask.query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status.upper())
    
    tasks = query.order_by(FarmTask.due_date.asc()).all()
    return api_response(data={"tasks": [t.to_dict() for t in tasks]})

@calendar_bp.route('', methods=['POST'])
def create_task():
    user_id = session.get('user_id')
    if not user_id:
        return unauthorized()

    data = request.get_json() or {}
    title = data.get('title', '').strip()
    due_date_str = data.get('due_date', '').strip()
    category = data.get('category', 'FIELD_WORK')

    if not title:
        return bad_request("Task title is required.")
    
    try:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
    except ValueError:
        return bad_request("Due date must be in YYYY-MM-DD format.")

    task = FarmTask(
        user_id=user_id,
        title=title,
        due_date=due_date,
        category=category,
        notes=data.get('notes', '')
    )
    db.session.add(task)
    db.session.commit()

    return api_response(data={"task": task.to_dict()}, status_code=201)

@calendar_bp.route('/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    user_id = session.get('user_id')
    if not user_id:
        return unauthorized()

    task = FarmTask.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return not_found("Task not found.")

    data = request.get_json() or {}
    if 'status' in data:
        task.status = data['status'].upper()
    if 'title' in data:
        task.title = data['title']

    db.session.commit()
    return api_response(data={"task": task.to_dict()})

