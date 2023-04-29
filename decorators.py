"""
Module containing example decorators that can be used with and without ()
"""
from functools import wraps


# Basic decorator
def decorated(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        print("Decoration start...")
        result = fn(*args, ** kwargs)
        print("Decoration end...")
        return result
    return inner


@decorated
def test_func(a=1):
    print("Function executed")
    return 5 + a


# A more advanced decorator variant whcih also allows parameters to be passes
# downside is that it always needs to be passes with parentheses
def decorator_factory(var1='', var2=''):
    def decorated(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            params = " and ".join(
                [var1, var2]) if var1 and var2 else var1 or var2
            print(f"Decoration start with {params}...")
            result = fn(*args, ** kwargs)
            print(f"Decoration end with {params}...")
            return result
        return inner
    return decorated


@decorator_factory(var2="test2")
def test_func2(a=1):
    print("Function executed")
    return 5 + a


# A more flexible option allowing the function to be executed using both types
# the lru_cache decorator uses this method s well
def flexible_decorator(var1=False, var2=False):
    def decorated(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            param1 = "param1" if isinstance(var1, bool) and var1 else ''
            param2 = "param2" if isinstance(var2, bool) and var1 else ''
            params = " ".join([param1, param2])
            print(f"Decoration start with {params}...")
            result = fn(*args, ** kwargs)
            print(f"Decoration end with {params}...")
            return result
        return inner

    # The below checks will allow the decorator to behave both as a simple decorator and as a decorator factory
    if callable(var1):
        # a callable was passed in (1st variable)
        return decorated(var1)
    elif isinstance(var1, bool) or isinstance(var2, bool):
        # parameter triggered, then return the decorator function
        return decorated
    else:
        raise ValueError(
            "Expected argument to be a bool, a callable, or None.")


@flexible_decorator
def test_func3_1(a=1):
    print("Function executed")
    return 5 + a


@flexible_decorator(var2=False)
def test_func3_2(a=1):
    print("Function executed")
    return 5 + a


@flexible_decorator(var1=True, var2=True)
def test_func3_3(a=1):
    print("Function executed")
    return 5 + a


if __name__ == "__main__":
    print(test_func(4))
    print("="*40)
    print(test_func2(4))
    print("="*40)
    print(test_func3_1(4))
    print(test_func3_2(4))
    print(test_func3_3(4))

    # RESULTS FROM EXECUTION:
    # Decoration start...
    # Function executed
    # Decoration end...
    # 9
    # ========================================
    # Decoration start with test2...
    # Function executed
    # Decoration end with test2...
    # 9
    # ========================================
    # Decoration start with  param2...
    # Function executed
    # Decoration end with  param2...
    # 9
    # Decoration start with  ...
    # Function executed
    # Decoration end with  ...
    # 9
    # Decoration start with param1 param2...
    # Function executed
    # Decoration end with param1 param2...
    # 9
