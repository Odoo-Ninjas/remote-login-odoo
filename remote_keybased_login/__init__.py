from . import controllers
from . import models

def post_init_hook(cr, registry):
    registry['res.users'].set_remote_keys()

