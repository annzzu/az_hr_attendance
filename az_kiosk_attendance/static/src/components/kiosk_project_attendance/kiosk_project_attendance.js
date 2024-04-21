/** @odoo-module **/

import {Component, useState} from "@odoo/owl";

export class KioskProjectAttendance extends Component {
    async setup() {
        this.state = useState({
            project_id: null,
            task_id: null,
            description: '',
            attendance: null,
            projects_dict: {},
        });
        this.checkedIn = this.props.employeeData.attendance_state === 'checked_in';
    }

    // async onProjectChange(ev) {
    //     if (this.state.project_id) {
    //         const tasks = await this.rpc('get_project_tasks', {
    //             'project_id': this.state.project_id,
    //         });
    //         this.state.tasks_dict = tasks;
    //     }
    // }

    async onConfirm(ev) {
        // save attendance
        await this.props.onAdditionalInfoConfirm();
    }

}

KioskProjectAttendance.template = "az_project_attendance.KioskProjectAttendance";
KioskProjectAttendance.props = {
    employeeData: {type: Object},
    kioskReturn: {type: Function},
    onAdditionalInfoConfirm: {type: Function}
}
