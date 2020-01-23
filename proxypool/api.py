from .config import STABLE_REDIS_KEY as table
from .logger import logger
from .db import myredis

from flask import Flask, make_response, jsonify, abort, g
import random

__all__ = ['app']

app = Flask(__name__)


def redis_conn():
    if not hasattr(g, 'redis'):
        g.redis = myredis
    return g.redis


@app.route('/proxypool/')
def index():
    return jsonify(
        {'count': 'get num of proxies',
         'get': 'get one of best proxies randomly',
         'get_all': 'get all proxies',
         'get_all_ws': 'get all proxies with scores'
         }
    )


@app.route('/proxypool/count')
def get_count():
    conn = redis_conn()
    num = conn.count(table)
    return jsonify({'count': num})


@app.route('/proxypool/get')
def get_proxy():
    conn = redis_conn()
    proxies = conn.get(table, 0, 5)
    if proxies:
        proxy = random.choice(proxies)
        return jsonify({'proxy': proxy})
    else:
        return jsonify({'proxy': proxies})


@app.route('/proxypool/get_all')
def get_all_proxies():
    conn = redis_conn()
    proxies = conn.get(table)
    return jsonify({'proxies': proxies})


@app.route('/proxypool/get_all_ws')
def get_all_ws():
    conn = redis_conn()
    proxies = conn.get(table, isS=True)
    return jsonify({'proxies': proxies})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run()
