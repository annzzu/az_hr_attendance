/** @odoo-module */
import {patch} from "@web/core/utils/patch";
import {ActivityMenu} from "@hr_attendance/components/attendance_menu/attendance_menu";
import {isIosApp} from "@web/core/browser/feature_detection";
import {ProjectAttendanceForm} from "../project_attendance_form/project_attendance_form";
import {useProjectService} from "../../hooks/use_projects";
import {EventBus} from "@odoo/owl";

patch(ActivityMenu.prototype, {
    /**
     * @override
     */
    setup() {
        this.bus = new EventBus();
        this.useProjectService = useProjectService();
        super.setup(...arguments);
        this.state.projectsDict = this.useProjectService.state.projectsDict;
    },
    /**
     * @override
     */
    async searchReadEmployee() {
        await super.searchReadEmployee(...arguments);
        if (!this.state.checkedIn) {
            this.additionalInfo = {
                project_id: null,
                task_id: null,
                description: '',
                tasksDict: {},
            }
            console.log('from menu ONCHECKOUT', this.additionalInfo);
        } else {
            this.additionalInfo = this.employee['ongoing_attendance'];
        }

    },

    async onAdditionalInfoChange(data) {
        this.state.additionalInfo = data;
    },

    async signInOut() {
        let kwargs = {
            additionalInfo: this.state.additionalInfo,
        }
        // iOS app lacks permissions to call `getCurrentPosition`
        if (!isIosApp()) {
            navigator.geolocation.getCurrentPosition(
                async ({coords: {latitude, longitude}}) => {
                    await this.rpc("/hr_attendance/systray_check_in_out", {
                        latitude,
                        longitude,
                        ...kwargs,
                    })
                    await this.searchReadEmployee()
                },
                async err => {
                    await this.rpc("/hr_attendance/systray_check_in_out", kwargs)
                    await this.searchReadEmployee()
                },
                {
                    enableHighAccuracy: true,
                }
            )
        } else {
            await this.rpc("/hr_attendance/systray_check_in_out", kwargs)
            await this.searchReadEmployee()
        }
    },
});

ActivityMenu.components = {
    ...ActivityMenu.components,
    ProjectAttendanceForm
};