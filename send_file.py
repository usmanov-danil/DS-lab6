# Import libraries
import sys
import socket
import os


def main():
    if len(sys.argv) != 4:
        print("As arguments should be passed: the name of file, server address, port")
        exit(0)

    # Get args
    FILE_NAME = sys.argv[1]
    HOST = sys.argv[2]
    PORT = int(sys.argv[3])
    BUFFER_SIZE = 1024

    # Create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # Send file
    with open(FILE_NAME, "rb") as f:
        print("The file opened")
        s.send(FILE_NAME.ljust(BUFFER_SIZE, chr(0)).encode())

        l = f.read(BUFFER_SIZE)
        percent_sent_old = -1
        cnt = len(l)
        FILE_SIZE = os.path.getsize(FILE_NAME)

        while l:
            s.send(l)
            if FILE_SIZE == 0:  # The file has size less than byte
                FILE_SIZE = cnt
                print("mda")

            percent_sent = int(100 * (cnt / FILE_SIZE))
            if percent_sent > percent_sent_old:
                print("Sent: {}%".format(percent_sent))

            l = f.read(BUFFER_SIZE)
            cnt += len(l)
            percent_sent_old = percent_sent

    print("Done sending")
    s.close()


if __name__ == "__main__":
    main()
