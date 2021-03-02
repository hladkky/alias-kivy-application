from kivy import metrics
from kivy.core.window import Window


def determine_banner_height():
    '''
    Utility function for determining the height (dp) of the banner ad.

    Returns
    -------
    height : int
        Height of banner ad in dp.
    '''
    height = 32
    upper_bound = metrics.dp(720)
    if Window.height > upper_bound:
        height = 90
    elif (
        Window.height > metrics.dp(400)
        and Window.height <= upper_bound
    ):
        height = 50
    return height
