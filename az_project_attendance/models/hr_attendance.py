from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    project_id = fields.Many2one("project.project")
    task_id = fields.Many2one(
        "project.task",
        domain="['|',('project_id', '=', False),('project_id', '=', project_id)]",
    )
    description = fields.Text()

    @api.onchange("project_id")
    def _onchange_project_id(self):
        self.task_id = False

    @api.constrains("project_id", "task_id")
    def _constrains_additional_info(self):
        for record in self:
            if not record.project_id or not record.task_id:
                raise ValidationError(_("Project and Task are required."))
            elif record.task_id.id not in record.project_id.task_ids.ids:
                raise ValidationError(_("Task must belong to the selected project."))
