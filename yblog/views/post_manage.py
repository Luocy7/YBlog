# -*- coding:utf-8 _*-
"""
    @author: Luocy
    @time: 2020/04/02
    @copyright: © 2020 Luocy <luocy77@gmail.com>
"""

from flask import request, current_app, jsonify
from yblog.utils.RestResUtil import RestResponse
from yblog.database.postService import *
from yblog.extensions import cache, csrf


@csrf.exempt
def post_manage():
    # todo :auth
    x_real_ip = request.headers.get('X-Real-IP', '')
    x_forwarder_for = request.headers.get('X-Forwarded-For', '')
    if x_real_ip or x_forwarder_for:
        return jsonify(RestResponse.fail(msg='Invalid Request!', code=400)), 400

    signature = request.headers.get("YBlog-Signature")
    if not signature or not signature.startswith("luocy"):
        return jsonify(RestResponse.fail(msg='Invalid request!', code=400)), 400

    request_data = request.get_json()

    if not request_data:
        return jsonify(RestResponse.fail(msg='Invalid data!', code=400)), 400

    for k, v in request_data.items():
        if isinstance(request_data[k], str):
            request_data[k] = v.strip()

    try:
        method = request_data['method']
        md_name = request_data['md_name']
    except KeyError:
        return jsonify(RestResponse.fail(msg='Invalid data!', code=400)), 400

    if method == 'created':
        try:
            create_post_by_name(request_data)
        except DBError as e:
            current_app.logger.error(e)
            return jsonify(RestResponse.fail(msg='Fail to create Post <{}>'.format(md_name), code=400)), 400

        cache.clear()
        msg = 'Created Post <{}>'.format(md_name)
        current_app.logger.info(msg)
        return jsonify(RestResponse.ok(msg=msg, code=200))

    elif method == 'deleted':
        try:
            delete_post_with_data(request_data)
        except DBError as e:
            current_app.logger.error(e)
            return jsonify(RestResponse.fail(msg='Fail to delete Post <{}>'.format(md_name), code=400)), 400

        cache.clear()
        msg = 'Deleted Post <{}>'.format(md_name)
        current_app.logger.info(msg)
        return jsonify(RestResponse.ok(msg=msg, code=200))

    elif method == 'moved':
        dest_name = request_data.get('dest_name', '')
        try:
            change_postname_with_data(request_data)
        except DBError as e:
            current_app.logger.error(e)
            return jsonify(RestResponse.fail(msg='Fail to move Post <{}>'.format(md_name), code=400)), 400

        cache.clear()
        msg = 'Moved Post <{}> to <{}>'.format(md_name, dest_name)
        current_app.logger.info(msg)
        return jsonify(RestResponse.ok(msg=msg, code=200))

    elif method == 'modified':
        try:
            update_post_by_name(request_data)
        except DBError as e:
            current_app.logger.error(e)
            return jsonify(RestResponse.fail(msg='Fail to modifie Post <{}>'.format(md_name), code=400)), 400

        cache.clear()
        msg = 'Modified Post <{}>'.format(md_name)
        current_app.logger.info(msg)
        return jsonify(RestResponse.ok(msg=msg, code=200))

    return jsonify(RestResponse.fail(msg='Invalid data!', code=400)), 400
