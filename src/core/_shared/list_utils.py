from typing import Final


class ListUtils:
    DEFAULT_PAGE_SIZE: Final = 2

    @staticmethod
    def sort(list_to_sort: list, order_by: str) -> list:
        return sorted(list_to_sort, key=lambda item: (getattr(item, order_by) is None, getattr(item, order_by, "")))

    @staticmethod
    def paginate(list_to_paginate: list, current_page: int) -> list:
        page_offset = (current_page - 1) * ListUtils.DEFAULT_PAGE_SIZE
        return list_to_paginate[page_offset:page_offset + ListUtils.DEFAULT_PAGE_SIZE]