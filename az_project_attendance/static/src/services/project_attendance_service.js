/** @odoo-module */
import {registry} from "@web/core/registry";
import {reactive} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";

const projectAttendanceService = {
        dependencies: ["rpc", "notification"],
        async start(env, {rpc, notification}) {
            function checkAdditionalInfo(args) {
                try {
                    let additional_info = args['additionalInfo'];
                    if (additional_info) {
                        let project_id = additional_info['project_id']
                        let task_id = additional_info['task_id'];
                        if (project_id && task_id) {
                            return true;
                        }
                    }
                    return false;
                } catch (error) {
                    return false;
                }
            }

            async function checkAdditionalInfoNotifyCreate(endpoint, args) {
                if (checkAdditionalInfo(args)) {
                    return await rpc(endpoint, args);
                } else {
                    notification.add(
                        _t("Required fields are missing\n Please select Project and Task to proceed.")
                    );
                }
            }

            async function systrayCheckInOut(args) {
                await checkAdditionalInfoNotifyCreate(
                    "/hr_attendance/systray_check_in_out",
                    args,
                );
            }

            async function getTaskList(projectId) {
                return await rpc("/hr_attendance/task_ids/" + projectId);
            }

            async function onAttendanceBarcodeScanned(barcode, token) {
                return await rpc('attendance_barcode_scanned', {
                    'barcode': barcode,
                    'token': token
                });
            }

            async function onManualSelection(token, employeeId, enteredPin) {
                return await rpc('manual_selection', {
                    'token': token,
                    'employee_id': employeeId,
                    'pin_code': enteredPin
                });
            }

            async function onAdditionalInfoConfirm(employeeId, additionalInfo) {
                return await checkAdditionalInfoNotifyCreate(
                    'project_attendance',
                    {
                        'employee_id': employeeId,
                        'additionalInfo': additionalInfo
                    }
                );
            }

            return {
                // state,
                systrayCheckInOut,
                getTaskList,
                onAttendanceBarcodeScanned,
                onManualSelection,
                onAdditionalInfoConfirm
            };

        }
    }
;

registry.category("services").add("az_project_attendance.projectAttendanceService", projectAttendanceService);