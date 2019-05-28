from functools import wraps


def login_required(func):
    @wraps(func)
    def is_check():
        return func
    return is_check

@login_required
def f():
    print('123')

print(f)
