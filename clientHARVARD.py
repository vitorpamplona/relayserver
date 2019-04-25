import socket # for connecting to the server
import json # to enconde and decode the data
import time

relay_server_host = '127.0.0.1'  # as both code is running on same pc
relay_server_port = 5000  # socket server port number

client_id = 'HARVARD'
client_send_to = 'MIT'

def client_program():
    print('Starting Client ' + client_id + ' connecting with ' + client_send_to)  # show in terminal

    client_socket = socket.socket()  # instantiate
    client_socket.connect((relay_server_host, relay_server_port))  # connect to the server

    client_socket.send(json.dumps({"client_id": client_id}).encode())  

    # Wait for 1 seconds otherwise socket concatenates the two sends
    time.sleep(1)

    ############ Runs First layers of ML ##########
    partial_forward_prop_results = "!@#$!#$!#$!@#$!@#$!@"
    
    # send to MIT to contine the process. 
    messageToMIT = {"to": client_send_to, "data": partial_forward_prop_results}
    print('Sending Activation Function ' + messageToMIT['data'] + ' to ' + messageToMIT['to'])
    client_socket.send(json.dumps(messageToMIT).encode())  

    # waits for MIT to finish and receives the results from the back_propagation. 
    partial_backward_prop_resultsRaw = client_socket.recv(1024).decode();
    partial_backward_prop_results = json.loads(partial_backward_prop_resultsRaw) 

    if 'error' not in partial_backward_prop_results.keys(): 
        ############ Continues Back Propagation ##########
        print('Received Gradients ' + partial_backward_prop_results['data'] + ' from ' + partial_backward_prop_results['from'])
    else: 
        print('ERROR: Please start MIT first ')

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()