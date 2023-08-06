import seaborn as sns
import urllib.request as req
from IPython.core.display import HTML


def load_css(theme=None):
    response_main = req.urlopen(
        'https://raw.githubusercontent.com/sprakshith/TechDeciphersStyles/main/static/main.css')

    if theme == 'cyan_sisters':
        response_theme = req.urlopen(
            'https://raw.githubusercontent.com/sprakshith/TechDeciphersStyles/main/static/cyan_sisters.css')
        return HTML('<style>' + response_main.read().decode('utf-8') +
                    response_theme.read().decode('utf-8') + '</style>')
    if theme == 'dark_matter':
        response_theme = req.urlopen(
            'https://raw.githubusercontent.com/sprakshith/TechDeciphersStyles/main/static/cyan_sisters.css')
        return HTML('<style>' + response_main.read().decode('utf-8') +
                    response_theme.read().decode('utf-8') + '</style>')
    else:
        response_theme = req.urlopen(
            'https://raw.githubusercontent.com/sprakshith/TechDeciphersStyles/main/static/cyan_sisters.css')
        return HTML('<style>' + response_main.read().decode('utf-8') +
                    response_theme.read().decode('utf-8') + '</style>')


def get_color_palette(theme=None):
    if theme == 'cyan_sisters':
        colors = ['#cadeef', '#9bd4e4', '#39ace7', '#0784b5']
        return sns.color_palette(colors)
    else:
        return sns.color_palette("tab10")
