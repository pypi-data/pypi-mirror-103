import logging

from unittest import TestCase
from flask_wifiqr.__main__ import app


class TestWifiQREndpoints(TestCase):
    """ Test available flask endpoints
    """
    _multiprocess_can_split_ = True

    def setUp(self):
        super().setUp()
        logging.disable(logging.CRITICAL)

        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        self.client = app.test_client()

        self.assertEqual(app.debug, False)

    def test_that_index_uri_returns_200(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)

    def test_that_index_uri_returns_expected_content(self):
        response = self.client.get('/')

        self.assertIn(b'<title>WifiQR</title>', response.data)

    def test_that_image_uri_returns_200(self):
        response = self.client.get('/qrcode')

        self.assertEqual(response.status_code, 200)

    def test_that_image_uri_returns_expected_content(self):
        response = self.client.get('/qrcode')

        self.assertIn(b'PNG', response.data)
