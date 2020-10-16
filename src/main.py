from typing import Optional
import enum
import random
import typer

existing_usernames = ["rick", "morty"]


def get_random_role() -> str:
    return random.choice(["HERO", "KING", "CAPTAIN", "SOLDIER", "TRAITOR"])

def maybe_create_user(username: str, nickname: Optional[str], role: str=get_random_role):
    if username in existing_usernames:
        typer.echo("The user already exists")
        raise typer.Exit(code=1)
    else:
        if nickname:
            typer.echo(f"User created: {username} with nick '{nickname}' and role {role}")
        else:
            typer.echo(f"User created: {username} without nick")


def send_new_user_notification(username: str):
    typer.echo(f"Notification sent for new user: {username}")

def check_root(username: str):
    if username == "root":
        typer.secho("The root user is reserved!", err=True, fg=typer.colors.RED)
        raise typer.Abort()

# typer.Argument should be used to define argument help and other properties. 
def main(
    # the first arg to typer.Argument is the default value, if '...' then username is required
    username: str = typer.Argument(..., help="The required user name"),
    # nickname is optional and defaults to None. Typehint Optional[str] is not required by typer, 
    # but may be used by editor to warn if a None is used as str
    nickname: Optional[str] = typer.Argument(None, help="The optional nickname"),
    # Dynamic default value will call get_random_role to obtain the default.
    role: Optional[str] = typer.Argument(get_random_role, help='The role, one of ["HERO", "KING", "CAPTAIN", "SOLDIER", "TRAITOR"]')
):
    check_root(username=username)
    maybe_create_user(username=username, nickname=nickname, role=role)
    send_new_user_notification(username=username)
    
if __name__ == "__main__":
    typer.run(main)
