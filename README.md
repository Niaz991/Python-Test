# AI Skill game generation

This repository contains a FastAPI application with two endpoints, `/game-generation` and `/q-n-a-validation`. The application utilizes a configuration file, JSON templates, a utilities (utils) file, and a Game module file.

## Files

- **main.py**: The main FastAPI code file that defines the API endpoints (`/game-generation` and `/q-n-a-validation`).
- **config.py**: The configuration file used by the application to find JSON templates.
- **utils.py**: The utilities file containing helper functions or utility classes.
- **Game.py**: The Game module file that contains the `Game` class.

## Endpoints

### `/game-generation`

This endpoint is responsible for generating the game.
It uses the following data model as an input:
{
    "skill_name": "Agriculture",
    "skill_levels": ["Beginner", "Intermediate", "Advanced"],
    "user_skill_level": "Beginner",
    "goal_options": ["Basic proficiency", "Advanced proficiency", "Mastery"],
    "goal": "Advanced proficiency",
    "number_of_levels": 1,
    "level_questions": 1
  }
  

### `/qa-validation`

This endpoint handles the validation as true or false when the user answer matches the question or not.
The "correct" field here is changed to either true or false and the structure is returned as is.
The data model it requires as input:
{
    "question": "Describe one significant cultural aspect of Ancient Egypt.",
    "sample_answer": "Ancient Egyptians practiced mummification to preserve their bodies for the afterlife.",
    "user_answer": "making mummies of bodies",
    "correct": null 
}

## Configuration

The application uses a configuration file named `config.json`. Please ensure that this file is properly configured with the necessary settings.

## Usage

1. Clone the repository:

    ```bash
    git clone https://gitlab.com/Codistan/ai-generated/python.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the FastAPI application:

    ```bash
    uvicorn main:app --reload
    ```

4. Access the API at `http://3.231.9.211/` and explore the defined endpoints.

## Additional Information

Feel free to customize and extend the codebase based on your project requirements. If you encounter any issues or have suggestions for improvement, please [open an issue](https://github.com/your-username/your-repository/issues).

Happy coding!
