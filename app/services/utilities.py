import re
from typing import Dict
from icecream import ic


class Data_Cleaner:
    def __init__(self):
        pass

    def create_params(self, form_data: Dict[str, str]) -> Dict[str, str]:
        """Create API Parameters from form data, filtering out empty values.

        Args:
            form_field (Dict[str,str]): _description_

        Returns:
            Dict[str,str]: _description_
        """
        params = {}

        # Define mapping from form fields to API parameters
        # TODO verify I have a way to search all of these
        field_mapping = {
            "city": "by_city",
            "state": "by_state",
            "name": "by_name",
            "type": "by_type",
            "postal_code": "by_postal",
        }

        for form_field, api_param in field_mapping.items():
            value = form_data.get(form_field, "").strip()
            if value:  # Only non-empty values
                params[api_param] = value
        return params

    def create_map_link(self, json_data):
        modified_data = json_data.copy()
        for brewery in modified_data:
            street = brewery["address_1"]
            city = brewery["city"]
            state = brewery["state"]
            postal_code = brewery["postal_code"]
            address = f"{street} {city} {state}, {postal_code}"

            brewery["address"] = address.replace(" ", "+")
        ic(modified_data)
        return modified_data

    def proper_names(self, json_data):
        """
        Converts dictionary keys from underscore_separated format to Title Case format.
        Takes the first element from json_data (assuming it's a list) and transforms
        all dictionary keys by replacing underscores with spaces and converting to
        title case format.
        Args:
            json_data (list): A list containing at least one dictionary element.
                                Only the first element (index 0) will be processed.
        Returns:
            dict: A new dictionary with the same values but with keys converted
                    from underscore_separated format to "Title Case" format.
        Example:
            >>> json_data = [{"first_name": "John", "last_name": "Doe"}]
            >>> result = self.proper_names(json_data)
            >>> print(result)
            {"First Name": "John", "Last Name": "Doe"}
        """

        json_data = json_data[0]

        new_json_data = {}
        for key, value in json_data.items():
            key_new = re.sub(r"[_]+", " ", key).strip().title()
            new_json_data[key_new] = value
        return new_json_data
