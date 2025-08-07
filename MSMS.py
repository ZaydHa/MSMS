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



git init
git add MSMS.py
git commit -m "Checkpoint A: Added Student and Teacher classes"


