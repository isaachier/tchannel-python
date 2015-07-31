from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from tornado import gen

from . import THRIFT
from tchannel.thrift import serializer


class ThriftArgScheme(object):

    NAME = THRIFT

    def __init__(self, tchannel):
        self._tchannel = tchannel

    @gen.coroutine
    def __call__(self, request=None, headers=None, timeout=None, hostport=None):  # TODO remove hostport here...

        # serialize
        headers = serializer.serialize_headers(headers=headers)
        body = serializer.serialize_body(call_args=request.call_args)

        response = yield self._tchannel.call(
            scheme=self.NAME,
            service=request.service,
            arg1=request.endpoint,
            arg2=headers,
            arg3=body,
            hostport=hostport
        )

        # deserialize
        response.headers = serializer.deserialize_headers(
            headers=response.headers
        )
        body = serializer.deserialize_body(
            body=response.body,
            result_type=request.result_type
        )
        response.body = body.success

        raise gen.Return(response)

    def stream(self):
        pass

    def register(self):
        pass
