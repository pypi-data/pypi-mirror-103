from urllib.parse import unquote

import mal_tier_list_bbcode_gen.exceptions as exceptions

from mal_tier_list_bbcode_gen.image import Image


class Entry(Image):
    def __init__(self, mal_url, image_source, image_url):
        super(Entry, self).__init__(image_source, image_url)
        self.mal_url = self._validate_mal_url(mal_url)

        self.name = unquote(self.mal_url.split("/")[-1]).replace("_", " ")

    def __repr__(self):
        return self.name

    def _validate_mal_url(self, mal_url):
        if mal_url.startswith("https://myanimelist.net/"):
            return mal_url
        else:
            raise exceptions.InvalidMALURL(
                f"'{mal_url}' is not a valid MAL URL. All MAL URLs should "
                f"start with 'https://myanimelist.net/'.")

    def get_bbcode(self):
        return f'[url={self.mal_url}][img]{self.image_url}[/img][/url]'
