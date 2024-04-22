/** @odoo-module */
import { useService } from "@web/core/utils/hooks";
import { useState } from "@odoo/owl";

export function useProjectAttendanceService() {
    return useState(useService("az_project_attendance.projectAttendanceService"));
}