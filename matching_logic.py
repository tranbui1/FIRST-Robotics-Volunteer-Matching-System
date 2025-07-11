import pandas as pd
import re

data = "/Users/chansoon/Downloads/Matching Logic - Sheet1.csv"

class Matches():
    def __init__(self, data_path):
        self.data_path = data_path

        # Get all columns
        self.df = pd.read_csv(data_path)
        self.all_role_names = self.df["role_name"].tolist()

        # Create a scoreboard to find the best match
        self.all_role_scoreboard = {role_name : 0 for role_name in self.all_role_names}

        # Initialize a data table (list of dictionaries format)
        self.dataset = self.create_dataset(convert=True)

        # Initialize a data table with roles allowed for age exceptions
        self.age_exception_dataset = self.create_age_exception_dataset()

    def create_dataset(self, convert=False):
        """
        Create a "data table"
        """
        if convert:
            # Convert boolean texts to actual boolean values
            self.df.replace({"TRUE": True, "FALSE": False}, inplace=True)

        # Create a dict-based data table from the given csv file
        data_table = self.df.to_dict(orient="records")

        return data_table
    
    def create_age_exception_dataset(self):
        """
        Create a "data table" with only roles that can be petitioned to lower
        the age requirement.
        """
        age_exception_dataset = []

        for role in self.dataset:
            if role["age_exception_allowed"]: 
                age_exception_dataset.append(role)

        return age_exception_dataset

    def extract_value(self, raw_str):
        """
        Extracts the first continous numerical value from a string. Supports ints and 
        floats, additional decimal conversion support provided for fractions represented 
        by a slash.
        """
        raw_str = raw_str.strip()

        # Ensure that the string contains at least one digit
        if not any(digit.isnumeric() for digit in raw_str):
            return -1

        # Extract fractions
        fraction_match = re.search(r"(\d+)\s*/\s*(\d+)", raw_str)
        if fraction_match:
            numerator, denominator = fraction_match.groups()

            # Prevent division by 0 error
            if denominator == 0:
                return -1

            return float(numerator) / float(denominator)

        # Extract decimals
        decimal_match = re.search(r"\d+.\d+", raw_str)
        if decimal_match:
            return float(decimal_match.group())
        
        # Extract ints 
        int_match = re.search(r"\d+", raw_str)
        if int_match:
            return int(int_match.group())

        return -1

    def assess_age(self, dataset, age, student_status=False):
        """
        Process roles based on the user's input age.
        
        TODO: match the logic and ask about student status
        """
        for role in dataset:
            role_name = role["role_name"]
            age_min_raw = role["age_min"]
            age_pref_raw = role["age_preference"]

            # Get a safe age minimum
            if str(age_min_raw).isnumeric():
                age_min = int(age_min_raw)
            elif age_min_raw == "Students":
                age_min = "Students"
            else:
                # Try to extract as many numbers as possible
                age_min = self.extract_value(age_min_raw)
            
            # Get a safe age preference
            if age_pref_raw:
                if str(age_pref_raw).isnumeric():
                    age_pref = int(age_pref_raw)
                else:
                    age_pref = self.extract_value(age_pref_raw)
            else:
                age_pref = False # Default age preference value

            # Increment each role if the meet the age condition
            if isinstance(age_min, int) and age_min <= age:
                if not age_pref:
                    self.all_role_scoreboard[role_name] += 5
                elif age_pref and age_pref > age:
                    self.all_role_scoreboard[role_name] += 3
            
            # Increment roles with student status if applicable
            if student_status and age_min == "Students":
                self.all_role_scoreboard[role_name] += 5
    
    def assess_physical_ability(self, dataset, response=False):
        """
        Note: question would be something like "Do you prefer roles with
        lots of physical activity?"
        """
        for role in dataset:
            role_name = role["role_name"]

            # Increment roles involving physical activity if the response is positive
            if response:
                if role["physical_req"]:
                    self.all_role_scoreboard[role_name] += 5

    # TODO: implement
    def assess_standing_ability(self):
        """ 
        Note: question would be like "Are you able to stand for long 
        periods of time?"
        """
        return

    # TODO: implement
    def assess_moving_ability(self):
        """ 
        Note: question would be like "Are you able to move for long 
        periods of time?"
        """
        return

    def assess_availability(self, dataset, days):
        """
        Days is defined to be preset options like 0.5 days or 4 days.

        For users, days is the maximum availability.

        NOTE: function implemented with notion that days can also be -1, meaning
        varies, or -2, meaning completely available.

        Function supports deciphering of input decimal days and slash days 
        (slash = using eval).

        Also supports deciphering of hours.
        """
        # Error check to make sure days is valid before working with it
        
        days_value_extracted = self.extract_value(days)
        
        # Convert hours to days if needed
        if "hours" in days:
            days_value_extracted /= 24

        for role in dataset:
            time_commitment = role["time_commitment"]

            time_commitment_extracted = extract_value(time_commitment)

            # Convert hours to days if needed
            if "hours" in time_commitment:
                time_commitment_extracted /= 24

            # TODO: tomorrow
    
    def get_best_fit_roles(self, num=3):
        return sorted(self.all_role_scoreboard.items(), key=lambda item: item[1], reverse=True)[0:num]
        
match = Matches(data)
match.assess_age(match.dataset, 18)
match.assess_physical_ability(match.dataset, True)
print(match.get_best_fit_roles())


    