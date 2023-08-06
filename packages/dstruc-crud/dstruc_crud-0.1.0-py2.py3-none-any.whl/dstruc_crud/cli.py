"""Console script for dstruc_crud."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for dstruc_crud."""
    click.echo("Replace this message by putting your code into "
               "dstruc_crud.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
