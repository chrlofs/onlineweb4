from rest_framework.routers import DefaultRouter, SimpleRouter


class VersionedRouter(SimpleRouter):
    shared_router = DefaultRouter()

    def register(self, *args, **kwargs):
        self.shared_router.register(*args, **kwargs)
        # super().register(*args, **kwargs)  # Python 3 way of calling super method
        super(SimpleRouter, self).register(*args, **kwargs)  # Python 2 way of calling super method


class APIVersionOneRouter(VersionedRouter):
    pass


class APIVersionTwoRouter(VersionedRouter):
    pass


def inherit_version_routes(previous_router, new_router):
    """
    Combines two routers by overriding any route with routes the new router if it already exists in the old router.
    :param previous_router: The routes you want to inherit, if there are no new routes
    :type previous_router: VersionedRouter
    :param new_router: The new routes, which overrides any matching in previous_routes.
    :type new_router: VersionedRouter
    :return: list
    """

    if not previous_router:
        return new_router.shared_router.urls

    prev_urls = previous_router.shared_router.urls
    new_route_names = [u.name for u in APIVersionTwoRouter.shared_router.urls]
    new_routes = [u for u in prev_urls if u.name not in new_route_names]
    new_routes.extend(new_router.shared_router.urls)

    return new_routes


