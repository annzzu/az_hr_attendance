from odoo import fields, models


class Project(models.Model):
    _inherit = "project.project"

    def get_project_tasks(self):
        task_ids = self.env["project.task"].search(
            [("project_id.id", "=", self.id)]
        )
        task_ids = task_ids.sorted(lambda project: project.id)
        return [{"id": task.id, "name": task.name} for task in task_ids]
