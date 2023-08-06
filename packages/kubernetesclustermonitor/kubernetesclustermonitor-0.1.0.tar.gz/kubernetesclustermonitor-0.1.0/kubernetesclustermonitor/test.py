import click
import subprocess

@click.group()
def cli():
    pass

@click.command()
def run():
    process = subprocess.Popen(['kubectl', 'get', 'pods', '-n', 'backend'], stdout=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate()
    click.echo(stdout)

cli.add_command(run)

if __name__ == '__main__':
    cli()
