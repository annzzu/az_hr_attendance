/** @odoo-module */
import {patch} from "@web/core/utils/patch";
import kiosk from "@hr_attendance/public_kiosk/public_kiosk_app";
import {KioskProjectAttendance} from "../components/kiosk_project_attendance/kiosk_project_attendance";
import {_t} from "@web/core/l10n/translation";

patch(kiosk.kioskAttendanceApp.prototype, {
    /**
     * @override
     */
    setup() {
        super.setup(...arguments);
    },
    /**
     * @override
     */
    switchDisplay(screen) {
        const displays = ["main", "greet", "manual", "pin", "project_attendance"]
        if (displays.includes(screen)) {
            this.state.active_display = screen;
        } else {
            this.state.active_display = "main";
        }
    },
    /**
     * @override
     */
    async onManualSelection(employeeId, enteredPin) {
        const result = await this.rpc('manual_selection', {
            'token': this.props.token,
            'employee_id': employeeId,
            'pin_code': enteredPin
        })
        if (result && result.attendance) {
            this.employeeData = result;
            this.switchDisplay('project_attendance');

            // this.switchDisplay('greet');
        } else {
            if (enteredPin) {
                this.displayNotification(_t("Wrong Pin"))
            }
        }
    },
    /**
     * @override
     */
    async onAdditionalInfoConfirm() {
        this.switchDisplay('greet');
    },
});

kiosk.kioskAttendanceApp.components = {
    ...kiosk.kioskAttendanceApp.components,
    KioskProjectAttendance
};
