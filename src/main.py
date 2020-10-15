import typer


def main(good: bool = True):
    message_start = "everithing is "
    if good:
        ending = typer.style("good", fg=typer.colors.GREEN, bold=True)
    else:
        ending = typer.style("bad", fg=typer.colors.WHITE, bg=typer.colors.RED)
    
    message = message_start + ending
    typer.echo(message)
    typer.secho(f"This is printed to stderr ...", err=True, fg=typer.colors.MAGENTA, bg=typer.colors.WHITE)

if __name__ == "__main__":
    typer.run(main)
