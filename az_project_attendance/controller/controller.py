# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _, api
from odoo.http import request
from odoo.addons.hr_attendance.controllers.main import HrAttendance


def try_convert_to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


class AZHrAttendance(HrAttendance):
    # override
    @http.route('/hr_attendance/attendance_user_data', type="json", auth="user")
    def user_attendance_data(self):
        result = super(AZHrAttendance, self).user_attendance_data() or {}
        employee = request.env.user.employee_id
        if employee:
            result.update({
                "project_ids": [
                    {"project_id": project, "id": project.id, "name": project.name}
                    for project in request.env["project.project"].search([])],
                "ongoing_attendance": self.get_ongoing_attendance(),
            })
        return result

    # override
    @http.route('/hr_attendance/systray_check_in_out', type="json", auth="user")
    def systray_attendance(self, latitude=False, longitude=False, **kwargs):
        attendance = super().systray_attendance(latitude, longitude)
        employee = request.env.user.employee_id
        additional_info = kwargs.get('additionalInfo', {})
        employee.last_attendance_id.write({
            'project_id': try_convert_to_int(additional_info.get('project_id')),
            'task_id': try_convert_to_int(additional_info.get('task_id')),
            'description': additional_info.get('description') or '',
        })
        return attendance

    @http.route("/hr_attendance/project_ids", type="json", auth="user")
    def user_attendance_project_data(self):
        project_ids = request.env["project.project"].search([])
        project_ids = project_ids.sorted(lambda project: project.id)
        return [{"project_id": project, "id": project.id, "name": project.name}
                for project in project_ids]

    @http.route("/hr_attendance/task_ids/<string:project_id>", type="json", auth="user")
    def user_attendance_task_data(self, project_id):
        task_ids = request.env["project.task"].search(
            [("project_id.id", "=", project_id)]
        )
        task_ids = task_ids.sorted(lambda project: project.id)
        return [{"id": task.id, "name": task.name}
                for task in task_ids]

    @staticmethod
    def get_ongoing_attendance():
        employee = request.env.user.employee_id
        last_attendance_id = employee.last_attendance_id
        if not last_attendance_id:
            return {}
        project = last_attendance_id.project_id
        task_dict = [{"id": task.id, "name": task.name}
                     for task in project.task_ids] if project else []
        return {
            "project_id": project.id,
            "task_id": last_attendance_id.task_id.id,
            "description": last_attendance_id.description or '',
            "attendance_id": last_attendance_id.id,
            "tasksDict": task_dict
        }
