Music School Management System (MSMS) – PST2
Overview
This is the PST2 (Persistence Upgrade) stage of the Music School Management System project for FIT1056 – Introduction to Software Engineering. PST2 focuses on solving the “Amnesia & Chaos” problem from PST1 by adding persistent data storage, full CRUD operations, and new receptionist features.
All data is now stored in a structured JSON file (msms.json), making it permanent across sessions. The code has been refactored into pst2_main.py for better organization.
Features Implemented in PST2
Persistence Engine
load_data(path): Loads all data from msms.json or creates a default structure if the file does not exist.
save_data(path): Saves all current application data into a JSON file in a human-readable format.
CRUD Operations
add_teacher(): Add new teacher records.
update_teacher(teacher_id, **fields): Update specific teacher details.
remove_teacher(teacher_id): Delete a teacher by ID.
add_student(): Add new student records.
update_student(student_id, **fields): Update student details.
remove_student(student_id): Delete a student by ID.
Receptionist Features
check_in(student_id, course_id, timestamp): Record a student’s attendance.
print_student_card(student_id): Generate a text file with a student’s details.
Extra Features
Search Students – Find students by name or partial match.
Enroll in New Courses – Assign a student to additional courses.
Menu options updated to include these features.
Project Structure
MSMS/
• pst2_main.py – Main application logic and menu
• msms.json – Persistent data storage file
• README.md – Project documentation
• .gitignore – Git ignore rules
How to Run
Make sure you have Python 3 installed.
Clone this repository: git clone https://github.com/<your-username>/MSMS.git then cd MSMS
Run the application: python pst2_main.py
Follow the menu prompts to add, update, delete, search, check-in, or print student cards.
How to Test
Add a Teacher → Check msms.json for updated teacher list.
Add a Student → Verify in JSON file.
Update & Remove → Ensure changes are reflected permanently.
Check-in → Confirm attendance record appears in msms.json.
Print Student Card → Check the generated .txt file.
Search Students → Try partial name matches.
Enroll in New Course → Confirm course list updates in JSON.
Design Choices & Assumptions
JSON was chosen for persistence because it is human-readable, lightweight, and easily handled in Python.
Global app_data Dictionary holds all students, teachers, attendance records, and ID counters in a single structure.
Immediate Save After Changes ensures no data is lost if the program closes unexpectedly.
ID System ensures each student and teacher has a unique identifier.
Commit History (PST2)
feat: Added persistence engine (load_data, save_data)
refactor: Updated CRUD functions for new data structure
feat: Added receptionist features (check_in, print_student_card)
feat: Added search & enroll functionality
chore: Updated main loop for persistence
Author
Name: Zayd Hamza
Student ID: [Your ID here]
Unit: FIT1056 – Introduction to Software Engineering
