import enum


class GameState(enum.Enum):
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"
