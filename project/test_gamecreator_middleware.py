from AmazingRaceApp.api.GameCreatorMiddleware import GameCreatorMiddleware

g = GameCreatorMiddleware("blam")
games = g.get_created_games()

for game in games:
    print(game.code)