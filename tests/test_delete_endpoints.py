import json


def test_delete_student_success(client, seeded_db):
    student_id = seeded_db['student_id']
    # delete the student
    resp = client.post(f"/user/students/delete/{student_id}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['success'] is True

    # ensure student removed from DB (use app context)
    from app.models import Student
    with client.application.app_context():
        assert Student.query.get(student_id) is None


def test_delete_program_blocked_when_students_exist(client, seeded_db):
    prog_id = seeded_db['program_id']
    resp = client.post(f"/user/programs/delete/{prog_id}")
    assert resp.status_code == 400
    data = resp.get_json()
    assert data['success'] is False
    assert 'students' in data['message'] or 'cannot' in data['message'] or 'linked' in data['message']


def test_delete_program_success_after_removing_students(client, seeded_db):
    prog_id = seeded_db['program_id']
    stu_id = seeded_db['student_id']
    # delete student first
    r1 = client.post(f"/user/students/delete/{stu_id}")
    assert r1.status_code == 200 and r1.get_json().get('success')

    r2 = client.post(f"/user/programs/delete/{prog_id}")
    assert r2.status_code == 200
    assert r2.get_json().get('success') is True


def test_delete_college_blocked_when_programs_exist(client, seeded_db):
    col_id = seeded_db['college_id']
    resp = client.post(f"/user/colleges/delete/{col_id}")
    assert resp.status_code == 400
    data = resp.get_json()
    assert data['success'] is False


def test_delete_college_success_after_remove_program(client, seeded_db):
    col_id = seeded_db['college_id']
    prog_id = seeded_db['program_id']
    stu_id = seeded_db['student_id']

    # remove student then program
    r1 = client.post(f"/user/students/delete/{stu_id}")
    assert r1.status_code == 200
    r2 = client.post(f"/user/programs/delete/{prog_id}")
    assert r2.status_code == 200

    r3 = client.post(f"/user/colleges/delete/{col_id}")
    assert r3.status_code == 200
    assert r3.get_json().get('success') is True
