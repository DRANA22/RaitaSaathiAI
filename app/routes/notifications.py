from flask import Blueprint, request, session
from app.extensions import db
from app.models import User, FarmerNotification
from app.utils.errors import api_response

notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')

def get_or_create_active_user():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return user
    from flask import current_app
    if current_app and current_app.config.get('TESTING'):
        user = User.query.first()
        if user:
            session['user_id'] = user.id
        return user
    return None

@notifications_bp.route('', methods=['GET'])
def get_notifications():
    """Retrieve notifications for the current farmer."""
    user = get_or_create_active_user()
    if not user:
        return api_response(data={"notifications": [], "unread_count": 0})

    notifs = FarmerNotification.query.filter_by(user_id=user.id).order_by(FarmerNotification.created_at.desc()).limit(20).all()
    unread_count = FarmerNotification.query.filter_by(user_id=user.id, is_read=False).count()

    return api_response(data={
        "notifications": [n.to_dict() for n in notifs],
        "unread_count": unread_count
    })

@notifications_bp.route('/mark-read', methods=['POST'])
def mark_read():
    """Mark all or specific notification as read."""
    user = get_or_create_active_user()
    if not user:
        return api_response(data={"marked": 0})

    data = request.get_json() or {}
    notif_id = data.get('notification_id')

    if notif_id:
        n = FarmerNotification.query.filter_by(id=notif_id, user_id=user.id).first()
        if n:
            n.is_read = True
    else:
        FarmerNotification.query.filter_by(user_id=user.id, is_read=False).update({FarmerNotification.is_read: True})

    db.session.commit()
    return api_response(data={"success": True})

