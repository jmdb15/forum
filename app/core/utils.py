from urllib.parse import quote, urljoin


def build_image_url(
    image_url: str | None,
    base_url: str,
):
    if image_url is None or image_url == "":
        return None

    path = image_url.replace("\\", "/").lstrip("/")

    return urljoin(
        base_url.rstrip("/") + "/",
        f"{quote(path, safe='/')}",
    )
