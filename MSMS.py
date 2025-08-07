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

def add_teacher(name, speciality):
    global next_teacher_id
    teacher = teacher(next_teacher_id, name, speciality) # Create new teacher object
    teacher_db.append(teacher) # Add to teacher database
    next_teacher_id += 1 # Increment teacher ID for next teacher
    return teacher

def find_student_by_id(student_id):
    for student in student_db:
        if student.id == student_id:
            return student
    return None

def find_teacher_by_id(teacher_id):
    for teacher in teacher_db:
        if teacher.id == teacher_id:
            return teacher
    return None

def print_all_students():
    print ("All Students:")
    for student in student_db:
        print(f"ID: {student.id}, Name: {student.name}, Enrolled in: {', '.join(student.enrolled_in)}")

def print_all_teachers():
    print("All Teachers:")
    for teacher in teacher_db:
        print(f"ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}")
        
