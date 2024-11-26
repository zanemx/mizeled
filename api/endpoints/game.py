from fastapi import APIRouter
from engine.types import ReqGameCreate, ReqGamePlay
from engine.game import create_game, get_games, get_game, play_move, delete_game

router = APIRouter()


def create_response_object(data=None, status=200, error=""):
    res = {"status": status, "error": error, "data": data}
    if error and status == 200:
        res["status"] = 400
    return res


@router.post("/create")
async def create(req: ReqGameCreate):
    create_game(req.user_id)
    return "ok"


@router.get("/{user_id}")
async def games(user_id: str):
    return get_games(user_id)


@router.get("/{user_id}/{game_id}")
async def get(user_id: str, game_id: str):
    return get_game(user_id, game_id)


@router.post("/{user_id}/{game_id}/play")
async def play(req: ReqGamePlay, user_id: str, game_id: str):
    game, matched = play_move(user_id, game_id, req.a, req.b)
    return create_response_object(data={"matched": matched, "game": game})


# delete game
@router.delete("/{user_id}/{game_id}")
async def delete(user_id: str, game_id: str):
    delete_game(user_id, game_id)
    return "ok"
