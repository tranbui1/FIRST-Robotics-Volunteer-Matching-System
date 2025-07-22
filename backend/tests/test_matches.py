from matching_logic import Matches, PreferenceResponse, AvailabilityResponse
from test_data import TestData
import pandas as pd
import random
import unittest

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

        self.match_system = Matches(dataset=self.data, student_status=True)

    def test_create_dataset(self):
        # Short test

    # ..... lol i'll write later

    def test_assess_availability(self):
        # Most basic test case


