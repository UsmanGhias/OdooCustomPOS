# ------------------------------------ 15th try (after making journals)------------------------------------
from odoo import models, api, fields
import logging
import re


_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'

    # For Creating a new company.
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

                # Automatically create a chart of accounts for the new company
                self._create_chart_of_accounts(user.company_id)

        except Exception as e:
            _logger.exception(f"Error during company switch for user {user.name}")

    # For Creating a new user and switching the company
    @api.model
    def create(self, vals):
        new_user = super(ResUsers, self).create({**vals, 'company_id': self.env.ref('base.main_company').id})

        # Assign the group ID of 'Access Rights / Administration' to the new user
        admin_group = self.env.ref('base.group_erp_manager')  # Replace with the actual XML ID
        new_user.write({'groups_id': [(4, admin_group.id)]})

        # Add the new user to the 'account.group_account_manager' group
        account_manager_group = self.env.ref('account.group_account_manager')
        new_user.write({'groups_id': [(4, account_manager_group.id)]})

        # Add the new user to the 'base.group_partner_manager' group
        extra_right_group = self.env.ref('base.group_partner_manager')
        new_user.write({'groups_id': [(4, extra_right_group.id)]})

        # Add the new user to the 'stock.group_stock_manager' group
        inventory_group = self.env.ref('stock.group_stock_manager')
        new_user.write({'groups_id': [(4, inventory_group.id)]})

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

    # For creating chart of accounts
    @api.model
    def _create_chart_of_accounts(self, company):
        # Function to clean non-alphanumeric characters from a string
        def clean_code(input_str):
            return re.sub(r'\W+', '', input_str)
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
        except Exception as e:
            _logger.exception(f"Error during chart of accounts creation for company {company.name}")