from models.user import User_v1
from extensions import db
from flask import request, jsonify, flash

def add_user():
    username = request.form.get('username')
    full_name = request.form.get('fullname')
    division = request.form.get('division')
    role_id = request.form.get('role_id')

    new_user = User_v1(
        username=username,
        full_name=full_name,
        division=division,
        role_id=role_id
    )

    db.session.add(new_user)
    db.session.commit()

    flash("User added successfully", "success")
    return new_user   


def edit_user(user_id):
    user = User_v1.get_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    username = request.form.get('username')
    full_name = request.form.get('full_name')
    division = request.form.get('division')
    role = request.form.get('role')
    
    if username:
        existing_user = User_v1.query.filter_by(username=username).first()
        if existing_user and existing_user.user_id != user_id:
            return jsonify({'error': 'Username already exists'}), 409
        user.username = username
    
    if full_name:
        user.full_name = full_name
    if division:
        user.division = division
    if role:
        user.role = role
    
    try:
        user.save()
        return jsonify({'message': 'User updated successfully', 'user': user.user_data}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def delete_user(user_id):
    user = User_v1.get_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500