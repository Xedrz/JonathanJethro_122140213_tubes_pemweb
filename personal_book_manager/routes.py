def includeme(config):
    """Add routes to the config."""
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    
    # Book routes
    config.add_route('book_search', '/api/books/search')
    config.add_route('book_add', '/api/books/add')
    config.add_route('book_list', '/api/books')
    config.add_route('book_detail', '/api/books/{id}')
    config.add_route('book_update', '/api/books/{id}/update')
    config.add_route('book_delete', '/api/books/{id}/delete')
    config.scan()
