import json
import datetime

DATA_FILE = "msms.json"
app_data = {}  # Global data store

# --- Core Persistence Engine ---
def load_data(path=DATA_FILE):
    """Loads all application data from a JSON file, with fallback to sample data if incomplete."""
    global app_data
    try:
        with open(path, 'r') as f:
            loaded = json.load(f)
            # Validate loaded data
            if not loaded.get("students") or not loaded.get("teachers"):
                raise ValueError("Data incomplete")
            app_data = loaded
            print("Data loaded successfully.")
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        print("Initializing with default structure + sample data.")
        app_data = {
            "students": [
                {"id": 1, "name": "Alice Smith", "enrolled_in": ["Piano 101", "Theory 1"]},
                {"id": 2, "name": "Bob Johnson", "enrolled_in": ["Guitar Basics"]}
            ],
            "teachers": [
                {"id": 1, "name": "Mr. Taylor", "speciality": "Piano"},
                {"id": 2, "name": "Ms. Chen", "speciality": "Guitar"}
            ],
            "attendance": [],
            "next_student_id": 3,
            "next_teacher_id": 3
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
    teacher_id = app_data['next_teacher_id']
    new_teacher = {"id": teacher_id, "name": name, "speciality": speciality}
    app_data['teachers'].append(new_teacher)
    app_data['next_teacher_id'] += 1
    print(f"Teacher '{name}' added.")

def update_teacher(teacher_id, **fields):
    for teacher in app_data['teachers']:
        if teacher['id'] == teacher_id:
            teacher.update(fields)
            print(f"Teacher {teacher_id} updated.")
            return
    print(f"Error: Teacher with ID {teacher_id} not found.")

def remove_teacher(teacher_id):
    original_count = len(app_data['teachers'])
    app_data['teachers'] = [t for t in app_data['teachers'] if t['id'] != teacher_id]
    if len(app_data['teachers']) < original_count:
        print(f"Teacher {teacher_id} removed.")
    else:
        print(f"Error: Teacher with ID {teacher_id} not found.")

def update_student(student_id, **fields):
    for student in app_data['students']:
        if student['id'] == student_id:
            student.update(fields)
            print(f"Student {student_id} updated.")
            return
    print(f"Error: Student with ID {student_id} not found.")

def remove_student(student_id):
    original_count = len(app_data['students'])
    app_data['students'] = [s for s in app_data['students'] if s['id'] != student_id]
    if len(app_data['students']) < original_count:
        print(f"Student {student_id} removed.")
    else:
        print(f"Error: Student with ID {student_id} not found.")

# --- Receptionist Features ---
def check_in(student_id, course_id, timestamp=None):
    if timestamp is None:
        timestamp = datetime.datetime.now().isoformat()
    check_in_record = {
        "student_id": student_id,
        "course_id": course_id,
        "timestamp": timestamp
    }
    app_data['attendance'].append(check_in_record)
    print(f"Student {student_id} checked into {course_id}.")

def print_student_card(student_id):
    student_to_print = None
    for s in app_data['students']:
        if s['id'] == student_id:
            student_to_print = s
            break
    if student_to_print:
        filename = f"{student_id}_card.txt"
        with open(filename, 'w') as f:
            f.write("========================\n")
            f.write("  MUSIC SCHOOL ID BADGE\n")
            f.write("========================\n")
            f.write(f"ID: {student_to_print['id']}\n")
            f.write(f"Name: {student_to_print['name']}\n")
            f.write(f"Enrolled In: {', '.join(student_to_print.get('enrolled_in', []))}\n")
        print(f"Printed student card to {filename}.")
    else:
        print(f"Error: Could not print card, student {student_id} not found.")

# --- Main Application Loop ---
def main():
    load_data()  # Load all data from file at startup

    while True:
        print("\n===== MSMS v2 (Persistent) =====")
        print("1. Add Teacher")
        print("2. Update Teacher Info")
        print("3. Remove Teacher")
        print("4. Update Student Info")
        print("5. Remove Student")
        print("6. Check-in Student")
        print("7. Print Student Card")
        print("q. Quit and Save")

        choice = input("Enter your choice: ").strip()
        made_change = False

        if choice == '1':
            name = input("Enter teacher name: ").strip()
            speciality = input("Enter speciality: ").strip()
            add_teacher(name, speciality)
            made_change = True

        elif choice == '2':
            try:
                teacher_id = int(input("Enter teacher ID to update: "))
                speciality = input("Enter new speciality: ")
                update_teacher(teacher_id, speciality=speciality)
                made_change = True
            except ValueError:
                print("Invalid input. Teacher ID must be a number.")

        elif choice == '3':
            try:
                teacher_id = int(input("Enter teacher ID to remove: "))
                remove_teacher(teacher_id)
                made_change = True
            except ValueError:
                print("Invalid input. Teacher ID must be a number.")

        elif choice == '4':
            try:
                student_id = int(input("Enter student ID to update: "))
                name = input("Enter new name (leave blank to skip): ").strip()
                enrolled_in = input("Enter courses (comma separated, leave blank to skip): ").strip()
                fields = {}
                if name:
                    fields["name"] = name
                if enrolled_in:
                    fields["enrolled_in"] = [c.strip() for c in enrolled_in.split(",")]
                update_student(student_id, **fields)
                made_change = True
            except ValueError:
                print("Invalid input. Student ID must be a number.")

        elif choice == '5':
            try:
                student_id = int(input("Enter student ID to remove: "))
                remove_student(student_id)
                made_change = True
            except ValueError:
                print("Invalid input. Student ID must be a number.")

        elif choice == '6':
            try:
                student_id = int(input("Enter student ID: "))
                course_id = input("Enter course ID: ")
                check_in(student_id, course_id)
                made_change = True
            except ValueError:
                print("Invalid input. Student ID must be a number.")

        elif choice == '7':
            try:
                student_id = int(input("Enter student ID: "))
                print_student_card(student_id)
            except ValueError:
                print("Invalid input. Student ID must be a number.")

        elif choice.lower() == 'q':
            print("Saving final changes and exiting.")
            break

        else:
            print("Invalid choice. Please try again.")

        if made_change:
            save_data()

    save_data()  # Final save on exit

if __name__ == "__main__":
    main()
