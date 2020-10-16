from typing import Optional
import typer

existing_usernames = ["rick", "morty"]


def maybe_create_user(username: str, nickname: str):
    if username in existing_usernames:
        typer.echo("The user already exists")
        raise typer.Exit(code=1)
    else:
        if nickname:
            typer.echo(f"User created: {username} with nick '{nickname}'")
        else:
            typer.echo(f"User created: {username} without nick")


def send_new_user_notification(username: str):
    typer.echo(f"Notification sent for new user: {username}")

def check_root(username: str):
    if username == "root":
        typer.secho("The root user is reserved!", err=True, fg=typer.colors.RED)
        raise typer.Abort()

# typer.Argument should be used to define argument help and other properties. 
# the first arg to typer.Argument is the default value, if '...' then argument is required
def main(
    username: str = typer.Argument(..., help="The required user name"),
    nickname: Optional[str] = typer.Argument(None, help="The optional nickname")
):
    check_root(username=username)
    maybe_create_user(username=username, nickname=nickname)
    send_new_user_notification(username=username)
    
if __name__ == "__main__":
    typer.run(main)
