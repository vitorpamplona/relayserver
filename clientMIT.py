import socket # for connecting to the server
import json # to enconde and decode the data
import time

relay_server_host = '127.0.0.1'  # as both code is running on same pc
relay_server_port = 5000  # socket server port number

client_id = 'MIT'
client_send_to = 'HARVARD'

def client_program():
    print('Starting Client ' + client_id + ' connecting with ' + client_send_to)  # show in terminal

    client_socket = socket.socket()  # instantiate
    client_socket.connect((relay_server_host, relay_server_port))  # connect to the server

    client_socket.send(json.dumps({"client_id": client_id}).encode())  

    # Wait for 1 seconds otherwise socket concatenates the two sends
    time.sleep(1)

    # waiting for HARVARD to finish the first forward propagation
    msgRaw = client_socket.recv(1024).decode()
    partial_forward_prop_results = json.loads(msgRaw)  # receive response
    
    ############ Runs last layers layers of Forward propagation ##########
    print('Received Activation Functions ' + partial_forward_prop_results['data'] + ' from ' + partial_forward_prop_results['from'])

    ############ Evaluates results ##########

    ############ Runs Backprogatation ##########
    partial_backpropagation_prop_results = "ZXCVZXVCZXVZXCVZXVC"

    # send to HARVARD to finish the process. 
    messageToHarvard = {"to": client_send_to, "data": partial_backpropagation_prop_results}
    print('Sending Gradients ' + partial_forward_prop_results['data'] + ' to ' + partial_forward_prop_results['from'])
    client_socket.send(json.dumps(messageToHarvard).encode())  # send message

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()