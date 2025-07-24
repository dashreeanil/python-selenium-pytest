import requests
import allure
from utils.logger_utility import logger

try:
    from jsonschema import validate as jsonschema_validate, ValidationError
except ImportError:
    jsonschema_validate = None
    ValidationError = Exception

class APIUtility:
    """
    Utility class for generic API interactions with logging and Allure steps.
    """

    @allure.step("Send GET request to '{url}'")
    def get(self, url, params=None, headers=None, **kwargs):
        """
        Send a GET request.
        Args:
            url (str): The endpoint URL.
            params (dict, optional): Query parameters.
            headers (dict, optional): Request headers.
            **kwargs: Additional arguments for requests.get.
        Returns:
            Response: requests.Response object.
        """
        try:
            logger.info(f"Sending GET request to {url} with params={params} and headers={headers}")
            response = requests.get(url, params=params, headers=headers, **kwargs)
            logger.info(f"Received response: {response.status_code}")
            allure.attach(str(response.text), name="GET Response", attachment_type=allure.attachment_type.TEXT)
            return response
        except Exception as e:
            logger.error(f"GET request to {url} failed: {e}")
            allure.attach(str(e), name="GET Request Error", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Send POST request to '{url}'")
    def post(self, url, data=None, json=None, headers=None, **kwargs):
        """
        Send a POST request.
        Args:
            url (str): The endpoint URL.
            data (dict, optional): Form data.
            json (dict, optional): JSON body.
            headers (dict, optional): Request headers.
            **kwargs: Additional arguments for requests.post.
        Returns:
            Response: requests.Response object.
        """
        try:
            logger.info(f"Sending POST request to {url} with data={data}, json={json}, headers={headers}")
            response = requests.post(url, data=data, json=json, headers=headers, **kwargs)
            logger.info(f"Received response: {response.status_code}")
            allure.attach(str(response.text), name="POST Response", attachment_type=allure.attachment_type.TEXT)
            return response
        except Exception as e:
            logger.error(f"POST request to {url} failed: {e}")
            allure.attach(str(e), name="POST Request Error", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Send PUT request to '{url}'")
    def put(self, url, data=None, json=None, headers=None, **kwargs):
        """
        Send a PUT request.
        Args:
            url (str): The endpoint URL.
            data (dict, optional): Form data.
            json (dict, optional): JSON body.
            headers (dict, optional): Request headers.
            **kwargs: Additional arguments for requests.put.
        Returns:
            Response: requests.Response object.
        """
        try:
            logger.info(f"Sending PUT request to {url} with data={data}, json={json}, headers={headers}")
            response = requests.put(url, data=data, json=json, headers=headers, **kwargs)
            logger.info(f"Received response: {response.status_code}")
            allure.attach(str(response.text), name="PUT Response", attachment_type=allure.attachment_type.TEXT)
            return response
        except Exception as e:
            logger.error(f"PUT request to {url} failed: {e}")
            allure.attach(str(e), name="PUT Request Error", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Send DELETE request to '{url}'")
    def delete(self, url, headers=None, **kwargs):
        """
        Send a DELETE request.
        Args:
            url (str): The endpoint URL.
            headers (dict, optional): Request headers.
            **kwargs: Additional arguments for requests.delete.
        Returns:
            Response: requests.Response object.
        """
        try:
            logger.info(f"Sending DELETE request to {url} with headers={headers}")
            response = requests.delete(url, headers=headers, **kwargs)
            logger.info(f"Received response: {response.status_code}")
            allure.attach(str(response.text), name="DELETE Response", attachment_type=allure.attachment_type.TEXT)
            return response
        except Exception as e:
            logger.error(f"DELETE request to {url} failed: {e}")
            allure.attach(str(e), name="DELETE Request Error", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Validate response status code is {expected_status}")
    def validate_status_code(self, response, expected_status):
        """
        Validate the response status code.
        Args:
            response (requests.Response): The response object.
            expected_status (int): Expected HTTP status code.
        Returns:
            bool: True if status matches, else False.
        """
        actual_status = response.status_code
        logger.info(f"Validating status code: expected={expected_status}, actual={actual_status}")
        try:
            assert actual_status == expected_status, f"Expected {expected_status}, got {actual_status}"
            return True
        except AssertionError as e:
            logger.error(str(e))
            allure.attach(str(e), name="Status Code Validation Error", attachment_type=allure.attachment_type.TEXT)
            return False

    @allure.step("Get JSON from response")
    def get_json(self, response):
        """
        Get JSON content from a response.
        Args:
            response (requests.Response): The response object.
        Returns:
            dict: Parsed JSON content.
        """
        try:
            json_data = response.json()
            logger.info(f"JSON response: {json_data}")
            return json_data
        except Exception as e:
            logger.error(f"Failed to parse JSON: {e}")
            allure.attach(str(e), name="JSON Parse Error", attachment_type=allure.attachment_type.TEXT)
            raise

    @allure.step("Validate response body contains expected key-value pairs")
    def validate_response_body(self, response, expected_body):
        """
        Validate that the response body contains the expected key-value pairs.
        Args:
            response (requests.Response): The response object.
            expected_body (dict): Dictionary of expected key-value pairs.
        Returns:
            bool: True if all key-value pairs are present and match, else False.
        """
        try:
            json_data = response.json()
            for key, value in expected_body.items():
                assert key in json_data, f"Key '{key}' not found in response body"
                assert json_data[key] == value, f"Value for key '{key}' does not match. Expected: {value}, Actual: {json_data[key]}"
            logger.info("Response body validation passed.")
            return True
        except Exception as e:
            logger.error(f"Response body validation failed: {e}")
            allure.attach(str(e), name="Response Body Validation Error", attachment_type=allure.attachment_type.TEXT)
            return False

    @allure.step("Validate response body contains expected key-value pairs (contains operation)")
    def validate_response_body_contains(self, response, expected_body):
        """
        Validate that the response body contains the expected key-value pairs (using 'in' for values).
        Args:
            response (requests.Response): The response object.
            expected_body (dict): Dictionary of expected key-value pairs or substrings.
        Returns:
            bool: True if all key-value pairs or substrings are present, else False.
        """
        try:
            json_data = response.json()
            for key, value in expected_body.items():
                assert key in json_data, f"Key '{key}' not found in response body"
                assert value in str(json_data[key]), (
                    f"Value for key '{key}' does not contain expected substring. "
                    f"Expected to contain: {value}, Actual: {json_data[key]}"
                )
            logger.info("Response body 'contains' validation passed.")
            return True
        except Exception as e:
            logger.error(f"Response body 'contains' validation failed: {e}")
            allure.attach(str(e), name="Response Body Contains Validation Error", attachment_type=allure.attachment_type.TEXT)
            return False

    @allure.step("Validate response JSON schema")
    def validate_json_schema(self, response, schema):
        """
        Validate the response JSON against a provided schema.
        Args:
            response (requests.Response): The response object.
            schema (dict): JSON schema to validate against.
        Returns:
            bool: True if schema is valid, else False.
        """
        if not jsonschema_validate:
            logger.error("jsonschema package is not installed.")
            allure.attach("jsonschema package is not installed.", name="Schema Validation Error", attachment_type=allure.attachment_type.TEXT)
            return False
        try:
            json_data = response.json()
            jsonschema_validate(instance=json_data, schema=schema)
            logger.info("JSON schema validation passed.")
            return True
        except ValidationError as e:
            logger.error(f"JSON schema validation failed: {e}")
            allure.attach(str(e), name="Schema Validation Error", attachment_type=allure.attachment_type.TEXT)
            return False
        except Exception as e:
            logger.error(f"Schema validation error: {e}")
            allure.attach(str(e), name="Schema Validation Error", attachment_type=allure.attachment_type.TEXT)
            return False