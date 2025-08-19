from flask import Blueprint, jsonify

base_bp = Blueprint('base', __name__)

@base_bp.route('/')
def index():
    return jsonify({'message': 'Bienvenido a DNSentinnel'})