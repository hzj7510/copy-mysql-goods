from flask import Flask
from flask import request
from flask import Response
from changetable import changedb
from flask.ext.cache import Cache

import hashlib

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@app.route('/changedb')
def hello_world():
    h = hashlib.md5()
    h.update(request.url.encode('utf-8'))
    v = h.hexdigest()
    value = cache.get(v)
    if value is None:
        # try:
        origin_name = request.args.get('oname', '')
        purpose_name = request.args.get('pname', '')
        if len(origin_name) == 0 or len(purpose_name) == 0:
            return Response("{'error':'输入错误'}", status=201, mimetype='application/json')
        else:
            err_info = changedb(origin_name, purpose_name)
            if len(err_info) == 0:
                cache.set(v, '1', timeout=30)
                return Response("{'success':'更新完成'}", status=200, mimetype='application/json')
            else:
                return Response(err_info, status=201, mimetype='application/json')
        # except Exception as e:
        #     print(e)
    return '请不要重复操作, 请30秒后再次尝试'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=True)
    # app.run()