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
from odoo import models, api, fields, _

import logging
import re
import random
import string
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Add a new field to trigger the chart of accounts configuration
    auto_configure_chart_of_accounts = fields.Boolean(
        string='Automatically Configure Chart of Accounts',
        help='Enable this option to automatically configure the chart of accounts when needed.')

    @api.model
    def set_values(self):
        super(ResConfigSettings, self).set_values()

        # Store the value of auto_configure_chart_of_accounts in system parameters
        self.env['ir.config_parameter'].set_param(
            'your_module.auto_configure_chart_of_accounts', self.auto_configure_chart_of_accounts)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()

        # Retrieve the value of auto_configure_chart_of_accounts from system parameters
        auto_configure_chart_of_accounts = self.env['ir.config_parameter'].get_param(
            'your_module.auto_configure_chart_of_accounts', default=False)

        res.update(
            auto_configure_chart_of_accounts=auto_configure_chart_of_accounts,
        )
        return res

class AccountAccount(models.Model):
    _inherit = 'account.account'

    def _get_chart_of_accounts(self, company):
        # Check if the chart of accounts is already configured for the company
        if not company.chart_of_accounts_id:
            # Check if automatic configuration is enabled
            auto_configure_chart_of_accounts = self.env['ir.config_parameter'].get_param(
                'your_module.auto_configure_chart_of_accounts', default=False)

            if auto_configure_chart_of_accounts:
                # Automatically configure the chart of accounts
                self._create_chart_of_accounts(company)

    def _create_chart_of_accounts(self, company):
        # Implement your logic to create the chart of accounts here
        # This could include creating accounts, account types, and setting up the chart structure
        # Ensure that the created accounts are linked to the correct company
        pass

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _create_chart_of_accounts(self, company):
        def clean_code(input_str):
            # Ensure the code contains only alphanumeric characters and dots
            return re.sub(r'[^a-zA-Z0-9.]', '', input_str).lower()

        try:
            # Create chart of account for cash journal
            cash_account_code = self.clean_code(f"{company.id}cash")
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
                'code': self.clean_code(f"{company.id}bank"),
                'account_type': 'asset_cash',
                'company_id': company.id,
            }
            bank_account_id = self.env['account.account'].sudo().create(bank_account_data)
            _logger.info(f"Chart of Account created for {company.name} - Bank Account with ID: {bank_account_id}")

            # Create chart of accounts for Point of Sale Journal
            pos_account_data = {
                'name': f"{company.name}'s Point of Sale Account",
                'code': self.clean_code(f"{company.id}pos"),
                'account_type': 'asset_receivable',
                'company_id': company.id,
            }
            pos_account_id = self.env['account.account'].sudo().create(pos_account_data)
            _logger.info(f"Chart of Account created for {company.name} - Point of Sale Account with ID: {pos_account_id}")

            # Set Fiscal Localization to Pakistan for the new company
            self._set_fiscal_localization(company)

            # Set generic chart of account
            self._install_generic_chart_template(company)

        except Exception as e:
            _logger.warning(f"Company creation failed: {e}")
            _logger.exception(f"Error during chart of accounts creation for company {company.name}")

    def _set_fiscal_localization(self, company):
        try:
            # Set fiscal localization to Pakistan (replace with your actual module name)
            localization_pk = self.env['ir.module.module'].search([('name', '=', 'generic_coa')], limit=1)
            if localization_pk:
                localization_pk.button_install()

            _logger.info(f"Fiscal Localization set to Pakistan for company: {company.name}")

        except Exception as e:
            _logger.exception(f"Error setting fiscal localization for company {company.name}")

    @api.model
    def _install_generic_chart_template(self, company):
        try:
            # Ensure the accounting module is installed (e.g., 'l10n_generic_coa')
            accounting_module_name = 'l10n_generic_coa'
            accounting_module = self.env['ir.module.module'].search([('name', '=', accounting_module_name)], limit=1)
            if accounting_module and accounting_module.state != 'installed':
                accounting_module.sudo().button_immediate_install()

            # Search for a generic chart of accounts template
            chart_template = self.env['account.chart.template'].search([('name', 'ilike', 'generic')], limit=1)
            if chart_template:
                # Apply the chart template to the company
                chart_template.with_context(force_company=company.id).try_loading_for_current_company()

                _logger.info(f"Generic chart of accounts installed for company {company.name}: {chart_template.name}")
            else:
                _logger.warning("No generic chart of accounts template found.")
                raise UserError(
                    _("No suitable chart of accounts template found. Please check the system configuration."))

        except Exception as e:
            _logger.exception(f"Error installing generic chart of accounts for company {company.name}: {e}")
            raise UserError(_("Failed to install chart of accounts. Please contact your system administrator."))

    # Set up journals and payment methods for a company
    def _setup_journals_and_payment_methods(self, company):
        try:
            # Create or find necessary journals (e.g., sales, purchase, cash, bank)
            sale_journal = self._find_or_create_journal(company, 'sale', 'Sale Journal')
            purchase_journal = self._find_or_create_journal(company, 'purchase', 'Purchase Journal')
            cash_journal = self._find_or_create_journal(company, 'cash', 'Cash Journal')
            bank_journal = self._find_or_create_journal(company, 'bank', 'Bank Journal')

            # Set up payment methods for POS and invoicing using these journals
            # This is a simplified setup; adjust as per your business logic
            pos_payment_method = self.env['pos.payment.method'].create({
                'name': 'Cash',
                'is_cash_count': True,
                'cash_journal_id': cash_journal.id,
                'company_id': company.id,
            })

            # Link the payment method to the POS configurations of the company
            for pos_config in self.env['pos.config'].search([('company_id', '=', company.id)]):
                pos_config.write({'payment_method_ids': [(4, pos_payment_method.id)]})

            _logger.info("Journals and payment methods set up for company: {}".format(company.name))

        except Exception as e:
            _logger.exception("Error setting up journals and payment methods: {}".format(e))

    # Helper function to find or create journals
    def _find_or_create_journal(self, company, journal_type, journal_name):
        journal = self.env['account.journal'].search([('company_id', '=', company.id), ('type', '=', journal_type)],
                                                     limit=1)
        if not journal:
            journal = self.env['account.journal'].create({
                'name': journal_name,
                'type': journal_type,
                'company_id': company.id,
                # Add other necessary fields and default accounts as per your accounting setup
            })
        return journal

    # Create and configure Point of Sale (POS) for a company and user
    def _create_pos_for_company(self, company, user):
        pos_name = ''.join(random.choice(string.ascii_letters) for _ in range(8))

        pos_data = {
            'name': f"{pos_name}'s POS",
            'company_id': company.id,
        }
        pos_id = self.env['pos.config'].sudo().create(pos_data)
        _logger.info(f"Point of Sale (POS) created for {company.name} with ID: {pos_id}")

    # Cron job to create POS for a company and user after a delay
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

    # Cron job to switch the company for a user after a delay
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
                    'interval_number': 1,  # Adjust the delay as needed
                    'interval_type': 'minutes',
                    'numbercall': 1,
                    'doall': True,
                    'user_id': user.id,
                })

        except Exception as e:
            _logger.exception(f"Error during company switch for user {user.name}")

    # Create and configure a new company for a user
    def _create_and_configure_company(self, user):
        new_company_name = f"{user.name}'s Company"
        new_company = self.env['res.company'].sudo().create({
            'name': new_company_name,
            'currency_id': self.env.ref('base.PKR').id,  # Adjust currency as needed
        })
        user.write({'company_ids': [(4, new_company.id)], 'company_id': new_company.id})
        _logger.info(f"Company created: {new_company.name}")

        # Install chart of accounts
        self._install_chart_of_accounts(new_company)

        return new_company

    # Override create method to set up a new user
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
