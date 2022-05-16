import socket
import sys
import os
import transmitter
import receiver

class Share:
    def __init__(self): 
        self.run()
    

    def run(self):
        if self.has_args():
            self.handle_arg_input()
        else:
            self.handle_manual_input()

    def check_directory(self, dir):
        dir = dir.replace("\\", "/")
        if not os.path.isdir(dir):
            print("that directory does not exist")
            return None
        else:
            return dir


    def handle_manual_input(self):
        mode = input("mode (r/t): ").lower()
        
        if  mode == "r":
            save_directory = input("save directory: ").replace("\\", "/")
            self.run_receiver(save_directory)
        
        elif mode == "t":
            ip = input("receiver ip: ")
            directory = input("file directory: ").replace("\\", "/")
            self.run_transmitter(ip, directory)

    # neds bit of debuggin. 
    def handle_arg_input(self):
        if sys.argv[1] == '-r':
            self.run_receiver()
        
        elif sys.argv[1] == '-t':
            print("t mode")
            if len(sys.argv) == 4:
                recv_ip = sys.argv[2]
                to_send = (os.getcwd() + "/" + (sys.argv[3] if sys.argv[3] != '.' else "")).replace("\\", "/")
                self.run_transmitter(recv_ip, to_send)
        
        else:
            print(self.get_help_msg())
            input("Press Enter to finish")

    
    def has_args(self):
        return len(sys.argv) > 1


    def run_transmitter(self, recv, dir):
        print("Running in Transmitter Mode\n")
        confirmation = input(f"Are you sure you want to send {dir} to {recv}? (y/n): ")
        
        if confirmation.lower() != "y":
            return

        transmitter.Transmitter(recv, dir)
        input("\nPress enter to finish")


    def run_receiver(self, save_dir):
        receiver.Receiver(save_dir)
        

    def get_help_msg(self):
        msg = """
            wrong input
        """
        return msg
        

share = Share()







    
        
