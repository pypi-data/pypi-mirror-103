from os.path import basename, splitext

import click

from mal_tier_list_bbcode_gen.bbcodegenerator import BBCodeGenerator
from mal_tier_list_bbcode_gen.spreadsheetparser import SpreadsheetParser


@click.command()
@click.option('--output_path', default=None, type=str,
              help='Path to file where the BBCode will be saved. Default '
              'path is generated based on the input file name like this: '
              '<name>.ods -> <name>.bbcode.txt')
@click.argument('ods_file_path', type=click.Path(exists=True))
def main(output_path, ods_file_path):
    parser = SpreadsheetParser(ods_file_path)
    parser.parse_tiers()

    generator = BBCodeGenerator(parser.settings, parser.tiers)
    generator.generate_bbcode()

    if not output_path:
        output_path = splitext(basename(ods_file_path))[0] + '.bbcode.txt'

    generator.write_bbcode_to_file(output_path)
    generator.write_html_preview_to_file('preview.html')
