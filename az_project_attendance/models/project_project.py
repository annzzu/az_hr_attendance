from odoo import api, models
from ..controller.controller import try_convert_to_int


class Project(models.Model):
    _inherit = "project.project"

    @api.model
    def get_task_list(self, project_id=None):
        """
        Retrieve a sorted list of tasks associated with a project.

        :param int project_id: The ID of the project to fetch tasks for.
            If None, tasks associated with the current project will be fetched.
        :returns: A list of dictionaries containing task IDs and names.
            Example: [{"id": task.id, "name": task.name}, ...]
        :rtype: list[dict]
        """
        if project_id:
            project_id = self.sudo().browse(try_convert_to_int(project_id))
        else:
            project_id = self
        task_ids = project_id.task_ids.sorted(lambda task: task.id)
        return [{"id": task.id, "name": task.name} for task in task_ids]

    def get_project_list(self):
        """
        Retrieve a list of projects.

        This method fetches a list of all projects from the database,
        sorts them by their IDs, and returns a list of dictionaries
        containing project IDs and names.

        :returns: A list of dictionaries with project IDs and names.
        :rtype: List[Dict[str, Union[int, str]]]
        """
        project_ids = self.sudo().search([])
        project_ids = project_ids.sorted(lambda project: project.id)
        return [{"id": project.id, "name": project.name} for project in project_ids]
