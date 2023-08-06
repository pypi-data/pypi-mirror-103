# -*- coding: utf-8 -*-
import json
import time
import traceback
from abc import abstractmethod
from datetime import datetime
from typing import Optional, Dict

import pytz
import requests
from flask import current_app
from pydantic import Field
from pydantic.main import ModelMetaclass, BaseModel
from requests import Response
from requests.adapters import HTTPAdapter

from easi_py_common.core.error import ServiceException, RestClientException

HEADER = {'Content-Type': 'application/json; charset=UTF-8'}
DST_MODE_SERVICE = 'service'
DST_MODE_OTHER = 'other'


class ClientRequestData(BaseModel):
    url: str = Field(..., description='url')
    method: str = Field(..., description='method')
    json_data: Optional[Dict] = Field(description='url')
    params: Optional[Dict] = Field(description='url')
    timeout: object = Field(..., description='url')
    other_kwargs: Optional[Dict] = Field(description='url')
    dst: Optional[object] = Field(description='url')
    request_time: int
    request_time_str: str
    response_time: int
    response_time_str: str

    class Config:
        arbitrary_types_allowed = True


class RestClientResponseDecoder:
    @abstractmethod
    def get_data(self, request_data: ClientRequestData, response: Response):
        pass


class ServiceRestClientResponseDecoder(RestClientResponseDecoder):
    def __init__(self, dst_mode=DST_MODE_SERVICE):
        self.dst_mode = dst_mode

    def get_data(self, request_data: ClientRequestData, response: Response):
        dst = request_data.dst
        status_code = response.status_code
        if status_code == 200:
            result = response.json()
            if (
                    isinstance(result, bool)
                    or isinstance(result, int)
                    or isinstance(result, float)
                    or isinstance(result, str)
            ):
                return result
            if self.dst_mode == DST_MODE_SERVICE:
                code = result.get('code', 0)
                if code != 0:
                    raise ServiceException(code=code, msg=result.get('message', ''))
                result = result.get('data')

            if dst and dst.__class__ == ModelMetaclass:
                return dst.parse_obj(result)
            return result

        if 400 <= status_code < 500:
            raise RestClientException(code=status_code, msg='Internal Server Error')
        else:
            raise RestClientException(code=status_code, msg='Internal Server Error')


def _now_log_datetime() -> (int, str):
    return (int(time.time() * 1000),
            datetime.strftime(datetime.now(pytz.timezone('Etc/GMT-8')).replace(tzinfo=None), '%Y.%m.%d %H:%M:%S'))


class LogServiceRestClientResponseDecoder(ServiceRestClientResponseDecoder):
    def __init__(self, dst_mode=DST_MODE_SERVICE):
        super().__init__(dst_mode)
        self.dst_mode = dst_mode

    @abstractmethod
    def success_log(self, request_data: ClientRequestData, response: Response, response_data):
        pass

    @abstractmethod
    def error_log(self, request_data: ClientRequestData, response: Response, exception: Exception):
        pass

    def get_data(self, request_data: ClientRequestData, response: Response):
        try:
            response_data = super().get_data(request_data, response)

            try:
                self.success_log(request_data, response, response_data)
            except Exception as success_log_e:
                current_app.logger.error('success_log: {}\n{}'.format(success_log_e, traceback.format_exc()))

            return response_data
        except Exception as e:
            try:
                self.error_log(request_data, response, e)
            except Exception as error_log_e:
                current_app.logger.error('error_log: {}\n{}'.format(error_log_e, traceback.format_exc()))

            raise e


class RestClient:
    def __init__(self, url, timeout=(5, 5), http_adapter=None, before_request=None,
                 response_decoder: RestClientResponseDecoder = None):
        self.url = url
        if http_adapter is None:
            http_adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=0)
        session = requests.Session()
        session.mount('http://', http_adapter)
        session.mount('https://', http_adapter)

        self.session = session
        self.timeout = timeout
        self.before_request = before_request
        self.response_decoder = response_decoder
        if not self.response_decoder:
            self.response_decoder = ServiceRestClientResponseDecoder(dst_mode=DST_MODE_SERVICE)

    def _get_url(self, uri):
        if 'SERVICE_CLIENT' in current_app.config and 'http' not in self.url:
            service_client_keys = current_app.config['SERVICE_CLIENT']
            self.url = self.url.format(**service_client_keys)
        return self.url + uri

    def get(self, uri, params=None, timeout=None, dst=None, **kwargs):
        if timeout is None:
            timeout = self.timeout
        request_time, request_time_str = _now_log_datetime()
        _url = self._get_url(uri)

        if callable(self.before_request):
            _request_parms = {
                'url': _url,
                'method': 'GET',
                'params': params,
            }
            _kwargs = self.before_request(_request_parms)
            kwargs.update(_kwargs)

        resp = self.session.get(
            _url,
            params=params,
            timeout=timeout,
            **kwargs
        )
        response_time, response_time_str = _now_log_datetime()
        request_data = ClientRequestData(
            url=_url,
            method='GET',
            json_data=None,
            params=params,
            timeout=timeout,
            other_kwargs=kwargs,
            dst=dst,
            request_time=request_time,
            request_time_str=request_time_str,
            response_time=response_time,
            response_time_str=response_time_str,
        )
        return self._do_response(resp, request_data)

    def post(self, uri, json_data=None, params=None, timeout=None, dst=None, request_by_alias: bool = True, **kwargs):
        if timeout is None:
            timeout = self.timeout
        request_time, request_time_str = _now_log_datetime()
        _url = self._get_url(uri)
        data = None
        if json_data:
            data = (json.dumps(json_data.dict(by_alias=request_by_alias))
                    if isinstance(json_data, BaseModel)
                    else json.dumps(json_data))

        if callable(self.before_request):
            _request_parms = {
                'url': _url,
                'method': 'POST',
                'data': data,
                'params': params,
            }
            _kwargs = self.before_request(_request_parms)
            kwargs.update(_kwargs)

        if 'headers' in kwargs:
            kwargs.get('headers').update(HEADER)
        else:
            kwargs['headers'] = HEADER

        resp = self.session.post(
            _url,
            data=data,
            params=params,
            timeout=timeout,
            **kwargs
        )
        response_time, response_time_str = _now_log_datetime()
        request_data = ClientRequestData(
            url=_url,
            method='POST',
            json_data=json_data,
            params=params,
            timeout=timeout,
            other_kwargs=kwargs,
            dst=dst,
            request_time=request_time,
            request_time_str=request_time_str,
            response_time=response_time,
            response_time_str=response_time_str,
        )
        return self._do_response(resp, request_data)

    def put(self, uri, json_data=None, params=None, timeout=None, dst=None, request_by_alias: bool = True, **kwargs):
        if timeout is None:
            timeout = self.timeout
        request_time, request_time_str = _now_log_datetime()
        _url = self._get_url(uri)

        data = None
        if json_data:
            data = (json.dumps(json_data.dict(by_alias=request_by_alias))
                    if isinstance(json_data, BaseModel)
                    else json.dumps(json_data))

        if callable(self.before_request):
            _request_parms = {
                'url': _url,
                'method': 'PUT',
                'data': data,
                'params': params,
            }
            _kwargs = self.before_request(_request_parms)
            kwargs.update(_kwargs)

        if 'headers' in kwargs:
            kwargs.get('headers').update(HEADER)
        else:
            kwargs['headers'] = HEADER

        resp = self.session.put(
            _url,
            data=data,
            params=params,
            timeout=timeout,
            **kwargs
        )
        response_time, response_time_str = _now_log_datetime()
        request_data = ClientRequestData(
            url=_url,
            method='PUT',
            json_data=json_data,
            params=params,
            timeout=timeout,
            other_kwargs=kwargs,
            dst=dst,
            request_time=request_time,
            request_time_str=request_time_str,
            response_time=response_time,
            response_time_str=response_time_str,
        )
        return self._do_response(resp, request_data)

    def delete(self, uri, params=None, timeout=None, dst=None, **kwargs):
        if timeout is None:
            timeout = self.timeout

        request_time, request_time_str = _now_log_datetime()

        _url = self._get_url(uri)
        if callable(self.before_request):
            _request_parms = {
                'url': _url,
                'method': 'DELETE',
                'params': 'params',
            }
            _kwargs = self.before_request(_request_parms)
            kwargs.update(_kwargs)

        resp = self.session.delete(
            _url,
            params=params,
            timeout=timeout,
            **kwargs
        )

        response_time, response_time_str = _now_log_datetime()
        request_data = ClientRequestData(
            url=_url,
            method='DELETE',
            json_data=None,
            params=params,
            timeout=timeout,
            other_kwargs=kwargs,
            dst=dst,
            request_time=request_time,
            request_time_str=request_time_str,
            response_time=response_time,
            response_time_str=response_time_str,
        )
        return self._do_response(resp, request_data)

    def _do_response(self, resp, request_data: ClientRequestData):

        return self.response_decoder.get_data(request_data, resp)
