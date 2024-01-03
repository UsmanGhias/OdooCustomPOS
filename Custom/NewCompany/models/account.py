# # from odoo import models, fields, api, _
# # class Account(models.Model):
# #     _inherit = 'account.account'
# #     @api.model
# #     def create(self, vals):
# #         # print('Create method is called')
# #
# #         # Generate a unique company name
# #         company_name = self._generate_unique_company_name()
# #         # Create the new company
# #         company = self.env['res.company'].sudo().create({'name': company_name})
# #         # Create a new POS system for the company
# #
# #         pos_config = self.env['pos.config'].sudo().create({
# #             'name': f'POS for {company_name}',
# #             'company_id': company.id,
# #             # Add other POS configuration fields as needed
# #         })
# #         # Call the original create method
# #         res = super().create(vals)
# #         return res
# #
# #     def _generate_unique_company_name(self):
# #         # Generate a unique company name using a sequence
# #         sequence_code = 'res.company'
# #         # while True:
# #         #     company_number = self.env['ir.sequence'].next_by_code(sequence_code)
# #         #     company_name = f'Company {company_number}' if company_number else 'Company'
# #         #     existing_company = self.env['res.company'].search([('name', '=', company_name)])
# #         #     if not existing_company:
# #         #         break
# #
# #         if not self.env['ir.sequence'].search([('code', '=',  sequence_code)]):
# #             self.env['ir.sequence'].sudo().create({
# #                 'name': 'Company Sequence',
# #                 'code': sequence_code,
# #                 'prefix':  'company',
# #                 'padding': 3
# #             })
# #         company_number = self.env['ir.sequence'].next_by_code(sequence_code) or 1
# #         company_name = f'Company {company_number}'
# #         print(f'Created Company: {company_name}')
# #
# #         return company_name
#
# # ----------------------------- Modified Code -----------------------------
#
# from odoo import models, fields, api
#
# # class ResUsers(models.Model):
# #     _inherit = 'res.users'
# #
# #     department_id = fields.Many2one('hr.department', string='Department')
# #
# #     @api.model
# #     def create(self, values):
# #         # Check if the user is assigned to a specific department
# #         if 'department_id' in values and values['department_id']:
# #             # Create a new company and assign it to the user if it doesn't exist
# #             if 'company_ids' not in values:
# #                 company_vals = {
# #                     'name': values['login'] + 'Company',
# #                     'currency_id': self.env.ref('base.USD').id,
# #                 }
# #                 company = self.env['res.company'].create(company_vals)
# #                 values['company_ids'] = [(4, company.id, 0)]
# #
# #             # Call the original method to create the user
# #             user = super(ResUsers, self).create(values)
# #
# #             # Restrict access to POS module for the user
# #             pos_group = self.env.ref('point_of_sale.group_pos_user')
# #             other_groups = self.env['res.groups'].search([('id', '!=', pos_group.id)])
# #             user.write({'groups_id': [(3, group.id) for group in other_groups]})
# #
# #             return user
# #         else:
# #
# #             # If the user is not assigned to a department, raise an exception
# #             raise ValueError('Users must be assigned to a department')
#
#
# # ----------------------------------------- Third Try # -----------------------------------------
# from odoo import models, fields, api
#
# class ResUsers(models.Model):
#     _inherit = 'res.users'
#
#     @api.model
#     def create(self, values):
#         # Call the original create method
#         user = super(ResUsers, self).create(values)
#
#         # check if the user is logging out
#         if values.get('active') is False:
#             # Create a new company with the user's name
#             company_name = user.name
#             company = self.env['res.company'].create({
#                 'name': company_name,
#             })
#
#             # Set the user's company to the newly created company
#             user.write({'company_id': company.id})
#
#             # Set the user type to internal
#             user.write({'user_type': 'internal'})
#
#             # Update the allowed companies for the user
#             user.write({'allowed_company_ids': [(4, company.id)]})
#
#             # Create a new POS for the user
#             pos_config = self.env['pos.config'].create({
#                 'name': f'POS for {company_name}',
#                 'company_id': company.id,
#                 # Add other POS configuration fields as needed
#             })
#             user.write({'pos_config_id': pos_config.id})
#
#         return user
#
# #-------------------------------------------------------
# # from odoo import models, fields, api
# #
# # class ResUsers(models.Model):
# #     _inherit = 'res.users'
# #
# #     @api.model
# #     def create(self, vals):
# #         # Ensure internal user creation
# #         vals['groups_id'] = [(4, self.env.ref('base.group_user').id)]
# #
# #         # Create the user without company assignment
# #         new_user = super(ResUsers, self).create(vals)
# #
# #         # Create a new company automatically
# #         new_company = self.env['res.company'].create({'name': new_user.name})
# #
# #         # Set user's company and allowed company
# #         new_user.company_id = new_company.id
# #         new_user.allowed_company_ids = [(4, new_company.id)]
# #
# #         # Restrict access to only POS Module using group permissions
# #         pos_group = self.env.ref('point_of_sale.group_pos_user')
# #         other_groups = self.env['res.groups'].search([('id', '!=', pos_group.id)])
# #         new_user.write({'groups_id': [(3, group.id) for group in other_groups]})
# #
# #         return new_user
# from odoo import models, fields, api
#
# class ResUsers(models.Model):
#     _inherit = 'res.users'
#
#     @api.model
#     def create(self, vals):
#         try:
#             # Create the user with the "admin company" as the initial default
#             new_user = super(ResUsers, self).create({**vals, 'company_id': self.env.ref('base.main_company').id})
#
#             # Create the company after the user
#             company_vals = {
#                 'name': new_user.name,
#                 'currency_id': self.env.ref('base.PKR').id,
#             }
#             new_company = self.env['res.company'].sudo().create(company_vals)
#
#             # Allow access to both companies (assuming the field exists)
#             new_user.allowed_companies_ids = [(4, new_company.id), (4, self.env.ref('base.main_company').id)]
#
#             # Create POS config (after company and user creation)
#             pos_config = self.env['pos.config'].create({
#                 'name': f'POS for {new_user.name}',
#                 'company_id': new_company.id,
#                 # Add other POS configuration fields
#             })
#
#         except Exception as e:
#             print("Error creating company or POS config:", e)
#             raise
#
#         return new_user
#
# from odoo import models, fields, api
#
# class ResUsers(models.Model):
#     _inherit = 'res.users'
#
#     @api.model
#     def create(self, vals):
#         # Generate a unique company name based on the user's name
#         company_name = vals.get('name') or 'New Company'  # Ensure a default name
#
#         # Create the new company
#         company = self.env['res.company'].sudo().create({'name': company_name})
#
#         # Assign the company to the user
#         vals['company_id'] = company.id
#
#         # Call the original create method to create the user
#         res = super(ResUsers, self).create(vals)
#
#         return res
# from odoo import models, fields, api
# from odoo.exceptions import AccessError
# import logging
#
# _logger = logging.getLogger(__name__)
#
# class ResUsers(models.Model):
#     _inherit = 'res.users'
#
#     @api.model
#     def create(self, vals):
#         # Create the user with the default company initially
#         new_user = super(ResUsers, self.sudo()).create({**vals, 'company_id': self.env.ref('base.main_company').id})
#
#         # Create the company after the user
#         company_vals = {
#             'name': new_user.name,
#             'currency_id': self.env.ref('base.PKR').id,  # Adjust currency as needed
#         }
#         new_company = self.env['res.company'].sudo().create(company_vals)
#
#         # Schedule a cron job to switch the user's company after 1 minute
#         self.env['ir.cron'].sudo().create({
#             'name': f"Switch Company for User {new_user.id}",
#             'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
#             'state': 'code',
#             'code': 'model._cron_switch_company_after_delay(%s, %s)' % (new_user.id, new_company.id),
#             'interval_number': 1,
#             'interval_type': 'minutes',
#             'numbercall': 1,
#             'doall': True,
#         })
#
#         return new_user
#
#     @api.model
#     def _cron_switch_company_after_delay(self, user_id, company_id):
#         """Wrapper function for cron job to switch the user's company."""
#         user = self.browse(user_id)
#         company = self.env['res.company'].browse(company_id)
#         self.switch_company_after_delay(user, company)
#
#     def switch_company_after_delay(self, user, company):
#         """Switches the user's company to the specified one after a delay."""
#         try:
#             # Set the user context to an admin user
#             with self.env.cr.savepoint():
#                 user = user.sudo()  # Switch to admin user
#                 target_company = user.default_company_id or company
#                 user.write({'company_id': target_company.id})
#                 _logger.info(f"Company switched successfully for user: {user.name}")
#         except AccessError as ae:
#             _logger.error(f"Access error switching company for user {user.name}: {ae}")
#             # Handle the access error as needed
#         except Exception as e:
#             _logger.error(f"Error switching company for user {user.name}: {e}")
#             # Consider logging or notification for other errors

#
# from odoo import models, api
# import logging
#
# _logger = logging.getLogger(__name__)
#
# class ResUsers(models.Model):
#     _inherit = 'res.users'
#
#     @api.model
#     def create(self, vals):
#         # Create the user with the default company initially
#         new_user = super(ResUsers, self).create({**vals, 'company_id': self.env.ref('base.main_company').id})
#
#         # Check if a company with the same name as the user exists
#         existing_company = self.env['res.company'].sudo().search([('name', '=', new_user.name)], limit=1)
#
#         if existing_company:
#             # Schedule a cron job to switch the user's company after 1 minute
#             self.env['ir.cron'].sudo().create({
#                 'name': f"Switch Company for User {new_user.id}",
#                 'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
#                 'state': 'code',
#                 'code': 'model._cron_switch_company_after_delay(%s, %s)' % (new_user.id, existing_company.id),
#                 'interval_number': 1,
#                 'interval_type': 'minutes',
#                 'numbercall': 1,
#                 'doall': True,
#             })
#         else:
#             # Create the company after the user
#             company_vals = {
#                 'name': new_user.name,
#                 'currency_id': self.env.ref('base.PKR').id,  # Adjust currency as needed
#             }
#             new_company = self.env['res.company'].sudo().create(company_vals)
#
#             # Schedule a cron job to switch the user's company after 1 minute
#             self.env['ir.cron'].sudo().create({
#                 'name': f"Switch Company for User {new_user.id}",
#                 'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
#                 'state': 'code',
#                 'code': 'model._cron_switch_company_after_delay(%s, %s)' % (new_user.id, new_company.id),
#                 'interval_number': 1,
#                 'interval_type': 'minutes',
#                 'numbercall': 1,
#                 'doall': True,
#             })
#
#         return new_user
#
#     @api.model
#     def _cron_switch_company_after_delay(self, user_id, company_id):
#         """Wrapper function for cron job to switch the user's company."""
#         user = self.browse(user_id)
#         company = self.env['res.company'].browse(company_id)
#
#         # Run the switching logic with admin privileges
#         self.sudo().switch_company_after_delay(user, company)
#
#     def switch_company_after_delay(self, user, company):
#         """Switches the user's company to the specified one after a delay."""
#         try:
#             with api.Environment.manage():  # Ensure a valid database cursor
#                 with self.env.cr.savepoint():
#                     user.write({'company_id': company.id})
#                     _logger.info(f"Company switched successfully for user: {user.name}")
#         except Exception as e:
#             _logger.error(f"Error switching company for user {user.name}: {e}")
#
#
# from odoo import models, api
# import logging
# import os
#
# _logger = logging.getLogger(__name__)
#
# class ResUsers(models.Model):
#     _inherit = 'res.users'
#
#     @api.model
#     def _cron_switch_company_after_delay(self, user_id, company_id):
#         admin_user = os.environ.get('admin')
#         admin_password = os.environ.get('admin')
#
#         # Use sudo with admin credentials for privileged operations
#         self.with_user(user=admin_user, password=admin_password).sudo().switch_company_after_delay(user_id, company_id)
#
#     @api.model
#     def create(self, vals):
#         # Create the user with the default company initially
#         new_user = super(ResUsers, self).create({**vals, 'company_id': self.env.ref('base.main_company').id})
#
#         # Check if a company with the same name as the user exists
#         existing_company = self.env['res.company'].sudo().search([('name', '=', new_user.name)], limit=1)
#
#         if existing_company:
#             # Schedule a cron job to switch the user's company after 1 minute
#             self.env['ir.cron'].sudo().create({
#                 'name': f"Switch Company for User {new_user.id}",
#                 'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
#                 'state': 'code',
#                 'code': 'model._cron_switch_company_after_delay(%s, %s)' % (new_user.id, existing_company.id),
#                 'interval_number': 1,
#                 'interval_type': 'minutes',
#                 'numbercall': 1,
#                 'doall': True,
#             })
#         else:
#             # Create the company after the user
#             company_vals = {
#                 'name': new_user.name,
#                 'currency_id': self.env.ref('base.PKR').id,  # Adjust currency as needed
#             }
#             new_company = self.env['res.company'].sudo().create(company_vals)
#
#             # Schedule a cron job to switch the user's company after 1 minute
#             self.env['ir.cron'].sudo().create({
#                 'name': f"Switch Company for User {new_user.id}",
#                 'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
#                 'state': 'code',
#                 'code': 'model._cron_switch_company_after_delay(%s, %s)' % (new_user.id, new_company.id),
#                 'interval_number': 1,
#                 'interval_type': 'minutes',
#                 'numbercall': 1,
#                 'doall': True,
#             })
#
#         return new_user
#
#     @api.model
#     def _cron_switch_company_after_delay(self, user_id, company_id):
#         """Wrapper function for cron job to switch the user's company."""
#         user = self.browse(user_id)
#         company = self.env['res.company'].browse(company_id)
#
#         # Run the switching logic with elevated privileges
#         with self.env.cr.savepoint():
#             user.sudo().write({'company_id': company.id})
#             _logger.info(f"Company switched successfully for user: {user.name}")


from odoo import models, api
import logging
import os

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _cron_switch_company_after_delay(self, user_id, company_id):
        admin_user = os.environ.get('admin')
        admin_password = os.environ.get('admin')

        # Use sudo with admin credentials for privileged operations
        self.with_user(user=admin_user, password=admin_password).sudo().switch_company_after_delay(user_id, company_id)

    @api.model
    def create(self, vals):
        # Create the user with the default company initially
        new_user = super(ResUsers, self).create({**vals, 'company_id': self.env.ref('base.main_company').id})

        # Check if a company with the same name as the user exists
        existing_company = self.env['res.company'].sudo().search([('name', '=', new_user.name)], limit=1)

        if existing_company:
            # Schedule a cron job to switch the user's company after 1 minute
            self.env['ir.cron'].sudo().create({
                'name': f"Switch Company for User {new_user.id}",
                'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
                'state': 'code',
                'code': 'model._cron_switch_company_after_delay(%s, %s)' % (new_user.id, existing_company.id),
                'interval_number': 1,
                'interval_type': 'minutes',
                'numbercall': 1,
                'doall': True,
                'user_id': new_user.id,  # Pass user ID to cron job
            })

            # Assign the group ID of 'Access Rights / Administration' to the new user
            admin_group = self.env.ref('your_admin_group_xml_id')  # Replace with the actual XML ID
            new_user.write({'groups_id': [(4, admin_group.id)]})

        else:
            # Create the company after the user
            company_vals = {
                'name': new_user.name,
                'currency_id': self.env.ref('base.PKR').id,  # Adjust currency as needed
            }
            new_company = self.env['res.company'].sudo().create(company_vals)

            # Schedule a cron job to switch the user's company after 1 minute
            self.env['ir.cron'].sudo().create({
                'name': f"Switch Company for User {new_user.id}",
                'model_id': self.env['ir.model'].search([('model', '=', 'res.users')], limit=1).id,
                'state': 'code',
                'code': 'model._cron_switch_company_after_delay(%s, %s)' % (new_user.id, new_company.id),
                'interval_number': 1,
                'interval_type': 'minutes',
                'numbercall': 1,
                'doall': True,
                'user_id': new_user.id,  # Pass user ID to cron job
            })

            # Assign the group ID of 'Access Rights / Administration' to the new user
            admin_group = self.env.ref('base.group_erp_manager')  # Replace with the actual XML ID
            new_user.write({'groups_id': [(4, admin_group.id)]})

        return new_user

    @api.model
    def _cron_switch_company_after_delay(self, user_id, company_id):
        """Wrapper function for cron job to switch the user's company."""
        user = self.browse(user_id)
        company = self.env['res.company'].browse(company_id)

        # Run the switching logic with elevated privileges
        with self.env.cr.savepoint():
            user.sudo().write({'company_id': company.id})
            _logger.info(f"Company switched successfully for user: {user.name}")
