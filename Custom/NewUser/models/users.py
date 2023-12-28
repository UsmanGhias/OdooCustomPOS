from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, values):
        # Set the user type to internal
        values['user_type'] = 'internal'

        # Call the original create method with updated values
        user = super(ResUsers, self).create(values)

        # check if the user is logging out
        if values.get('active') is False:
            # Create a new company with the user's name
            company_name = user.name
            company = self.env['res.company'].create({
                'name': company_name,
            })

            # Set the user's company to the newly created company
            user.write({'company_id': company.id})

            # Update the allowed companies for the user
            user.write({'allowed_company_ids': [(4, company.id)]})

        return user
