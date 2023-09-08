from rest_framework.pagination import PageNumberPagination


class PageNumberPagination(PageNumberPagination):
    """Custom pagination class to provide consistent API pagination hooks.

    This class wraps Django Rest Framework's built-in ``PageNumberPagination`` class.
    """

    page_size_query_param = "page_size"
    page_size = 25
