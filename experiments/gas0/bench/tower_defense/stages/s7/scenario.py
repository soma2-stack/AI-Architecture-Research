from td.game import summary
from td.model import Enemy, Game

game = Game(enemies=[Enemy("last", 20, 0, 5, alive=False)])
print(summary(game)["enemies"])
