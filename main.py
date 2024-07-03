from fastapi import FastAPI, Request, HTTPException
import uvicorn
from pydantic import BaseModel
from utils import q_n_a_validation
from Game import Game
app = FastAPI()

class GameRequirements(BaseModel):
    skill_name: str
    skill_levels: list | None = ["Beginner", "Intermediate", "Advanced"]
    user_skill_level: str | None = "Beginner"
    number_of_levels: int | None = 3
    level_questions : int| None = 6
    goal: str | None = None
    goal_options: list | None = ["Basic proficiency", "Advanced proficiency", "Mastery"]


class QandAValidation(BaseModel):

    question: str
    sample_answer: str | None = None
    user_answer: str
    correct: bool | None = None

@app.post("/qa-validation")
async def qa_validation(data: QandAValidation):
    if not data:
        raise HTTPException(status_code=400, detail="The provided dictionary is empty")
    
    else:
        data.correct = q_n_a_validation(data.question, data.user_answer) 

    return data


@app.post("/game-generation")
async def game_generation(game_req: GameRequirements):
    if not game_req:
        raise HTTPException(status_code=400, detail="The provided dictionary is empty")
    
    else:
        game = Game(game_req)
        try:
            game.populate_game()
        except HTTPException as exc:
            raise HTTPException(status_code=400, detail="Requested topic violates content guidelines ") from exc

    return game.game


    