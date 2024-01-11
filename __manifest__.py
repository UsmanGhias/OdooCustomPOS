{
    'name': 'New Company access',
    'version': '1.0',
    'summary': 'Custom module to restrict users to the Point of Sale module',
    'description': """
        This module customizes the login process and restricts users to the Point of Sale module.
    """,
    'author': 'Usman Ghias',
    'website': 'www.telenoc.org',
    'depends': ['point_of_sale', 'hr', 'base', 'account', 'account_accountant'],
    'installable': True,
    'application': True,
}