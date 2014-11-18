def absurl(request, url):
    if not url:
        return None

    if not url.startswith('/'):
        return url

    return request.build_absolute_uri(url)
