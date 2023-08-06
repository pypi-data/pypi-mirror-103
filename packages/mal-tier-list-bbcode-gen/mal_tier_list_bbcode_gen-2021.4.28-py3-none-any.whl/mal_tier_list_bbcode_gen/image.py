import re

import mal_tier_list_bbcode_gen.exceptions as exceptions


class Image:
    SOURCES = ['direct URL', 'Google Drive']

    def __init__(self, image_source, image_url):
        self.image_source = image_source
        self.image_url = image_url

        self._process_image_url()

    def _process_image_url(self):
        if self.image_source == 'direct URL':
            pass
        elif self.image_source == 'Google Drive':
            file_id_search = re.search(r'([-\w]{25,})', self.image_url)
            if file_id_search:
                file_id = file_id_search.group(1)
                self.image_url = f'https://drive.google.com/uc?id={file_id}'
            else:
                raise exceptions.GoogleDriveSourceError(
                    f"Couldn't identify file ID in the following Google Drive "
                    f"URL: '{self.image_url}'.")
        else:
            raise exceptions.InvalidImageSourceError(
                f"'{self.image_source}' is not a valid image source. Choose "
                f"from {self.SOURCES}.")

    def get_bbcode(self):
        return f'[img]{self.image_url}[/img]'
