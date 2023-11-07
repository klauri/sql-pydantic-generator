import click

@click.command()
def hello():
    click.echo('Hellooooo worlldddddd!!!!')

@click.command()
@click.option('--sql-language')
def generate(sql_language):
    print(sql_language)

if __name__=='__main__':
    generate()