import sys
from socket import *
from urlparse import urlparse
import time

param = sys.argv[1]

def get_http_header_field_value(header, field):
    field_start = header.find(field)
    field_end = header.find('\r\n', field_start)
    # this assumes that there is a space between the
    # field name and value
    field_value_start = field_start + len(field) + 2
    field_value = header[field_value_start : field_end]
    return field_value

def print_html_body(text):
    html_start = text.find("<html")
    html_end = text.find("</html>", html_start)
    print text[html_start : html_end] + "</html>"

def recvall(s):
    response = ""
    while True:
        res = s.recv(4096)
        if not res:
            break
        response += res
    return response

def client(raw_url, redirect_counter):
    url = urlparse(raw_url)
    if url.scheme != "http":
        sys.stderr.write("Error: non-http URL")
        sys.exit(1)
    host, port = url.netloc, url.port
    path = url.path or '/'
    if port:
        port_start = host.find(':')
        host_without_port = host[:port_start]
    else:
        host_without_port = host
        port = 80
    request_line = "GET " + path + " HTTP/1.0\r\n"
    host_header = "Host: " + host + '\r\n\r\n'
    message = request_line + host_header

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((host_without_port,port))
    clientSocket.sendall(message)
    response = recvall(clientSocket)
    # TODO to use the Content-Length header field
    # to know how many bytes to recv
    #content_length = int(get_http_header_field_value(response, "Content-Length"))
    #response = clientSocket.recv(content_length)
    clientSocket.close()

    response_code_start = response.find(' ') + 1
    response_code = int(response[response_code_start : response_code_start + 3])
    if response_code == 200:
        content_type = get_http_header_field_value(response, "Content-Type")
        if "text/html" in content_type:
            print_html_body(response)
            time.sleep(5)
            sys.exit(0)
        else: sys.exit(10)
    elif response_code in (301, 302):
        new_loc = get_http_header_field_value(response, "Location")
        redirect_counter += 1
        if redirect_counter <= 10:
            sys.stderr.write("Redirected to: " + new_loc + '\n')
            client(new_loc, redirect_counter)
        else:
            sys.stderr.write("Error: More than 10 redirects. Giving up.")
            sys.exit(2)
    elif response_code >= 400:
        content_type = get_http_header_field_value(response, "Content-Type")
        if "text/html" in content_type:
            print_html_body(response)
        sys.exit(400)

client(param, 0)
