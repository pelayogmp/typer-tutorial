from typing import Optional
import enum
import random
import typer

existing_usernames = ["rick", "morty"]
VALID_ROLES = ("HERO", "KING", "CAPTAIN", "SOLDIER", "TRAITOR")
VERSION = "0.1.0"
ME = "UserManager-CLI"

def get_random_role() -> str:
    return random.choice(VALID_ROLES)

def maybe_create_user(username: str, password: str, email: str, country: str, cfg_dir: str, nickname: Optional[str], role: str=get_random_role):
    if username in existing_usernames:
        typer.echo("The user already exists")
        raise typer.Exit(code=1)
    else:
        if nickname:
            typer.echo(f"User created: {username} with nick '{nickname}', password {password}, email {email}, role {role}, operates in {country} with cfg dir at {cfg_dir}")
        else:
            typer.echo(f"User created: {username} without nick, password {password}, email {email}, role {role} and operates in {country} with cfg dir at {cfg_dir}")


def send_new_user_notification(username: str):
    typer.echo(f"Notification sent for new user: {username}")

def check_root(username: str):
    if username == "root":
        typer.secho("The root user is reserved!", err=True, fg=typer.colors.RED)
        raise typer.Abort()

def role_callback_breaks_completion(role:str):
    # This breaks completion
    typer.echo(f"Validating parameter: role")
    if role.upper() in VALID_ROLES:
        return role.upper()
    
    raise typer.BadParameter(f"Select one from {VALID_ROLES}")

def role_callback_without_param(ctx: typer.Context, role:str):
    if ctx.resilient_parsing:
        # return inmediatly during completion
        return
    typer.echo(f"Validating parameter: role")
    if role.upper() in VALID_ROLES:
        return role.upper()
    
    raise typer.BadParameter(f"Select one from {VALID_ROLES}")

def role_callback(ctx: typer.Context, param: typer.CallbackParam, role:str):
    if ctx.resilient_parsing:
        # return inmediatly during completion
        return
    # Use the CallbackPaaram object properties
    typer.echo(f"Validating parameter: {param.name}")
    if role.upper() in VALID_ROLES:
        return role.upper()
    
    raise typer.BadParameter(f"Select one from {VALID_ROLES}")

def version_callback(value: bool):
    if value:
        typer.echo(f"{ME} version {VERSION}")
        raise typer.Exit()

# typer.Argument should be used to define argument help and other properties. 
def main(
    # the first arg to typer.Argument is the default value, if '...' then username is required
    # Note the metavar keyword to change the CLI argument name in help
    username: str = typer.Argument(..., help="The required user name", metavar="✨username✨"),
    # nickname is optional and defaults to None. Typehint Optional[str] is not required by typer, 
    # but may be used by editor to warn if a None is used as str
    nickname: Optional[str] = typer.Option(None, "--alias", "--nick", "-a", help="The optional nickname"),
    # Dynamic default value will call get_random_role to obtain the default.
    role: str = typer.Option(get_random_role, "--role", "-r",
                             help=f'The role, one of {VALID_ROLES}', 
                             show_default="randomly selected", callback=role_callback),
                                    
    # Required option, note ellipsis '...', and help, typer will prompt for it if missing.
    # promp may be boolean or string
    # typer.Option() receives as a first function argument the default value, e.g. None, 
    # and all the next positional values are to define the CLI option name(s).
    country: str = typer.Option(..., "--area", "-a", help="Area of operation", prompt="Enter your area of operation"),
    # You can prompt for confimation too
    email: str = typer.Option(..., help="Your email", prompt="Enter your email", confirmation_prompt=True),
    # You can prompt and hide input too
    password: str = typer.Option(..., "--password", "-p", help="Your password", prompt="Enter your password", confirmation_prompt=True, hide_input=True),
    # You can hide an argument in help...
    hidden_in_help: str = typer.Argument("NotShownInHelp", hidden=True),
    # You can retrieve arguments from a list of env vars, use first found. and hide them from help
    cfg_dir: str = typer.Option("~/.config", "--config-dir", "-c", envvar=["USER_CFG", "GLOBAL_CFG"], show_envvar=True),
    # Version, declare "--version" to avoid automatic "--no-version", also use is_eager=True to process before any other parameter
    version: Optional[bool] = typer.Option(None, "--version", "-V", callback=version_callback, is_eager=True)
):
    """
    (Fake) Register new user for War of Empires MMCCCIII
    """
    check_root(username=username)
    maybe_create_user(username=username, password=password, nickname=nickname, email=email, role=role, country=country, cfg_dir=cfg_dir)
    send_new_user_notification(username=username)
    
if __name__ == "__main__":
    typer.run(main)
