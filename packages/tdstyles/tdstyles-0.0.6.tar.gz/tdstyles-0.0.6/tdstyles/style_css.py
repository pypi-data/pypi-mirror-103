import seaborn as sns
import urllib.request as req
from IPython.core.display import HTML


current_theme = 'gray_area'


def load_css(theme=None):
    """
    Four themes available right now: 'cyan_sisters', 'dark_matter', 'genus_lavandula' and 'gray_area'.
    """
    global current_theme

    response_main = req.urlopen(
        'https://raw.githubusercontent.com/sprakshith/TechDeciphersStyles/main/static/main.css')

    if theme == 'cyan_sisters':
        current_theme = 'cyan_sisters'

        response_theme = req.urlopen(
            'https://raw.githubusercontent.com/sprakshith/TechDeciphersStyles/main/static/cyan_sisters.css')

        return HTML('<style>' + response_main.read().decode('utf-8') +
                    response_theme.read().decode('utf-8') + '</style>')
    elif theme == 'dark_matter':
        current_theme = 'dark_matter'

        response_theme = req.urlopen(
            'https://raw.githubusercontent.com/sprakshith/TechDeciphersStyles/main/static/dark_matter.css')

        return HTML('<style>' + response_main.read().decode('utf-8') +
                    response_theme.read().decode('utf-8') + '</style>')
    elif theme == 'genus_lavandula':
        current_theme = 'genus_lavandula'

        response_theme = req.urlopen(
            'https://raw.githubusercontent.com/sprakshith/TechDeciphersStyles/main/static/genus_lavandula.css')

        return HTML('<style>' + response_main.read().decode('utf-8') +
                    response_theme.read().decode('utf-8') + '</style>')
    else:
        current_theme = 'gray_area'

        response_theme = req.urlopen(
            'https://raw.githubusercontent.com/sprakshith/TechDeciphersStyles/main/static/gray_area.css')

        return HTML('<style>' + response_main.read().decode('utf-8') +
                    response_theme.read().decode('utf-8') + '</style>')


def get_color_palette():
    if current_theme == 'cyan_sisters':
        return sns.color_palette(['#39ace7', '#0784b5'])
    elif current_theme == 'dark_matter':
        return sns.color_palette(['#757575', '#212121'])
    elif current_theme == 'genus_lavandula':
        return sns.color_palette(['#a176c6', '#8653af'])
    else:
        return sns.color_palette(['#78909C', '#37474F'])


def get_background_color():
    if current_theme == 'cyan_sisters':
        return '#cadeef'
    elif current_theme == 'dark_matter':
        return '#e0e0e0'
    elif current_theme == 'genus_lavandula':
        return '#e9d5eb'
    else:
        return '#CFD8DC'


def get_font_color():
    if current_theme == 'cyan_sisters':
        return '#39ace7'
    elif current_theme == 'dark_matter':
        return '#757575'
    elif current_theme == 'genus_lavandula':
        return '#a176c6'
    else:
        return '#78909C'


def get_font_dict(fontsize=14, fontweight='light'):
    return {
                'fontsize': fontsize,
                'fontweight': fontweight,
                'fontfamily': 'serif',
                'horizontalalignment': 'center',
                'color': get_font_color()
            }
