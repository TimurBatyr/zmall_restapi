from rest_framework import pagination


class PostPagination(pagination.LimitOffsetPagination):
    default_limit = 25
    min_limit = 1
    max_limit = 1000
    min_offset = 1
    max_offset = 100