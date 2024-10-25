#!/usr/bin/env python3
"""
exercise.py
"""
import redis
import uuid
import typing
from functools import wraps


def count_calls(method: typing.Callable) -> typing.Callable:
    """
    Decorator That counts how many times the decorated method
    is called.
    It increments a counter stored in redis, using the method's
    qualified name as the key.
    Args:
        method (typing.Callable): The method to be wrapped

    Returns:
        typing.Callable: The wrapped method with call-counting functionality
    """

    @wraps(method)
    def wrapper(self, *args, **kwds):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwds)

    return wrapper


def call_history(method: typing.Callable) -> typing.Callable:
    """
    store the history of input and output of a particular function
    Args:
        method (typing.Callable): method

    Returns:
        typing.Callable: return of method
    """

    @wraps(method)
    def wrapper(self, *args, **kwds):
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        result = method(self, *args, **kwds)
        self._redis.rpush(f"{method.__qualname__}:outputs", result)
        return result

    return wrapper


class Cache:
    """
    Cache Class for interacting with Redis
    """

    def __init__(self) -> None:
        """
        Constructor of Cache Class
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: typing.Union[str, bytes, int, float]) -> str:
        """
        Stores the given data identified by a randomly generated key
        in Redis.
        The method is decorated to store record call count and input/
        output history
        Args:
            data (typing.Union[str, bytes, int, float]): data to be stored

        Returns:
            str: The randomly generated key that
                 references the stored data
        """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str, fn: typing.Optional[typing.Callable] = None):
        """
        convert data back to desired format
        Args:
            key (str): key that reference a particular value
            fn (typing.Optional[typing.Callable]):

            optional callable
            to be called on the
            data retreived
            to cast it to the
            desired type

        Returns:
            _type_: desired format for the value stored
                    using the given key
        """
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, key: str):
        """
        parameterize .get by passing appropriate
        conversion function
        Args:
            key (str): key that reference a particular value

        Returns:
            _type_: decoded byte string (regular string)
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str):
        """
        parameterize .get by passing appropriate
        conversion function
        Args:
            key (str): key that reference a particular value

        Returns:
            _type_: integer
        """
        return self.get(key, int)


cache = Cache()


def replay(method: typing.Callable) -> None:
    """
    display the history of calls of a particular function
    Args:
        method (typing.Callable): function
    """
    method_name = method.__qualname__
    no_of_times_called = cache.get_int(method_name)

    print(f"{method_name} was called {no_of_times_called} times:")
    for input, output in zip(
        cache._redis.lrange(f"{method_name}:inputs", 0, -1),
        cache._redis.lrange(f"{method_name}:outputs", 0, -1),
    ):
        print(f"{method_name}(*{input.decode()}) -> {output.decode()}")
