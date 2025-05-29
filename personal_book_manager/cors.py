def cors_tween_factory(handler, registry):
    def cors_tween(request):
        # Handle OPTIONS requests
        if request.method == 'OPTIONS':
            response = request.response
            response.headers.update({
                'Access-Control-Allow-Origin': 'http://localhost:3000',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Max-Age': '86400',  # 24 hours
            })
            return response
        
        # For other requests
        response = handler(request)
        response.headers.update({
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Credentials': 'true',
        })
        return response
    return cors_tween

