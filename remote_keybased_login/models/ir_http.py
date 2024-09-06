import time
from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"
    _description = "HTTP Routing"

    @classmethod                                                                      
    def _postprocess_args(cls, arguments, rule):
        if request.httprequest.session.redirect_to_web == "1":
            request.httprequest.session.redirect_to_web = None
            return request.redirect('/web', 301)

        res = super()._postprocess_args(arguments, rule)
        return res

    @classmethod
    def _authenticate(cls, endpoint):
        path = request.httprequest.path
        if path.startswith("/web/login") and request.params.get("remote_key"):
            key = request.params["remote_key"]
            user = (
                request.env["res.users"].sudo().search([("remote_login_key", "=", key)])
            )
            if user:
                request.httprequest.session.uid = user[0].id
                session_token = user[0]._compute_session_token(request.session.sid)
                request.httprequest.session.session_token = session_token
                request.httprequest.session.redirect_to_web = "1"
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
