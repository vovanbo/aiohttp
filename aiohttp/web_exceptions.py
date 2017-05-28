from http import HTTPStatus

from .web_response import Response


__all__ = (
    'HTTPException',
    'HTTPError',
    'HTTPRedirection',
    'HTTPSuccessful',
    'HTTPOk',
    'HTTPCreated',
    'HTTPAccepted',
    'HTTPNonAuthoritativeInformation',
    'HTTPNoContent',
    'HTTPResetContent',
    'HTTPPartialContent',
    'HTTPMultipleChoices',
    'HTTPMovedPermanently',
    'HTTPFound',
    'HTTPSeeOther',
    'HTTPNotModified',
    'HTTPUseProxy',
    'HTTPTemporaryRedirect',
    'HTTPPermanentRedirect',
    'HTTPClientError',
    'HTTPBadRequest',
    'HTTPUnauthorized',
    'HTTPPaymentRequired',
    'HTTPForbidden',
    'HTTPNotFound',
    'HTTPMethodNotAllowed',
    'HTTPNotAcceptable',
    'HTTPProxyAuthenticationRequired',
    'HTTPRequestTimeout',
    'HTTPConflict',
    'HTTPGone',
    'HTTPLengthRequired',
    'HTTPPreconditionFailed',
    'HTTPRequestEntityTooLarge',
    'HTTPRequestURITooLong',
    'HTTPUnsupportedMediaType',
    'HTTPRequestRangeNotSatisfiable',
    'HTTPExpectationFailed',
    'HTTPMisdirectedRequest',
    'HTTPUnprocessableEntity',
    'HTTPFailedDependency',
    'HTTPUpgradeRequired',
    'HTTPPreconditionRequired',
    'HTTPTooManyRequests',
    'HTTPRequestHeaderFieldsTooLarge',
    'HTTPUnavailableForLegalReasons',
    'HTTPServerError',
    'HTTPInternalServerError',
    'HTTPNotImplemented',
    'HTTPBadGateway',
    'HTTPServiceUnavailable',
    'HTTPGatewayTimeout',
    'HTTPVersionNotSupported',
    'HTTPVariantAlsoNegotiates',
    'HTTPInsufficientStorage',
    'HTTPNotExtended',
    'HTTPNetworkAuthenticationRequired',
)


############################################################
# HTTP Exceptions
############################################################

class HTTPException(Response, Exception):

    # You should set in subclasses:
    # status = 200

    status_code = None
    empty_body = False

    def __init__(self, *, headers=None, reason=None,
                 body=None, text=None, content_type=None):
        Response.__init__(self, status=self.status_code,
                          headers=headers, reason=reason,
                          body=body, text=text, content_type=content_type)
        Exception.__init__(self, self.reason)
        if self.body is None and not self.empty_body:
            self.text = "{}: {}".format(self.status, self.reason)


class HTTPError(HTTPException):
    """Base class for exceptions with status codes in the 400s and 500s."""


class HTTPRedirection(HTTPException):
    """Base class for exceptions with status codes in the 300s."""


class HTTPSuccessful(HTTPException):
    """Base class for exceptions with status codes in the 200s."""


class HTTPOk(HTTPSuccessful):
    status_code = HTTPStatus.OK


class HTTPCreated(HTTPSuccessful):
    status_code = HTTPStatus.CREATED


class HTTPAccepted(HTTPSuccessful):
    status_code = HTTPStatus.ACCEPTED


class HTTPNonAuthoritativeInformation(HTTPSuccessful):
    status_code = HTTPStatus.NON_AUTHORITATIVE_INFORMATION


class HTTPNoContent(HTTPSuccessful):
    status_code = HTTPStatus.NO_CONTENT
    empty_body = True


class HTTPResetContent(HTTPSuccessful):
    status_code = HTTPStatus.RESET_CONTENT
    empty_body = True


class HTTPPartialContent(HTTPSuccessful):
    status_code = HTTPStatus.PARTIAL_CONTENT


############################################################
# 3xx redirection
############################################################


class _HTTPMove(HTTPRedirection):

    def __init__(self, location, *, headers=None, reason=None,
                 body=None, text=None, content_type=None):
        if not location:
            raise ValueError("HTTP redirects need a location to redirect to.")
        super().__init__(headers=headers, reason=reason,
                         body=body, text=text, content_type=content_type)
        self.headers['Location'] = str(location)
        self.location = location


class HTTPMultipleChoices(_HTTPMove):
    status_code = HTTPStatus.MULTIPLE_CHOICES


class HTTPMovedPermanently(_HTTPMove):
    status_code = HTTPStatus.MOVED_PERMANENTLY


class HTTPFound(_HTTPMove):
    status_code = HTTPStatus.FOUND


# This one is safe after a POST (the redirected location will be
# retrieved with GET):
class HTTPSeeOther(_HTTPMove):
    status_code = HTTPStatus.SEE_OTHER


class HTTPNotModified(HTTPRedirection):
    # FIXME: this should include a date or etag header
    status_code = HTTPStatus.NOT_MODIFIED
    empty_body = True


class HTTPUseProxy(_HTTPMove):
    # Not a move, but looks a little like one
    status_code = HTTPStatus.USE_PROXY


class HTTPTemporaryRedirect(_HTTPMove):
    status_code = HTTPStatus.TEMPORARY_REDIRECT


class HTTPPermanentRedirect(_HTTPMove):
    status_code = HTTPStatus.PERMANENT_REDIRECT


############################################################
# 4xx client error
############################################################


class HTTPClientError(HTTPError):
    pass


class HTTPBadRequest(HTTPClientError):
    status_code = HTTPStatus.BAD_REQUEST


class HTTPUnauthorized(HTTPClientError):
    status_code = HTTPStatus.UNAUTHORIZED


class HTTPPaymentRequired(HTTPClientError):
    status_code = HTTPStatus.PAYMENT_REQUIRED


class HTTPForbidden(HTTPClientError):
    status_code = HTTPStatus.FORBIDDEN


class HTTPNotFound(HTTPClientError):
    status_code = HTTPStatus.NOT_FOUND


class HTTPMethodNotAllowed(HTTPClientError):
    status_code = HTTPStatus.METHOD_NOT_ALLOWED

    def __init__(self, method, allowed_methods, *, headers=None, reason=None,
                 body=None, text=None, content_type=None):
        allow = ','.join(sorted(allowed_methods))
        super().__init__(headers=headers, reason=reason,
                         body=body, text=text, content_type=content_type)
        self.headers['Allow'] = allow
        self.allowed_methods = allowed_methods
        self.method = method.upper()


class HTTPNotAcceptable(HTTPClientError):
    status_code = HTTPStatus.NOT_ACCEPTABLE


class HTTPProxyAuthenticationRequired(HTTPClientError):
    status_code = HTTPStatus.PROXY_AUTHENTICATION_REQUIRED


class HTTPRequestTimeout(HTTPClientError):
    status_code = HTTPStatus.REQUEST_TIMEOUT


class HTTPConflict(HTTPClientError):
    status_code = HTTPStatus.CONFLICT


class HTTPGone(HTTPClientError):
    status_code = HTTPStatus.GONE


class HTTPLengthRequired(HTTPClientError):
    status_code = HTTPStatus.LENGTH_REQUIRED


class HTTPPreconditionFailed(HTTPClientError):
    status_code = HTTPStatus.PRECONDITION_FAILED


class HTTPRequestEntityTooLarge(HTTPClientError):
    status_code = HTTPStatus.REQUEST_ENTITY_TOO_LARGE


class HTTPRequestURITooLong(HTTPClientError):
    status_code = HTTPStatus.REQUEST_URI_TOO_LONG


class HTTPUnsupportedMediaType(HTTPClientError):
    status_code = HTTPStatus.UNSUPPORTED_MEDIA_TYPE


class HTTPRequestRangeNotSatisfiable(HTTPClientError):
    status_code = HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE


class HTTPExpectationFailed(HTTPClientError):
    status_code = HTTPStatus.EXPECTATION_FAILED


class HTTPMisdirectedRequest(HTTPClientError):
    status_code = 421


class HTTPUnprocessableEntity(HTTPClientError):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY


class HTTPFailedDependency(HTTPClientError):
    status_code = HTTPStatus.FAILED_DEPENDENCY


class HTTPUpgradeRequired(HTTPClientError):
    status_code = HTTPStatus.UPGRADE_REQUIRED


class HTTPPreconditionRequired(HTTPClientError):
    status_code = HTTPStatus.PRECONDITION_REQUIRED


class HTTPTooManyRequests(HTTPClientError):
    status_code = HTTPStatus.TOO_MANY_REQUESTS


class HTTPRequestHeaderFieldsTooLarge(HTTPClientError):
    status_code = HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE


class HTTPUnavailableForLegalReasons(HTTPClientError):
    status_code = 451

    def __init__(self, link, *, headers=None, reason=None,
                 body=None, text=None, content_type=None):
        super().__init__(headers=headers, reason=reason,
                         body=body, text=text, content_type=content_type)
        self.headers['Link'] = '<%s>; rel="blocked-by"' % link
        self.link = link


############################################################
# 5xx Server Error
############################################################
#  Response status codes beginning with the digit "5" indicate cases in
#  which the server is aware that it has erred or is incapable of
#  performing the request. Except when responding to a HEAD request, the
#  server SHOULD include an entity containing an explanation of the error
#  situation, and whether it is a temporary or permanent condition. User
#  agents SHOULD display any included entity to the user. These response
#  codes are applicable to any request method.


class HTTPServerError(HTTPError):
    pass


class HTTPInternalServerError(HTTPServerError):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR


class HTTPNotImplemented(HTTPServerError):
    status_code = HTTPStatus.NOT_IMPLEMENTED


class HTTPBadGateway(HTTPServerError):
    status_code = HTTPStatus.BAD_GATEWAY


class HTTPServiceUnavailable(HTTPServerError):
    status_code = HTTPStatus.SERVICE_UNAVAILABLE


class HTTPGatewayTimeout(HTTPServerError):
    status_code = HTTPStatus.GATEWAY_TIMEOUT


class HTTPVersionNotSupported(HTTPServerError):
    status_code = HTTPStatus.HTTP_VERSION_NOT_SUPPORTED


class HTTPVariantAlsoNegotiates(HTTPServerError):
    status_code = HTTPStatus.VARIANT_ALSO_NEGOTIATES


class HTTPInsufficientStorage(HTTPServerError):
    status_code = HTTPStatus.INSUFFICIENT_STORAGE


class HTTPNotExtended(HTTPServerError):
    status_code = HTTPStatus.NOT_EXTENDED


class HTTPNetworkAuthenticationRequired(HTTPServerError):
    status_code = HTTPStatus.NETWORK_AUTHENTICATION_REQUIRED
