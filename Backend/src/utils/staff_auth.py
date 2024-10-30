from flask import request, jsonify
from functools import wraps

"""
Decorator to authorise acces if HR  role is provided, else deny access
"""
def hr_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        role = request.headers.get('X-User-Role')

        if not role:
            return jsonify({'message': 'Role information is missing!'}), 401

        if int(role) != 2:  # 2 is Staff role
            return jsonify({'message': 'Not authorized. Only HR personnel can access this resource.'}), 403

        return f(*args, **kwargs)

    return decorated