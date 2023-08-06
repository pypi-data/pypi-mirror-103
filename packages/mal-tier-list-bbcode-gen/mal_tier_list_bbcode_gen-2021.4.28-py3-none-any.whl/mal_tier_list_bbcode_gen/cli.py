import warnings

from os.path import basename, splitext

import click

import mal_tier_list_bbcode_gen.utils as utils

from mal_tier_list_bbcode_gen.tierlistgenerator import TierListGenerator


@click.command()
@click.argument('ods_file_path', type=click.Path(exists=True))
def main(ods_file_path):
    with warnings.catch_warnings(record=True) as w:
        generator = TierListGenerator(ods_file_path)
        generator.generate()

        bbcode_output_path = splitext(basename(ods_file_path))[0] + '.txt'
        html_output_path = splitext(basename(ods_file_path))[0] + '.html'

        utils.write_to_file(bbcode_output_path, generator.bbcode,
                            f"BBCode saved to {bbcode_output_path}")
        utils.write_to_file(html_output_path, generator.html,
                            f"HTML preview saved to {html_output_path}")

        if w:
            print(*[f"Warning: {warning.message}" for warning in w], sep='\n')
