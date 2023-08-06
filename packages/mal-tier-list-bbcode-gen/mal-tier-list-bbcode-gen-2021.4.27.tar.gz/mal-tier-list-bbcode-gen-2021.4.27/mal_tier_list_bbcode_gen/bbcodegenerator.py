import bbcode


class BBCodeGenerator:
    def __init__(self, settings, tiers):
        self.settings = settings
        self.tiers = tiers

        self.bbcode = None

    def _generate_bbcode_for_header(self, header):
        return f"{header.get_bbcode()}\n" if header is not None else ''

    def _calculate_newline_after(self, no_entries):
        entries_per_row = self.settings['entries_per_row']

        newline_after = []
        if entries_per_row > 0:
            newline_after = range(
                entries_per_row-1, no_entries-1, entries_per_row)

        ends = ['\n' if i in newline_after else '' for i in range(
            no_entries-1)]
        ends.append('\n')

        return ends

    def _generate_bbcode_for_tier(self, tier):
        bbcode = self._generate_bbcode_for_header(tier['header'])
        newline_after = self._calculate_newline_after(len(tier['entries']))

        bbcode += ''.join(f"{e.get_bbcode()}{n}" for e, n in zip(
            tier['entries'], newline_after))

        return bbcode

    def generate_bbcode(self):
        self.bbcode = ''

        for tier in self.tiers.values():
            self.bbcode += self._generate_bbcode_for_tier(tier)

    def write_bbcode_to_file(self, file_name):  # pragma: no cover
        with open(file_name, 'w') as f:
            f.write(self.bbcode)

        print(f"BBCode saved to {file_name}")

    def _generate_html_preview(self):
        parser = bbcode.Parser(replace_links=False)
        parser.add_simple_formatter('img', '<img src=%(value)s>')

        return parser.format(self.bbcode)

    def write_html_preview_to_file(self, file_name):  # pragma: no cover
        html = self._generate_html_preview()
        with open(file_name, 'w') as f:
            f.write(html)

        print(f"HTML preview saved to {file_name}")
