# Monash School Management System (MSMS) – PST3

This project is a **menu-driven Python application** that manages a simple music school.  
It was built for **FIT1056 – Programming** PST3 and demonstrates **object-oriented programming**, JSON persistence, and a layered design (Model–Controller–View).

---

##  Features

### Base PST3 (required)
- **Models (Fragment 3.1)**  
  - `User`, `StudentUser`, `TeacherUser`, `Course`
- **Controller (Fragment 3.2)**  
  - `ScheduleManager` handles persistence to `data/msms.json`
- **Business logic (Fragment 3.3)**  
  - `check_in(student_id, course_id)`
- **View (Fragment 3.4)**  
  - `main.py` CLI with options to:
    - View daily roster
    - Check-in a student
    - List courses for a teacher
    - List courses for a student

 #Extended Features (added on top of PST3)
1. **Attendance status**  
   - Check-in now records `present`, `late`, or `absent`.
   - Added `list_attendance()` to view logs.

2. **Auto-increment IDs & creation**  
   - New students, teachers, and courses can be created in the CLI.
   - IDs are managed with `next_student_id`, `next_teacher_id`, `next_course_id` in JSON.

3. **Enrolments & lessons**  
   - Enrol/unenrol students from courses.
   - Add lessons (day, time, room) to existing courses.

4. **Richer JSON databank**  
   - `data/msms.json` preloaded with:
     - Students
     - Teachers
     - Courses (with lessons)
     - Attendance log
     - Auto-increment counters

---

## 📂 Project structure

