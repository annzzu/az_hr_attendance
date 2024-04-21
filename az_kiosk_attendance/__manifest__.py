# -*- coding: utf-8 -*-
{
    "name": "AZ Kiosk Project attendances",
    "summary": """
        AZ Kiosk Project attendances
    """,
    "description": """
       AZ Kiosk Project attendances
    """,
    "author": "Ana Zurabashvili",
    "category": "Technical",
    "version": "17.0.1.0.0",
    "application": True,
    "installable": True,
    "depends": [
        "hr_attendance",
        "project",
    ],
    "data": [
        "views/hr_attendance_kiosk_templates.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "az_kiosk_attendance/static/src/**/*",
        ],
        'hr_attendance.assets_public_attendance': [
            # Front-end libraries
            ('include', 'web._assets_helpers'),
            ('include', 'web._assets_frontend_helpers'),
            'web/static/lib/jquery/jquery.js',
            'web/static/src/scss/pre_variables.scss',
            'web/static/lib/bootstrap/scss/_variables.scss',
            ('include', 'web._assets_bootstrap_frontend'),
            ('include', 'web._assets_bootstrap_backend'),
            '/web/static/lib/odoo_ui_icons/*',
            '/web/static/lib/bootstrap/scss/_functions.scss',
            '/web/static/lib/bootstrap/scss/_mixins.scss',
            '/web/static/lib/bootstrap/scss/utilities/_api.scss',
            'web/static/src/libs/fontawesome/css/font-awesome.css',
            ('include', 'web._assets_core'),

            # Public Kiosk app and its components
            "hr_attendance/static/src/public_kiosk/**/*",
            "hr_attendance/static/src/hr_attendance.scss",
            'hr_attendance/static/src/components/**/*',
            "web/static/src/views/fields/formatters.js",

            # Barcode reader utils
            "web/static/src/webclient/barcode/barcode_scanner.js",
            "web/static/src/webclient/barcode/barcode_scanner.xml",
            "web/static/src/webclient/barcode/barcode_scanner.scss",
            "web/static/src/webclient/barcode/crop_overlay.js",
            "web/static/src/webclient/webclient_layout.scss",
            "web/static/src/webclient/barcode/crop_overlay.xml",
            "web/static/src/webclient/barcode/crop_overlay.scss",
            "web/static/src/webclient/barcode/ZXingBarcodeDetector.js",
            "barcodes/static/src/components/barcode_scanner.js",
            "barcodes/static/src/components/barcode_scanner.xml",
            "barcodes/static/src/components/barcode_scanner.scss",
            "barcodes/static/src/barcode_service.js",

            # Kanban view mock
            "web/static/src/views/kanban/kanban_controller.scss",
            "web/static/src/search/search_panel/search_panel.scss",
            "web/static/src/search/control_panel/control_panel.scss",

            # Mine Kiosk app and its components
            "az_kiosk_attendance/static/src/public_kiosk/**/*",
            "az_kiosk_attendance/static/src/components/**/*",

        ],
    },
    "license": "OPL-1",
    "support": "anaz.zurabashvili@gmail.com",
}
