#! /usr/bin/python
import socket  # Import socket module
import signal  # For hadnling SIGINT
import sys


def main():
    port = 50000  # Define port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    host = socket.gethostbyname(socket.gethostname())  # Get machine IP
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Wait for client connection.
    print("Server listening...")

    files = dict()
    while True:
        print("Waiting for incoming connections...")
        conn, (ip, port) = s.accept()
        print("Got connection from:", (ip, port))

        FILE_NAME = conn.recv(1024).decode().replace(chr(0), "")
        if FILE_NAME in files.keys():
            files[FILE_NAME] += 1
            splitted = FILE_NAME.split(".")
            FILE_NAME = splitted[0] + "_" + str(files[FILE_NAME]) + "." + splitted[1]
        else:
            files[FILE_NAME] = 0

        with open(FILE_NAME, "wb") as f:
            print("The file opened")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                # write data to a file
                f.write(data)
            print("The file received")


def signal_handler(sig, frame):
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
