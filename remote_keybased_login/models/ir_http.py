import uuid
import time
from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"
    _description = "HTTP Routing"

    @classmethod                                                                      
    def _dispatch(cls, endpoint):
        if request.session.redirect_to_web == "1":
            request.session.redirect_to_web = None
            return request.redirect('/web', 301)
        res = super()._dispatch(endpoint)
        return res

    @classmethod
    def _authenticate(cls, endpoint):
        path = request.httprequest.path
        if path.startswith("/web/login") and request.httprequest.values.get("remote_key"):
            key = request.httprequest.values["remote_key"]
            user = (
                request.env["res.users"].sudo().search([("remote_login_key", "=", key)])
            )
            if user:
                request.session.uid = user[0].id
                session_token = user[0]._compute_session_token(request.session.sid)
                request.session.session_token = session_token
                request.env = api.Environment(request.env.cr, user.id, request.env.context)
                request.session.redirect_to_web = "1"
                return "remote_key"
            else:
                time.sleep(20)

        res = super()._authenticate(endpoint)
        return res

    @classmethod
    def _auth_method_remote_key(cls):
        import pudb

        pudb.set_trace()
        request.uid = request.session.uid
