# pst2_main.py - The Persistent Application

import json
import datetime

DATA_FILE = "msms.json"
app_data = {}  # This global dictionary will hold ALL our data.

# --- Core Persistence Engine ---
def load_data(path=DATA_FILE):
    """Loads all application data from a JSON file."""
    global app_data
    try:
        with open(path, 'r') as f:
            app_data = json.load(f)
            print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Initializing with default structure.")
        app_data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }
    except json.JSONDecodeError:
        print("Data file is corrupted or empty. Resetting to default structure.")
        app_data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }


def save_data(path=DATA_FILE):
    """Saves all application data to a JSON file."""
    try:
        with open(path, 'w') as f:
            json.dump(app_data, f, indent=4)
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error saving data: {e}")


# --- CRUD Operations ---

def add_teacher(name, speciality):
    """Adds a teacher dictionary to the data store."""
    teacher_id = app_data['next_teacher_id']
    new_teacher = {"id": teacher_id, "name": name, "speciality": speciality}
    app_data['teachers'].append(new_teacher)
    app_data['next_teacher_id'] += 1
    print(f"Core: Teacher '{name}' added.")


def update_teacher(teacher_id, **fields):
    """Finds a teacher by ID and updates their data with provided fields."""
    for teacher in app_data['teachers']:
        if teacher['id'] == teacher_id:
            teacher.update(fields)
            print(f"Teacher {teacher_id} updated.")
            return
    print(f"Error: Teacher with ID {teacher_id} not found.")


def remove_student(student_id):
    """Removes a student from the data store."""
    original_count = len(app_data['students'])
    app_data['students'] = [s for s in app_data['students'] if s['id'] != student_id]
    if len(app_data['students']) < original_count:
        print(f"Student {student_id} removed.")
    else:
        print(f"Error: Student with ID {student_id} not found.")


def remove_teacher(teacher_id):
    """Removes a teacher from the data store."""
    original_count = len(app_data['teachers'])
    app_data['teachers'] = [t for t in app_data['teachers'] if t['id'] != teacher_id]
    if len(app_data['teachers']) < original_count:
        print(f"Teacher {teacher_id} removed.")
    else:
        print(f"Error: Teacher with ID {teacher_id} not found.")


def update_student(student_id, **fields):
    """Finds a student by ID and updates their data with provided fields."""
    for student in app_data['students']:
        if student['id'] == student_id:
            student.update(fields)
            print(f"Student {student_id} updated.")
            return
    print(f"Error: Student with ID {student_id} not found.")
