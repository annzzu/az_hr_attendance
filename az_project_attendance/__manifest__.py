# -*- coding: utf-8 -*-
{
    "name": "AZ Apexive Project attendances",
    "summary": """
        AZ apexive Project attendances
    """,
    "description": """
       AZ apexive Project attendances
    """,
    "author": "Ana Zurabashvili",
    "category": "Technical",
    "version": "17.0.1.0.0",
    "application": True,
    "installable": True,
    "depends": [
        "web",
        "hr_attendance",
        "project",
        "barcodes"
    ],
    "data": [
        "views/hr_attendance_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "az_project_attendance/static/src/**/*",
        ],

    },
    "license": "OPL-1",
    "support": "anaz.zurabashvili@gmail.com",
}
