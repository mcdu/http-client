# http-client
Simple http client similar in functionality to Unix's curl.

# Basic usage:

Takes one parameter: an http web address to fetch.

Example:

$ python http_client.py http://www.catb.org/esr/faqs/hacker-howto.html

A port number may also be included after the URL preceded by a colon, as in: http://portquiz.net:8080/

If successful (eventually gets "200 OK" response), returns exit code 0 and prints response body (html code) to stdout.

# Restrictions:

- Only supports input URLs starting with "http://" (no HTTPS)
- All requests are assumed to use the HTTP "GET" method
- The response's content-type should be "text/html".
- The client can understand and follow 301 and 302 redirects.
        - An example of a url with a 301 permanent redirect is http://airbedandbreakfast.com/ which redirects to https://www.airbnb.com/belong-anywhere
        - An example of a url with a 302 temporary redirect is http://maps.google.com/ which redirects to http://maps.google.com/maps, 
        which redirects to https://www.google.com:443/maps
After 10 redirects, it will give up and return an error.
