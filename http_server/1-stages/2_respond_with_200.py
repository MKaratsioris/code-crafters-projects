from socket import socket, create_server

# TODO Create a class to encapsulate the functionality

def handle_request(client_socket: socket) -> None:
    """ """
    request: str = client_socket.recv(1_024).decode()
    print(f"Request:\n{request}")
    status: str = "HTTP/1.1 200 OK"
    headers: str = ""
    body: str = ""
    response: str = "\r\n".join([status, headers, body])
    client_socket.sendall(response.encode())


def main() -> None:
    """ """
    server_socket: socket = create_server(("localhost", 4221), reuse_port=True)
    print("HTTP Server is running on localhost:4221...")
    try:
        while True:
            print("Waiting for a connection...")
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with client ({client_address})")
            handle_request(client_socket=client_socket)
            client_socket.close()
    except KeyboardInterrupt as e:
        print("HTTP Server is shutting down...")
    finally:
        server_socket.close()
        print("HTTP Serber has been shut down successfully!")


if __name__ == "__main__":
    main()
