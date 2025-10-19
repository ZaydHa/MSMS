import json
import pytest
from app.schedule import ScheduleManager

@pytest.fixture
def fresh_manager(tmp_path):
    seed = {
        "students": [{"id": 1, "name": "Alice Johnson", "email": "alice@mail.com", "enrolled_course_ids": []}],
        "teachers": [{"id": 1, "name": "Mr. Smith", "email": "smith@mail.com"}],
        "courses": [{"id": 1, "title": "Piano 101", "teacher_id": 1}],
        "attendance": [],
        "finance_log": []
    }
    test_file = tmp_path / "test_data.json"
    test_file.write_text(json.dumps(seed))
    return ScheduleManager(data_path=str(test_file))

def test_add_student_and_payment(fresh_manager):
    s = fresh_manager.add_student("Bob", "bob@mail.com", [])
    assert s["id"] == 2
    ok = fresh_manager.record_payment(s["id"], 120.0, "Card")
    assert ok is True
    hist = fresh_manager.get_payment_history(s["id"])
    assert len(hist) == 1 and hist[0]["amount"] == 120.0

def test_check_in_success(fresh_manager):
    alice = fresh_manager._student_by_id(1)
    alice["enrolled_course_ids"].append(1)
    fresh_manager._save_data()
    assert fresh_manager.check_in(1, 1) is True
    assert len(fresh_manager.attendance) == 1

def test_export_reports_empty_ok(fresh_manager, tmp_path):
    p_csv = tmp_path / "payments.csv"
    a_csv = tmp_path / "attendance.csv"
    assert fresh_manager.export_report("payments", str(p_csv)) is True
    assert fresh_manager.export_report("attendance", str(a_csv)) is True
    assert p_csv.exists() and a_csv.exists()
