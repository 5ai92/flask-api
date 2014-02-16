# coding: utf8
from __future__ import unicode_literals
from flask import request
from flaskapi import exceptions
import flaskapi
import io
import unittest

app = flaskapi.FlaskAPI(__name__)


class MediaTypeParsingTests(unittest.TestCase):
    def test_json_request(self):
        kwargs = {
            'method': 'PUT',
            'input_stream': io.BytesIO(b'{"key": 1, "other": "two"}'),
            'content_type': 'application/json'
        }
        with app.test_request_context(**kwargs):
            self.assertEqual(request.data, {"key": 1, "other": "two"})

    def test_no_content_request(self):
        kwargs = {
            'method': 'PUT'
        }
        with app.test_request_context(**kwargs):
            self.assertFalse(request.data)

    def test_invalid_content_type_request(self):
        kwargs = {
            'method': 'PUT',
            'input_stream': io.BytesIO(b'Cannot parse this content type.'),
            'content_type': 'text/plain'
        }
        with app.test_request_context(**kwargs):
            with self.assertRaises(exceptions.UnsupportedMediaType):
                request.data