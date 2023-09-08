from urllib.parse import urlparse

from django.conf import settings


def get_site_url():
    if not settings.CURRENT_DOMAIN:
        raise Exception("Environment variable CURRENT_DOMAIN must exist")
    domain = settings.CURRENT_DOMAIN.strip("/").split("/")[-1]
    scheme = "http://" if settings.IN_DEV else "https://"
    site_url = urlparse(f"{scheme}{domain}")
    if settings.CURRENT_PORT:
        netloc = f"{site_url.netloc}:{settings.CURRENT_PORT}"
        site_url = site_url._replace(netloc=netloc)
    return site_url.geturl()
