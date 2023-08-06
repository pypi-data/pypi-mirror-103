# from pagetools.src.Page import Page
#
# import click
# from lxml import etree
#
#
# @click.command("get_char_occurence", help="Retrieve all files in which the specified characters occur")
# @click.argument("files", nargs=-1)
# @click.option("-c", "--characters", nargs=-1)
# def get_char_occurence_cli(files):
#
#     with click.progressbar(files) as _files:
#         for file in _files:
#             try:
#                 page = Page(file)
#             except etree.XMLSyntaxError:
#                 click.echo(f"{file}: Not a valid XML file. Skipping…", err=True)
#                 continue
#             except etree.ParseError:
#                 click.echo(f"{file}: XML can't be parsed. Skipping…", err=True)
#                 continue
#
#
#
# if __name__ == "__main__":
#     get_char_occurence_cli()
