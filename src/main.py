from typing import Optional
import enum
import random
import typer

existing_usernames = ["rick", "morty"]


def get_random_role() -> str:
    return random.choice(["HERO", "KING", "CAPTAIN", "SOLDIER", "TRAITOR"])

def maybe_create_user(username: str, country: str, cfg_dir: str, nickname: Optional[str], role: str=get_random_role):
    if username in existing_usernames:
        typer.echo("The user already exists")
        raise typer.Exit(code=1)
    else:
        if nickname:
            typer.echo(f"User created: {username} with nick '{nickname}', role {role}, operates in {country} with cfg dir at {cfg_dir}")
        else:
            typer.echo(f"User created: {username} without nick, role {role} and operates in {country} with cfg dir at {cfg_dir}")


def send_new_user_notification(username: str):
    typer.echo(f"Notification sent for new user: {username}")

def check_root(username: str):
    if username == "root":
        typer.secho("The root user is reserved!", err=True, fg=typer.colors.RED)
        raise typer.Abort()

# typer.Argument should be used to define argument help and other properties. 
def main(
    # the first arg to typer.Argument is the default value, if '...' then username is required
    # Note the metavar keyword to change the CLI argument name in help
    username: str = typer.Argument(..., help="The required user name", metavar="✨username✨"),
    # nickname is optional and defaults to None. Typehint Optional[str] is not required by typer, 
    # but may be used by editor to warn if a None is used as str
    nickname: Optional[str] = typer.Argument(None, help="The optional nickname"),
    # Dynamic default value will call get_random_role to obtain the default.
    role: Optional[str] = typer.Argument(get_random_role, 
                                        help='The role, one of ["HERO", "KING", "CAPTAIN", "SOLDIER", "TRAITOR"]', 
                                        show_default="randomly selected"),
    # argument with default value, help and default value shown. Note that show_default may be boolean or string
    country: str = typer.Argument("Entire World", help="Area of operation", show_default=True),
    # You can hide an argument in help...
    hidden_in_help: str = typer.Argument("NotShownInHelp", hidden=True),
    # You can retrieve arguments from a list of env vars, use first found. and hide them from help
    cfg_dir: str = typer.Argument("~/.config", envvar=["USER_CFG", "GLOBAL_CFG"], show_envvar=True)
):
    """
    (Fake) Register new user for War of Empires MMCCCIII
    """
    check_root(username=username)
    maybe_create_user(username=username, nickname=nickname, role=role, country=country, cfg_dir=cfg_dir)
    send_new_user_notification(username=username)
    
if __name__ == "__main__":
    typer.run(main)
