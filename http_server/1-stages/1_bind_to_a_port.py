from socket import socket, create_server

# TODO Create a class to encapsulate the functionality

def main() -> None:
    """ """
    server_socket: socket = create_server(("localhost", 4221), reuse_port=True)
    print("HTTP Server is running on localhost:4221")
    try:
        while True:
            print("Waiting for a connection...")
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with client: {client_address}")
            client_socket.close()
    except KeyboardInterrupt as e:
        print("HTTP Server is shutting down")
    finally:
        server_socket.close()
        print("HTTP Server has been shut down successfully")

if __name__ == "__main__":
    main()