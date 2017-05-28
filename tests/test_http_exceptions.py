"""Tests for http_exceptions.py"""
from http import HTTPStatus

from aiohttp import http_exceptions


def test_bad_status_line1():
    err = http_exceptions.BadStatusLine(b'')
    assert str(err) == "b''"


def test_bad_status_line2():
    err = http_exceptions.BadStatusLine('Test')
    assert str(err) == 'Test'


def test_http_error_exception():
    exc = http_exceptions.HttpProcessingError(
        code=500, message='Internal error')
    assert exc.code == 500
    assert exc.message == 'Internal error'


def test_http_error_exception_with_http_status():
    exc = http_exceptions.HttpProcessingError(
        code=HTTPStatus.INTERNAL_SERVER_ERROR, message='Internal error')
    assert exc.code == 500
    assert exc.code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert exc.code is HTTPStatus.INTERNAL_SERVER_ERROR
    assert exc.message == 'Internal error'
