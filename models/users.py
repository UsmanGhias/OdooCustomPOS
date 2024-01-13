#------------------------------------ 15th try (after making journals)------------------------------------
#
# from odoo import models, api, fields
# import logging
# import re
#
#
# _logger = logging.getLogger(__name__)
#
# class ResUsers(models.Model):
#     _inherit = 'res.users'
#
#     # For Creating a new company.
#     @api.model
#     def _cron_switch_company_after_delay(self, user_id, company_id, default_company_id):
#         user = self.browse(user_id)
#         company = self.env['res.company'].browse(company_id)
#         default_company = self.env['res.company'].browse(default_company_id)
#
#         _logger.info(f"_cron_switch_company_after_delay called for user: {user.name}, company: {company.name}")
#
#         try:
#             # Run the switching logic with elevated privileges
#             with self.env.cr.savepoint():
#                 # Create a new company with the user's name
#                 new_company_name = f"{user.name}'s Company"
#                 new_company = self.env['res.company'].sudo().create({
#                     'name': new_company_name,
#                     'currency_id': self.env.ref('base.PKR').id,  # Adjust currency as needed
#                 })
#
#                 # Assign the user to the new company
#                 user.write({'company_ids': [(4, new_company.id, 0)]})
#
#                 # Set the new company as the default company for the user
#                 user.write({'company_id': new_company.id})
#
#                 _logger.info(f"Company switched successfully for user: {user.name}")
#
#                 # Automatically create a chart of accounts for the new company
#                 self._create_chart_of_accounts(user.company_id)
#
#         except Exception as e:
#             _logger.exception(f"Error during company switch for user {user.name}")
#
#     # For Creating a new user and switching the company
#     @api.model
#     def create(self, vals):
#         new_user = super(ResUsers, self).create({**vals, 'company_id': self.env.ref('base.main_company').id})
#
#         # Assign the group ID of 'Access Rights / Administration' to the new user
#         admin_group = self.env.ref('base.group_erp_manager')  # Replace with the actual XML ID
#         new_user.write({'groups_id': [(4, admin_group.id)]})
#
#         # Add the new user to the 'account.group_account_manager' group
#         account_manager_group = self.env.ref('account.group_account_manager')
#         new_user.write({'groups_id': [(4, account_manager_group.id)]})
#
#         # Add the new user to the 'base.group_partner_manager' group
#         extra_right_group = self.env.ref('base.group_partner_manager')
#         new_user.write({'groups_id': [(4, extra_right_group.id)]})
#
#         # Add the new user to the 'stock.group_stock_manager' group
#         inventory_group = self.env.ref('stock.group_stock_manager')
#         new_user.write({'groups_id': [(4, inventory_group.id)]})
#
#         # Schedule a cron job to switch the user's company after 2 minutes
#         self.env['ir.cron'].sudo().create({
#             'name': f"Switch Company for User {new_user.id}",
#             'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
#             'state': 'code',
#             'code': 'model._cron_switch_company_after_delay(%s, %s, %s)' % (new_user.id, new_user.company_id.id, self.env.ref('base.main_company').id),
#             'interval_number': 2,
#             'interval_type': 'minutes',
#             'numbercall': 1,
#             'doall': True,
#             'user_id': new_user.id,  # Pass user ID to cron job
#         })
#         # Automatically resolve company access for the new user
#         self._cron_switch_company_after_delay(new_user.id, new_user.company_id.id, self.env.ref('base.main_company').id)
#
#         return new_user
#
#     # For creating chart of accounts
#     @api.model
#     def _create_chart_of_accounts(self, company):
#         # Function to clean non-alphanumeric characters from a string
#         def clean_code(input_str):
#             return re.sub(r'\W+', '', input_str)
#         try:
#             # Create chart of account for cash journal
#             cash_account_code = clean_code(f"{company.id}_cash")
#             _logger.info(f"Generated Cash Account Code: {cash_account_code}")
#             cash_account_data = {
#                 'name': f"{company.name}'s Cash Account",
#                 'code': cash_account_code,
#                 'account_type': 'asset_cash',
#                 'company_id': company.id,
#             }
#             cash_account_id = self.env['account.account'].sudo().create(cash_account_data)
#             _logger.info(f"Chart of Account created for {company.name} - Cash Account with ID: {cash_account_id}")
#
#             # Create chart of accounts for Bank Journal
#             bank_account_data = {
#                 'name': f"{company.name}'s Bank Account",
#                 'code': clean_code(f"{company.id}_bank"),
#                 'account_type': 'asset_cash',
#                 'company_id': company.id,
#             }
#             bank_account_id = self.env['account.account'].sudo().create(bank_account_data)
#             _logger.info(f"Chart of Account created for {company.name} - Bank Account with ID: {bank_account_id}")
#
#             # Create chart of accounts for Point of Sale Journal
#             pos_account_data = {
#                 'name': f"{company.name}'s Point of Sale Account",
#                 'code': clean_code(f"{company.id}_pos"),
#                 'account_type': 'asset_receivable',
#                 'company_id': company.id,
#             }
#             pos_account_id = self.env['account.account'].sudo().create(pos_account_data)
#             _logger.info(f"Chart of Account created for {company.name} - Point of Sale Account with ID: {pos_account_id}")
#         except Exception as e:
#             _logger.exception(f"Error during chart of accounts creation for company {company.name}")


#-------------------- Second Work ----------------------
# #
# from odoo import models, api, fields
# import logging
# import re
# from psycopg2 import errors
# import random
# import string
#
#
# _logger = logging.getLogger(__name__)
#
# class ResUsers(models.Model):
#     _inherit = 'res.users'
#
#     @api.model
#     def _create_chart_of_accounts(self, company):
#         def clean_code(input_str):
#             return re.sub(r'\W+', '', input_str).lower()
#
#         try:
#             # Create chart of account for cash journal
#             cash_account_code = clean_code(f"{company.id}_cash")
#             _logger.info(f"Generated Cash Account Code: {cash_account_code}")
#             cash_account_data = {
#                 'name': f"{company.name}'s Cash Account",
#                 'code': cash_account_code,
#                 'account_type': 'asset_cash',
#                 'company_id': company.id,
#             }
#             cash_account_id = self.env['account.account'].sudo().create(cash_account_data)
#             _logger.info(f"Chart of Account created for {company.name} - Cash Account with ID: {cash_account_id}")
#
#             # Create chart of accounts for Bank Journal
#             bank_account_data = {
#                 'name': f"{company.name}'s Bank Account",
#                 'code': clean_code(f"{company.id}_bank"),
#                 'account_type': 'asset_cash',
#                 'company_id': company.id,
#             }
#             bank_account_id = self.env['account.account'].sudo().create(bank_account_data)
#             _logger.info(f"Chart of Account created for {company.name} - Bank Account with ID: {bank_account_id}")
#
#             # Create chart of accounts for Point of Sale Journal
#             pos_account_data = {
#                 'name': f"{company.name}'s Point of Sale Account",
#                 'code': clean_code(f"{company.id}_pos"),
#                 'account_type': 'asset_receivable',
#                 'company_id': company.id,
#             }
#             pos_account_id = self.env['account.account'].sudo().create(pos_account_data)
#             _logger.info(f"Chart of Account created for {company.name} - Point of Sale Account with ID: {pos_account_id}")
#
#             # Set Fiscal Localization to Pakistan for the new company
#             self._set_pakistani_accounting(company)
#
#         except Exception as e:
#             _logger.warning(f"Company creation failed: {e}")
#             _logger.exception(f"Error during chart of accounts creation for company {company.name}")
#
#     @api.model
#     def _set_pakistani_accounting(self, company):
#         # Set Fiscal Localization to Pakistan
#         company.chart_template_id = self.env.ref('l10n_pk.pk_chart_template')
#
#     @api.model
#     def _create_pos_for_company(self, company, user):
#         # Generate a random name for the POS configuration
#         pos_name = ''.join(random.choice(string.ascii_letters) for _ in range(8))
#
#         pos_data = {
#             'name': f"{pos_name}'s POS",
#             'company_id': company.id,
#         }
#         pos_id = self.env['pos.config'].sudo().create(pos_data)
#         _logger.info(f"Point of Sale (POS) created for {company.name} with ID: {pos_id}")
#
#     @api.model
#     def _cron_create_pos_after_delay(self, user_id, company_id):
#         user = self.browse(user_id)
#         company = self.env['res.company'].browse(company_id)
#
#         _logger.info(f"_cron_create_pos_after_delay called for user: {user.name}, company: {company.name}")
#
#         try:
#             with self.env.cr.savepoint():
#                 # Create POS for the new company and user
#                 self._create_pos_for_company(company, user)
#
#         except Exception as e:
#             _logger.exception(f"Error during POS creation for user {user.name}")
#
#     @api.model
#     def _cron_switch_company_after_delay(self, user_id, company_id, default_company_id):
#         user = self.browse(user_id)
#         company = self.env['res.company'].browse(company_id)
#
#         _logger.info(f"_cron_switch_company_after_delay called for user: {user.name}, company: {company.name}")
#
#         try:
#             with self.env.cr.savepoint():
#                 new_company_name = f"{user.name}'s Company"
#                 new_company = self.env['res.company'].sudo().create({
#                     'name': new_company_name,
#                     'currency_id': self.env.ref('base.PKR').id,  # Adjust currency as needed
#                 })
#
#                 user.write({'company_ids': [(4, new_company.id, 0)]})
#                 user.write({'company_id': new_company.id})
#
#                 _logger.info(f"Company switched successfully for user: {user.name}")
#
#                 # Create chart of accounts for the new company
#                 self._create_chart_of_accounts(new_company)
#
#                 # Schedule a cron job to create POS for the new company and user after 10 seconds
#                 self.env['ir.cron'].sudo().create({
#                     'name': f"Create POS for User {user.id}",
#                     'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
#                     'state': 'code',
#                     'code': 'model._cron_create_pos_after_delay(%s, %s)' % (user.id, new_company.id),
#                     'interval_number': 10,  # Adjust the delay as needed
#                     'interval_type': 'minutes',
#                     'numbercall': 1,
#                     'doall': True,
#                     'user_id': user.id,
#                 })
#
#         except Exception as e:
#             _logger.exception(f"Error during company switch for user {user.name}")
#
#     @api.model
#     def create(self, vals):
#         new_user = super(ResUsers, self).create({**vals, 'company_id': self.env.ref('base.main_company').id})
#
#         # Assign groups to the new user
#         groups_to_add = [
#             'base.group_erp_manager',
#             'account.group_account_manager',
#             'base.group_partner_manager',
#             'stock.group_stock_manager'
#         ]
#
#         new_user.write({'groups_id': [(4, self.env.ref(group).id) for group in groups_to_add]})
#
#         # Schedule a cron job to switch the user's company after 2 minutes
#         self.env['ir.cron'].sudo().create({
#             'name': f"Switch Company for User {new_user.id}",
#             'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
#             'state': 'code',
#             'code': 'model._cron_switch_company_after_delay(%s, %s, %s)' % (
#                 new_user.id, new_user.company_id.id, self.env.ref('base.main_company').id),
#             'interval_number': 2,
#             'interval_type': 'minutes',
#             'numbercall': 1,
#             'doall': True,
#             'user_id': new_user.id,
#         })
#
#         # Automatically resolve company access for the new user
#         self._cron_switch_company_after_delay(new_user.id, new_user.company_id.id, self.env.ref('base.main_company').id)
#
#         return new_user

# -- Working ---

from odoo import models, api, fields
import logging
import re
import random
import string

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _create_chart_of_accounts(self, company):
        def clean_code(input_str):
            # Ensure the code contains only alphanumeric characters and dots
            return re.sub(r'[^a-zA-Z0-9.]', '', input_str).lower()

        try:
            # Create chart of account for cash journal
            cash_account_code = clean_code(f"{company.id}_cash")
            _logger.info(f"Generated Cash Account Code: {cash_account_code}")
            cash_account_data = {
                'name': f"{company.name}'s Cash Account",
                'code': cash_account_code,
                'account_type': 'asset_cash',
                'company_id': company.id,
            }
            cash_account_id = self.env['account.account'].sudo().create(cash_account_data)
            _logger.info(f"Chart of Account created for {company.name} - Cash Account with ID: {cash_account_id}")

            # Create chart of accounts for Bank Journal
            bank_account_data = {
                'name': f"{company.name}'s Bank Account",
                'code': clean_code(f"{company.id}_bank"),
                'account_type': 'asset_cash',
                'company_id': company.id,
            }
            bank_account_id = self.env['account.account'].sudo().create(bank_account_data)
            _logger.info(f"Chart of Account created for {company.name} - Bank Account with ID: {bank_account_id}")

            # Create chart of accounts for Point of Sale Journal
            pos_account_data = {
                'name': f"{company.name}'s Point of Sale Account",
                'code': clean_code(f"{company.id}_pos"),
                'account_type': 'asset_receivable',
                'company_id': company.id,
            }
            pos_account_id = self.env['account.account'].sudo().create(pos_account_data)
            _logger.info(f"Chart of Account created for {company.name} - Point of Sale Account with ID: {pos_account_id}")

            # Set Fiscal Localization to Pakistan for the new company
            self._set_pakistani_accounting(company)

        except Exception as e:
            _logger.warning(f"Company creation failed: {e}")
            _logger.exception(f"Error during chart of accounts creation for company {company.name}")

    @api.model
    def _set_pakistani_accounting(self, company):
        # Set Fiscal Localization to Pakistan
        company.chart_template_id = self.env.ref('l10n_pk.pk_chart_template')

    @api.model
    def _create_pos_for_company(self, company, user):
        # Generate a random name for the POS configuration
        pos_name = ''.join(random.choice(string.ascii_letters) for _ in range(8))

        pos_data = {
            'name': f"{pos_name}'s POS",
            'company_id': company.id,
        }
        pos_id = self.env['pos.config'].sudo().create(pos_data)
        _logger.info(f"Point of Sale (POS) created for {company.name} with ID: {pos_id}")

    @api.model
    def _cron_create_pos_after_delay(self, user_id, company_id):
        user = self.browse(user_id)
        company = self.env['res.company'].browse(company_id)

        _logger.info(f"Cron create POS after delay called for user: {user.name}, company: {company.name}")

        try:
            with self.env.cr.savepoint():
                # Create POS for the new company and user
                self._create_pos_for_company(company, user)

        except Exception as e:
            _logger.exception(f"Error during POS creation for user {user.name}")

    @api.model
    def _cron_switch_company_after_delay(self, user_id, company_id, default_company_id):
        user = self.browse(user_id)
        company = self.env['res.company'].browse(company_id)

        _logger.info(f"Cron switch company after delay called for user: {user.name}, company: {company.name}")

        try:
            with self.env.cr.savepoint():
                new_company_name = f"{user.name}'s Company"
                new_company = self.env['res.company'].sudo().create({
                    'name': new_company_name,
                    'currency_id': self.env.ref('base.PKR').id,  # Adjust currency as needed
                })

                user.write({'company_ids': [(4, new_company.id, 0)]})
                user.write({'company_id': new_company.id})

                _logger.info(f"Company switched successfully for user: {user.name}")

                # Create chart of accounts for the new company
                self._create_chart_of_accounts(new_company)

                # Schedule a cron job to create POS for the new company and user after 10 seconds
                self.env['ir.cron'].sudo().create({
                    'name': f"Create POS for User {user.id}",
                    'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
                    'state': 'code',
                    'code': 'model._cron_create_pos_after_delay(%s, %s)' % (user.id, new_company.id),
                    'interval_number': 10,  # Adjust the delay as needed
                    'interval_type': 'minutes',
                    'numbercall': 1,
                    'doall': True,
                    'user_id': user.id,
                })

        except Exception as e:
            _logger.exception(f"Error during company switch for user {user.name}")

    @api.model
    def create(self, vals):
        new_user = super(ResUsers, self).create({**vals, 'company_id': self.env.ref('base.main_company').id})

        # Assign groups to the new user
        groups_to_add = [
            'base.group_erp_manager',
            'account.group_account_manager',
            'base.group_partner_manager',
            'stock.group_stock_manager'
        ]

        new_user.write({'groups_id': [(4, self.env.ref(group).id) for group in groups_to_add]})

        # Schedule a cron job to switch the user's company after 2 minutes
        self.env['ir.cron'].sudo().create({
            'name': f"Switch Company for User {new_user.id}",
            'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
            'state': 'code',
            'code': 'model._cron_switch_company_after_delay(%s, %s, %s)' % (
                new_user.id, new_user.company_id.id, self.env.ref('base.main_company').id),
            'interval_number': 2,
            'interval_type': 'minutes',
            'numbercall': 1,
            'doall': True,
            'user_id': new_user.id,
        })

        # Automatically resolve company access for the new user
        self._cron_switch_company_after_delay(new_user.id, new_user.company_id.id, self.env.ref('base.main_company').id)

        return new_user

#
#
# from odoo import models, api, fields
# import logging
# import re
# import random
# import string
#
# _logger = logging.getLogger(__name__)
#
# class ResUsers(models.Model):
#     _inherit = 'res.users'
#
#     @api.model
#     def _create_chart_of_accounts(self, company):
#         def clean_code(input_str):
#             # Ensure the code contains only alphanumeric characters and dots
#             return re.sub(r'[^a-zA-Z0-9.]', '', input_str).lower()
#
#         try:
#             # Create chart of account for cash journal
#             cash_account_code = clean_code(f"{company.id}_cash")
#             _logger.info(f"Generated Cash Account Code: {cash_account_code}")
#             cash_account_data = {
#                 'name': f"{company.name}'s Cash Account",
#                 'code': cash_account_code,
#                 'account_type': 'asset_cash',
#                 'company_id': company.id,
#             }
#             cash_account_id = self.env['account.account'].sudo().create(cash_account_data)
#             _logger.info(f"Chart of Account created for {company.name} - Cash Account with ID: {cash_account_id}")
#
#             # Create chart of accounts for Bank Journal
#             bank_account_data = {
#                 'name': f"{company.name}'s Bank Account",
#                 'code': clean_code(f"{company.id}_bank"),
#                 'account_type': 'asset_cash',
#                 'company_id': company.id,
#             }
#             bank_account_id = self.env['account.account'].sudo().create(bank_account_data)
#             _logger.info(f"Chart of Account created for {company.name} - Bank Account with ID: {bank_account_id}")
#
#             # Create chart of accounts for Point of Sale Journal
#             pos_account_data = {
#                 'name': f"{company.name}'s Point of Sale Account",
#                 'code': clean_code(f"{company.id}_pos"),
#                 'account_type': 'asset_receivable',
#                 'company_id': company.id,
#             }
#             pos_account_id = self.env['account.account'].sudo().create(pos_account_data)
#             _logger.info(f"Chart of Account created for {company.name} - Point of Sale Account with ID: {pos_account_id}")
#
#             # Set Fiscal Localization to a generic chart template if the admin is on the generic chart
#             admin = self.env['res.users'].sudo().search([('id', '=', 1)])  # Assuming admin user has ID 1
#             if admin and admin.company_id.chart_template_id.code == 'l10n_generic_coa':
#                 self._set_generic_accounting(company)
#             else:
#                 self._set_pakistani_accounting(company)
#
#         except Exception as e:
#             _logger.warning(f"Company creation failed: {e}")
#             _logger.exception(f"Error during chart of accounts creation for company {company.name}")
#
#     @api.model
#     def _set_generic_accounting(self, company):
#         # Set Fiscal Localization to a generic chart template
#         company.chart_template_id = self.env.ref('l10n_generic_coa')
#
#
#     @api.model
#     def _cron_switch_company_after_delay(self, user_id, company_id, default_company_id):
#         user = self.browse(user_id)
#         company = self.env['res.company'].browse(company_id)
#
#         _logger.info(f"Cron switch company after delay called for user: {user.name}, company: {company.name}")
#
#         try:
#             with self.env.cr.savepoint():
#                 new_company_name = f"{user.name}'s Company"
#                 new_company = self.env['res.company'].sudo().create({
#                     'name': new_company_name,
#                     'currency_id': self.env.ref('base.PKR').id,  # Adjust currency as needed
#                 })
#
#                 user.write({'company_ids': [(4, new_company.id, 0)]})
#                 user.write({'company_id': new_company.id})
#
#                 _logger.info(f"Company switched successfully for user: {user.name}")
#
#                 # Create chart of accounts and POS for the new company
#                 self._create_chart_of_accounts(new_company)
#                 self._create_pos_for_company(new_company, user)
#
#         except Exception as e:
#             _logger.exception(f"Error during company switch for user {user.name}")
#
#     @api.model
#     def _set_generic_accounting(self, company):
#         # Set Fiscal Localization to a generic chart template
#         company.chart_template_id = self.env.ref('l10n_generic_coa')
#
#     @api.model
#     def _create_pos_for_company(self, company, user):
#         # Generate a random name for the POS configuration
#         pos_name = ''.join(random.choice(string.ascii_letters) for _ in range(8))
#
#         # Create POS configuration
#         pos_data = {
#             'name': f"{pos_name}'s POS",
#             'company_id': company.id,
#         }
#         pos_id = self.env['pos.config'].sudo().create(pos_data)
#         _logger.info(f"Point of Sale (POS) created for {company.name} with ID: {pos_id}")
#
#         # Set company for payment methods associated with the POS
#         payment_methods = self.env['pos.payment.method'].search([('pos_config_id', '=', pos_id.id)])
#         payment_methods.write({'company_id': company.id})
#
#         return pos_id
#
#     @api.model
#     def _cron_create_pos_after_delay(self, user_id, company_id):
#         user = self.browse(user_id)
#         company = self.env['res.company'].browse(company_id)
#
#         _logger.info(f"Cron create POS after delay called for user: {user.name}, company: {company.name}")
#
#         try:
#             with self.env.cr.savepoint():
#                 # Create POS for the new company and user
#                 self._create_pos_for_company(company, user)
#
#         except Exception as e:
#             _logger.exception(f"Error during POS creation for user {user.name}")
#
#     @api.model
#     def _cron_switch_company_after_delay(self, user_id, company_id, default_company_id):
#         user = self.browse(user_id)
#         company = self.env['res.company'].browse(company_id)
#
#         _logger.info(f"Cron switch company after delay called for user: {user.name}, company: {company.name}")
#
#         try:
#             with self.env.cr.savepoint():
#                 new_company_name = f"{user.name}'s Company"
#                 new_company = self.env['res.company'].sudo().create({
#                     'name': new_company_name,
#                     'currency_id': self.env.ref('base.PKR').id,  # Adjust currency as needed
#                 })
#
#                 user.write({'company_ids': [(4, new_company.id, 0)]})
#                 user.write({'company_id': new_company.id})
#
#                 _logger.info(f"Company switched successfully for user: {user.name}")
#
#                 # Create chart of accounts for the new company
#                 self._create_chart_of_accounts(new_company)
#
#                 # Schedule a cron job to create POS for the new company and user after 10 seconds
#                 self.env['ir.cron'].sudo().create({
#                     'name': f"Create POS for User {user.id}",
#                     'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
#                     'state': 'code',
#                     'code': 'model._cron_create_pos_after_delay(%s, %s)' % (user.id, new_company.id),
#                     'interval_number': 10,  # Adjust the delay as needed
#                     'interval_type': 'minutes',
#                     'numbercall': 1,
#                     'doall': True,
#                     'user_id': user.id,
#                 })
#
#         except Exception as e:
#             _logger.exception(f"Error during company switch for user {user.name}")
#
#     @api.model
#     def create(self, vals):
#         new_user = super(ResUsers, self).create({**vals, 'company_id': self.env.ref('base.main_company').id})
#
#         # Assign groups to the new user
#         groups_to_add = [
#             'base.group_erp_manager',
#             'account.group_account_manager',
#             'base.group_partner_manager',
#             'stock.group_stock_manager'
#         ]
#
#         new_user.write({'groups_id': [(4, self.env.ref(group).id) for group in groups_to_add]})
#
#         # Schedule a cron job to switch the user's company after 2 minutes
#         self.env['ir.cron'].sudo().create({
#             'name': f"Switch Company for User {new_user.id}",
#             'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
#             'state': 'code',
#             'code': 'model._cron_switch_company_after_delay(%s, %s, %s)' % (
#                 new_user.id, new_user.company_id.id, self.env.ref('base.main_company').id),
#             'interval_number': 2,
#             'interval_type': 'minutes',
#             'numbercall': 1,
#             'doall': True,
#             'user_id': new_user.id,
#         })
#
#         # Automatically resolve company access for the new user
#         self._cron_switch_company_after_delay(new_user.id, new_user.company_id.id, self.env.ref('base.main_company').id)
#
#         return new_user

#-- Next Working -------------


    @api.model
    def create(self, vals):
        new_user = super(ResUsers, self).create({**vals, 'company_id': self.env.ref('base.main_company').id})

        # Assign groups to the new user
        groups_to_add = [
            'base.group_erp_manager',
            'account.group_account_manager',
            'base.group_partner_manager',
            'stock.group_stock_manager'
        ]

        new_user.write({'groups_id': [(4, self.env.ref(group).id) for group in groups_to_add]})

        # Schedule a cron job to switch the user's company after 2 minutes
        self.env['ir.cron'].sudo().create({
            'name': f"Switch Company for User {new_user.id}",
            'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
            'state': 'code',
            'code': 'model._cron_switch_company_after_delay(%s, %s, %s)' % (
                new_user.id, new_user.company_id.id, self.env.ref('base.main_company').id),
            'interval_number': 2,
            'interval_type': 'minutes',
            'numbercall': 1,
            'doall': True,
            'user_id': new_user.id,
        })

        # Automatically resolve company access for the new user
        self._cron_switch_company_after_delay(new_user.id, new_user.company_id.id, self.env.ref('base.main_company').id)

        # Create chart of accounts for the new user's company
        self._create_chart_of_accounts(new_user.company_id)

        # Schedule a cron job to create POS for the new user's company after 10 seconds
        self.env['ir.cron'].sudo().create({
            'name': f"Create POS for User {new_user.id}",
            'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
            'state': 'code',
            'code': 'model._cron_create_pos_after_delay(%s, %s)' % (new_user.id, new_user.company_id.id),
            'interval_number': 10,  # Adjust the delay as needed
            'interval_type': 'minutes',
            'numbercall': 1,
            'doall': True,
            'user_id': new_user.id,
        })

        return new_user