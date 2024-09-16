import uuid
from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class User(models.Model):
    _inherit = "res.users"

    remote_login_key = fields.Char("Remote Login-Key")

    @api.model
    def set_remote_keys(self):
        for user in self.search([]):
            if not user.remote_login_key:
                user.remote_login_key = str(uuid.uuid4())
                self.env.cr.commit()
