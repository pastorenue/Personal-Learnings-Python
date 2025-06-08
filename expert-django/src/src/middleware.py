# In a file like yourapp/middleware.py
class SkipStaticFileProfilingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for a static file
        path = request.path.lower()
        if path.endswith(('.ico', '.css', '.js', '.jpg', '.png', '.gif', '.svg')):
            # Set a flag that the profiler middleware can check
            request._skip_profile = True
        
        return self.get_response(request)