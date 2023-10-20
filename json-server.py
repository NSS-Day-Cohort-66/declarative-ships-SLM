import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status


# Add your imports below this line
from views import ShippingShipsView, HaulerView, DocksView


class JSONServer(HandleRequests):

    def do_GET(self):
        url = self.parse_url(self.path)
        view = self.determine_view(url)

        try:
            view.get(self, url["pk"])
        except AttributeError:
            return self.response("No view for that route", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_PUT(self):
        url = self.parse_url(self.path)
        view = self.determine_view(url)

        try:
            view.update(self, self.get_request_body(), url["pk"])
        except AttributeError:
            return self.response("No view for that route", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_POST(self):
        # Parse the URL
        url = self.parse_url(self.path)
        # Determine the correct view needed to handle the requests
        view = self.determine_view(url)
        # Get the request body
<<<<<<< HEAD
        request_body = self.get_request_body()
        # Invoke the correct method on the view
        try:
            view.create(self, request_body)
        # Make sure you handle the AttributeError in case the client requested a route that you don't support
        except AttributeError:
            return self.response("No view for that route", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
=======
        body = self.get_request_body()
        # Invoke the correct method on the view
        try:
            view.get(self, body, url["pk"])
        # Make sure you handle the AttributeError in case the client requested a route that you don't support
        except AttributeError:
            return self.response("No view for that route", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
        # Once you implement this method, delete the following line of code
        # return self.response("", status.HTTP_405_UNSUPPORTED_METHOD.value)
>>>>>>> 49b53a7 (garbage code)

    def do_DELETE(self):
        url = self.parse_url(self.path)
        view = self.determine_view(url)

        try:
            view.delete(self, url["pk"])
        except AttributeError:
            return self.response("No view for that route", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def determine_view(self, url):
        """Lookup the correct view class to handle the requested route

        Args:
            url (dict): The URL dictionary

        Returns:
            Any: An instance of the matching view class
        """
        try:
            routes = {
                "docks": DocksView,
                "haulers": HaulerView,
                "ships": ShippingShipsView,
            }

            matching_class = routes[url["requested_resource"]]
            return matching_class()
        except KeyError:
            return status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value


#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    host = ''
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
