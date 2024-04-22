/** @odoo-module */
import {patch} from "@web/core/utils/patch";
import kiosk from "@hr_attendance/public_kiosk/public_kiosk_app";
import {KioskProjectAttendance} from "../components/kiosk_project_attendance/kiosk_project_attendance";
import {_t} from "@web/core/l10n/translation";
import {useProjectAttendanceService} from "../hooks/use_project_attendance";

patch(kiosk.kioskAttendanceApp.prototype, {

    /**
     * @override
     * add service for rpc and notification
     */
    setup() {
        this.useProjectAttendanceService = useProjectAttendanceService();
        super.setup(...arguments);
    },

    /**
     * @override
     * add project_attendance in the active display screen.
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
     * add  navigation to the project_attendance screen after result
     */
    async onBarcodeScanned(barcode) {
        if (this.lockScanner || this.state.active_display !== 'main') {
            return;
        }

        this.lockScanner = true;

        const result = await this.useProjectAttendanceService.onAttendanceBarcodeScanned(
            barcode,
            this.props.token
        )

        if (result && result.employee_name) {
            this.employeeData = result;
            this.prepareAdditionalInfo(this.employeeData.id, null, 'barcode');
        } else {
            this.displayNotification(_t("No employee corresponding to Badge ID '%(barcode)s.'", {barcode}));
        }

        this.lockScanner = false;
    },

    /**
     * @override
     * add  navigation to the project_attendance screen after result
     */
    async onManualSelection(employeeId, enteredPin) {
        const result = await this.useProjectAttendanceService.onManualSelection(
            this.props.token,
            employeeId,
            enteredPin
        );
        if (result && result.attendance) {
            this.employeeData = result;
            this.prepareAdditionalInfo(employeeId, enteredPin);
        } else {
            if (enteredPin) {
                this.displayNotification(_t("Wrong Pin"))
            }
        }
    },

    /**
     * Handle confirmation of project_attendance screen additional information.
     *
     * This function sends the additional information to an RPC call to update project attendance.
     * If successful, it updates the employee data and switches the display to 'greet'.
     *
     * @param {Object} data - The additional information data to confirm.
     */
    async onAdditionalInfoConfirm(data) {
        const result = await this.useProjectAttendanceService.onAdditionalInfoConfirm(
            this.state.employee_id,
            data,
        );

        if (result && result.attendance) {
            this.employeeData = result;
            this.switchDisplay('greet');
        } else {
            this.displayNotification(_t("Something went wrong!"));
        }
    },

    /**
     * Prepare additional information for project attendance.
     *
     * Sets the employee ID, PIN code, additional information, checked-in status,
     * and kiosk mode based on the provided parameters. Then switches the display
     * to 'project_attendance'.
     *
     * @param {string} employeeId - The ID of the employee.
     * @param {string} enteredPin - The entered PIN code.
     * @param {string} kioskMode - The mode of the kiosk (default is 'manual').
     */
    prepareAdditionalInfo(employeeId, enteredPin, kioskMode = 'manual') {
        this.state.employee_id = employeeId;
        this.state.pin_code = enteredPin;
        this.state.additionalInfo = this.employeeData?.ongoing_attendance || null;
        this.state.checkedIn = this.employeeData?.attendance_state === 'checked_in';
        this.state.kiosk_mode = kioskMode;
        this.switchDisplay('project_attendance');
    }
});

kiosk.kioskAttendanceApp.components = {
    ...kiosk.kioskAttendanceApp.components,
    KioskProjectAttendance
};
