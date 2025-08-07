class student:
    def __init__(self, student_id, name): # Initialize student object
        self.id = student_id # Assign student ID
        self.name = name # Assign student name
        self.enrolled_in = [] # Initialize empty list for enrolled instruments


class teacher:
    def __init__(self, teacher_id, name, speciality): # Initialize teacher object
        self.id = teacher_id # Assign teacher ID
        self.name = name # Assign teacher name
        self.speciality = speciality # Assign teacher speciality

student_db = [] # Global data stores 
teacher_db = [] # Global data stores
next_student_id = 1 # Global data stores
next_teacher_id = 1 # Global data stores 

def add_student(name):
    global next_student_id
    new_student = student(next_student_id, name) # Create new student object
    student_db.append(student) # Add to student database
    next_student_id += 1 # Increment student ID for next student
    return student


