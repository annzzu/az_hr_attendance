# -*- coding: utf-8 -*-
import logging
import datetime
from odoo import http, _
from odoo.http import request
from odoo.addons.hr_attendance.controllers.main import HrAttendance
from odoo.tools import float_round

_logger = logging.getLogger(__name__)


def try_convert_to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


class AZHrAttendance(HrAttendance):

    @staticmethod
    def get_employee_id(employee_id):
        """
        Convert the employee_id to an integer, return the corresponding employee record.

        :param employee_id: The ID of the employee.
        :returns: The employee record if the ID is valid, None otherwise.
        """
        return request.env["hr.employee"].sudo().browse(try_convert_to_int(employee_id))

    @http.route(
        "/hr_attendance/task_ids/<string:project_id>", type="json", auth="public"
    )
    def user_attendance_task_data(self, project_id):
        """
        Get the list of tasks for a given project.

        :param project_id: The ID of the project.
        :returns: The list of tasks for the project.
        """
        return request.env["project.project"].get_task_list(project_id)

    @http.route("/hr_attendance/systray_check_in_out", type="json", auth="user")
    def systray_attendance(self, latitude=False, longitude=False, **kwargs):
        """
        Override the systray_attendance method to add additional info in attendance.

        :param latitude: The latitude of the location.
        :param longitude: The longitude of the location.
        :returns: The attendance record.
        """
        attendance = super().systray_attendance(latitude, longitude)
        attendance_id = attendance.get("ongoing_attendance").get("attendance_id")
        attendance_id = request.env["hr.attendance"].browse(attendance_id)
        self.attendance_update(attendance_id, **kwargs)
        return attendance

    @http.route("/hr_attendance/manual_selection", type="json", auth="public")
    def manual_selection(self, token, employee_id, pin_code):
        """
        Override manual_selection method to remove attendance create/write logic
        and return the employee's attendance information if the pin codes match.

        :param token: The token used for authentication.
        :param employee_id: The ID of the employee.
        :param pin_code: The pin code entered by the employee.
        :returns: A dictionary with the employee's attendance information,
                  or an empty dictionary if the pin codes do not match or are not used.
        """
        company = self._get_company(token)
        if company:
            employee = self.get_employee_id(employee_id)
            if employee.company_id == company and (
                (not company.attendance_kiosk_use_pin) or (employee.pin == pin_code)
            ):
                return self._get_employee_info_response(
                    employee, kiosk_mode="manual_selection"
                )
        return {}

    @http.route("/hr_attendance/attendance_barcode_scanned", type="json", auth="public")
    def scan_barcode(self, token, barcode):
        """
        Override scan_barcode method to remove attendance create/write logic
        and return the employee's attendance.

        :param token: The token used for authentication.
        :param barcode: The barcode scanned by the employee.
        :returns: A dictionary with the employee's attendance information,
          or an empty dictionary if no employee is found with the provided barcode.
        """
        company = self._get_company(token)
        if company:
            domain = [("barcode", "=", barcode), ("company_id", "=", company.id)]
            employee = request.env["hr.employee"].sudo().search(domain, limit=1)
            if employee:
                return self._get_employee_info_response(employee, kiosk_mode="barcode")
        return {}

    @http.route("/hr_attendance/project_attendance", type="json", auth="public")
    def project_attendance(self, employee_id, **kwargs):
        """
        Handle the attendance of a project for a given employee.

        This function attempts to change the attendance status of
        the specified employee in the context of a project.
        If an exception occurs during the process, it logs the error and returns
        an empty dictionary.

        :param employee_id: The ID of the employee.
        :param kwargs: Additional keyword arguments.
        :returns: A dictionary with the updated attendance information, or an empty dictionary if an error occurs.
        """
        try:
            return self.employee_attendance_action_change(
                employee_id=employee_id, mode="kiosk", **kwargs
            )
        except Exception as e:
            _logger.info("saving additional info in attendance", e)
            return {}

    @staticmethod
    def get_ongoing_attendance(employee_id, kiosk_mode=False):
        """
        Get the ongoing attendance record for a given employee.

        This function retrieves the last attendance record for the specified employee
        and checks if it's ongoing. If the attendance is ongoing, returns a dict
        with full additional details about the attendance.
        If the attendance is not ongoing or if the kiosk mode is enabled and
        the last attendance is checked out, it returns an empty dictionary.

        :param employee_id: The ID of the employee.
        :param kiosk_mode: boolean if the function is being called in kiosk mode.
                           Defaults to False.
        :returns: A dictionary with details about the ongoing attendance,
                  or an empty dictionary if there is no ongoing attendance.
        """
        last_attendance_id = employee_id.last_attendance_id
        if not last_attendance_id or (kiosk_mode and last_attendance_id.check_out):
            return {}

        project_id = last_attendance_id.sudo().project_id
        task_id = last_attendance_id.sudo().task_id
        task_list = project_id.get_task_list() if project_id else []
        full_info = {
            "description": last_attendance_id.description or "",
            "project_name": project_id.name if project_id else "",
            "task_name": task_id.name if task_id else "",
        }
        show_additional_info = any([value != "" for value in full_info.values()])
        result = {
            "project_id": project_id.id,
            "task_id": last_attendance_id.task_id.id,
            "description": last_attendance_id.description or "",
            "attendance_id": last_attendance_id.id,
            "task_list": task_list,
            "full_info": full_info if show_additional_info else None,
        }
        return result

    def employee_attendance_action_change(self, employee_id, mode, **kwargs):
        """
        Change the attendance additional info of a specified employee.

        This function retrieves the employee record using the provided employee_id,
        gets the geoip response using the provided mode, and changes the attendance
        status of the employee. It also updates the attendance with any additional
        information provided in kwargs.

        :param employee_id: The ID of the employee.
        :param mode: The mode used to get the geoip response.
        :param kwargs: Additional keyword arguments used to update the attendance.
        :returns: The updated attendance information for the employee.
        """
        employee_id = self.get_employee_id(employee_id)
        attendance = employee_id.sudo()._attendance_action_change(
            self._get_geoip_response(mode)
        )
        self.attendance_update(attendance, **kwargs)
        return self._get_employee_info_response(employee_id)

    def attendance_update(self, attendance, **kwargs):
        """
        Update the attendance record with additional information.

        This function takes an attendance record and a set of keyword arguments.
        It extracts the additional information from the keyword arguments and updates
        the attendance record with this information.

        :param attendance: The attendance record to be updated.
        :param kwargs: Additional keyword arguments used to update the attendance.
        :returns: The updated attendance record.
        """
        if attendance:
            additional_info = kwargs.get("additionalInfo")
            additional_info = self.get_additional_info(additional_info)
            if additional_info:
                attendance.write(additional_info)
        return attendance

    @staticmethod
    def get_additional_info(additional_info):
        """
        Extract additional information from a given dictionary.

        :param additional_info: The dictionary from which the information is extracted.
        :returns: A dictionary with the extracted information.
        """
        return (
            {
                "project_id": try_convert_to_int(additional_info.get("project_id")),
                "task_id": try_convert_to_int(additional_info.get("task_id")),
                "description": additional_info.get("description") or "",
            }
            if additional_info
            else {}
        )

    def _get_employee_info_response_override(self, employee, kiosk_mode=False):
        """
        Override
        !!! this function is a copy of the original function
        !!! with additional info added to the response
        !!! it uses monkey patch to the original function

        Get the employee's information and attendance details,
        including additional information and projects.

        This function retrieves the employee's information and attendance details.

        :param employee: The employee record for which the information is retrieved.
        :param kiosk_mode: boolean if the function is being called in kiosk mode.
        :returns: A dictionary with the employee's information and attendance details,
         or an empty dictionary if the employee record is not provided.
        """
        response = {}
        if employee:
            project_list = request.env["project.project"].get_project_list()
            overtime_today_domain = [
                ("employee_id", "=", employee.id),
                ("date", "=", datetime.date.today()),
                ("adjustment", "=", False),
            ]
            overtime_today = (
                request.env["hr.attendance.overtime"]
                .sudo()
                .search(overtime_today_domain)
                .duration
                or 0
            )
            response = {
                "id": employee.id,
                "employee_name": employee.name,
                "employee_avatar": employee.image_1920,
                "hours_today": float_round(employee.hours_today, precision_digits=2),
                "total_overtime": float_round(
                    employee.total_overtime, precision_digits=2
                ),
                "last_attendance_worked_hours": float_round(
                    employee.last_attendance_worked_hours, precision_digits=2
                ),
                "last_check_in": employee.last_check_in,
                "attendance_state": employee.attendance_state,
                "hours_previously_today": float_round(
                    employee.hours_previously_today, precision_digits=2
                ),
                "kiosk_delay": employee.company_id.attendance_kiosk_delay * 1000,
                "attendance": {
                    "check_in": employee.last_attendance_id.check_in,
                    "check_out": employee.last_attendance_id.check_out,
                },
                "overtime_today": overtime_today,
                "use_pin": employee.company_id.attendance_kiosk_use_pin,
                "display_systray": employee.company_id.attendance_from_systray,
                "display_overtime": employee.company_id.hr_attendance_display_overtime,
                "project_list": project_list,
                "ongoing_attendance": self.get_ongoing_attendance(employee, kiosk_mode),
            }

        return response


"""
monkey patching of the original method to add additional info to the response
"""
HrAttendance._get_employee_info_response = (
    AZHrAttendance._get_employee_info_response_override
)
