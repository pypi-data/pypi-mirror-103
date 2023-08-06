from mako.template import Template
from fastapi.responses import HTMLResponse


def render_html(filename: str = "", **kwargs):
    return HTMLResponse(Template(filename=filename).render(**kwargs))


def base_response(code: int, msg: str, data=None) -> dict:
    """
    基础返回格式
    :param code:
    :param msg:
    :param data:
    :return:
    """
    if data is None:
        data = {}
    result = {
        "code": code,
        "message": msg,
        "data": data
    }
    return result


def success(data=None, msg: str = ''):
    """成功返回格式"""
    return base_response(0, msg, data)


def fail(code=-1, msg: str = '', data=None):
    """失败返回格式"""
    return base_response(code, msg, data)


class UnicornException(Exception):

    def __init__(self, code, errmsg, data=None):
        """
        失败返回格式
        :param code:
        :param errmsg:
        """
        if data is None:
            data = {}
        self.code = code
        self.errmsg = errmsg
        self.data = data
