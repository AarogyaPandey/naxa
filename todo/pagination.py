from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    """
    This class  is used to set the pagination scheme for our API.
    """
    page_size=3
    page_size_query_param='page_size'
    max_page_size=2 