from flask import request, jsonify
from functools import wraps

"""
    Decorator to control access to staff schedules based on user roles: HR (role 1) can access any staff schedule, 
    while other users can only access their own schedule. Returns 401 if user info is missing, or 403 if access 
    is unauthorized.
"""
def staff_schedule_access_control(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_role = request.headers.get('X-User-Role')
        user_id = request.headers.get('X-User-ID')
        requested_staff_id = kwargs.get('staff_id')

        if not user_role or not user_id:
            return jsonify({"code": 401, "message": "Unauthorized: Missing user information"}), 401

        user_role = int(user_role)
        user_id = int(user_id)

        if user_role != 1 and user_id != requested_staff_id:
            return jsonify({"code": 403, "message": "Forbidden: You can only view your own schedule"}), 403

        return f(*args, **kwargs)
    return decorated_function