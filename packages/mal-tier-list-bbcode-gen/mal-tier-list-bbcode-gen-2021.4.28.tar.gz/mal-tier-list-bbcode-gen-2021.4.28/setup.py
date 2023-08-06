import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()

entry_points = {
    'console_scripts': [
        'mal-tier-list-bbcode-gen = mal_tier_list_bbcode_gen.cli:main',
    ]
}

setuptools.setup(
    name='mal-tier-list-bbcode-gen',
    version='2021.4.28',
    packages=setuptools.find_packages(),
    include_package_data=True,
    description='BBCode generator for MyAnimeList tier lists',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/juliamarc/mal-tier-list-bbcode-gen',
    install_requires=['click', 'bbcode', 'ezodf', 'lxml'],
    entry_points=entry_points,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
