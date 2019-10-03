from AmazingRaceApp.api.GameCreatorMiddleware import GameCreatorMiddleware
from AmazingRaceApp.api.GameMiddleware import GameMiddleware

g = GameCreatorMiddleware("blam")
games = g.created_games()

for game in games:
    print(game)

game = GameMiddleware("NZSL-JWBK")
for player in game.game_leaderboard():
    print(player)
