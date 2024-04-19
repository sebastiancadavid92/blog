from rest_framework.pagination import PageNumberPagination

class Pagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
       
        self.total_queryset = queryset.count()  # Guardar el número total de elementos en el queryset
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return {
            'count': self.total_queryset,  # Número total de elementos en el queryset
            'next': self.get_next_link(),  # Enlace a la página siguiente
            'previous': self.get_previous_link(),
            'current':self.page.number,  # Enlace a la página anterior
            'num_pages': self.page.paginator.num_pages,  # Número total de páginas
            'results': data  # Datos de la página actual
        }

class PaginationLike(PageNumberPagination):
    page_size = 20
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
       
        self.total_queryset = queryset.count()  # Guardar el número total de elementos en el queryset
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return {
            'count': self.total_queryset,  # Número total de elementos en el queryset
            'next': self.get_next_link(),  # Enlace a la página siguiente
            'previous': self.get_previous_link(),
            'current':self.page.number,  # Enlace a la página anterior
            'num_pages': self.page.paginator.num_pages,  # Número total de páginas
            'results': data  # Datos de la página actual
        }