# -*- coding: utf-8 -*-
{
    "name": "AZ Project attendances",
    "summary": """
        AZ Project attendances
        add project, task, description to attendances
    """,
    "author": "Ana Zurabashvili",
    "category": "Technical",
    "version": "17.0.1.0.0",
    "application": True,
    "installable": True,
    "depends": ["hr_attendance", "project"],
    "data": [
        "views/hr_attendance_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "az_project_attendance/static/src/**/*",
        ],
        "hr_attendance.assets_public_attendance": [
            "az_project_attendance/static/src/**/*",
            ("remove", "az_project_attendance/static/src/components/attendance_menu/*"),
        ],
    },
    "license": "LGPL-3",
    "support": "anaz.zurabashvili@gmail.com",
    "images": ["static/description/attendance.png"],
    "description": """
# AZ Project Attendance

<img src="az_project_attendance/static/description/icon.png" width="50" height="50" style="border-radius: 50%;">

![Odoo Version 17](https://img.shields.io/badge/odoo-17%20v-875A7B.svg)

![Icon](az_project_attendance/static/description/attendance.png)

The AZ Project Attendance is a module that extends the functionality of the hr_attendance and project modules in Odoo.
It allows users/employees to record their attendance with additional information such as the project, task, and
description.

# ONLINE AVAILABLE : <a href="https://5dba-46-49-48-30.ngrok-free.app">Odoo Apps</a>

### Credentials:

- User: admin
- Password: admin

## Table of Contents

- [Features](#features)
- [Usage](#usage)
-
    - [Kiosk Mode](#kiosk-mode)
-
    - [Systray](#systray)
-
    - [Form View](#form-view)
- [Support](#support)

## Features

- Allows users to record attendance with additional information: project, task, and description.
- Integrates with the hr_attendance and project modules.
- Works in various modes: form view, systray, and kiosk.

## Usage

### Kiosk Mode

<img src="az_project_attendance/static/description/kiosk_attendance_form_check_in.png" height="200">
<img src="az_project_attendance/static/description/kiosk_attendance_form_check_out.png" height="200">
<img src="az_project_attendance/static/description/kiosk_attendance_result.png" height="200">

<a href="https://youtu.be/8-F3J98MyzY">Pin attendance video</a>
<a href="https://youtu.be/kuhCqAieNDY">Barcode attendance video</a>

[![IMAGE ALT TEXT](http://img.youtube.com/vi/8-F3J98MyzY?si=nQUYyUW5Pv2V9pL-/0.jpg)](http://www.youtube.com/watch?v=8-F3J98MyzY?si=nQUYyUW5Pv2V9pL- "Kiosk Pin Attendance Video")
[![IMAGE ALT TEXT](http://img.youtube.com/vi/kuhCqAieNDY?si=hmuzL4vdgYYEaZaN/0.jpg)](http://www.youtube.com/watch?v=kuhCqAieNDY?si=hmuzL4vdgYYEaZaN "Kiosk Barcode Attendance Video")

In the kiosk mode, users can record their attendance along with the project, task, and description from a public
terminal.

### Systray


<img src="az_project_attendance/static/description/attendance_systray_check_in.png" height="200">
<img src="az_project_attendance/static/description/attendance_systray_check_out.png" height="200">

<a href="https://youtu.be/8-F3J98MyzY">Attendance systray</a>

[![IMAGE ALT TEXT](http://img.youtube.com/vi/IkOsXxIZRaI?si=KsOV3EIYSGIcLJhS/0.jpg)](http://www.youtube.com/watch?v=IkOsXxIZRaI?si=KsOV3EIYSGIcLJhS "Systray Attendance Video")

In the systray mode, users can quickly record their attendance along with the project, task, and description without
having to navigate to a separate page.

### Form View

![GIF](az_project_attendance/static/description/attendance_form.gif)

In the form view, users can record their attendance along with the project, task, and description.

## Support

For any issues or queries, please contact the author at anaz.zurabashvili@gmail.com

<img src="az_project_attendance/static/description/icon.png" width="50" height="50" style="border-radius: 50%;">


    """,
}
