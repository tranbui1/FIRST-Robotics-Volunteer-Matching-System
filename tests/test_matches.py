from matching_logic import Matches, PreferenceResponse, AvailabilityResponse
from test_data import TestData
import pandas as pd
import random

class MatchTestUtils:
    def __init__(self, data: list[dicts] = None, data_path: str = None):
        self.data = None

        if data:
            self.data = data

        if isinstance(data_path, str):
            try:
                self.data = pd.read_csv(data_path)
            except error as e:
                print(e)

        if self.data == None:
            self.data = random.choice([TestData.short_test_data, 
                                       TestData.medium_test_data])

        self.match_system = Matches(self.data)

    def test_create_dataset(self):
        # Ensure that the formatting is correct, etc.
        return

    # ..... lol i'll write later

    def test_assess_availability(self):
        # Most basic test case


