/** @odoo-module */

import {Component, useState} from "@odoo/owl";
import {useProjectService} from "../../hooks/use_projects";

export class ProjectAttendanceForm extends Component {

    setup() {
        this.useProjectService = useProjectService();
        this.state = useState({
            ...this.props.additionalInfo,
        });
    }

    async onProjectSelected(ev) {
        this.state.project_id = ev.target.value;
        this.state.tasksDict = await this.useProjectService.getTasksDict(ev.target.value);
        this.onChange();
    }

    onTaskSelected(ev) {
        this.state.task_id = ev.target.value;
        this.onChange();
    }

    onDescriptionChange(ev) {
        this.state.description = ev.target.value;
        this.onChange();
    }

    onChange() {
        this.props.onAdditionalInfoChange({
            project_id: this.state.project_id,
            task_id: this.state.task_id,
            description: this.state.description,
            tasksDict: this.state.tasksDict,
        });
    }

}

ProjectAttendanceForm.template = "az_project_attendance.ProjectAttendanceForm";
ProjectAttendanceForm.props = {
    checkedIn: {
        type: Boolean,
    },
    additionalInfo: {
        type: Object,
    },
    projectsDict: {
        type: Array,
    },
    onAdditionalInfoChange: {
        type: Function,
        optional: true,
    },
};