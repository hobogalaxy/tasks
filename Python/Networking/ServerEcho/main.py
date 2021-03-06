from server import Server
import socket


def main():
    server = Server()

    try:
        server.initialize_socket()
    except socket.error:
        print("Error: Initializing socket failed.")

    host = input("Type server IP or just press enter to use default (default is {}):".format(server.DEFAULT_HOST))
    host = host.strip()  # get rid of whitespaces at the end and beginning
    if host == "":
        host = server.DEFAULT_HOST

    allowed_chars = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'}
    if not set(host).issubset(allowed_chars) or len(host) < 7 or len(host) > 15 or host.count('.') != 3:
        print("Incorrect IP address.")
        server.close_all()
        return

    port = input("Type port number or just press enter to use default (default is {}):".format(server.DEFAULT_PORT))

    if port != "":
        try:
            port = int(port)
        except ValueError:
            print("Error: Given input is not a number.")
            server.close_all()
            return
    else:
        port = server.DEFAULT_PORT

    while True:
        try:
            print("Server is listening...")
            conn, addr = server.run(host=host, port=port)
        except socket.error:
            print("Error: Could not establish server.")
            server.close_all()
            return

        print("Connection established with address:", addr, end="\n\n")

        disconnected = server.echo_service(conn, addr)
        conn.close()
        if not disconnected:    # if there was error than break loop
            break

    server.close_all()

    print("Server closed.")


if __name__ == "__main__":
    main()
