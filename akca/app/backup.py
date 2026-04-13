import click

@click.command
@click.argument("directory")
@click.pass_context
def backup(ctx, directory: str):
    try:
        ctx.obj.backup(directory)
    except Exception as e:
        ctx.obj.logger.error(f"Error creating backup: {e}")
        raise SystemExit(1)
    click.echo("Backup created successfully")