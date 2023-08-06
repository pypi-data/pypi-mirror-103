# MAL Tier List BBCode Generator

![](https://github.com/juliamarc/mal-tier-list-bbcode-gen/actions/workflows/mal-tier-list-bbcode-gen.yaml/badge.svg)
![](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/juliamarc/0ef08769e202a6eb28e1a4fe176f7eb6/raw/version-badge.json)
![](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/juliamarc/0ef08769e202a6eb28e1a4fe176f7eb6/raw/coverage-badge.json)
![](https://img.shields.io/badge/language-python-yellow.svg)

`mal-tier-list-bbcode-gen` is a Python package that generates BBCode for
tier lists with custom images corresponding to entries in MAL (characters, anime, manga, people).
Each image is also a link to the respective entry's MAL page.

[Example character tier list](https://myanimelist.net/blog.php?eid=844887)

## Installation
```
pip install mal-tier-list-bbcode-gen
```
or
```
git clone https://github.com/juliamarc/mal-tier-list-bbcode-gen
cd mal-tier-list-bbcode-gen
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
For Windows use `venv\Scripts\activate.bat` or `venv\Scripts\activate.ps1` to activate the virtual environment.

## User guide
### Tiers
Each tier is represented by one sheet of the [`tiers.ods` spreadsheet](https://github.com/juliamarc/mal-tier-list-bbcode-gen/raw/main/tiers.ods).
By default there are 7 tiers named 'tier S', 'tier A', 'tier B' ..., 'tier F'.
I provided an example filled out tier in the sheet named `EXAMPLE TIER`.

### Headers
Each tier has a header.
The headers are images.
I provided a default header for each tier in `tiers.ods` (color-coded in the typical tier list style).

Some example headers and the `.xcf` file (GIMP format) that was used to generate them can be found in `example-headers`.

### Entries
Each entry consists of a link to MAL and a link to an image.

### Image source
The images need to be hosted somewhere.
Currently there are two options:
* upload your images to an image hosting service like [Postimages](https://postimages.org/) and use the direct URL, or
* upload your images to Google Drive
    - create a folder for the images
    - make it public ("Anyone with the link can view")
    - use the generated share links ("Get sharable link" for each image)

### Image size
It's best for all the images to be the same size.
MAL's BBCode doesn't allow for resizing, so the desired image size needs to be set before upload.

Another tip on image size is to make the header width divisible by the entry image's width so they tile nicely.

### Settings
Basic settings can be found in the `SETTINGS` sheet.
Curretnly there are two settings:
* "Tier order" - list of the tier sheets that will be included in the BBCode and the order in which they will be displayed
* "Entries per row" - how many entries will be displayed in one row

## Usage

You can edit the [`tiers.ods` spreadsheet](https://github.com/juliamarc/mal-tier-list-bbcode-gen/raw/main/tiers.ods) directly or create a copy of it.
I will show an example for `tiers.ods` here, but if your file is named differently replace `tiers` with your file's name.

1. Fill out `tiers.ods`
2. Run
    - `mal-tier-list-bbcode-gen tiers.ods` if you installed with pip, or
    - `python -m mal_tier_list_bbcode_gen tiers.ods` if you used `git clone`

The BBCode can be found in `tiers.bbcode.txt` and a preview of it is in `preview.html`.

### Adding a tier
Add a sheet to the spreadsheet and add its name to the "Tier order" in `SETTINGS`.

### Removing a tier
Delete the tier's name from the "Tier order" in `SETTINGS`.
The sheet doesn't have to be removed from the spreadsheet.
