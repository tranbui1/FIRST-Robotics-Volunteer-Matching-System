import re

PREF_EXPERIENCE_KEYWORDS = {
    "FRC CONTROL SYSTEM EXPERIENCE": [
        "frc control system", "hands-on frc control system", "control system experience",
        "diagnostic tools", "first robotics competition control system",
        "control system wiring", "understanding of control system wiring"
    ],
    
    "FIELD MANAGEMENT SYSTEM EXPERIENCE": [
        "field management system", "fms", "game field", "field electronics",
        "field mechanical", "field electrical"
    ],
    
    "FRC REFEREE EXPERIENCE": [
        "frc referee", "referee experience", "prior years of first robotics competition referee",
        "referee", "refereeing"
    ],
    
    "FRC JUDGE EXPERIENCE": [
        "judge", "frc judge", "judge at frc event", "judging experience",
        "years as a judge"
    ],
    
    "ROBOT BUILD EXPERIENCE": [
        "robot build experience", "team robot build experience", "first robot build experience",
        "robot build", "build experience", "current season experience",
        "current season robo build experience"
    ],
    
    "MACHINE SHOP EXPERIENCE": [
        "machine tools", "variety of machine tools", "experience machinist",
        "experienced machinist", "welder experience", "significant machine shop experience",
        "machinist/welder experience"
    ],
    
    "FIRST SAFETY KNOWLEDGE": [
        "first safety principles", "safety principles", "knowledge of first safety",
        "thorough knowledge of first safety"
    ],
    
    "MANAGEMENT/SUPERVISION EXPERIENCE": [
        "supervise", "manage", "evaluate volunteers", "volunteer management",
        "event management", "able to supervise", "supervision experience"
    ],
    
    "GAME RULES KNOWLEDGE": [
        "game rules", "event rules", "safety rules", "game & event rules",
        "game and safety rules", "basic game knowledge", "match process knowledge",
        "basic knowledge of match process", "basic game and match process knowledge"
    ],
    
    "TEAM EXPERIENCE": [
        "team mentors", "team experience", "team match participation",
        "alumni", "team mentor experience"
    ],
    
    "PUBLIC SPEAKING/PRESENTATION EXPERIENCE": [
        "public speaking", "emcee", "first emcee", "prior first emcee",
        "tv experience", "radio experience", "acting experience",
        "tv/radio/acting experience"
    ],
    
    "FACILITY/EVENT KNOWLEDGE": [
        "facility layout", "event layout", "facility and event layout",
        "general knowledge of facility", "general knowledge of first",
        "first robotics competition knowledge", "can learn on site"
    ],
    
    "PIT VOLUNTEER EXPERIENCE": [
        "pit volunteer", "first pit volunteer", "years as first pit volunteer",
        "pit volunteer preferred"
    ]
}

REQ_SKILLS_KEYWORDS = {
    "pv": [
        "computer skills", "basic computer skills", "email", "websites", 
        "spreadsheets", "word", "excel", "online forms", "competent computer skills"
    ],
    
    "PROFICIENT USE OF OFFICE MATERIALS": [
        "word", "excel", "printers", "copiers", "office software", 
        "office technology", "spreadsheets", "proficient use of office software"
    ],
    
    "PROGRAMMING PROFICIENCY": [
        "programming", "c++", "java", "python", "labview", "programming proficiency",
        "computer proficiency", "proficient use of", "proficiency in"
    ],
    
    "PHOTO/VIDEO PROCESSING SOFTWARE SKILLS": [
        "photo processing", "video processing", "photo processing software", 
        "shooting indoor", "low light", "fast-paced environment", "photography",
        "video editing", "image processing"
    ],
    
    "MECHANICAL/TECHNICAL SKILLS": [
        "mechanical", "technical", "robot inspection", "tools", "mechanical skills",
        "technical skills", "mechanical/technical", "basic mechanical", 
        "technical experience", "mechanical aptitude", "electrical aptitude",
        "game rules", "robot control", "diagnostics"
    ],
    
    "ADVANCED MACHINE SHOP SKILLS": [
        "welding", "milling", "lathes", "machinist", "welder", "machine shop",
        "vertical milling machine", "engine lathes", "torches", "drill press",
        "saws", "tig welder", "advanced machine shop", "mechanical/technical skills"
    ],
    
    "CONTROL SYSTEMS & DIAGNOSTICS": [
        "control systems", "diagnostics", "fms", "electronics", "field management system",
        "field electronics", "diagnostic tools", "robot control system", 
        "control systems & diagnostics", "electrical", "electronic systems"
    ],
}

REQ_EXPERIENCE_KEYWORDS = {
    "FRC CONTROL SYSTEM EXPERIENCE": [
        "frc control system", "hands-on frc control system", "control system experience",
        "diagnostic tools", "first robotics competition control system"
    ],
    
    "FIELD MANAGEMENT SYSTEM EXPERIENCE": [
        "field management system", "fms", "game field", "field electronics",
        "field mechanical", "field electrical"
    ],
    
    "FRC REFEREE EXPERIENCE": [
        "frc referee", "referee experience", "prior years of first robotics competition referee",
        "referee", "refereeing"
    ],
    
    "FRC JUDGE EXPERIENCE": [
        "judge", "frc judge", "judge at frc event", "judging experience",
        "years as a judge"
    ],
    
    "ROBOT BUILD EXPERIENCE": [
        "robot build experience", "team robot build experience", "first robot build experience",
        "robot build", "build experience", "current season experience"
    ],
    
    "MACHINE SHOP EXPERIENCE": [
        "machine tools", "variety of machine tools", "experience machinist",
        "experienced machinist", "welder experience", "significant machine shop experience",
        "machinist/welder experience"
    ],
    
    "FIRST SAFETY KNOWLEDGE": [
        "first safety principles", "safety principles", "knowledge of first safety",
        "thorough knowledge of first safety"
    ],
    
    "MANAGEMENT/SUPERVISION EXPERIENCE": [
        "supervise", "manage", "evaluate volunteers", "volunteer management",
        "event management", "able to supervise", "supervision experience"
    ],
    
    "GAME RULES KNOWLEDGE": [
        "game rules", "event rules", "safety rules", "game & event rules",
        "game and safety rules"
    ]
}

class RegexSkillCategorizer:
    """
    A class that categorizes a given string into predefined skill 
    categories using keyword-based regular expression matching.

    Attributes:
        category_patterns (dict): A dictionary mapping category 
            names to compiled regex patterns.
    """
    def __init__(self, keywords):
        """
        Initializes the RegexSkillCategorizer with a keyword 
        dictionary, compiling  regex patterns for each skill category.

        Args:
            keywords (dict): A dictionary where the keys are category 
                names (str) and the values are lists of keywords (list 
                of str).
        """
        self.category_patterns = {}

        for category, keyword in keywords.items():
            escaped_keywords = [re.escape(kw) for kw in keyword if kw]
            pattern = r'\b(' + '|'.join(escaped_keywords) + r')\b'
            self.category_patterns[category] = re.compile(pattern, re.IGNORECASE)

    def categorize_skills(self, raw_str: str):
        """
        Categorizes the input string by counting keyword matches for 
        each skill category.

        Args:
            raw_str (str): A text description potentially containing 
                skill-related information.

        Returns:
            dict: A dictionary mapping category names to the number of 
                keyword matches found.
        """
        if not raw_str:
            return {}
        
        category_scores = {}
        for category, pattern in self.category_patterns.items():
            matches = pattern.findall(raw_str)
            category_scores[category] = len(matches)

        return category_scores

    def get_top_category(self, category_skills: dict) -> str:
        """
        Insert docstrings here
        """
        if not isinstance(category_skills, dict):
            raise TypeError(f"Invalid type for skill categorizing input.\
                Expected a dict but got {type(category_skills)}")

        if not category_skills:
            return -1

        max_score = max(category_skills, key=category_skills.get)
        return max_score



