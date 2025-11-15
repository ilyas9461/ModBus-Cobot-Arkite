import socket

# initialize variables
ROBOT_IP = "172.16.0.10"
PRIMARY_PORT = 30001
SECONDARY_PORT = 30002
REALTIME_PORT = 30003
DASHBOARD_SERVER= 29999

# URScript command being sent to the robot
urscript_command = "set_digital_out(1, True)"
UR_PROGRAM_FILE="lys_CobotMetArkiteModbus.urp"  # lys_test1.urp

# Creates new line
NEW_LINE = "\n"

try:
    # Create a socket connection with the robot IP and port number defined above
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # connect to dashboard server on robot IP
        s.connect((ROBOT_IP, DASHBOARD_SERVER))

        # receive connection response
        response = s.recv(1024).decode()
        print(response)

        # Send the command
        s.sendall(("load "+UR_PROGRAM_FILE+NEW_LINE).encode("utf-8"))

        # receive and prints the response
        response = s.recv(1024).decode()
        print(response)

        s.sendall("power on\n".encode())
        response = s.recv(1024).decode()
        print(response)

        while response.find("IDLE") == -1:
            s.sendall("robotmode\n".encode())
            response = s.recv(1024).decode()
            if (response.find("RUNNING")):
                break
            
        print(response)
        
        s.sendall("brake release\n".encode())
        response = s.recv(1024).decode()
        print(response)

        while response.find("RUNNING") == -1:
            s.sendall("robotmode\n".encode())
            response = s.recv(1024).decode()
            
        print(response)    

        s.sendall("play\n".encode())
        response = s.recv(1024).decode()
        print(response)

except Exception as e:
    print(f"An error occurred: {e}")