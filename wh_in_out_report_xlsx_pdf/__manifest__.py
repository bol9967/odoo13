# -*- coding: utf-8 -*-
{
    'name': "Wh In Out Report Pdf and Xlsx",

    'summary': "This module is used for show the details of the product in and also those product will be out from the stock.",
    'description': """This module is used for show the details of the product in and also those product will be out from the stock.""",
    'author': "Jamshad Khan",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'report_xlsx', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard.xml',
'wizard/stock_detail_wizard.xml',
        'views/stock_detail.xml',

        'reports/reports_action.xml',
        'reports/wh_report_pdf.xml',
    ],
}
