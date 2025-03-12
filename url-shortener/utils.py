import random
import string

def generate_short_url(length=6):
    """Generates a random short URL string."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))
