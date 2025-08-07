class Student:
    def __init__(self, student_id, name): # Initialize student object
        self.id = student_id # Assign student ID
        self.name = name # Assign student name
        self.enrolled_in = [] # Initialize empty list for enrolled instruments


class Teacher:
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
    new_student = Student(next_student_id, name) # Create new student object
    student_db.append(new_student) # Add to student database
    next_student_id += 1 # Increment student ID for next student
    return new_student

def add_teacher(name, speciality):
    global next_teacher_id
    new_teacher = Teacher(next_teacher_id, name, speciality) # Create new teacher object
    teacher_db.append(new_teacher) # Add to teacher database
    next_teacher_id += 1 # Increment teacher ID for next teacher
    return new_teacher

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

def enroll_student_in_instrument(student_id, instrument_name):
    student = find_student_by_id(student_id)
    if student is None:
        return False
    if instrument_name in student.enrolled_in:
        return False
    student.enrolled_in.append(instrument_name)
    return True

if __name__ == "__main__":
    add_student("Alice")
    add_teacher("Mr. Smith", "Piano")
    enroll_student_in_instrument(1, "Piano")
    print_all_students()
    print_all_teachers()