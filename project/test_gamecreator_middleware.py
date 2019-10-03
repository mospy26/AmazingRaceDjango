from AmazingRaceApp.api.GameCreatorMiddleware import GameCreatorMiddleware

g = GameCreatorMiddleware("blam")
games = g.created_games()

for game in games:
    print(game)