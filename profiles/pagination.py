from rest_framework.pagination import PageNumberPagination


class CommonPagination(PageNumberPagination):
    """Pagination for common views."""

    page_size = 100
    page_size_query_param = "page_size"