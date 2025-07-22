class Response:
    def __init__(self, response: str) -> None:
        self.response = response
        self.parse_response()

    def parse_response(self):
        raise NotImplementedError("Subclasses must implement parse_response() \
                themselves.")

class AvailabilityResponse(Response):
    """
    Parses user response into defined availability and complete 
    availability.
    """  
    def __init__(self, response: str):
        super().__init__(response)
    
    def parse_response(self):
        """
        Parses user response into three class attributes: 

            - self.defined (bool): True if the user provided a 
                specific number of available days.
            - self.completely (bool): True if the user is available 
                for all days.
            - self.days (int | float | None): The number of available 
                days if self.defined is True; otherwise, None.

        NOTE: Function expects self.response to be either a positive int,
        indicating a defined availability, or -1 to indicate complete 
        availability.
        """
        if self.response > 0:
            self.defined = True
            self.completely = False
            self.days = int(self.response)
        elif int(self.response) == -1:
            self.defined = False
            self.completely = True
            self.days = 999
        else:
            raise ValueError(f"Invalid user input: input is {self.response} \
                when it should be an interger > 0 or -1 specifically.")

class PreferenceResponse(Response):
    """
    Parses user response into yes, no, or no preference booleans.
    """
    def __init__(self, response: str):
        super().__init__(response)

    def parse_response(self):
        """
        Parses user response into three booleans indicating truthy 
        yes, no, or no preference. 

        Returns:
            - None. Initializes class attributes to be retrieved.
        """
        # Initialize all attributes to 0
        self.yes = 0
        self.no = 0
        self.no_pref = 0
        
        if self.response == "YES":
            self.yes = 1
        elif self.response == "NO":
            self.no = 1
        elif self.response == "NO_PREF":
            self.no_pref = 1
        else:
            raise ValueError(f"Invalid preference response input value. The \
                value is {self.response} when it should be 'YES', 'NO', \
                'NO_PREF'")

class MultiChoiceResponse(Response):
    """
    Parses a response with multiple categorical choices, such as
    'BTS', 'FRONT', or 'NO_PREF'. Supports arbitrary labeled options.

    Attributes:
        - self.choice (str): The parsed and standardized user choice.
    """
    def __init__(self, response: str, valid_options: set[str]) -> None:
        self.response = response
        self.valid_options = {opt.upper() for opt in valid_options}
        self.choice = self.parse_response()

    def parse_response(self) -> str:
        response_upper = self.response.upper()

        if response_upper in self.valid_options:
            return response_upper
        else:
            raise ValueError(
                f"Invalid option '{self.response}'. "
                f"Expected one of: {', '.join(self.valid_options)}"
            )
