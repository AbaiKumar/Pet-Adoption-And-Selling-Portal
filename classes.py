class User:
    def __init__(self, mail, pwd):
        self.name = mail
        self.mail = mail
        self.pwd = pwd
        self.contact = ""


class Usersurvey:
    def __init__(self, time_commitment, living_space,
                 activity_level, preferences, travel_frequency, noise_tolerance):
        self.time_commitment = time_commitment
        self.living_space = living_space
        self.activity_level = activity_level
        self.preferences = preferences
        self.travel_frequency = travel_frequency
        self.noise_tolerance = noise_tolerance


class petsurveyupdate():
    def __init__(self, petbreed, time_commitment, living_space,
                 activity_level, preferences, travel_frequency, noise_tolerance):
        self.name = ''
        self.pet = petbreed
        self.time_commitment = time_commitment
        self.living_space = living_space
        self.activity_level = activity_level
        self.preferences = preferences
        self.travel_frequency = travel_frequency
        self.noise_tolerance = noise_tolerance


class CompatibilityScore:
    def __init__(self):
        self.score = 0

    def calculate(self, survey, pet_survey):
        self.score = 0
        self.score += 30 if survey['time_commitment'].strip(
        ) == pet_survey['time_commitment'].strip() else 15
        self.score += 15 if survey['living_space'].strip(
        ) == pet_survey['living_space'].strip() else 7.5
        self.score += 10 if survey['activity_level'].strip(
        ) == pet_survey['activity_level'].strip() else 5
        self.score += 20 if survey['travel_frequency'].strip(
        ) == pet_survey['travel_frequency'].strip() else 10
        self.score += 25 if survey['noise_tolerance'].strip(
        ) == pet_survey['noise_tolerance'].strip() else 12.5
        return self.score


sc = CompatibilityScore()
