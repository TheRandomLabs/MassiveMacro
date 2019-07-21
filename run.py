import click

from massivemacro import main


@click.command()
@click.option("--gui/--no-gui", default=True, help="Whether to show a GUI.")
def run(gui):
	main.main(gui)


if __name__ == "__main__":
	run()
