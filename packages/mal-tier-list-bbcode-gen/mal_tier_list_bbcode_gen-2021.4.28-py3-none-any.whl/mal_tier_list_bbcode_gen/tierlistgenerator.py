from mal_tier_list_bbcode_gen.bbcodegenerator import BBCodeGenerator
from mal_tier_list_bbcode_gen.spreadsheetparser import SpreadsheetParser


class TierListGenerator(BBCodeGenerator):
    def __init__(self, ods_file_path):
        settings, tiers = self._parse_spreadsheet(ods_file_path)
        super().__init__(settings, tiers)

    def _parse_spreadsheet(self, ods_file_path):
        parser = SpreadsheetParser(ods_file_path)
        parser.parse_tiers()

        return parser.settings, parser.tiers

    def generate(self):
        self.generate_bbcode()
        self.generate_html()
