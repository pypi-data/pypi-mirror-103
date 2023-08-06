# -*- coding: utf-8 -*-
"""
----------------------------------------------------
    File Name:              base
    Description             
    Author:                 hzy
    date:                   2019/4/4
----------------------------------------------------
"""
from flask_templates.common.class_holder import class_register

__author__ = 'hzy'

import functools
import time
import copy
from flask import request
import traceback

from flask_templates.common.utils import read_parm, construct_result, BaseError, doublewrap
from flask_templates.var import ErrorCode, INNER_ERROR_STRING
from flask_templates.service.base import *
from flask_templates.common.logger import logger


class ViewError(BaseError):
    base_msg = 'view error'
    message = ''
    code = 0

    def __init__(self):
        super().__init__(msg=self.message)

    @property
    def resp(self):
        return construct_result(self.code, self.message)


class ParamLostError(ViewError):
    code = ErrorCode.PARAM_LOST_ERROR
    message = 'param {param} lost!'

    def __init__(self, **kwargs):
        self.message = self.message.format(**kwargs)
        super().__init__()


class ParamIncorrectError(ViewError):
    code = ErrorCode.PARAM_INCORRECT_ERROR
    message = 'param {param} incorrect!'

    def __init__(self, **kwargs):
        self.message = self.message.format(**kwargs)
        super().__init__()


class ViewValidationError(ViewError):
    code = ErrorCode.VALIDATION_ERROR

    def __init__(self, msg, data):
        self.message = msg
        self.messages = msg
        self.valid_data = data
        super().__init__()


def check_param_range(param_name, param, _min=None, _max=None):
    try:
        if _min is None:
            condition = param <= _max
        elif _max is None:
            condition = param >= _min
        else:
            condition = _min <= param <= _max
        if condition:
            return
        else:
            raise ParamIncorrectError(param=param_name)
    except:
        raise ParamIncorrectError(param=param_name)


class ResultFilter:

    def filter(self, request, result, filter_chain=None, *args, **kwargs):
        return result


class ResultFilterChain:
    __pos = 0
    __n = 0
    __filter_list = []
    __service = None

    def set_service(self, service):
        self.__service = service

    def add_filter(self, filter_config):
        self.__filter_list.append(filter_config)
        self.__n += 1

    def sort(self):
        self.__filter_list = sorted(self.__filter_list, key=lambda x: x['order'])

    def do_filter(self, request, result, *args, **kwargs):
        if self.__pos < self.__n:
            filter_config = self.__filter_list[self.__pos]
            self.__pos += 1
            result = filter_config["filter"].filter(request, result, filter_chain=self, *args, **kwargs)
        elif self.__service:
            result = self.__service(result, *args, **kwargs)
        return result


default_filter_chain = ResultFilterChain()


def filter_register(name="__default", order=9999):
    chain = ClassHolder().get(ResultFilterChain, default=default_filter_chain)

    def do(obj):
        if not isinstance(obj, ResultFilter):
            raise ServiceError("filter instance type error")
        chain.add_filter(dict(filter=obj, order=order))
        chain.sort()

    return class_register(name=name, after_callback=do)


@doublewrap
# def check_request_params(*deco_params,serialize_cls=None):
def check_request_params(func, *deco_params, serialize_cls=None, auth=True, construct=True):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        # print(deco_params)
        try:
            params = read_parm(request)
            for one in deco_params:
                if one not in params:
                    raise ParamLostError(param=one)
                kwargs[one] = params[one]
            for one in params:
                if one not in kwargs:
                    kwargs[one] = params[one]
            if serialize_cls is not None:
                kwargs = serialize_cls().load(kwargs)
            service_func = func
            if auth:
                service_func = check_auth()(func)
            result = service_func(*args, **kwargs)
            result = copy.copy(ClassHolder().get(ResultFilterChain, default=default_filter_chain)).do_filter(request, result,
                                                                                                  *args,
                                                                                                  **kwargs)
            extra_dict = dict()
            if isinstance(result, tuple):
                extra_dict.update(result[1])
                result = result[0]
            return construct_result(data=result, **extra_dict) if construct else result
        except Exception as e:
            method = request.method
            url = request.url
            logger.error('{} {} {}'.format(method, url, kwargs))
            logger.error(traceback.format_exc())
            if isinstance(e, (ViewError, ServiceForViewError)):
                return e.resp
            if isinstance(e, BankFeignError):
                return construct_result(ErrorCode.BANK_FEIGN_ERROR, message=INNER_ERROR_STRING)
            if isinstance(e, CountiFeignError):
                return construct_result(ErrorCode.COUNTI_FEIGN_ERROR, message=INNER_ERROR_STRING)
            if isinstance(e, CountiValidationError):
                return construct_result(ErrorCode.COUNTI_VALIDATION_ERROR, message=INNER_ERROR_STRING)
            return construct_result(ErrorCode.SYSTEM_BUG_ERROR, message=INNER_ERROR_STRING)

    return wrap

    # return wrapper


if __name__ == "__main__":
    start_t = time.time()
    a=ClassHolder().get(ResultFilterChain, default=default_filter_chain)
    a.add_filter({"filter":ResultFilter(),"order":1})
    a.do_filter(None,None)
    b=copy.copy(ClassHolder().get(ResultFilterChain, default=default_filter_chain))
    pass

    print("use time: %s" % (time.time() - start_t))
