from app.schedule import ScheduleManager

def print_roster(manager, day):
    roster = manager.get_daily_roster(day)
    if not roster:
        print("No lessons found for", day)
        return
    print("Roster for", day)
    for r in roster:
        course = r["course"]
        teacher = r["teacher"]
        students = [s.name for s in r["students"]]
        print(" -", r["time"], "|", course.name, "| Room", r["room"],
              "| Teacher:", teacher.name if teacher else course.teacher_id,
              "| Students:", ", ".join(students))

def do_check_in(manager):
    try:
        student_id = int(input("Student ID: "))
        course_id = int(input("Course ID: "))
    except ValueError:
        print("IDs must be numbers")
        return
    status = input("Status (present/late/absent) [press Enter for present]: ").strip().lower()
    if status == "":
        status = "present"
    manager.check_in(student_id, course_id, status)

def list_teacher_schedule(manager):
    try:
        tid = int(input("Teacher ID: "))
    except ValueError:
        print("Teacher ID must be a number.")
        return
    day = input("Day (press Enter to skip): ")
    items = manager.get_courses_for_teacher(tid, day if day else None)
    if not items:
        print("No courses found")
        return
    print("Teacher schedule:")
    for c in items:
        lesson_info = []
        for l in c.lessons:
            text = l["day"] + " " + l["start_time"] + " (Room " + l["room"] + ")"
            lesson_info.append(text)
        print(" -", c.name, "|", "; ".join(lesson_info))

def list_student_schedule(manager):
    try:
        sid = int(input("Student ID: "))
    except ValueError:
        print("Student ID must be a number.")
        return
    day = input("Day (press Enter to skip): ")
    items = manager.get_courses_for_student(sid, day if day else None)
    if not items:
        print("No courses found")
        return
    print("Student schedule:")
    for c in items:
        lesson_info = []
        for l in c.lessons:
            text = l["day"] + " " + l["start_time"] + " (Room " + l["room"] + ")"
            lesson_info.append(text)
        print(" -", c.name, "|", "; ".join(lesson_info))

def add_student(manager):
    name = input("Student name: ").strip()
    email = input("Student email (optional): ").strip()
    manager.add_student(name, email)

def add_teacher(manager):
    name = input("Teacher name: ").strip()
    speciality = input("Speciality: ").strip()
    email = input("Email (optional): ").strip()
    manager.add_teacher(name, speciality, email)

def add_course(manager):
    name = input("Course name: ").strip()
    instrument = input("Instrument: ").strip()
    try:
        teacher_id = int(input("Teacher ID: "))
    except ValueError:
        print("Teacher ID must be a number.")
        return
    manager.add_course(name, instrument, teacher_id)

def enrol_student(manager):
    try:
        course_id = int(input("Course ID: "))
        student_id = int(input("Student ID: "))
    except ValueError:
        print("IDs must be numbers")
        return
    manager.enrol_student(course_id, student_id)

def unenrol_student(manager):
    try:
        course_id = int(input("Course ID: "))
        student_id = int(input("Student ID: "))
    except ValueError:
        print("IDs must be numbers")
        return
    manager.unenrol_student(course_id, student_id)

def show_attendance(manager):
    filt = input("Filter by (s)tudent, (c)ourse, or (n)one? ").strip().lower()
    sid = None
    cid = None
    if filt == "s":
        try:
            sid = int(input("Student ID: "))
        except ValueError:
            print("Not a number.")
            return
    elif filt == "c":
        try:
            cid = int(input("Course ID: "))
        except ValueError:
            print("Not a number.")
            return
    records = manager.list_attendance(student_id=sid, course_id=cid)
    if not records:
        print("No attendance records.")
        return
    print("Attendance records:")
    for r in records:
        print(" - student:", r.get("student_id"), "| course:", r.get("course_id"),
              "| status:", r.get("status", "present"), "| at:", r.get("timestamp"))

def add_lesson(manager):
    try:
        course_id = int(input("Course ID: "))
    except ValueError:
        print("Course ID must be a number.")
        return
    day = input("Day (e.g., Monday): ").strip()
    time = input("Start time (e.g., 16:00): ").strip()
    room = input("Room: ").strip()
    manager.add_lesson(course_id, day, time, room)

def main():
    manager = ScheduleManager()

    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        print("[1] View daily roster")
        print("[2] Check-in a student (with status)")
        print("[3] List courses for a teacher")
        print("[4] List courses for a student")
        print("[5] Add student")
        print("[6] Add teacher")
        print("[7] Add course")
        print("[8] Enrol student in course")
        print("[9] Unenrol student from course")
        print("[10] Show attendance")
        print("[11] Add lesson to a course")
        print("[q] Quit")
        choice = input("Enter choice: ").strip().lower()

        if choice == '1':
            day = input("Enter day (e.g., Monday): ").strip()
            print_roster(manager, day)
        elif choice == '2':
            do_check_in(manager)
        elif choice == '3':
            list_teacher_schedule(manager)
        elif choice == '4':
            list_student_schedule(manager)
        elif choice == '5':
            add_student(manager)
        elif choice == '6':
            add_teacher(manager)
        elif choice == '7':
            add_course(manager)
        elif choice == '8':
            enrol_student(manager)
        elif choice == '9':
            unenrol_student(manager)
        elif choice == '10':
            show_attendance(manager)
        elif choice == '11':
            add_lesson(manager)
        elif choice == 'q':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
