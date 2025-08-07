# MSMS
Music School Management System
# MSMS
## Overview

This project is the first stage (PST1) of the Music School Management System for FIT1056 - Introduction to Software Engineering (2025 Semester 2). The goal is to build a simple, in-memory prototype that models the core functionality of managing students, teachers, and instrument enrollments.

---

What each part does

- Student and Teacher Classes:**  
  Define the data structure for students (ID, name, enrolled instruments) and teachers (ID, name, specialty).

- In-Memory Databases:**  
  Use global lists 'student_db' and 'teacher_db' to store all records temporarily during program execution.

- ID Counters:
  Manage unique incremental IDs for students and teachers.

- Core Helper Functions:
  Functions to add students and teachers, search, enroll students in instruments, and retrieve records.

- Front Desk Functions:
  Higher-level functions that simulate receptionist actions like registering students and enrolling instruments.

- Main Menu:
  A console-based interactive menu allowing users to:
  - Add students and assign instruments
  - Add instruments to existing students
  - Add new teachers
  - Search students and teachers by name or specialty
  - List all students or teachers
  - Exit the system

---

## How to run and test

1. Make sure you have Python 3 installed.  
   Check with: `python3 --version`

2. Run the application:  
   ```bash
   python3 MSMS.py
