from odoo import api
from . import models
from odoo import SUPERUSER_ID

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.users'].set_remote_keys()
