import socket
import time
import folderscan


class Transmitter:
    def __init__(self, receiver, directory):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.connect((receiver, 6969))
        except:
            print(f"There was an error connecting to {receiver}")

        self.send_directory(directory)

    def send_directory(self, directory):
        print("\nSending Files...\n")
        
        folder_size = 0
        start_time = time.time()

        files = folderscan.get_files(directory)
        for file in files:
            with open(file, "rb") as file_open:
                
                file_displacement = directory.split("/")[-1] + "/" + ("/".join([i for i in file.split("/") if i not in directory.split("/")]))
                file_bytes = file_open.read()
                file_size = len(file_bytes)
                #print(file_size)
                folder_size += file_size

                # send data to receiver     *time interevals so that packets dont concatinate on receiver
                self.sock.sendall(bytes(file_displacement, "utf-8"))
                time.sleep(0.5)
                self.sock.sendall(bytes(str(file_size), "utf-8"))
                time.sleep(0.5)
                self.sock.sendall(file_bytes)
                time.sleep(0.5)

                print(file.split("/")[-1])
        

        # completion message
        self.sock.sendall(bytes("OK200", "utf-8"))

        finish_time = time.time() - start_time
        print(f"\n{folder_size} bytes successfuly sent in {round(finish_time, 2)} seconds")
        print("Transmission complete\n")
