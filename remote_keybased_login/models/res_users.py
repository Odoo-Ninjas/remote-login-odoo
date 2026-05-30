import uuid
from odoo import api, fields, models


class User(models.Model):
    _inherit = "res.users"

    remote_login_key = fields.Char("Remote Login-Key", copy=False)

    @api.model
    def set_remote_keys(self):
        for user in self.search([]):
            if not user.remote_login_key:
                user.remote_login_key = str(uuid.uuid4())
                self.env.cr.commit()

    @api.model
    def clear_remote_keys(self):
        """Wipe all auto-login tokens (e.g. after a restore that carried
        over keys from the dumped DB's origin). Fresh keys are regenerated
        lazily by set_remote_keys() on the next login fetch."""
        self.search([("remote_login_key", "!=", False)]).write(
            {"remote_login_key": False}
        )
        self.env.cr.commit()
