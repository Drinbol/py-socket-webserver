import socket
import os
import sys

def genheaders(response_code, filetype):
    header_lookup = {
        200: 'HTTP/1.1 200 OK\n',
        404: 'HTTP/1.1 404 Not Found\n',
        204: 'HTTP/1.1 204 No Content\n\n'
    }

    if response_code in header_lookup:
        header = header_lookup[response_code]
    else:
        header = ''

    filetype_lookup = {
        "html": 'Content-Type: text/html\n\n',
        "png": 'Content-Type: image/png\n\n'
    }

    if filetype in filetype_lookup:
        header += filetype_lookup[filetype]
    elif response_code != 204:
        header += 'Content-Type: text/plain\n\n'

    return header


def handlerequest(request_data):
    headers = request_data.split('\n')
    file_name = headers[0].split()[1]
    if file_name == "/favicon.ico":
        return (204, None, "ico")
    file_name = file_name.split('/')[1]
    if file_name == '':
        file_name = 'index.html'
    if not os.path.isfile(file_name):
        return (404, None, None)
    try:
        file_type = file_name.split('.')[1]
        file_object = open(file_name, 'rb')
        return (200, file_object, file_type)
    except:
        return (404, None, None)

def run_server(port_num):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', port_num))
    s.listen(1)

    try:
        while True:
            conn, addr = s.accept()
            data = conn.recv(1024)
            request = data.decode()
            response_code, file_object, file_type = handlerequest(request)
            headers = genheaders(response_code, file_type)
            conn.sendall(headers.encode())
            if response_code == 200:
                for line in file_object.readlines():
                    conn.send(line)
                file_object.close()
            conn.close()
    except KeyboardInterrupt:
        s.close()
        sys.exit(0)

if __name__ == "__main__":
    run_server(int(sys.argv[1]))
