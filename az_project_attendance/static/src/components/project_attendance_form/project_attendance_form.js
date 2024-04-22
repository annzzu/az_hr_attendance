/** @odoo-module */

import {Component, useState} from "@odoo/owl";
import {useProjectAttendanceService} from "../../hooks/use_project_attendance";

export class ProjectAttendanceForm extends Component {

    /**
     * Setup method to initialize the service and state.
     */
    setup() {
        this.useProjectAttendanceService = useProjectAttendanceService();
        this.state = useState({
            ...this.props.additionalInfo,
        });
    }

    /**
     * Determines whether to show the project form.
     * @returns {boolean} - True if the user is checked in or if no project is selected, false otherwise.
     */
    showProjectForm() {
        return this.props.checkedIn ? this.state.project_id : true;
    }

    /**
     * Event handler for when a project is selected.
     * Updates the state with the selected project and fetches the corresponding task list.
     * @param {Event} ev - The event object.
     */
    async onProjectSelected(ev) {
        this.state.project_id = ev.target.value;
        this.state.task_list = await this.useProjectAttendanceService.getTaskList(ev.target.value);
        this.onChange();
    }

    /**
     * Event handler for when a task is selected.
     * Updates the state with the selected task.
     * @param {Event} ev - The event object.
     */
    onTaskSelected(ev) {
        this.state.task_id = ev.target.value;
        this.onChange();
    }

    /**
     * Event handler for when the description changes.
     * Updates the state with the new description.
     * @param {Event} ev - The event object.
     */
    onDescriptionChange(ev) {
        this.state.description = ev.target.value;
        this.onChange();
    }

    /**
     * Updates the additional info with the current state.
     */
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
    project_list: {
        type: Array,
    },
    onAdditionalInfoChange: {
        type: Function,
        optional: true,
    },
};