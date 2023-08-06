import json
import redis
import logging

from web_frame.context import config
from web_frame.utils.CommonUtil import CJsonEncoder


def get_redis_conn(host=None, port=None, **options):
    if not host:
        host = config.cache_ip
    if not port:
        port = config.cache_port
    redis_conn = redis.Redis(host=host, port=port, **options)
    return redis_conn


def get_cache(key, decode=True):
    try:
        value = get_redis_conn().get(key)
    except ConnectionError as e:
        logging.warning(f"缓存服务连接失败：{e}")
        value = None
    if value:
        if decode:
            result = json.loads(value.decode())
        else:
            result = value
        logging.info("hit cache: {}".format(key))
        return result
    logging.debug("miss cache: {}".format(key))
    return None


def set_cache(key, value):
    logging.debug(f"set cache: {key}")
    try:
        redis_conn = get_redis_conn()
        if isinstance(value, dict):
            redis_conn.set(key, json.dumps(value, cls=CJsonEncoder, ensure_ascii=False))
        else:
            redis_conn.set(key, value)
    except ConnectionError as e:
        logging.warning(f"缓存服务连接失败：{e}")
