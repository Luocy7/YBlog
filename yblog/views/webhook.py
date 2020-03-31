# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/03/30
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

import hmac
import hashlib
from flask import request, current_app, jsonify
from yblog.extensions import csrf
from yblog.utils.RestResUtil import RestResponse
from yblog.task.task import git_status


@csrf.exempt
def yblg_github_moniter():
    if request.method == 'POST':
        signature = request.headers.get("X-Hub-Signature")
        if not signature or not signature.startswith("sha1="):
            return jsonify(RestResponse.fail(msg='X-Hub-Signature required!', code=400)), 400

        # Create local hash of payload
        github_webhook_secret = current_app.config['GITHUB_WEBHOOK_SECRET'].encode("utf-8")
        digest = hmac.new(github_webhook_secret,
                          request.data, hashlib.sha1).hexdigest()
        verify_signature = "sha1=" + digest

        # Verify signature
        if not hmac.compare_digest(signature, verify_signature):
            return jsonify(RestResponse.fail(msg='Invalid signature!', code=400)), 400

        request_data = request.get_json()

        # We are only interested in push events from the a certain repo
        if request_data.get("repository", {}).get("name") != "Notes":
            return jsonify(RestResponse.fail(msg='Dont care!', code=200)), 200

        current_app.logger.info('Webhook celery Job  Start')
        task = git_status.delay()

        return jsonify(RestResponse.ok(msg='Success', code=200))
    else:
        return jsonify(RestResponse.fail(msg='Invalid method!', code=400)), 400
