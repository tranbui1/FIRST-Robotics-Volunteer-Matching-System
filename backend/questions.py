questions = {
    "age": {
        "question": "What is your age?",
        "type": "number-age",
        "prompt" : "Select your age",
        "id": 0
    },
    "physical_ability": {
        "question": "Do you prefer roles with physical activity?",
        "type": "select-3",
        "options": ["Yes", "No", "No Preference"],
        "id": 1
    },
    "physical_ability_stand": {
        "question": "Are you able to stand for long periods of time?",
        "type": "select-2",
        "options": ["Yes", "No"],
        "id": 2
    },
    "physical_ability_move": {
        "question": "Are you able to move around for long periods of time (e.g., walking, lifting)?",
        "type": "select-2",
        "options": ["Yes", "No"],
        "id": 3
    },
    "availability": {
        "question": "How many days are you available to volunteer for?",
        "type": "number-days",
        "prompt" : "Select your availability",
        "id": 4
    },
    "working_preference": {
        "question": "Do you prefer working behind the scenes, front-facing, or no preference?",
        "type": "select-3",
        "options": ["Behind the scenes", "Front-facing", "No Preference"],
        "id": 5
    },
    "leadership_preference": {
        "question": "Do you prefer roles with leadership responsibilities?",
        "type": "select-3",
        "options": ["Yes", "No", "No Preference"],
        "id": 6
    },
    "prior_experience": {
        "question": "Do you have any prior experience with FIRST, volunteering or participating in the competitions?",
        "type": "select-2",
        "options": ["Yes", "No"],
        "id": 7
    },
    "game_knowledge": {
        "question": "How much knowledge do you have of the FIRST Robotics Competition and game rules?",
        "type": "custom-dropdown",
        "options": ["None", "Limited", "Average", "Thorough"],
        "prompt" : "Select your level of knowledge",
        "id": 8
    },
    "required_skills": {
        "question": "Which of the following required skills do you have?",
        "type": "multiselect",
        "options": [
            "Basic computer literacy",
            "Programming (C++, Java, Python, or LabVIEW)",
            "Photo and video editing",
            "Control systems and diagnostics",
            "Technical writing",
            "Event coordination",
            "FIRST Robotics safety protocol compliance"
        ],
        "prompt" : "Select your skills",
        "id": 9
    },
    "experience": {
        "question": "Which of the following experiences do you have?",
        "type": "multiselect",
        "options": [
            "FIRST Robotics Competition Control System experience",
            "4 years of FIRST Robotics Competition referee experience",
            "2 years of FIRST robot build experience",
            "Event management experience",
            "3 years of Robotics Competition judging experience",
            "Technical inspection experience"
        ],
        "prompt" : "Select your experience",
        "id": 10
    }
}

keys = ["age", "physical_ability", "physical_ability_stand", 
        "physical_ability_move", "availability", "working_preference",
            "leadership_preference", "prior_experience", 
            "game_knowledge", "required_skills", "experience"
        ]

class Questions:
    def get_question(self, question_id):
        if question_id > len(questions) - 1:
            question_id = 0
        return questions[keys[question_id]]

    def get_type(self, question_id):
        return questions[question_id]["type"]

    def get_options(self, question_id):
        return questions[question_id]["options"]