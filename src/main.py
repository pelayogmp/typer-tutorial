import typer

existing_usernames = ["rick", "morty"]


def maybe_create_user(username: str):
    if username in existing_usernames:
        typer.echo("The user already exists")
        raise typer.Exit(code=1)
    else:
        typer.echo(f"User created: {username}")


def send_new_user_notification(username: str):
    typer.echo(f"Notification sent for new user: {username}")

def check_root(username: str):
    if username == "root":
        typer.secho("The root user is reserved!", err=True, fg=typer.colors.RED)
        raise typer.Abort()

def main(username: str):
    check_root(username=username)
    maybe_create_user(username=username)
    send_new_user_notification(username=username)
    
if __name__ == "__main__":
    typer.run(main)
