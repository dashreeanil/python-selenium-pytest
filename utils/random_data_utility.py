

class RandomDataUtility:
    """
    Utility class for generating random data.
    """

    @staticmethod
    def generate_random_string(length=10):
        """
        Generate a random string of fixed length.
        :param length: Length of the random string.
        :return: Random string.
        """
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def generate_random_email():
        """
        Generate a random email address.
        :return: Random email address.
        """
        import random
        import string
        domain = ''.join(random.choices(string.ascii_lowercase, k=5))
        return f"{RandomDataUtility.generate_random_string(8)}@{domain}.com"    
    

    def genrerate_random_name(self):
        """
        Generate a random name.
        :return: Random name.
        """
        import random
        first_names = ["John", "Jane", "Alice", "Bob", "Charlie"]
        last_names = ["Smith", "Doe", "Johnson", "Brown", "Williams"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"  
    
    @staticmethod
    def generate_random_number(min_value=1, max_value=100):    
        """
        Generate a random number within a specified range.
        :param min_value: Minimum value of the range.
        :param max_value: Maximum value of the range.
        :return: Random number.
        """
        import random
        return random.randint(min_value, max_value) 
    
    @staticmethod
    def generate_random_date(start_date, end_date):
        """
        Generate a random date between two dates.
        :param start_date: Start date (datetime object).
        :param end_date: End date (datetime object).
        :return: Random date (datetime object).
        """
        import random
        from datetime import timedelta
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        return start_date + timedelta(days=random_days)
    
    @staticmethod
    def generate_random_phone_number():
        """
        Generate a random phone number.
        :return: Random phone number in the format (XXX) XXX-XXXX.
        """
        import random
        area_code = random.randint(100, 999)
        central_office_code = random.randint(100, 999)
        line_number = random.randint(1000, 9999)
        return f"({area_code}) {central_office_code}-{line_number}"
    
    @staticmethod
    def generate_random_address():
        """
        Generate a random address.
        :return: Random address.
        """
        import random
        import string
        street_number = random.randint(1, 9999)
        street_name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
        city = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=5))
        state = ''.join(random.choices(string.ascii_uppercase, k=2))
        zip_code = ''.join(random.choices(string.digits, k=5))
        return f"{street_number} {street_name} St, {city}, {state} {zip_code}"
    

    