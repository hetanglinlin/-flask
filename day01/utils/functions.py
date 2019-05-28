
# 1. 外层函数内嵌内层函数
# 2. 外层函数返回内层函数
# 3. 内层函数调用外层函数的参数

from flask import request, redirect
from functools import wraps


def login_required(func):
    @wraps(func)
    def is_check():
        token = request.cookies.get('token')
        if token == '1914e7628d3241ffa203001aa0fbdf3d':
            # 校验成功则继续调用func，func为被装饰器装饰的函数
            return func()
        return redirect('/login/')

    return is_check


