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
    manager.check_in(student_id, course_id)

def list_teacher_schedule(manager):
    tid = int(input("Teacher ID: "))
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
    sid = int(input("Student ID: "))
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

def main():
    manager = ScheduleManager()

    while True:
        print("\n===== MSMS v3 (Object-Oriented) =====")
        print("[1] View daily roster")
        print("[2] Check-in a student")
        print("[3] List courses for a teacher")
        print("[4] List courses for a student")
        print("[q] Quit")
        choice = input("Enter choice: ").strip().lower()

        if choice == '1':
            day = input("Enter day (e.g., Monday): ")
            print_roster(manager, day)
        elif choice == '2':
            do_check_in(manager)
        elif choice == '3':
            list_teacher_schedule(manager)
        elif choice == '4':
            list_student_schedule(manager)
        elif choice == 'q':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
