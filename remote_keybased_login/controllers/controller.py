import uuid
from odoo import http
from odoo.http import request


class RemoteLoginController(http.Controller):

    @http.route("/keylogin", auth="public", type="http")
    def handler(self, **post):
        key=post['remote_key']
        redirect = request.redirect(f"/web/login?remote_key={key}&random={uuid.uuid4()}")
        redirect.set_cookie("session_id", "", max_age=365 * 24 * 3600)
        return redirect
