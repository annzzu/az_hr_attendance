/** @odoo-module */
import {patch} from "@web/core/utils/patch";
import {ActivityMenu} from "@hr_attendance/components/attendance_menu/attendance_menu";
import {isIosApp} from "@web/core/browser/feature_detection";
import {ProjectAttendanceForm} from "../project_attendance_form/project_attendance_form";
import {useProjectAttendanceService} from "../../hooks/use_project_attendance";

patch(ActivityMenu.prototype, {

    /**
     * Updates the additional info with the current state.
     */
    setup() {
        this.useProjectAttendanceService = useProjectAttendanceService();
        super.setup(...arguments);
    },

    /**
     * Fetch the employee's project list and set the additional info based on the check-in status.
     * @override
     */
    async searchReadEmployee() {
        await super.searchReadEmployee(...arguments);
        this.state.project_list = this.employee['project_list'];
        if (!this.state.checkedIn) {
            this.additionalInfo = {
                project_id: null,
                task_id: null,
                description: '',
                task_list: [],
            }
        } else {
            this.additionalInfo = this.employee['ongoing_attendance'];
        }

    },

    /**
     * Update the additional info state when it changes.
     * @param {Object} data - The new additional info.
     */
    async onAdditionalInfoChange(data) {
        this.state.additionalInfo = data;
    },

    /**
     * Handle the sign in/out action.
     * If not on iOS app, it will try to get the current geolocation.
     * @override
     */
    async signInOut() {
        // iOS app lacks permissions to call `getCurrentPosition`
        if (!isIosApp()) {
            navigator.geolocation.getCurrentPosition(
                async ({coords: {latitude, longitude}}) => {
                    await this.checkInAndReadEmployee({
                        latitude,
                        longitude,
                    });
                },
                async err => {
                    await this.checkInAndReadEmployee();
                },
                {
                    enableHighAccuracy: true,
                }
            )
        } else {
            await this.checkInAndReadEmployee();
        }
    },

    /**
     * Check in/out the employee and fetch the employee's data.
     * @param {Object} args - The arguments to pass to the check in/out service.
     */
    async checkInAndReadEmployee(args = {}) {
        args = {
            ...args,
            additionalInfo: this.state.additionalInfo ||
                this.employee['ongoing_attendance'],
        }
        await this.useProjectAttendanceService.systrayCheckInOut(args);
        await this.searchReadEmployee();
    }
});

ActivityMenu.components = {
    ...ActivityMenu.components,
    ProjectAttendanceForm
};