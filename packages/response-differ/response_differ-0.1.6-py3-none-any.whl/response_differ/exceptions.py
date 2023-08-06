from hashlib import sha1


class CheckFailed(AssertionError):

    __module__ = "builtins"


CACHE = {}


def get_exception(name):
    if name in CACHE:
        exception_class = CACHE[name]
    else:
        exception_class = type(name, (CheckFailed,), {})
        exception_class.__qualname__ = CheckFailed.__name__
        exception_class.__name__ = CheckFailed.__name__
        CACHE[name] = exception_class
    return exception_class


def _get_hashed_exception(prefix, message):
    messages_digest = sha1(message.encode("utf-8")).hexdigest()
    name = f"{prefix}{messages_digest}"
    return get_exception(name)


def get_grouped_exception(*exceptions: AssertionError):
    messages = [exception.args[0] for exception in exceptions]
    message = "".join(messages)
    return _get_hashed_exception("GroupedException", f"{message}")


def get_status_code_error(status_code):
    name = f"StatusCodeError{status_code}"
    return get_exception(name)


def get_response_type_error(expected, received):
    name = f"SchemaValidationError{expected}_{received}"
    return get_exception(name)


def get_malformed_media_type_error(media_type):
    name = f"MalformedMediaType{media_type}"
    return get_exception(name)


def get_missing_content_type_error():
    return get_exception("MissingContentTypeError")


def get_response_parsing_error(exception):
    return _get_hashed_exception("ResponseParsingError", str(exception))


def get_headers_error(message):
    return _get_hashed_exception("MissingHeadersError", message)
