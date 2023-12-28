{
    'name': 'Custom POS Access',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Custom module to restrict users to the Point of Sale module',
    'description': """
        This module customizes the login process and restricts users to the Point of Sale module.
    """,
    'author': 'Junaid Alam',
    'website': 'www.telenoc.org',
    'depends': ['point_of_sale', 'hr', 'base', 'account'],
    'data':[
        'security/ir.model.access.csv',
        'views/res_users.xml',
        'views/my_company.xml',
    ],
    'data':[
        'views/account_account_views.xml',
    ],
    'installable': True,
    'auto_install': True,
}