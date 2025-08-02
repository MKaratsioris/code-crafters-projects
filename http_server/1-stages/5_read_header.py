from socket import socket, create_server

def print_request(request_lines: list[str]) -> None:
    print(f"\tRequest:")
    for line in request_lines:
        print(f"\t\t{line}")

def print_response(status: str, headers: str, body: str) -> None:
    print(f"\tResponse:")
    print(f"\t\t{status}")
    headers_list: list[str] = headers.split('\r\n')
    for header in headers_list:
        print(f"\t\t{header}")
    print(f"\n\t\t{body}")

def parse_request(data: str) -> tuple[str, str, str, list[str]]:
    """ """
    lines: list[str] = data.split('\r\n')
    print_request(request_lines=lines)
    first_line: str = lines[0]
    method, path, version = first_line.split(' ')
    return method, path, version, lines[1:]

def get_response_status(path: str) -> str:
    """ """
    if path.startswith("/") and len(path) == 1:
        return "HTTP/1.1 200 OK"
    if path.startswith("/echo/"):
        return "HTTP/1.1 200 OK"
    if path.startswith("/user-agent"):
        return "HTTP/1.1 200 OK"
    return "HTTP/1.1 404 Not Found"

def get_response_headers(path: str, request_lines: list[str]) -> str:
    """ """
    if path.startswith("/") and len(path) == 1:
        return "Content-Length: 0\r\n"
    if path.startswith("/echo/"):
        return f"Content-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n"
    if path.startswith("/user-agent"):
        for line in request_lines:
            if line.startswith("User-Agent"):
                user_agent_value = line[12:]
                return f"Content-Type: text/plain\r\nContent-Length: {len(user_agent_value)}\r\n"
    return ""
    

def get_response_body(path: str, request_lines: list[str]) -> str:
    """ """
    if path.startswith("/") and len(path) == 1:
        return ""
    if path.startswith("/echo/"):
        return path[6:]
    if path.startswith("/user-agent"):
        for line in request_lines:
            if line.startswith("User-Agent"):
                return line[12:]
    return "404 Not Found"

def handle_request(client_socket: socket) -> None:
    """ """
    request: str = client_socket.recv(1_024).decode()
    _, path, _, req_lines = parse_request(data=request)
    status: str = get_response_status(path=path)
    headers: str = get_response_headers(path=path, request_lines=req_lines)
    body: str = get_response_body(path=path, request_lines=req_lines)
    response: str = "\r\n".join([status, headers, body])
    print_response(status=status, headers=headers, body=body)
    client_socket.sendall(response.encode())

def main():
    server_socket = create_server(("localhost", 4221), reuse_port=True)
    print("[HTTP Server] Running on localhost:4221")
    try:
        while True:
            print("[HTTP Server] Listening for connections...\n")
            client_socket, client_address = server_socket.accept()
            print(f"[HTTP Server] Connection established with client {client_address[0]}:{client_address[1]}")
            handle_request(client_socket=client_socket)
            client_socket.close()
    except KeyboardInterrupt as e:
        print("[HTTP Server] Shutting down...")
    finally:
        server_socket.close()
        print("[HTTP Server] Shut down successfully!")


if __name__ == "__main__":
    main()