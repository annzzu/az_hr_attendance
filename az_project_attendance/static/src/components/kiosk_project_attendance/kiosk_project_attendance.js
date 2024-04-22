/** @odoo-module **/

import {Component, useState} from "@odoo/owl";
import {ProjectAttendanceForm} from "../project_attendance_form/project_attendance_form";

/**
 * This class represents the KioskProjectAttendance component.
 * It manages additional the state of the project attendance form in the kiosk mode.
 */
export class KioskProjectAttendance extends Component {
    /**
     * Setup method to initialize the state.
     * The state includes the project list, additional info, and the check-in status.
     */
    async setup() {
        const employeeData = this.props.employeeData;
        this.state = useState({
            project_list: employeeData['project_list'],
            additionalInfo: employeeData['ongoing_attendance'],
            checkedIn: this.props.checkedIn,
        });
    }

    /**
     * Method to handle the confirmation of the form.
     * It calls the onAdditionalInfoConfirm prop with the current additional info.
     */
    async onConfirm() {
        await this.props.onAdditionalInfoConfirm(this.state.additionalInfo);
    }

    /**
     * Method to handle the change of the additional info.
     * It updates the state with the new additional info.
     * @param {Object} data - The new additional info.
     */
    onAdditionalInfoChange(data) {
        this.state.additionalInfo = data;
    }
}

KioskProjectAttendance.template = "az_project_attendance.KioskProjectAttendance";
KioskProjectAttendance.props = {
    checkedIn: {type: Boolean},
    employeeData: {type: Object},
    kioskReturn: {type: Function},
    onAdditionalInfoConfirm: {type: Function},
    onClickBack: {type: Function},
}
KioskProjectAttendance.components = {
    ProjectAttendanceForm
}