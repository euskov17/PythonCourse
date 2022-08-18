import re


def normalize_path(path: str) -> str:
    """
    :param path: unix path to normalize
    :return: normalized path
    """
    if not path:
        return '.'
    replaced = re.sub('/(\./)+', '/', path)
    while re.search('[^/\.]+/\.\./', replaced) or re.search('/{2,}', replaced):
        replaced = re.sub('/{2,}', '/', replaced)
        replaced = re.sub('^/(\.\./)+', '/', replaced)
        replaced = re.sub('[^/\.]+/\.\./', '', replaced)
    if re.fullmatch('/+', replaced):
        return '/'
    replaced = re.sub('^\./', '', replaced)
    replaced = re.sub('/+$', '', replaced)
    replaced = re.sub('^/(\.\./)+', '/', replaced)
    replaced = re.sub('[^/\.]+/\.\.$', '', replaced)
    if re.fullmatch('/+', replaced):
        return '/'
    replaced = re.sub('/+$', '', replaced)
    if replaced:
        return replaced
    else:
        return '.'
