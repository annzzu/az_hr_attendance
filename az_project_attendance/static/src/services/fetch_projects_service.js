/** @odoo-module */
import {registry} from "@web/core/registry";
import {reactive} from "@odoo/owl";

const projectService = {
        dependencies: ["rpc"],
        async start(env, {rpc}) {
            let projectsDict = await rpc("/hr_attendance/project_ids");
            const state = reactive({projectsDict: projectsDict});

            async function getTasksDict(projectId) {
                return await rpc("/hr_attendance/task_ids/" + projectId);
            }

            return {
                state,
                getTasksDict,
            };

        }
    }
;

registry.category("services").add("az_project_attendance.projectService", projectService);