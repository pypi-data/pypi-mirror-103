import urllib.request as req
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from IPython.core.display import HTML


def descriptive_plot(figsize=(8, 6), title=None, title_pos=None, content_title=None, content_title_pos=None,
                     content=None, content_pos=None, background_color=None):
    if title is None:
        title = 'Enter Title Here'

    if content_title is None:
        content_title = 'Enter Description Title'

    if content is None:
        content = '''
                     Lorem ipsum dolor sit amet, consectetur 
                     adipiscing elit, sed do eiusmod tempor 
                     incididunt ut labore et dolore magna a-
                     -liqua. Ut enim ad minim veniam, quis 
                     nostrud exercitation ullamco laboris
                     nisi aliquip ex ea commodo consequat.

                     Duis aute irure dolor in reprehenderit 
                     in voluptate velit esse cillum dolore 
                     eu fugiat nulla pariatur. 

                     Excepteur sint occaecat cupidatat non 
                     proident, sunt in culpa qui officia 
                     deserunt mollit anim id est laborum.
                  '''

    if title_pos is None:
        title_pos = [0.125, 0.9]

    if content_title_pos is None:
        content_title_pos = [0.99, 0.9]

    if content_pos is None:
        content_pos = [0.85, 0.35]

    if background_color is None:
        background_color = '#fbfbfb'

    fig, ax = plt.subplots(1, 1, figsize=figsize, facecolor=background_color)
    fig.text(title_pos[0], title_pos[1], title, fontsize=18, fontweight='bold', fontfamily='serif')
    ax.set_facecolor(background_color)

    fig.text(content_title_pos[0], content_title_pos[1], content_title, fontsize=18,
             fontweight='bold', fontfamily='serif')
    fig.text(content_pos[0], content_pos[1], content, fontsize=12, fontweight='light', fontfamily='serif')

    l1 = lines.Line2D([0.95, 0.95], [0, 1], transform=fig.transFigure, figure=fig, color='black', lw=0.2)
    fig.lines.extend([l1])

    return ax


def load_css():
    response = req.urlopen('https://raw.githubusercontent.com/sprakshith/TechDeciphersStyles/main/static/style.css')
    return HTML('<style>' + response.read().decode('utf-8') + '</style>')
