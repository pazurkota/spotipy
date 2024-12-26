import typer
from api.authorization import Authorization
from api.player import SpotifyPlayer

player_commands = typer.Typer()

def get_player():
    auth = Authorization()
    auth.authenticate()
    return SpotifyPlayer(auth)

@player_commands.command()
def play():
    player = get_player()
    typer.echo(player.play_playback())

@player_commands.command()
def stop():
    player = get_player()
    typer.echo(player.stop_playback())

@player_commands.command()
def next():
    player = get_player()
    typer.echo(player.skip_to_next())

@player_commands.command()
def previous():
    player = get_player()
    typer.echo(player.skip_to_previous())

@player_commands.command()
def seek(seconds: int):
    player = get_player()
    typer.echo(player.seek_to_position(seconds))

@player_commands.command()
def volume(volume_percent: int):
    player = get_player()
    typer.echo(player.set_volume(volume_percent))

@player_commands.command()
def repeat(repeat_mode: str):
    player = get_player()
    typer.echo(player.set_repeat_mode(repeat_mode))

@player_commands.command()
def shuffle(shuffle: bool):
    player = get_player()
    typer.echo(player.set_shuffle_mode(shuffle))