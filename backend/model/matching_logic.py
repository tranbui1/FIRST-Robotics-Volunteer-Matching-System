from .response import *
from .keywords import *
import pandas as pd
import re

data = "/Users/chansoon/Downloads/Matching Logic - Sheet1.csv"

class Matches:
    def __init__(self, student_status, data_path=None, dataset=None):
        self.index = -1 # Start a negative because we immediately increment

        if not dataset:
            self.df = pd.read_csv(data_path)
            self.all_role_names = self.df["role_name"].tolist()

            # Initialize dataset with booleans converted
            self.dataset = self.create_dataset(convert_booleans=True)
            
        # If a dataset is directly provided, used primarily for testing
        else:
            self.dataset = dataset
            
        # Create a scoreboard to keep track of the best match
        self.all_role_scoreboard = {role["role_name"] : 0 for role in self.dataset}
        
        self.eliminated_roles = set()

        # # TODO: integrate age_exception_datasets in the future if needed
        # self.age_exception_dataset = self.create_special_dataset("age_exception_allowed")

        self.student_status = student_status

    def create_dataset(self, convert_booleans: bool = False) -> list[dict]:
        """
        Converts a pandas dataframe into a dataset (list of dicts), 
        with an option to convert string booleans into actual 
        booleans.

        Args: 
            - convert_booleans (bool, optional): If True, converts 
                string representations of booleans into Pythonic 
                booleans. Defaults to False.

        Returns: 
            - list[dict]: Dataset as a list of dictionaries, each 
                representing a row.
        """
        df_copy = self.df.copy()

        if convert_booleans:
            target = {"true", "false"}
            df_copy = df_copy.map(
                lambda word: word.lower() if isinstance(word, str) \
                and word.lower() in target else word
            )
            df_copy.replace({"true": True, "false": False}, inplace=True)

        return df_copy.to_dict(orient="records")

    def create_special_dataset(self, attribute: str) -> list[dict]:
        """
        Filters the dataset to include only rows where the 
        specified attribute is truthy.

        Args:
            - attribute (str): The attribute to filter on.

        Returns:
            - list[dict]: Filtered dataset.

        Raises:
            - ValueError: If the attribute is not present 
                in the dataset.
        """
        if attribute not in self.dataset[0].keys():
            raise ValueError(f"{attribute} is not an attribute in the dataset.")

        return [role for role in self.dataset if role.get(attribute)]

    def eliminate_role(self, role_name: str) -> None:
        """
        Eliminates a role from consideration by adding it 
        to the eliminated set. Keep the score for fallback 
        purposes.
        
        Args:
            - role_name (str): The name of the role to 
                "eliminate"
        """
        self.eliminated_roles.add(role_name)

    def get_active_roles(self) -> list[dict]:
        """
        Returns only the roles that haven't been eliminated.
        
        Returns:
            - list[dict]: Dataset filtered to exclude 
                eliminated roles.
        """
        return [role for role in self.dataset if role["role_name"] not in self.eliminated_roles]

    def extract_numerical_value(self, raw_str: str) -> int | float:
        """
        Extracts the first continous numerical value from 
        a string. Supports extraction of ints, fractions, 
        and decimals, which are all either returned as ints 
        or floats. Can handle negative values.

        Args:
            - raw_str (str): The string to extract a number 
                from.

        Returns:
            - int | float: The extracted value or -1 for any 
                failures.

        Raises:
            - ValueError: If the string does not contain at 
                least one digit.
            - ZeroDivisionError: If the fraction extraction's 
                denominator is 0.
        """
        if not raw_str or pd.isna(raw_str):
            return -1
            
        raw_str = str(raw_str).strip()

        # Ensure that the string contains at least one digit
        if not any(digit.isnumeric() for digit in raw_str):
            return -1  # Return -1 instead of raising error

        # Extract fractions
        fraction_match = re.search(r"(-?\d+)\s*/\s*(\d+)", raw_str)
        if fraction_match:
            numerator, denominator = fraction_match.groups()

            if int(denominator) == 0:
                return -1  # Return -1 instead of raising error

            return float(numerator) / float(denominator)

        # Extract decimals
        decimal_match = re.search(r"-?\d+\.\d+", raw_str)
        if decimal_match:
            return float(decimal_match.group())
        
        # Extract ints 
        int_match = re.search(r"-?\d+", raw_str) 
        if int_match:
            return int(int_match.group())

        return -1 

    def assess_age(
        self, 
        dataset: list[dict], 
        age: int, 
        eliminate_unqualified: bool = False
    ) -> None:
        """
        Increment role scores if the user's age meets role 
        minimum age requirements or if student status applies. 
        Optionally eliminates roles that don't meet age 
        requirements, BUT respects age exceptions.

        Args:
            - dataset (list[dict]): The dataset containing 
                role dictionaries with minimum age information.
            - age (int): The user's age to compare against role 
                minimum age requirements.
            - eliminate_unqualified (bool): If True, eliminates 
                roles that don't meet age requirements (unless 
                age exceptions are allowed).

        Returns:
            - None: Updates self.all_role_scoreboard in place by 
                incrementing role scores based on the age criteria.

        Raises:
             -TypeError: If age is not an int and student_status 
                is not a bool.
        """
        if not isinstance(age, int):
            raise TypeError("Input age is not type int.")
        
        if not isinstance(self.student_status, bool):
            raise TypeError("Input student status is not type boolean.")

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
                age_min = self.extract_numerical_value(age_min_raw)
            
            # Get a safe age preference
            if age_pref_raw:
                if str(age_pref_raw).isnumeric():
                    age_pref = int(age_pref_raw)
                else:
                    age_pref = self.extract_numerical_value(age_pref_raw)
            else:
                age_pref = False # Default age preference value

            # Check if role should be eliminated
            age_qualified = False
            
            if isinstance(age_min, int) and age_min <= age:
                age_qualified = True
                if not age_pref:
                    self.all_role_scoreboard[role_name] += 5
                elif age_pref and age_pref > age:
                    self.all_role_scoreboard[role_name] += 3
            
            # Check student status qualification
            if self.student_status and age_min == "Students":
                age_qualified = True
                self.all_role_scoreboard[role_name] += 5
            
            # IMPORTANT: Only eliminate if not qualified AND elimination is enabled 
            # AND age exceptions are NOT allowed for this role
            if eliminate_unqualified and not age_qualified:
                age_exception_allowed = role.get("age_exception_allowed", False)
                
                if not age_exception_allowed:
                    self.eliminate_role(role_name)
                else:
                    # Age exception is possible, don't eliminate but give lower score
                    # This role stays in consideration but gets a penalty
                    self.all_role_scoreboard[role_name] -= 3
    
    def assess_physical_ability(
            self, 
            dataset: list[dict], 
            response: PreferenceResponse, 
            eliminate_unqualified: bool = False
        ) -> None:
        """
        Increments score roles if the user's response indicate 
        that they would prefer roles with physical activity. 
        Optionally eliminates roles that don't match physical 
        requirements.

        Args:
            - dataset (list[dict]): The dataset containing 
                role dictionaries with physical ability information.
            - response (PreferenceResponse): The user's response, 
                either yes, no, or no preference.
            - eliminate_unqualified (bool): If True, eliminates roles 
                that don't match physical requirements.

        Returns:
            - None: Updates all self.all_roles_scoreboard that 
                align with the user's response.

        NOTE: Question relating to this function would be something 
        like "Do you prefer roles with physical activity?"
        """
        if response.no_pref:
            return
        
        for role in dataset:
            role_name = role["role_name"]

            if response.yes:
                if role["physical_req"]:
                    self.all_role_scoreboard[role_name] += 5
                elif eliminate_unqualified and not role["physical_req"]:
                    # User wants physical roles but this role isn't physical
                    self.eliminate_role(role_name)
            elif response.no:
                if not role["physical_req"]:
                    self.all_role_scoreboard[role_name] += 5
                elif eliminate_unqualified and role["physical_req"]:
                    # User doesn't want physical roles but this role is physical
                    self.eliminate_role(role_name)

    def assess_standing_ability(
            self, dataset: list[dict], 
            response: PreferenceResponse, 
            eliminate_unqualified: bool = False
        ) -> None:
        """ 
        Assesses and optionally eliminates roles based on 
        standing requirements. Checks if "stand" or "walk" appears 
        in the physical_req field.
        
        Args:
            - dataset (list[dict]): The dataset containing role 
                dictionaries.
            - response (PreferenceResponse): User's ability/preference 
                for standing.
            - eliminate_unqualified (bool): If True, eliminates 
                roles that require standing when user cannot stand.
        
        Note: question would be like "Are you able to stand for long 
        periods of time?"
        """
        for role in dataset:
            role_name = role["role_name"]
            
            # Check if physical_req contains "stand" or "walk"
            physical_req = role.get("physical_req", "")
            requires_standing = False
            
            if isinstance(physical_req, str):
                physical_req_lower = physical_req.lower()
                requires_standing = "stand" in physical_req_lower or "walk" in physical_req_lower
            
            if response.no and requires_standing and eliminate_unqualified:
                # User cannot stand but role requires standing/walking
                self.eliminate_role(role_name)
            elif response.yes and requires_standing:
                # User can stand and role requires it
                self.all_role_scoreboard[role_name] += 3

    def assess_moving_ability(
        self, 
        dataset: list[dict], 
        response: PreferenceResponse, 
        eliminate_unqualified: bool = False
    ) -> None:
        """ 
        Assesses and optionally eliminates roles based on 
        moving requirements. Checks if movement-related terms 
        appear in the physical_req field.
        
        Args:
            - dataset (list[dict]): The dataset containing role     
                dictionaries.
            - response (PreferenceResponse): User's ability/preference 
                for moving.
            - eliminate_unqualified (bool): If True, eliminates 
                roles that require moving when user cannot move.
        
        Note: question would be like "Are you able to move for 
        long periods of time?"
        """
        for role in dataset:
            role_name = role["role_name"]
            
            # Check if physical_req contains movement-related terms
            physical_req = role.get("physical_req", "")
            requires_moving = False
            
            if isinstance(physical_req, str):
                physical_req_lower = physical_req.lower()
                # Check for various movement-related terms
                movement_terms = ["move", "walk", "run", "carry", "lift", "transport", "stand"]
                requires_moving = any(term in physical_req_lower for term in movement_terms)
            
            if response.no and requires_moving and eliminate_unqualified:
                # User cannot move but role requires moving
                self.eliminate_role(role_name)
            elif response.yes and requires_moving:
                # User can move and role requires it
                self.all_role_scoreboard[role_name] += 3
    
    def parse_time_commitment(self, time_commitment: str) -> int | float:
        """
        Parses time commitment from input, extracting numbers
        from a string. Handles fractional days and hours, which 
        are all converted into days. A day is defined to be 8 
        hours.

        Args:
            - time_commitment (str): A string containing text
                about time commitment.

        Returns:
            - int | float: The role's time commitment in days.

        Raises:
            TypeError: If input is not a string.
            ValueError: If input is missing or contains invalid 
                time commitment data.
        
        NOTE: Time commitment is expected to either be in days
        or hours format.
        """
        if not time_commitment or pd.isna(time_commitment):
            return 0  # Default to 0 for missing data

        time_commitment = str(time_commitment).strip()
        
        # Handle special cases
        if not time_commitment or time_commitment.lower() in ['varies', 'variable', 'tbd', 'to be determined']:
            return 0  # Default to 0 for variable commitments

        # Handle the case that the input is in the hours format
        in_hours = False
        if "hours" in time_commitment.lower() or "hr" in time_commitment.lower():
            in_hours = True

        time_extracted = self.extract_numerical_value(time_commitment)

        if time_extracted == -1 or time_extracted <= 0:
            return 0  # Default to 0 for invalid extractions

        return time_extracted if not in_hours else time_extracted / 8

    def assess_availability(
        self, 
        dataset: list[dict], 
        availability: AvailabilityResponse, 
        eliminate_unqualified: bool = False
    ) -> None:
        """
        Increments role scores based on the input user availability 
        and each role's minimum time commitment. Optionally 
        eliminates roles that exceed user's availability.

        Args:
            - dataset (list[dict]): The dataset containing role 
                dictionaries with time commitment information.
            - availability (AvailabilityResponse): The user's 
                maximum availability. Represented in bools and 
                either an int or float of the available days if 
                applicable.
            - eliminate_unqualified (bool): If True, eliminates 
                roles that exceed user's availability.

        Returns:
            - None: Updates all self.all_roles_scoreboard that 
                align with the user's availability.
        """
        if availability.defined:
            assert(availability.days is not None), "Days of availability is not defined"

        for role in dataset:
            role_name = role["role_name"]
            
            raw_time_commitment = role["time_commitment"]
            
            # Increment roles that vary in time commitment indiscriminately
            if raw_time_commitment.isalpha() and "varies" in raw_time_commitment.lower():
                time_commitment = 0
            else:
                time_commitment = self.parse_time_commitment(raw_time_commitment)

            if availability.completely:
                # User is available for all days, so all roles qualify
                self.all_role_scoreboard[role_name] += 5
            elif availability.defined:
                if availability.days >= time_commitment:
                    self.all_role_scoreboard[role_name] += 5
                elif eliminate_unqualified and availability.days < time_commitment:
                    # User doesn't have enough availability for this role
                    self.eliminate_role(role_name)

    def assess_working_pref(
        self, 
        dataset: list[dict], 
        pref: MultiChoiceResponse,
        eliminate_unqualified: bool = False
    ) -> None:
        """
        Increments role scores based on user input on whether 
        they prefer working behind the scenes (BTS) or front-facing 
        (working with volunteers/students). Optionally eliminates
        roles that don't match preference.

        Args:
            - dataset (list[dict]): The dataset containing role 
                dictionaries with working preference information.
            - pref (MultiChoiceResponse): The user's working 
                preference.
            - eliminate_unqualified (bool): If True, eliminates 
                roles that don't match user's working preference.

        Returns:
            - None: Updates all self.all_roles_scoreboard that 
                align with the user's preference.

        NOTE: Questions to call this method will be along the 
        lines of "Do you prefer working in roles behind the scenes, 
        front-facing, or no preference?"
        """
        valid = ["NO_PREF", "BTS", "FRONT"]
        if pref.choice not in valid:
            raise ValueError(f"Invalid user input: {pref.choice}, expected "
                f"a response from {valid}") 

        for role in dataset:
            role_name = role["role_name"]
            
            working_pref = role["work_pref"]

            if pref.choice == "NO_PREF":
                # No preference, so all roles get equal treatment
                continue
            elif pref.choice == "BTS":
                if working_pref == "BTS":
                    self.all_role_scoreboard[role_name] += 5
                elif eliminate_unqualified and working_pref == "FRONT":
                    # User wants BTS but role is front-facing
                    self.eliminate_role(role_name)
            elif pref.choice == "FRONT":
                if working_pref == "FRONT":
                    self.all_role_scoreboard[role_name] += 5
                elif eliminate_unqualified and working_pref == "BTS":
                    # User wants front-facing but role is BTS
                    self.eliminate_role(role_name)
            
    def assess_leadership_pref(
        self, 
        dataset: list[dict], 
        response: PreferenceResponse,
        eliminate_unqualified: bool = False):
        """
        Increments role scores based on the user's preference for
        roles involving leadership responsibilities.

        Args:
            - dataset (list[dict]): The dataset containing role 
                dictionaries with leadership information.
            - response (PreferenceResponse): The user's leadership
                preference stored in yes, no, and no preference
                booleans.
           - eliminate_unqualified (bool): If True, eliminates 
                roles that don't match user's leadership preference.
        
        Returns:
            - None. Updates the role scoreboard based on the 
                user and role's leadership attributes.
        """
        for role in dataset:
            role_name = role["role_name"]
            
            leadership = role.get("leadership_pref", False)

            # Ensure that our data is formatted correctly
            if not isinstance(leadership, bool):
                raise TypeError("Input type for leadership is not boolean type")

            # User prefers roles with leadership
            if response.yes and leadership:
                self.all_role_scoreboard[role_name] += 5

            # User prefers roles without leadership
            elif response.no and not leadership:
                self.all_role_scoreboard[role_name] += 5

            elif response.no_pref:
                return

            # Optional elimination based on eliminate_unqualified
            if eliminate_unqualified:
                if response.no and leadership:
                    self.eliminate_role(role_name)

                # Eliminate roles without leadership when the user prefers it
                elif response.yes and not leadership: 
                    self.eliminate_role(role_name)

    def parse_prior_first_experience(self, raw_value: str | bool) -> str:
        """
        Parses the prior_first_exp field to standardize 
        different formats.
        
        Args:
            raw_value: The raw value from the prior_first_exp 
            field.
            
        Returns:
            str: One of "REQUIRED", "PREFERRED", "FALSE", or 
            "UNKNOWN"
        """
        if not raw_value:
            return "UNKNOWN"

        if not isinstance(raw_value, str) and not isinstance(raw_value, bool):
            raise TypeError("Cannot parse user input for prior experience "
                    f"as it is not str or bool")

        # Bool
        if isinstance(raw_value, bool):
            if raw_value:
                return "REQUIRED"
            else:
                return "FALSE"
        
        # Str 
        if isinstance(raw_value, str):
            raw_value = raw_value.strip().upper()
            
            if "FALSE" in raw_value:
                return "FALSE"
            elif "TRUE" in raw_value:
                return "REQUIRED"
            elif "PREFERRED" in raw_value:
                return "PREFERRED"

            # In the case that the raw value is missing above keywords
            req_keywords = ["must", "required", "years", "prior years",
                "minimum", "experience required"]

            pref_keywords = ["recommended", "helpful", "knowledge of",
                "general knowledge", "understanding of"]
            
            if any(indicator in raw_value.lower() for indicator in req_keywords):
                return "REQUIRED"

            if any(indicator in raw_value.lower() for indicator in pref_keywords):
                return "PREFERRED"

        return "UNKNOWN" # Last case

    def assess_prior_first_experience(self, dataset: list[dict], response: bool):
        """
        Increments role scores based on the user's prior 
        FIRST experience.

        Args:
            - dataset (list[dict]): The dataset containing role 
                dictionaries with prior FIRST experience information.
            - response (bool): The user's prior experience with
                FIRST, either True or False for experience and no
                experience respectively.
        
        Returns:
            - None. Updates the role scoreboard based on the user's
                prior experience and the role's requirements.

        """
        if not isinstance(response, bool):
            raise TypeError("User response for prior experience is not a bool")

        for role in dataset:
            role_name = role["role_name"]
            prior_experience = self.parse_prior_first_experience(role["prior_first_exp"])

            # User has prior first experience
            if response:     
                if prior_experience == "REQUIRED":
                    self.all_role_scoreboard[role_name] += 8
                elif prior_experience == "PREFERRED":
                    self.all_role_scoreboard[role_name] += 5
                else:
                    self.all_role_scoreboard[role_name] += 3

            # User does not have prior first experience
            elif not response:
                if prior_experience == "FALSE":
                    self.all_role_scoreboard[role_name] += 5
                elif prior_experience == "PREFERRED":
                    self.all_role_scoreboard[role_name] -= 2
        
    def parse_knowledge_of_game(self, raw_value: str | bool) -> str:
        """
        Parses the basic_game_knowledge in the dataset to 
        standardize formats.

        Args: 
            - raw_value: The raw value from the target field

        Returns:
            - str: One of "NONE", "LIMITED", "AVERAGE", 
            "THOROUGH", or "UNKNOWN"
        """
        if not raw_value:
            return "UNKNOWN"
        
        if not isinstance(raw_value, str) and not isinstance(raw_value, bool):
            raise TypeError("Cannot parse user input for game knowledge \
                    as it is not str or bool")

        # Bool
        if isinstance(raw_value, bool):
            if raw_value:
                return "LIMITED"
            else:
                return "NONE"

        # Str
        if isinstance(raw_value, str):
            raw_value = raw_value.strip()
            raw_value_upper = raw_value.upper()
            raw_value_lower = raw_value.lower()

            # Direct string matches
            if "FALSE" in raw_value_upper:
                return "NONE"

            # Ensure that only True is present 
            elif "TRUE" in raw_value_upper and len(raw_value_upper) == 4:
                return "LIMITED"

            # Keywords for mapping levels
            thorough_keywords = ["thorough", "advanced", "in-depth"]
            average_keywords = ["average", "familiar", "general knowledge"]
            limited_keywords = ["can learn", "basic", "some knowledge"]

            if any(keyword in raw_value_lower for keyword in thorough_keywords):
                return "THOROUGH"
            elif any(keyword in raw_value_lower for keyword in average_keywords):
                return "AVERAGE"
            elif any(keyword in raw_value_lower for keyword in limited_keywords):
                return "LIMITED"

        # If no matches, return unknown
        return "UNKNOWN"

    def assess_knowledge_of_game(
        self, 
        dataset: list[dict], 
        response: str, 
        eliminate_unqualified: bool = False
    ):
        """
        Increment role scores based on the user's knowledge 
        of the FIRST Robotics Competition and game. Optionally 
        eliminates roles that require more knowledge than the 
        user has.

        Args:
            - dataset (list[dict]): The dataset containing role 
                dictionaries
            - response (str): User's game knowledge level ("NONE", 
                "LIMITED", "AVERAGE", "THOROUGH")
            - eliminate_unqualified (bool): If True, eliminates 
                roles that require more knowledge than the user has

        Returns:
            - None. Increments appropriate roles and optionally 
                eliminates unqualified ones.

        NOTE: Question relating to this function takes the form 
        of "How much knowledge do you have of FIRST's competition 
        and game rules?" 
            - Answers: "NONE", "LIMITED", "AVERAGE", "THOROUGH"
        """
        if not isinstance(response, str):
            raise TypeError("User response for game knowledge is not a string")

        # Define knowledge hierarchy (lowest to highest)
        knowledge_hierarchy = ["NONE", "LIMITED", "AVERAGE", "THOROUGH"]
        
        try:
            user_level = knowledge_hierarchy.index(response)
        except ValueError:
            raise ValueError(f"Invalid response: {response}. Must be one of {knowledge_hierarchy}")

        for role in dataset:
            role_name = role["role_name"]
            
            game_knowledge = self.parse_knowledge_of_game(role["basic_game_knowledge"])
            
            # Handle unknown or invalid game knowledge requirements
            if game_knowledge == "UNKNOWN":
                continue
            
            try:
                required_level = knowledge_hierarchy.index(game_knowledge)
            except ValueError:
                # If we can't parse the required level, skip scoring
                continue
            
            # Check if user meets the minimum requirement
            if user_level >= required_level:
                if response == game_knowledge:
                    # Exact match - highest score
                    self.all_role_scoreboard[role_name] += 8
                else:
                    # User has more knowledge than required - good but not perfect
                    self.all_role_scoreboard[role_name] += 5
            else:
                # Eliminate roles that require more knowledge than user has
                if eliminate_unqualified:
                    self.eliminate_role(role_name)
    
    def get_top_skill_category(self, skill_data: str | bool, keywords: dict) -> str | None:
        """
        Helper method to extract top skill category from role 
        data.
        
        Args:
            skill_data: Either a string containing skills or 
                a boolean.
            keywords: Dictionary of keywords for skill categorization.
        
        Returns:
            Top skill category as string, or None if no 
                skills found.
        """
        if isinstance(skill_data, bool):
            if not skill_data:
                return "NONE"
            else:
                raise ValueError("Data input for requirement checking is the "
                            "unspecified bool True when specified require skills are needed.")
    
        categorizer = RegexSkillCategorizer(keywords)
        role_skills = categorizer.categorize_skills(skill_data)
        return categorizer.get_top_category(role_skills)

    def assess_requirements_general(
        self, 
        dataset: list[dict], 
        req: str,
        keywords: dict,
        responses: set[str], 
        eliminate_unqualified: bool = False
    ) -> None:
        """
        Assess required skills for roles with optional 
        elimination.

        Args:
            - dataset (list[dict]): The dataset containing role 
                dictionaries
            - req (str): A column name from the original data file
                to be assessed.
            - keywords (dict): Words associated with a certain
                requirement used to classify a role's requirements. 
            - responses (set[str]): The user's response to the
                question. Can contain multiple choices. Defaults to
                "NONE"
            - eliminate_unqualified (bool): If True, eliminates 
                roles that require more qualifications than the user 
                has.

        Returns:
            - None. Updates the role scoreboard according to the
                user's qualifications and the role's requirements.
        
        NOTE: Front end input contains drop down menu with 
        responses ranging from the options dictated in 
        keywords.py
        """
        if not isinstance(responses, set):
            raise TypeError(f"Invalid user input for required skills. Expects a "
                        f"set but input is a {type(responses)} instead")

        responses.add("NONE")

        for role in dataset:
            role_name = role["role_name"]

            req_skill = role[req]
            top_req_skill = self.get_top_skill_category(req_skill, keywords)
            
            if not top_req_skill:
                continue

            if top_req_skill in responses:
                self.all_role_scoreboard[role_name] += 8

            # Optional elimination of roles if it requires skills the
            # user does not have
            if eliminate_unqualified:
                if top_req_skill not in responses:
                    self.eliminate_role(role_name)

    def assess_pref_experience(
        self, 
        dataset: list[dict], 
        req: str,
        keywords: dict,
        responses: set[str]
    ):
        """
        Assess preferred experience for roles - only 
        increments scores, never eliminates.

        Args:
            - dataset (list[dict]): The dataset containing role 
                dictionaries
            - req (str): A column name from the original data file
                to be assessed.
            - keywords (dict): Words associated with a certain
                preference used to classify a role's preferences. 
            - responses (set[str]): The user's response to the
                question. Can contain multiple choices. Defaults 
                to "NONE"

        Returns:
            - None. Updates the role scoreboard according to the
                user's qualifications and the role's preferences
                for experience.
        
        NOTE: Front end input contains drop down menu with 
        responses ranging from the options dictated in 
        keywords.py
        """
        if not isinstance(responses, set):
            raise TypeError(f"Invalid user input for preferred experience. Expects a "
                        f"set but input is a {type(responses)} instead")

        responses.add("NONE")

        for role in dataset:
            role_name = role["role_name"]

            req_skill = role[req]
            top_req_skill = self.get_top_skill_category(req_skill, keywords)
            
            if not top_req_skill:
                continue

            if top_req_skill in responses:
                self.all_role_scoreboard[role_name] += 3

    def next_assessment(self, data: dict, eliminate_unqualified=False):
        self.index += 1

        assessment = [
            match.assess_age,
            match.assess_physical_ability,
            match.assess_availability,
            match.assess_working_pref,
            match.leadership_pref,
            match.assess_prior_first_experience, 
            match.assess_knowledge_of_game, 
            match.assess_requirements_general,
            match.assess_requirements_general
        ]

        curr_assessment = assessment[self.index]
        # Ineffective, currently reconstructs params every function call when not necessary
        params = construct_params(match.dataset, data) 
        curr_params = params[data["question_id"]]

        curr_assessment(**curr_params)

    def construct_params(self, dataset, data):
        params = {
            "age": {
                "dataset": dataset,
                "response": data["answer"],
                "eliminate_unqualified": True
            },
            "physical ability": {
                "dataset": dataset,
                "response": PreferenceResponse(["answer"]),
                "eliminate_unqualified": True
            },
            "availability": {
                "dataset": dataset,
                "response": AvailabilityResponse(["answer"]),
                "eliminate_unqualified": True
            },
            "working preference": {
                "dataset": dataset,
                "response": MultiChoiceResponse(["answer"], {"NO_PREF", "BTS", "FRONT"}),
                "eliminate_unqualified": True
            },
            "leadership preference": {
                "dataset": dataset,
                "response": PreferenceResponse(["answer"]),
                "eliminate_unqualified": True
            },
            "prior first experience": {
                "dataset": dataset,
                "response": ["answer"]  # Boolean, probably True/False
            },
            "knowledge of game": {
                "dataset": dataset,
                "response": ["answer"],  # e.g. "LIMITED"
                "eliminate_unqualified": True
            },
            "required skills": {
                "dataset": dataset,
                "requirement_field": "required_skills",
                "keywords": REQ_SKILLS_KEYWORDS,
                "responses": {["answer"]},  # assuming it's a string like "PROGRAMMING PROFICIENCY"
                "eliminate_unqualified": True
            },
            "required experience": {
                "dataset": dataset,
                "requirement_field": "required_experience",
                "keywords": REQ_EXPERIENCE_KEYWORDS,
                "responses": {["answer"]},
                "eliminate_unqualified": True
            }
        }

        return params

    def get_remaining_roles_count(self) -> int:
        """
        Returns the number of roles still in consideration.
        
        Returns:
            - int: Number of roles not eliminated.
        """
        return len(self.all_role_scoreboard)

    def get_eliminated_roles(self) -> list[str]:
        """
        Returns a list of eliminated role names.
        
        Returns:
            - list[str]: List of eliminated role names.
        """
        return list(self.eliminated_roles)

    def get_best_fit_roles(self, num=3) -> dict:
        """
        Returns the top scoring roles that haven't been 
        eliminated.
        
        Args:
            - num (int): Number of top roles to return.
            
        Returns:
            - list[tuple]: List of (role_name, score) 
                tuples sorted by score.
        """
        remaining_roles = [role["role_name"] for role in match.dataset \
            if role["role_name"] not in match.get_eliminated_roles()]
        num_top_roles = len(remaining_roles)

        if num_top_roles > 3:
            result = {"Best fit roles": ", ".join(remaining_roles[:num])}

        # If there isn't enough best fit roles (3), recommend the next best roles
        if num_top_roles < 3:
            next_best = sorted(self.all_role_scoreboard.items(), key=lambda item: item[1], 
                reverse=True)[num_top_roles : num]
            
            result["Next best roles"] = ", ".join(role[0] for role in next_best)
        else:
            result["Next best roles"] = "None"

        return result

    # TODO: special case requiring certification
    # (Machine Shop Staff)

# Example test with elimination
match = Matches(data_path=data, student_status=True)

# Aiming for Field Resetter role
match.assess_age(match.dataset, 14, eliminate_unqualified=True)
match.assess_physical_ability(match.dataset, PreferenceResponse("NO_PREF"), eliminate_unqualified=True)
match.assess_availability(match.dataset, AvailabilityResponse(2), eliminate_unqualified=True)
match.assess_working_pref(match.dataset, MultiChoiceResponse("BTS", {"NO_PREF", "BTS", "FRONT"}), eliminate_unqualified=True)
match.assess_leadership_pref(match.dataset, PreferenceResponse("NO"), eliminate_unqualified=True)
match.assess_prior_first_experience(match.dataset, False)
match.assess_knowledge_of_game(match.dataset, "LIMITED", eliminate_unqualified=True)
match.assess_requirements_general(match.dataset, "required_skills", REQ_SKILLS_KEYWORDS, responses={"PROGRAMMING PROFICIENCY"}, eliminate_unqualified=True)
match.assess_requirements_general(match.dataset, "required_experience", REQ_EXPERIENCE_KEYWORDS, responses={"FIRST SAFETY KNOWLEDGE"}, eliminate_unqualified=True)

print(f"Remaining roles: {match.get_remaining_roles_count()}\n")
print(f"Eliminated roles: {match.get_eliminated_roles()}\n")
remaining_roles = [role["role_name"] for role in match.dataset if role["role_name"] not in match.get_eliminated_roles()]
print(f"Remaining roles: {remaining_roles}")
print("\n ====== RESULTS ======\n")
print(f"Best fit roles: {match.get_best_fit_roles()["Best fit roles"]}. Next best roles: {match.get_best_fit_roles()["Next best roles"]}\n")
