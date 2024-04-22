# -*- coding: utf-8 -*-
import time
from odoo.tests.common import tagged, TransactionCase, Form


@tagged("at_install", "post_install")
@tagged("az_project_attendance")
class TestProjectAttendance(TransactionCase):
    """Tests for attendance date ranges validity"""

    def create_project(self, index):
        return self.project_env.create(
            {
                "name": f"Project {index}",
            }
        )

    def create_task(self, index, project_id=None):
        project_id = project_id or self.project_1
        return self.task_env.create(
            {
                "name": f"Task {index} {project_id.name}",
                "project_id": project_id.id,
            }
        )

    def setUp(self):
        super(TestProjectAttendance, self).setUp()
        self.attendance_env = self.env["hr.attendance"]
        self.project_env = self.env["project.project"]
        self.task_env = self.env["project.task"]
        self.test_employee = self.env["hr.employee"].create({"name": "Jacky"})

        self.project_1 = self.create_project(index=1)
        self.project_2 = self.create_project(index=2)
        self.task_1 = self.create_task(index=1)
        self.task_2 = self.create_task(index=2, project_id=self.project_2)

    def test_001_test_project_attendance_required_fields(self):
        with Form(self.attendance_env) as attendance_form:
            attendance_form.employee_id = self.test_employee
            attendance_form.check_in = time.strftime("%Y-%m-10 11:00")
            attendance_form.check_out = time.strftime("%Y-%m-10 12:00")
            with self.assertRaises(AssertionError, msg="Project/Task is required"):
                attendance_1 = attendance_form.save()

            attendance_form.project_id = self.project_1
            attendance_form.task_id = self.task_1.id

            attendance_1 = attendance_form.save()

            self.assertEqual(
                attendance_1.project_id, self.project_1, "Project must be set"
            )
