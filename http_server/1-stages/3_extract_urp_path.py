from socket import socket, create_server

def parse_request(data: str) -> tuple[str, str, str]:
    """ """
    lines: list[str] = data.split('\r\n')
    print(f"\tRequest:")
    for line in lines:
        print(f"\t\t{line}")
    first_line: str = lines[0]
    method, path, version = first_line.split(' ')
    return method, path, version

def get_response(path: str) -> str:
    """ """
    response_status_dict: dict[str, str] = {
        "/": "HTTP/1.1 200 OK",
    }
    default_response_status: str = "HTTP/1.1 404 Not Found"
    return response_status_dict.get(path, default_response_status)

def handle_request(client_socket: socket) -> None:
    """ """
    request: str = client_socket.recv(1_024).decode()
    _, path, _ = parse_request(data=request)
    status: str = get_response(path=path)
    headers: str = ""
    body: str = ""
    response: str = "\r\n".join([status, headers, body])
    print(f"\tResponse:\n\t\t{response}")
    client_socket.sendall(response.encode())


def main() -> None:
    """ """
    server_socket: socket = create_server(("localhost", 4221), reuse_port=True)
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