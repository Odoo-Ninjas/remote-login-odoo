import uuid
from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class User(models.Model):
    _inherit = "res.users"

    remote_login_key = fields.Char("Remote Login-Key")

    @api.model
    def set_remote_keys(self):
        self.env.cr.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
        self.env.cr.execute("""
        UPDATE res_users
        SET remote_login_key = gen_random_uuid()
        WHERE remote_login_key is null
        ;
        """)
