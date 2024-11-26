from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    id: str


# Game objects
class Tile(BaseModel):
    id: int
    matched: bool
    slot_x: int
    slot_y: int
    match_id: str


class Grid(BaseModel):
    width: int
    height: int
    tiles: list[dict]


class Game(BaseModel):
    id: str
    user_id: str
    created_at: str
    updated_at: str
    # JSON String containing the grid
    grid: str
    state: str
    turn_count: int
    max_turns: int


# Request types
# these models represent incoming request params
class ReqGameCreate(BaseModel):
    user_id: str


class ReqGamePlay(BaseModel):
    a: int
    b: int
