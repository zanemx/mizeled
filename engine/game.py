import datetime
import json
from pprint import pprint

import nanoid
import redis
from engine.constants import GameState
from engine.grid import create_grid
from engine.types import Game

r = redis.Redis("localhost", 6379, db=0, decode_responses=True)


def create_game(user_id):
    grid = create_grid(4, 4)
    game_id = nanoid.generate()
    game = Game(
        id=game_id,
        user_id=user_id,
        created_at=datetime.datetime.now().isoformat(),
        updated_at=datetime.datetime.now().isoformat(),
        grid=json.dumps(grid),
        state=GameState.PLAYING.value,
        turn_count=0,
        max_turns=16,
    )

    r.hset(f"user:{user_id}:{game_id}", mapping=game.model_dump())

    return game


def get_games(user_id):
    keys = r.keys(f"user:{user_id}:*")
    games = [r.hgetall(key) for key in keys]
    return {"code": 200, "data": games}


def get_game(user_id, game_id):
    return r.hgetall(f"user:{user_id}:{game_id}")


def save_game(user_id, game_id, game):
    r.hset(f"user:{user_id}:{game_id}", mapping=game)


def play_move(user_id, game_id, a, b):
    game = get_game(user_id, game_id)

    if game["state"] != GameState.PLAYING.value:
        return (game, False)

    if int(game["turn_count"]) >= int(game["max_turns"]):
        game["state"] = GameState.LOST.value
        save_game(user_id, game_id, game)
        return (game, False)

    # I don't know why pydantic is turning this into a string
    game["turn_count"] = int(game["turn_count"]) + 1

    grid = json.loads(game["grid"])
    matched = False
    if grid["tiles"][int(a)]["match_id"] == grid["tiles"][int(b)]["match_id"]:
        ascii_art = """
         __  __       _       _     
        |  \/  |     (_)     | |    
        | \  / | __ _ _ _ __ | | __ 
        | |\/| |/ _` | | '_ \| |/ / 
        | |  | | (_| | | | | |   <  
        |_|  |_|\__,_|_|_| |_|_|\_\
        """
        print(ascii_art)

        grid["tiles"][int(a)]["matched"] = True
        grid["tiles"][int(b)]["matched"] = True

        game["grid"] = json.dumps(grid)

        matched = True

        if all(tile["matched"] for tile in grid["tiles"]):
            game["state"] = GameState.WON.value

    save_game(user_id, game_id, game)
    return (game, matched)


def delete_game(user_id, game_id):
    r.delete(f"user:{user_id}:{game_id}")
