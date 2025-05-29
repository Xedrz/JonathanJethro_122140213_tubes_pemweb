def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    
    # Auth routes
    config.add_route('register', '/api/register', request_method=['POST', 'OPTIONS'])
    config.add_route('login', '/api/login', request_method=['POST', 'OPTIONS'])
    config.add_route('home', '/')
    # Book routes
    config.add_route('get_books', '/api/books', request_method=['GET', 'OPTIONS'])
    config.add_route('book_add', '/api/books/add', request_method=['POST', 'OPTIONS'])
    config.add_route('book_detail', '/api/books/{id}', request_method=['GET', 'OPTIONS'])
    config.add_route('book_update', '/api/books/{id}', request_method=['PUT', 'OPTIONS'])
    config.add_route('book_delete', '/api/books/{id}', request_method=['DELETE', 'OPTIONS'])
    
    # Additional routes
    config.add_route('book_list', '/api/user/books', request_method=['GET', 'OPTIONS'])
    config.add_route('book_search', '/api/books/search', request_method=['GET', 'OPTIONS'])
    config.add_route('books_add_options', '/api/add/books', request_method=['OPTIONS'])
    config.add_route('books_id_options', '/api/books/{id}', request_method='OPTIONS')
    config.add_route('books_options', '/api/books', request_method='OPTIONS')
    config.add_route('upload_cover', '/api/books/{id}/cover', request_method=['POST', 'OPTIONS'])
    
    config.scan()