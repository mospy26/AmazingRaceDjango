from django.contrib.auth.models import User

from AmazingRaceApp.api.GameCreatorMiddleware import GameCreatorMiddleware
from AmazingRaceApp.api.GameMiddleware import _GameMiddleware
from AmazingRaceApp.models import Game

g = GameCreatorMiddleware("blam")
games = g.created_games()

for game in games:
    print(game)

game = _GameMiddleware("NZSL-JWBK")
for player in game.game_leaderboard():
    print(player)

for l in game.ordered_locations():
    print(l)

# need to rethink if someone sends post requests to corrupt data with wrong
# ranges (e.g. start_time later than end_time)

# also unsure if you want the creator to be able to add start and end times now
# or whether he should be able to do this while making a game live
# and if he can change the end time after is it archived
# and whether a game is automatically archived if it ended
# and if the game can be re opened after archived or ended (ended vs archived)

game = Game.objects.create(
    title="YEs!",
    archived=False,
    live=True,
    start_time="2019-10-01T07:15:34Z",
    end_time="2019-10-01T05:15:34Z",
)

game.players.add(User.objects.get(username='sukaiwen').pk)

game.save()
