import os
import json
import string

import config
from utils import get_completion, get_image, get_keywords, is_json

class Game():
    """ A game class to create a game object according to user requirements"""

    def __init__(self, game_data):

        self.skill =  game_data.skill_name
        self.skill_level = game_data.user_skill_level
        self.goal = game_data.goal
        self.level_count = game_data.number_of_levels
        self.ques_count = game_data.level_questions
        self.storyline = None


        try:
            with open(config.STORY_LINE_TEMPLATE, encoding='utf-8') as f:
                story_line_template = json.load(f)
                self.story_line_template = json.dumps(story_line_template)
        except FileNotFoundError as e:
            raise FileNotFoundError("storyline.json file not found") from e

        try:
            with open(config.LEVEL_TEMPLATE, encoding='utf-8') as f:
                level_template = json.load(f)
                self.level_template = json.dumps(level_template)

                
        except FileNotFoundError as e:
            raise FileNotFoundError("Level_template.json file not found")

        self.game = {}



    def get_storyline(self):
        """prompt gpt to get a storyline for the given skill and required number of levels
        A json object according to the template 'storyline.json' is returned"""
        system_prompt = f"You are a game writer and designer. Create a storyline for a learning \
                            game about {self.skill}. Goal is moving up from {self.skill_level} level to {self.goal}. \
                            The game should have {self.level_count} levels.\
                            Return the storyline in this format: {self.story_line_template}"
         

          
        storyline = get_completion(system_prompt)

        try:
            self.storyline = json.loads(storyline)
        
        except ValueError as e:
   
            raise ValueError("Invalid JSON") from e

    def get_challenges(self, level_story):
        """Use the storyline to generate questions on each level. 
        A json object according to the template 'game_template.json' is returned"""

        system_prompt = f"I have a storyline for a game to learn {self.skill}. \
                        Story for current level is ``` {level_story}``` \
                        The challenges should consist of question types limited to [MCQs, fill in the blanks, Free text].\
                        Every level should have {self.ques_count} questions. \
                        Return the game in this json format.{self.level_template} "
        

        game_challenges = get_completion(system_prompt)

        
        if is_json(game_challenges):
            game_challenges = json.loads(game_challenges)
            return game_challenges

        return json.dumps({"Invalid JSON"})


    def get_image_prompt(self, challenge: dict) -> str :
        """ Takes a challenge in the form of a dict (level_template.json)
            Generates a string prompt for Dall-E image generation """

        prompt = challenge["question"]
        
        if challenge["type"] == "mcq":
            
            ans_choice = challenge["correct_answer"]
            index = string.ascii_uppercase.index(ans_choice)
            ans = challenge["options"][index][ans_choice]["text"]

            prompt = prompt + ' ' + ans
            print(prompt)
        elif challenge["type"] == "fill_in_the_blank":
            try:
                prompt = prompt + ' ' + challenge["correct_answer"]
            except ValueError:
                print("correct mcq answer not found")
        elif challenge["type"] == "text":
            try:
                prompt = prompt + ' ' + challenge["sample_answer"] 
            except ValueError:
                print("sample text answer not found")
        return prompt

    
    def populate_game(self):
        """ This function will use all utilities to create the game 
        and populate the variable 'self.game ' """
        
        
        #### workflow

        ### Step 1: Generate story line using storyline template (storyline.json)
        self.get_storyline()
        try:

            self.game["game_title"] = self.storyline["game_title"]
            self.game["game_story"] = self.storyline["game_story"]
            self.game["levels"] = self.storyline["levels"]
        #### Step 2a: Use each levels storyline to create challenges using template (level_template.json)

            for i, level in enumerate(self.storyline["levels"], start= 0):
                challenges = self.get_challenges(level["story"])

                    #### Step 2b: Populate self.game with the game

                self.game["levels"][i]["challenges"] = challenges["challenges"]

                ##### Step 3: Use every challenge to generate a Dall E image 

                for j, challenge in enumerate(challenges["challenges"]):
                    image_prompt = self.get_image_prompt(challenge)
                    image_url = get_image(image_prompt)

                    self.game["levels"][i]["challenges"][j]["image_url"] = image_url
            


        except ValueError as e:
            raise ValueError("Invalid JSON object") from e



    
    def validate_json_schema(self):
        """ This function will take the chatGPT response and validate the schema"""
        