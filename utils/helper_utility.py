
import json
class HelperUtility:

    """A utility class providing helper functions for various tasks."""

    @staticmethod
    def read_data_from_json(file_path: str) -> dict:
        """Reads data from a JSON file and returns it as a dictionary."""
        import json
        with open(file_path, 'r') as file:
            return json.load(file)
        
    @staticmethod
    def get_test_data(test_case_id, page_key, file_path="resourses/test_data.json"):
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            print(f"Data loaded from {file_path}: {data}")
            print(data.get(page_key, []))
            if page_key not in data:
                raise ValueError(f"Page key '{page_key}' not found in the data.")
            for item in data[page_key]:
                if test_case_id in item:
                    return item[test_case_id]
            raise ValueError(f"Test case '{test_case_id}' not found under '{page_key}'.")
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{file_path}' not found.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON: {str(e)}")


    @staticmethod
    def format_string(input_string: str) -> str:
        """Formats the input string by stripping whitespace and converting to lowercase."""
        return input_string.strip().lower()

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Checks if the provided email is valid."""
        import re
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def generate_unique_id() -> str:
        """Generates a unique identifier."""
        import uuid
        return str(uuid.uuid4())
    
    @staticmethod
    def assert_for_text_conatins(actual_text: str, expected_text: str):
        """
        Asserts that the actual text contains the expected text.
        Args:
            actual_text (str): The text to check.
            expected_text (str): The text that should be contained in the actual text.
        """
        assert expected_text in actual_text, f"Expected '{expected_text}' to be in '{actual_text}'"
    


if __name__ == "__main__":
    # Example usage of HelperUtility
    helper = HelperUtility()
    print(helper.get_test_data("tc_001", "my_account_page"))
   
   