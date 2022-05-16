import socket
import threading
import os
import math


class Receiver:
    def __init__(self, save_dir):
        self.save_directory = (os.getcwd() if save_dir == "" else save_dir).replace("\\", "/")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST, self.PORT = socket.gethostbyname(socket.gethostname()), 6969
        
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen()

        threading.Thread(target=self.accept_transmitters).start()

        print("\nReceiver running")
        print(f"address is {self.HOST}\n")

    def accept_transmitters(self):
        while True:
            transmitter_socket, transmitter_address = self.sock.accept()
            transmitter_socket.sendall(bytes("connection has been established", "utf-8"))

            receiving_thread = threading.Thread(target=self.receive_data, args=[transmitter_socket])
            receiving_thread.start()

    def receive_data(self, transmitter_socket):
        print("A transmitter has connected\n")
        print("Downloading...\n")
        while True:
            
            recv_buffer = 65536
            
            file_displacement = transmitter_socket.recv(recv_buffer).decode('utf-8')
            
            if file_displacement == "OK200": 
                print("\ntransmission successful")
                break
            
            file_size = transmitter_socket.recv(recv_buffer)
            file_size = int(float(file_size.decode('utf-8')))

            expected_data_packets = int(math.ceil(file_size / recv_buffer))
            file_bytes = b''

            # recieve the separaet data packets and combine them
            for i in range(expected_data_packets):
                data_packet = transmitter_socket.recv(recv_buffer)
                file_bytes += data_packet

            # create the folders inbetween the save directory and file displacement
            file_final_save_directory = self.save_directory + "/" + "/".join(file_displacement.split("/")[0:-1])
            try:
                # try to handle case that folder already exists
                os.makedirs(file_final_save_directory)
            except:
                pass

            file_name = file_displacement.split("/")[-1]
            #print(file_name)
            # save the file with its bytes
            with open(file_final_save_directory + "/" + file_name, "wb") as new_file:
                new_file.write(file_bytes)

