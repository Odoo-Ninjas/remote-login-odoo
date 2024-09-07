# def pre_init_hook(cr):
    # pass

def post_init_hook(cr, registry):
    registry['res.users'].set_remote_keys()

# def uninstall_hook(cr, registry):
    # pass

from .models import *
# from .tests import *
