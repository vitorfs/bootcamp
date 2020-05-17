from django.conf import settings

from PIL import Image


def check_image_extension(filename):
    """Checks filename extension."""
    ext = ['.jpg', '.jpeg', '.png']
    for e in ext:
        if filename.endswith(e):
            return True
    return False


def image_compression(f):
    """Compresses the image."""
    try:
        f = settings.MEDIA_ROOT + f
        im = Image.open(f)
        im.save(f, optimize=True, quality=30)
    except:  # noqa: E722
        return ""
