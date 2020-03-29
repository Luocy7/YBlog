# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/30
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import hmac
import hashlib
from flask import request, current_app, abort, jsonify
from yblog.extensions import csrf
from yblog.utils.RestResUtil import RestResponse


@csrf.exempt
def yblg_github_moniter():
    if request.method == 'POST':
        signature = request.headers.get("X-Hub-Signature")
        if not signature or not signature.startswith("sha1="):
            abort(400, "X-Hub-Signature required")

        # Create local hash of payload
        github_webhook_secret = current_app.config['GITHUB_WEBHOOK_SECRET'].encode("utf-8")
        digest = hmac.new(github_webhook_secret,
                          request.data, hashlib.sha1).hexdigest()
        verify_signature = "sha1=" + digest
        current_app.logger.info("github request signature: {}".format(verify_signature))

        # Verify signature
        if not hmac.compare_digest(signature, verify_signature):
            abort(400, "Invalid signature")

        request_data = request.get_json()

        # We are only interested in push events from the a certain repo
        if request_data.get("repository", {}).get("name") != "YBlog":
            return jsonify(RestResponse.ok(msg='Dont care!')), 200

        # todo celery task
        # http://flask.pocoo.org/docs/1.0/patterns/celery/
        return jsonify(RestResponse.ok(msg='Success', code=200))
    else:
        abort(400)
