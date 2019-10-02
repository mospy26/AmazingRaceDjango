from django.contrib.auth.models import User


def run(*args):
    User.objects.create(
        username="sukaiwen",
        first_name="Keven",
        password="sukaiwen",
    )
    User.objects.create(
        username="coke",
        first_name="CocaCola",
        password="coke",
    )
    User.objects.create(
        username="usyd",
        first_name="USYD",
        password="usyd",
    )
    User.objects.create(
        username="echa",
        first_name="Edwin",
        password="echa",
    )
    User.objects.create(
        username="blam",
        first_name="Brenden",
        password="blam",
    )
    User.objects.create(
        username="mful",
        first_name="Mustafa",
        password="mful",
    )
