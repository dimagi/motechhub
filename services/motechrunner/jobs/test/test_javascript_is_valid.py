from django.test import SimpleTestCase
from jobs.javascript import javascript_is_valid


class JavascriptIsValidTest(SimpleTestCase):
    def test_bad(self):
        self.assertEqual(javascript_is_valid('(function (message)'), False)

    def test_good(self):
        self.assertEqual(javascript_is_valid('(function (message) {})'), True)
