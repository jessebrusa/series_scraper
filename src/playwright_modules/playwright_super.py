class PlaywrightSuper:
    def route_intercept(self, route, request):
        # Block URLs that match ad patterns
        if "ad" in request.url or "ads" in request.url:
            route.abort()
        else:
            route.continue_()