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
    if request.method == 'POST':
        # todo :auth

        request_data = request.get_json()

        if request_data:
            try:
                method = request_data['method']
                md_name = request_data['md_name']
            except KeyError:
                return jsonify(RestResponse.fail(msg='Invalid data!', code=400)), 400

            dest_name = request_data.get('dest_name', '')

            if method == 'created':
                try:
                    create_post_by_name(request_data)
                except DBError as e:
                    current_app.logger.error(e)
                    return jsonify(RestResponse.fail(msg='Fail to create Post <{}>'.format(md_name), code=400)), 400

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
        return jsonify(RestResponse.fail(msg='Invalid data!', code=400)), 400
    return jsonify(RestResponse.fail(msg='Invalid method!', code=400)), 400
