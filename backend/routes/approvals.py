from flask import Blueprint

approvals_bp = Blueprint('approvals', __name__)

# Example route
@approvals_bp.route('/approvals')
def get_approvals():
    return "Approvals route"
