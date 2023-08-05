import unittest
import pook

from trulioo_sdk.exceptions import *
from trulioo_sdk.configuration import Configuration
from trulioo_sdk.api_client import ApiClient
from trulioo_sdk.api.connection_api import ConnectionApi

BASE_URI = "https://gateway.trulioo.com"


class TestExceptions(unittest.TestCase):
    def setUp(self):
        configuration = Configuration(api_key={"ApiKeyAuth": "test-api-key"})
        self.api = ConnectionApi(api_client=ApiClient(configuration=configuration))

    def test_api_type_error(self):
        with self.assertRaises(ApiTypeError):
            self.api.test_authentication(unknown_kwarg="test")
        error = ApiTypeError("test", path_to_item=[1, "a"])
        assert str(error) == "test at [1]['a']"

    def test_api_key_error(self):
        error = ApiKeyError("test", path_to_item=[1, "a"])
        assert str(error) == "\"test at [1]['a']\""

    @pook.on
    def test_api_exception(self):
        pook.mock(
            url=BASE_URI + "/trial/connection/v1/testauthentication",
            method="GET",
            reply=300,
        )
        try:
            self.api.test_authentication(mode="trial")
        except ApiException as e:
            e.headers = "headers"
            e.body = "body"
            assert str(e) == (
                "(300)\n"
                "Reason: Multiple Choices\n"
                "HTTP response headers: headers\n"
                "HTTP response body: body\n"
            )
        error = ApiException()
        assert str(error) == "(None)\nReason: None\n"

    @pook.on
    def test_not_found_exception(self):
        pook.mock(
            url=BASE_URI + "/trial/connection/v1/testauthentication",
            method="GET",
            reply=404,
        )
        with self.assertRaises(NotFoundException):
            self.api.test_authentication(mode="trial")

    @pook.on
    def test_unauthorized_exception(self):
        pook.mock(
            url=BASE_URI + "/trial/connection/v1/testauthentication",
            method="GET",
            reply=401,
        )
        with self.assertRaises(UnauthorizedException):
            self.api.test_authentication(mode="trial")

    @pook.on
    def test_forbidden_exception(self):
        pook.mock(
            url=BASE_URI + "/trial/connection/v1/testauthentication",
            method="GET",
            reply=403,
        )
        with self.assertRaises(ForbiddenException):
            self.api.test_authentication(mode="trial")

    @pook.on
    def test_service_exception(self):
        pook.mock(
            url=BASE_URI + "/trial/connection/v1/testauthentication",
            method="GET",
            reply=500,
        )
        with self.assertRaises(ServiceException):
            self.api.test_authentication(mode="trial")

    def test_render_path(self):
        assert render_path([1, "a"]) == "[1]['a']"


if __name__ == "__main__":
    unittest.main()
