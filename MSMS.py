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

def find_student(term):
    term_lower = term.lower()
    results = [ student for student in student_db if term_lower in student.name.lower()]
    return results

def find_teacher(term):
    term_lower = term.lower()
    results = [ teacher for teacher in teacher_db if term_lower in teacher.name.lower() or term_lower in teacher.speciality.lower()]
    return results

def front_desk_register(name, instrument):
    student = add_student(name)
    enrolled = enroll_student_in_instrument(student.id, instrument)
    if enrolled:
        print(f"student '{student.name}' (ID:{student.id}) registered and enrolled in '{instrument}'.")
    else: 
        print(f"student '{student.name}' (ID: {student.id}) registered, but is not enrolled in {instrument} failed.")
    return student
    
def front_desk_enrol(student_id, instrument):
    student = find_student_by_id(student_id)
    if student is None:
        print(f"Student with ID {student_id} not found.")
        return False
    enrolled = enroll_student_in_instrument(student_id, instrument)
    if enrolled:
        print(f"Student '{student.name}' (ID: {student.id}) enrolled in '{instrument}'.")
        return True
    else:
        print(f"Student '{student.name}' (ID: {student.id}) is already enrolled in '{instrument}'.")
    return False

def front_desk_lookup(term):
    students_found = find_student(term)
    teachers_found = find_teacher(term)

    if students_found:
        print("Students found:")
        for student in students_found:
            instruments = ', '.join(student.enrolled_in) if student.enrolled_in else 'None'
            print(f"ID: {student.id}, Name: {student.name}, Enrolled in: {instruments}")
    else:
        print("No students found.")

    if teachers_found:
        print("Teachers found:")
        for teacher in teachers_found:
            print(f"ID: {teacher.id}, Name: {teacher.name}, Speciality: {teacher.speciality}")
    else:
        print("No teachers found.")


def main():
    print("Welcome to the Music School Management System!")

    while True:
        print("\n--- Main Menu ---")
        print("1. Add a new student and assign an instrument")
        print("2. Add an instrument to an existing student")
        print("3. Search for a student or teacher by name")
        print("4. Exit the system")

        choice = input("Select an option (1-4): ").strip()

        if choice == '1':
            name = input("Student's full name: ").strip()
            instrument = input("Instrument to enrol them in: ").strip()
            front_desk_register(name, instrument)

        elif choice == '2':
            try:
                student_id = int(input("Enter the student's ID: ").strip())
            except ValueError:
                print("That wasn't a valid number. Please try again.")
                continue
            instrument = input("Instrument to add: ").strip()
            front_desk_enrol(student_id, instrument)

        elif choice == '3':
            term = input("Type a name or part of a name to search: ").strip()
            front_desk_lookup(term)

        elif choice == '4':
            print("Thank you for using the Music School System. Goodbye! 👋")
            break

        else:
            print("Invalid option. Please pick a number from 1 to 4.")

if __name__ == "__main__":
    main()
