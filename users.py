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


#------------------------------ Stop -------------------------------------



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

    #
    # @api.model
    # def create(self, vals):
    #     new_user = super(ResUsers, self).create({**vals, 'company_id': self.env.ref('base.main_company').id})
    #
    #     # Assign groups to the new user
    #     groups_to_add = [
    #         'base.group_erp_manager',
    #         'account.group_account_manager',
    #         'base.group_partner_manager',
    #         'stock.group_stock_manager'
    #     ]
    #
    #     new_user.write({'groups_id': [(4, self.env.ref(group).id) for group in groups_to_add]})
    #
    #     # Schedule a cron job to switch the user's company after 2 minutes
    #     self.env['ir.cron'].sudo().create({
    #         'name': f"Switch Company for User {new_user.id}",
    #         'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
    #         'state': 'code',
    #         'code': 'model._cron_switch_company_after_delay(%s, %s, %s)' % (
    #             new_user.id, new_user.company_id.id, self.env.ref('base.main_company').id),
    #         'interval_number': 2,
    #         'interval_type': 'minutes',
    #         'numbercall': 1,
    #         'doall': True,
    #         'user_id': new_user.id,
    #     })
    #
    #     # Automatically resolve company access for the new user
    #     self._cron_switch_company_after_delay(new_user.id, new_user.company_id.id, self.env.ref('base.main_company').id)
    #
    #     # Create chart of accounts for the new user's company
    #     self._create_chart_of_accounts(new_user.company_id)
    #
    #     # Schedule a cron job to create POS for the new user's company after 10 seconds
    #     self.env['ir.cron'].sudo().create({
    #         'name': f"Create POS for User {new_user.id}",
    #         'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
    #         'state': 'code',
    #         'code': 'model._cron_create_pos_after_delay(%s, %s)' % (new_user.id, new_user.company_id.id),
    #         'interval_number': 10,  # Adjust the delay as needed
    #         'interval_type': 'minutes',
    #         'numbercall': 1,
    #         'doall': True,
    #         'user_id': new_user.id,
    #     })
    #
    #     return new_user


    #-------------------------Fiscal Account Working -------------------
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
#             return re.sub(r'[^a-zA-Z0-9.]', '', input_str).lower()
#
#         try:
#
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
#             self._set_fiscal_localization(company)
#
#             # Set generic chart of Accounts
#             self._set_generic_chart_of_accounts(company)
#
#             # Create and configure chart of accounts for the new POS
#             self._create_chart_of_accounts_for_pos(company, pos_account_id)
#
#         except Exception as e:
#             _logger.warning(f"Company creation failed: {e}")
#             _logger.exception(f"Error during chart of accounts creation for company {company.name}")
#
#     @api.model
#     def _set_fiscal_localization(self, company):
#         try:
#             localization_pk = self.env['ir.module.module'].search([('name', '=', 'l10n_pk')], limit=1)
#             if localization_pk and not localization_pk.state == 'installed':
#                 localization_pk.button_install()
#
#             _logger.info(f"Fiscal Localization set to Pakistan for company: {company.name}")
#
#         except Exception as e:
#             _logger.exception(f"Error setting fiscal localization for company {company.name}")
#
#     @api.model
#     def _create_pos_for_company(self, company, user):
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
#         _logger.info(f"Cron create POS after delay called for user: {user.name}, company: {company.name}")
#
#         try:
#             with self.env.cr.savepoint():
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
#                     'currency_id': self.env.ref('base.PKR').id,
#                 })
#
#                 user.write({'company_ids': [(4, new_company.id, 0)]})
#                 user.write({'company_id': new_company.id})
#
#                 _logger.info(f"Company switched successfully for user: {user.name}")
#
#                 self._create_chart_of_accounts(new_company)
#
#                 self.env['ir.cron'].sudo().create({
#                     'name': f"Create POS for User {user.id}",
#                     'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
#                     'state': 'code',
#                     'code': 'model._cron_create_pos_after_delay(%s, %s)' % (user.id, new_company.id),
#                     'interval_number': 1,
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
#     def _create_chart_of_accounts_for_pos(self, company, pos_account_id):
#         try:
#             # Replace this logic with your actual chart of accounts creation for the POS
#             # You might need to adapt it based on your specific requirements
#             chart_of_accounts_data = {
#                 'name': f"{company.name}'s POS Chart of Accounts",
#                 'code': f"{company.id}_pos_chart",
#                 'account_type': 'asset_receivable',  # Adjust the account type as needed
#                 'company_id': company.id,
#             }
#             chart_of_accounts_id = self.env['account.account'].sudo().create(chart_of_accounts_data)
#             _logger.info(f"Chart of Accounts created for {company.name}'s POS with ID: {chart_of_accounts_id}")
#
#             # Associate the chart of accounts with the POS
#             pos = self.env['pos.config'].browse(pos_account_id)
#             pos.write({'chart_of_accounts_id': chart_of_accounts_id.id})
#
#             _logger.info(f"POS {pos.name} configured with Chart of Accounts {chart_of_accounts_id.name}")
#
#         except Exception as e:
#             _logger.exception(f"Error during chart of accounts creation for POS {pos_account_id}")
#
#     @api.model
#     def create(self, vals):
#         new_user = super(ResUsers, self).create({**vals, 'company_id': self.env.ref('base.main_company').id})
#
#         groups_to_add = [
#             'base.group_erp_manager',
#             'account.group_account_manager',
#             'base.group_partner_manager',
#             'stock.group_stock_manager'
#         ]
#
#         new_user.write({'groups_id': [(4, self.env.ref(group).id) for group in groups_to_add]})
#
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
#         self._cron_switch_company_after_delay(new_user.id, new_user.company_id.id, self.env.ref('base.main_company').id)
#
#         return new_user
#

# ----------------------------------------New Code --------------------------------------------
#
# from odoo import models, api, fields, _
# import logging
# import re
# import random
# import string
# from odoo.exceptions import UserError
#
# _logger = logging.getLogger(__name__)
#
# class ResConfigSettings(models.TransientModel):
#     _inherit = 'res.config.settings'
#
#     auto_configure_chart_of_accounts = fields.Boolean(
#         string='Automatically Configure Chart of Accounts',
#         help='Enable this option to automatically configure the chart of accounts when needed.')
#
#     @api.model
#     def set_values(self):
#         super(ResConfigSettings, self).set_values()
#         self.env['ir.config_parameter'].set_param(
#             'company.auto_configure_chart_of_accounts', self.auto_configure_chart_of_accounts)
#
#     @api.model
#     def get_values(self):
#         res = super(ResConfigSettings, self).get_values()
#         auto_configure_chart_of_accounts = self.env['ir.config_parameter'].get_param(
#             'company.auto_configure_chart_of_accounts', default=False)
#         res.update(auto_configure_chart_of_accounts=auto_configure_chart_of_accounts,)
#         return res
#
# class AccountAccount(models.Model):
#     _inherit = 'account.account'
#
#         @api.model
#         def _create_chart_of_accounts(self, company):
#             def clean_code(input_str):
#                 return re.sub(r'[^a-zA-Z0-9.]', '', input_str).lower()
#
#             try:
#                 cash_account_code = clean_code(f"{company.id}cash")
#                 _logger.info(f"Generated Cash Account Code: {cash_account_code}")
#                 cash_account_data = {
#                     'name': f"{company.name}'s Cash Account",
#                     'code': cash_account_code,
#                     'account_type': 'asset_cash',
#                     'company_id': company.id,
#                 }
#                 cash_account_id = self.env['account.account'].sudo().create(cash_account_data)
#                 _logger.info(f"Chart of Account created for {company.name} - Cash Account with ID: {cash_account_id}")
#
#                 bank_account_data = {
#                     'name': f"{company.name}'s Bank Account",
#                     'code': clean_code(f"{company.id}bank"),
#                     'account_type': 'asset_cash',
#                     'company_id': company.id,
#                 }
#                 bank_account_id = self.env['account.account'].sudo().create(bank_account_data)
#                 _logger.info(f"Chart of Account created for {company.name} - Bank Account with ID: {bank_account_id}")
#
#                 pos_account_data = {
#                     'name': f"{company.name}'s Point of Sale Account",
#                     'code': clean_code(f"{company.id}pos"),
#                     'account_type': 'asset_receivable',
#                     'company_id': company.id,
#                 }
#                 pos_account_id = self.env['account.account'].sudo().create(pos_account_data)
#                 _logger.info(
#                     f"Chart of Account created for {company.name} - Point of Sale Account with ID: {pos_account_id}")
#
#                 self._set_fiscal_localization(company)
#                 self._install_generic_chart_template(company)
#
#             except Exception as e:
#                 _logger.warning(f"Company creation failed: {e}")
#                 _logger.exception(f"Error during chart of accounts creation for company {company.name}")
#
#     def _get_chart_of_accounts(self, company):
#         if not company.chart_of_accounts_id:
#             auto_configure_chart_of_accounts = self.env['ir.config_parameter'].get_param(
#                 'company.auto_configure_chart_of_accounts', default=False)
#
#             if auto_configure_chart_of_accounts:
#                 self._create_chart_of_accounts(company)
#
# class ResUsers(models.Model):
#     _inherit = 'res.users'
#
#     def _set_fiscal_localization(self, company):
#         try:
#             localization_pk = self.env['ir.module.module'].search([('name', '=', 'generic_coa')], limit=1)
#             if localization_pk:
#                 localization_pk.button_install()
#
#             _logger.info(f"Fiscal Localization set to Pakistan for company: {company.name}")
#
#         except Exception as e:
#             _logger.exception(f"Error setting fiscal localization for company {company.name}")
#
#     @api.model
#     def _install_generic_chart_template(self, company):
#         try:
#             accounting_module_name = 'l10n_generic_coa'
#             accounting_module = self.env['ir.module.module'].search([('name', '=', accounting_module_name)], limit=1)
#             if accounting_module and accounting_module.state != 'installed':
#                 accounting_module.sudo().button_immediate_install()
#
#             chart_template = self.env['account.chart.template'].search([('name', 'ilike', 'generic')], limit=1)
#             if chart_template:
#                 chart_template.with_context(force_company=company.id).try_loading_for_current_company()
#                 _logger.info(f"Generic chart of accounts installed for company {company.name}: {chart_template.name}")
#             else:
#                 _logger.warning("No generic chart of accounts template found.")
#                 raise UserError(_("No suitable chart of accounts template found. Please check the system configuration."))
#
#         except Exception as e:
#             _logger.exception(f"Error installing generic chart of accounts for company {company.name}: {e}")
#             raise UserError(_("Failed to install chart of accounts. Please contact your system administrator."))
#
#     def _setup_journals_and_payment_methods(self, company):
#         try:
#             sale_journal = self._find_or_create_journal(company, 'sale', 'Sale Journal')
#             purchase_journal = self._find_or_create_journal(company, 'purchase', 'Purchase Journal')
#             cash_journal = self._find_or_create_journal(company, 'cash', 'Cash Journal')
#             bank_journal = self._find_or_create_journal(company, 'bank', 'Bank Journal')
#
#             pos_payment_method = self.env['pos.payment.method'].create({
#                 'name': 'Cash',
#                 'is_cash_count': True,
#                 'company_id': company.id,
#             })
#
#             for pos_config in self.env['pos.config'].search([('company_id', '=', company.id)]):
#                 pos_config.write({'payment_method_ids': [(4, pos_payment_method.id)]})
#
#             _logger.info("Journals and payment methods set up for company: {}".format(company.name))
#
#         except Exception as e:
#             _logger.exception("Error setting up journals and payment methods: {}".format(e))
#
#     def _find_or_create_journal(self, company, journal_type, journal_name):
#         journal_code = f"{company.id}_{journal_type}"
#         journal = self.env['account.journal'].search([('company_id', '=', company.id), ('type', '=', journal_type)], limit=1)
#         if not journal:
#             journal = self.env['account.journal'].create({
#                 'name': journal_name,
#                 'code': journal_code,
#                 'type': journal_type,
#                 'company_id': company.id,
#             })
#         return journal
#
#     def _create_pos_for_company(self, company, user):
#         pos_name = ''.join(random.choice(string.ascii_letters) for _ in range(8))
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
#         _logger.info(f"Cron create POS after delay called for user: {user.name}, company: {company.name}")
#
#         try:
#             with self.env.cr.savepoint():
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
#                     'currency_id': self.env.ref('base.PKR').id,
#                 })
#
#                 user.write({'company_ids': [(4, new_company.id, 0)]})
#                 user.write({'company_id': new_company.id})
#
#                 _logger.info(f"Company switched successfully for user: {user.name}")
#
#                 self._create_chart_of_accounts(new_company)
#
#                 self.env['ir.cron'].sudo().create({
#                     'name': f"Create POS for User {user.id}",
#                     'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
#                     'state': 'code',
#                     'code': 'model._cron_create_pos_after_delay(%s, %s)' % (user.id, new_company.id),
#                     'interval_number': 1,
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
#         groups_to_add = [
#             'base.group_erp_manager',
#             'account.group_account_manager',
#             'base.group_partner_manager',
#             'stock.group_stock_manager'
#         ]
#
#         new_user.write({'groups_id': [(4, self.env.ref(group).id) for group in groups_to_add]})
#
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
#         self._cron_switch_company_after_delay(new_user.id, new_user.company_id.id, self.env.ref('base.main_company').id)
#         self._create_chart_of_accounts(new_user.company_id)
#         self._setup_journals_and_payment_methods(new_user.company_id)
#         self._create_pos_for_company(new_user.company_id, new_user)
#
#         return new_user

# ------------------------------- New Work --------------------------------
#
# from odoo import models, api, fields
# import logging
# import time
#
# _logger = logging.getLogger(__name__)
#
# class ResUsers(models.Model):
#     _inherit = 'res.users'
#
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
#
#                 _logger.info(f"Company switched successfully for user: {user.name}")
#
#                 self._install_generic_chart_template(new_company)
#
#         except Exception as e:
#             _logger.exception(f"Error during company switch for user {user.name}")
#
#     @api.model
#     def create(self, vals):
#         new_user = super(ResUsers, self).create({**vals, 'company_id': self.env.ref('base.main_company').id})
#
#         # Assign the group ID of 'Access Rights / Administration' to the new user
#         admin_group = self.env.ref('base.group_erp_manager')
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
#
#         # Automatically resolve company access for the new user
#         self._cron_switch_company_after_delay(new_user.id, new_user.company_id.id, self.env.ref('base.main_company').id)
#
#         # Set the default view for the user
#         pos_action = self.env.ref('point_of_sale.action_pos_config_kanban')
#         if pos_action:
#             new_user.write({'action_id': pos_action.id})
#         else:
#             _logger.warning("Point of Sale action not found")
#
#         # Duplicate View
#         # duplicate_pos_action = self.env.ref('point_of_sale.action_pos_config_duplicate')
#         # if duplicate_pos_action:
#         #     new_user.write({'action_id': duplicate_pos_action.id})
#         # else:
#         #     _logger.warning("Duplicate POS Home action not found")
#         #
#
#         self.env['ir.cron'].sudo().create({
#             'name': 'Set POS Access for User %s' % new_user.id,
#             'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
#             'state': 'code',
#             'code': 'model.set_pos_access(%s)' % new_user.id,
#             'interval_number': 2,
#             'interval_type': 'minutes',
#             'numbercall': 1,
#             'active': True,
#         })
#
#         def set_pos_access(self, user_id):
#             user = self.sudo().browse(user_id)
#             pos_group = self.env.ref('point_of_sale.group_pos_user').sudo()
#             user.sudo().write({'groups_id': [(4, pos_group.id)]})
#
#         return new_user
#
#     @api.model
#     def _install_generic_chart_template(cls, company):
#         try:
#             # Check if the company already has a chart of accounts installed
#             if not company.chart_template:
#                 # Get the data for the generic chart template
#                 chart_template_data = cls.env['account.chart.template'].sudo()._get_generic_coa_template_data()
#
#                 # first try with try_loading
#                 cls.env['account.chart.template'].sudo().try_loading('generic_coa', company, True)
#                 # Load the chart template for the new company
#                 # cls.env['account.chart.template'].sudo()._load(company, False, chart_template_data)
#
#                 # Additional logic to handle the chart template installation
#
#                 time.sleep(5)
#
#                 # Query installed journals
#                 installed_journals = cls.env['account.journal'].search([('company_id', '=', company.id)])
#
#                 # Print the names of installed journals
#                 for journal in installed_journals:
#                     _logger.info(f"Journal Name: {journal.name}")
#
#         except Exception as e:
#             _logger.exception(f"Error installing generic chart of accounts for company {company.name}")

#-------------------------------------Latest Code -----------------------------
#
# from odoo import models, api, fields
# import logging
# import time
#
# _logger = logging.getLogger(__name__)
#
# class ResUsers(models.Model):
#     _inherit = 'res.users'
#
# #   pos_dashboard_id = fields.Many2one('custom.pos.dashboard', string='POS Dashboard')
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
#
#                 _logger.info(f"Company switched successfully for user: {user.name}")
#
#                 self._install_generic_chart_template(new_company)
#
#         except Exception as e:
#             _logger.exception(f"Error during company switch for user {user.name}")
#
#     @api.model
#     def restrict_pos_access_only(self, user_id):
#         user = self.env['res.users'].browse(user_id)
#         pos_group = self.env.ref('point_of_sale.group_pos_user')
#         all_access_groups = self.env.ref('base.group_user')  # This is an example, adjust as necessary
#
#         # Remove the user from general access groups
#         user.sudo().write({'groups_id': [(3, all_access_groups.id)]})
#
#         # Add the user exclusively to the POS access group
#         user.sudo().write({'groups_id': [(4, pos_group.id)]})
#
#         _logger.info(f"Access restricted to POS only for user: {user.name}")
#
#
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
#
#         # Automatically resolve company access for the new user
#         self._cron_switch_company_after_delay(new_user.id, new_user.company_id.id, self.env.ref('base.main_company').id)
#
#         # Set the default view for the user
#         pos_config_view = self.env.ref('point_of_sale.action_pos_config_kanban')
#         new_user.write({'action_id': pos_config_view.id})
#
#         # Schedule to remove the user from ERP Manager group after 5 minutes
#         self.env['ir.cron'].sudo().create({
#             'name': f"Remove ERP Manager Access - {new_user.name}",
#             'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
#             'state': 'code',
#             'code': f"model.remove_user_from_erp_manager_group({new_user.id})",
#             'interval_number': 5,
#             'interval_type': 'minutes',
#             'numbercall': 1,
#             'doall': False,
#             'active': True,
#         })
#
#
#         # ------------------- Additional -----------------------
#         @api.model
#         def restrict_pos_access_only(self, user_id):
#             user = self.env['res.users'].browse(user_id)
#             pos_group = self.env.ref('point_of_sale.group_pos_user')
#             all_access_groups = self.env.ref('base.group_user')  # This is an example, adjust as necessary
#
#             # Remove the user from general access groups
#             user.sudo().write({'groups_id': [(3, all_access_groups.id)]})
#
#             # Add the user exclusively to the POS access group
#             user.sudo().write({'groups_id': [(4, pos_group.id)]})
#
#             _logger.info(f"Access restricted to POS only for user: {user.name}")
#
#         return new_user
#
#         @api.model
#         def remove_user_from_erp_manager_group(self, user_id):
#             """Removes the user from the ERP Manager group."""
#             user = self.browse(user_id)
#             erp_manager_group = self.env.ref('base.group_erp_manager')
#             user.sudo().write({'groups_id': [(3, erp_manager_group.id)]})
#             _logger.info(f"ERP Manager access removed for user: {user.name}")
#
#     @api.model
#     def _install_generic_chart_template(cls, company):
#         try:
#             # Check if the company already has a chart of accounts installed
#             if not company.chart_template:
#                 # Get the data for the generic chart template
#                 chart_template_data = cls.env['account.chart.template'].sudo()._get_generic_coa_template_data()
#
#                 # first try with try_loading
#                 cls.env['account.chart.template'].sudo().try_loading('generic_coa', company, True)
#                 # Load the chart template for the new company
#                 # cls.env['account.chart.template'].sudo()._load(company, False, chart_template_data)
#
#                 # Additional logic to handle the chart template installation
#
#                 time.sleep(5)
#
#                 # Query installed journals
#                 installed_journals = cls.env['account.journal'].search([('company_id', '=', company.id)])
#
#                 # Print the names of installed journals
#                 for journal in installed_journals:
#                     _logger.info(f"Journal Name: {journal.name}")
#
#         except Exception as e:
#             _logger.exception(f"Error installing generic chart of accounts for company {company.name}")
#

#-----------------------------------------


#
#
# from odoo import models, api, fields
# import logging
# import time
#
# _logger = logging.getLogger(__name__)
#
# class ResUsers(models.Model):
#     _inherit = 'res.users'
#
#     @api.model
#     def _grant_and_revoke_access_rights(self, user_id, required_group_ids):
#         user = self.browse(user_id)
#
#         # Grant the user the required access rights
#         user.write({'groups_id': [(4, group_id) for group_id in required_group_ids]})
#
#         # Perform the operations that require the access rights here
#         try:
#             # Your code logic here
#
#         except Exception as e:
#             _logger.exception(f"Error during operations with access rights for user {user.name}")
#
#         # Revoke the access rights once the operations are completed
#         user.write({'groups_id': [(3, group_id) for group_id in required_group_ids]})
#
#     @api.model
#     def create(self, vals):
#         new_user = super(ResUsers, self).create({**vals, 'company_id': self.env.ref('base.main_company').id})
#
#         # Define the group IDs that the user will temporarily have
#         required_group_ids = [self.env.ref('base.group_erp_manager').id,
#                               self.env.ref('account.group_account_manager').id,
#                               self.env.ref('base.group_partner_manager').id,
#                               self.env.ref('stock.group_stock_manager').id]
#
#         # Grant and revoke access rights as needed
#         self._grant_and_revoke_access_rights(new_user.id, required_group_ids)
#
#         # Schedule a cron job to remove the user from ERP Manager group after 5 minutes
#         self.env['ir.cron'].sudo().create({
#             'name': f"Remove ERP Manager Access - {new_user.name}",
#             'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
#             'state': 'code',
#             'code': f"model.remove_user_from_erp_manager_group({new_user.id})",
#             'interval_number': 5,
#             'interval_type': 'minutes',
#             'numbercall': 1,
#             'doall': False,
#             'active': True,
#         })
#
#         # Set the default view for the user
#         pos_config_view = self.env.ref('point_of_sale.action_pos_config_kanban')
#         new_user.write({'action_id': pos_config_view.id})
#
#         return new_user
#
#         # Schedule to remove the user from ERP Manager group after 5 minutes
#         self.env['ir.cron'].sudo().create({
#             'name': f"Remove ERP Manager Access - {new_user.name}",
#             'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
#             'state': 'code',
#             'code': f"model.remove_user_from_erp_manager_group({new_user.id})",
#             'interval_number': 5,
#             'interval_type': 'minutes',
#             'numbercall': 1,
#             'doall': False,
#             'active': True,
#         })
#
#
#         # ------------------- Additional -----------------------
#         @api.model
#         def restrict_pos_access_only(self, user_id):
#             user = self.env['res.users'].browse(user_id)
#             pos_group = self.env.ref('point_of_sale.group_pos_user')
#             all_access_groups = self.env.ref('base.group_user')  # This is an example, adjust as necessary
#
#             # Remove the user from general access groups
#             user.sudo().write({'groups_id': [(3, all_access_groups.id)]})
#
#             # Add the user exclusively to the POS access group
#             user.sudo().write({'groups_id': [(4, pos_group.id)]})
#
#             _logger.info(f"Access restricted to POS only for user: {user.name}")
#
#         return new_user
#
#         @api.model
#         def remove_user_from_erp_manager_group(self, user_id):
#             """Removes the user from the ERP Manager group."""
#             user = self.browse(user_id)
#             erp_manager_group = self.env.ref('base.group_erp_manager')
#             user.sudo().write({'groups_id': [(3, erp_manager_group.id)]})
#             _logger.info(f"ERP Manager access removed for user: {user.name}")
#
#     @api.model
#     def _install_generic_chart_template(cls, company):
#         try:
#             # Check if the company already has a chart of accounts installed
#             if not company.chart_template:
#                 # Get the data for the generic chart template
#                 chart_template_data = cls.env['account.chart.template'].sudo()._get_generic_coa_template_data()
#
#                 # first try with try_loading
#                 cls.env['account.chart.template'].sudo().try_loading('generic_coa', company, True)
#                 # Load the chart template for the new company
#                 # cls.env['account.chart.template'].sudo()._load(company, False, chart_template_data)
#
#                 # Additional logic to handle the chart template installation
#
#                 time.sleep(5)
#
#                 # Query installed journals
#                 installed_journals = cls.env['account.journal'].search([('company_id', '=', company.id)])
#
#                 # Print the names of installed journals
#                 for journal in installed_journals:
#                     _logger.info(f"Journal Name: {journal.name}")
#
#         except Exception as e:
#             _logger.exception(f"Error installing generic chart of accounts for company {company.name}")
#


from odoo import models, api, fields
import logging
import time

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _cron_switch_company_after_delay(self, user_id, company_id, default_company_id):
        user = self.browse(user_id)
        company = self.env['res.company'].browse(company_id)
        default_company = self.env['res.company'].browse(default_company_id)

        _logger.info(f"_cron_switch_company_after_delay called for user: {user.name}, company: {company.name}")

        try:
            # Run the switching logic with elevated privileges
            with self.env.cr.savepoint():
                # Create a new company with the user's name
                new_company_name = f"{user.name}'s Company"
                new_company = self.env['res.company'].sudo().create({
                    'name': new_company_name,
                    'currency_id': self.env.ref('base.PKR').id,  # Adjust currency as needed
                })

                # Assign the user to the new company
                user.write({'company_ids': [(4, new_company.id, 0)]})

                # Set the new company as the default company for the user
                user.write({'company_id': new_company.id})


                _logger.info(f"Company switched successfully for user: {user.name}")

                self._install_generic_chart_template(new_company)

        except Exception as e:
            _logger.exception(f"Error during company switch for user {user.name}")

    @api.model
    def create(self, vals):
        new_user = super(ResUsers, self).create({**vals, 'company_id': self.env.ref('base.main_company').id})

        # Assign the group ID of 'Access Rights / Administration' to the new user
        # admin_group = self.env.ref('base.group_erp_manager')  # Replace with the actual XML ID
        # new_user.write({'groups_id': [(4, admin_group.id)]})

        # Add the new user to the 'account.group_account_manager' group
        account_manager_group = self.env.ref('account.group_account_manager')
        new_user.write({'groups_id': [(4, account_manager_group.id)]})

        # Add the new user to the 'base.group_partner_manager' group
        extra_right_group = self.env.ref('base.group_partner_manager')
        new_user.write({'groups_id': [(4, extra_right_group.id)]})

        # Add the new user to the 'stock.group_stock_manager' group
        # inventory_group = self.env.ref('stock.group_stock_manager')
        # new_user.write({'groups_id': [(4, inventory_group.id)]})

        # Set the default view for the user
        pos_config_view = self.env.ref('point_of_sale.action_pos_config_kanban')
        new_user.write({'action_id': pos_config_view.id})

        # Schedule a cron job to switch the user's company after 2 minutes
        self.env['ir.cron'].sudo().create({
            'name': f"Switch Company for User {new_user.id}",
            'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
            'state': 'code',
            'code': 'model._cron_switch_company_after_delay(%s, %s, %s)' % (new_user.id, new_user.company_id.id, self.env.ref('base.main_company').id),
            'interval_number': 2,
            'interval_type': 'minutes',
            'numbercall': 1,
            'doall': True,
            'user_id': new_user.id,  # Pass user ID to cron job
        })

        # Automatically resolve company access for the new user
        self._cron_switch_company_after_delay(new_user.id, new_user.company_id.id, self.env.ref('base.main_company').id)

        return new_user

    @api.model
    def _install_generic_chart_template(cls, company):
        try:
            # Check if the company already has a chart of accounts installed
            if not company.chart_template:
                # Get the data for the generic chart template
                chart_template_data = cls.env['account.chart.template'].sudo()._get_generic_coa_template_data()

                # first try with try_loading
                cls.env['account.chart.template'].sudo().try_loading('generic_coa', company, True)
                # Load the chart template for the new company
                # cls.env['account.chart.template'].sudo()._load(company, False, chart_template_data)

                # Additional logic to handle the chart template installation

                time.sleep(5)

                # Query installed journals
                installed_journals = cls.env['account.journal'].search([('company_id', '=', company.id)])

                # Print the names of installed journals
                for journal in installed_journals:
                    _logger.info(f"Journal Name: {journal.name}")

        except Exception as e:
            _logger.exception(f"Error installing generic chart of accounts for company {company.name}")