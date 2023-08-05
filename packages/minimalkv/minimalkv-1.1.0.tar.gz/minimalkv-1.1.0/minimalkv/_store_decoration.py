from minimalkv.decorator import URLEncodeKeysDecorator, ReadOnlyDecorator


def decorate_store(store, decoratorname):
    decoratorname_part = decoratorname.split("(")[0]
    if decoratorname_part == "urlencode":
        return URLEncodeKeysDecorator(store)
    if decoratorname_part == "readonly":
        return ReadOnlyDecorator(store)
    raise ValueError("Unknown store decorator: " + str(decoratorname))
