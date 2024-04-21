from odoo import api, fields, models


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    project_id = fields.Many2one("project.project")
    task_id = fields.Many2one(
        "project.task",
        domain="['|',('project_id', '=', False), " "('project_id', '=', project_id)]",
    )
    description = fields.Text()

    @api.onchange("project_id")
    def _onchange_project_id(self):
        self.task_id = False
