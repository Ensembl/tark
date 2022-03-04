from django.db import connection, connections


def SqlPrintingMiddleware(get_response):
    def middleware(request):
        response = get_response(request)
        for query in connections['tark'].queries:
            print(f"Query: {query['sql']}, Time: {query['time']}")
        return response
    return middleware