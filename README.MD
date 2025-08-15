Music School Management System (MSMS) – PST2
Overview
This repository contains the PST2 (Persistence Upgrade) stage of the Music School Management System (MSMS), developed as part of FIT1056 – Introduction to Software Engineering, Semester 2. PST2 builds on PST1 by adding permanent data storage, expanded CRUD functionality, and receptionist features. All application data is now stored in a structured JSON file (msms.json), ensuring it is retained between program runs.
The old MSMS.py script from PST1 has been fully refactored into pst2_main.py, improving readability, maintainability, and modularity.
Objectives of PST2
Eliminate "Amnesia" – In PST1, data was stored in memory only, meaning it was lost when the program closed. PST2 introduces file persistence via a JSON file, so all data is saved permanently.
Improve Data Organization – All information (students, teachers, attendance, ID counters) is stored in a single global dictionary named app_data.
Introduce Robust CRUD Operations – Add missing "Update" and "Delete" functions and ensure changes are saved immediately.
Add Receptionist Tools – Ability to check in students and generate printable student cards.
Extend Functionality – Add Search Students and Enroll in New Courses.
Features Implemented
Persistence Engine
load_data(path) loads application data from msms.json. If the file doesn’t exist, creates a default structure:
{
"students": [],
"teachers": [],
"attendance": [],
"next_student_id": 1,
"next_teacher_id": 1
}
save_data(path) writes the current state of app_data to msms.json in a human-readable format.
CRUD Operations
Teachers:
add_teacher() – Adds a teacher with unique ID, name, and instrument taught.
update_teacher(teacher_id, **fields) – Updates teacher details.
remove_teacher(teacher_id) – Deletes a teacher by ID.
Students:
add_student() – Adds a student with unique ID, name, and courses.
update_student(student_id, **fields) – Updates student details.
remove_student(student_id) – Deletes a student by ID.
Receptionist Features
check_in(student_id, course_id, timestamp) – Adds attendance record.
print_student_card(student_id) – Generates a text file with student details.
Extra PST2 Features
search_students(query) – Searches students by name.
enroll_in_course(student_id, course_name) – Adds a course to a student’s record.
Project Structure
MSMS/
pst2_main.py – Main application logic and menu loop
msms.json – Persistent JSON data file
README.md – Documentation
.gitignore – Git ignore rules
How the Program Works
Startup – load_data() runs first, loading msms.json or creating default data.
Menu – Offers options to manage teachers, students, check-ins, searches, enrollments, and more.
Persistence – After any data change, save_data() is called immediately.
Exit – Data is already saved, so closing the program is safe.
How to Run
Install Python 3 if not already installed.
Clone the repository:
git clone https://github.com/<your-username>/MSMS.git
cd MSMS
Run the program:
python pst2_main.py
