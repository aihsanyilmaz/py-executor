from flask import jsonify
import os
import json

def list_fatals():
    fatals_dir = 'fatals'
    if not os.path.exists(fatals_dir):
        return jsonify({"error": "Fatals directory not found"}), 404
    
    fatal_files = [f for f in os.listdir(fatals_dir) if f.endswith('.txt')]
    return jsonify({"fatal_files": fatal_files})

def get_fatal_details(filename):
    fatals_dir = 'fatals'
    file_path = os.path.join(fatals_dir, filename)
    
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    
    try:
        with open(file_path, 'r') as f:
            content = json.load(f)
        return jsonify(content)
    except json.JSONDecodeError:
        return jsonify({"error": "File content is not in valid JSON format"}), 500

def save_fatal_error(process_id, error_details):
    fatals_dir = 'fatals'
    if not os.path.exists(fatals_dir):
        os.makedirs(fatals_dir)
    
    file_path = os.path.join(fatals_dir, f"{process_id}.txt")
    with open(file_path, 'w') as f:
        json.dump(error_details, f, indent=2)

def delete_fatal_error(filename):
    fatals_dir = 'fatals'
    file_path = os.path.join(fatals_dir, filename)
    
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    
    try:
        os.remove(file_path)
        return jsonify({"message": f"{filename} successfully deleted"}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred while deleting the file: {str(e)}"}), 500
