from hashlib import md5


def color(nickname):
    """
    Provides a consistent color for a nickname. Uses first 6 chars
    of nickname's md5 hash, and then slightly darkens the rgb values
    for use on a light background.
    """
    _hex = md5(nickname).hexdigest()[:6]
    darken = lambda s: str(int(round(int(s, 16) * .7)))
    return "rgb(%s)" % ",".join([darken(_hex[i:i+2]) for i in range(6)[::2]])