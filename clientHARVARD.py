import socket # for connecting to the server
import json # to enconde and decode the data
import time

relay_server_host = '127.0.0.1'  # as both code is running on same pc
relay_server_port = 5000  # socket server port number

client_id = 'HARVARD'
client_send_to = 'MIT'

def client_program():
    print('Starting Client ' + client_id + ' connecting with ' + client_send_to)  # show in terminal

    # instantiate
    client_socket = socket.socket()  
    # connect to the server
    client_socket.connect((relay_server_host, relay_server_port)) 

    # register this computer by name
    client_socket.send(format_client_id_msg(client_id))  

    # Wait for 1 second otherwise socket concatenates the two sends
    time.sleep(1)

    ############ Runs First layers of ML ##########
    activation_functions = calculate_partial_forward_prop()
    
    # send to MIT to contine the process. 
    client_socket.send(format_data_msg(client_send_to, activation_functions))  

    # waits for MIT to finish and receives the results from the back_propagation. 
    gradientsRaw = client_socket.recv(1024).decode();
    gradients = json.loads(gradientsRaw) 

    if 'error' not in gradients.keys(): 
        ############ Continues Back Propagation ##########
        print('Received Gradients ' + gradients['data'] + ' from ' + gradients['from'])

        calculate_partial_backward_prop(gradients['data'])
    else: 
        print('ERROR: Please start MIT first ')

    client_socket.close()  # close the connection

def calculate_partial_forward_prop():
    return "!@#$!#$!#$!@#$!@#$!@"

def calculate_partial_backward_prop(gradients):
    return ""

def format_client_id_msg(client_id):
    return json.dumps({"client_id": client_id}).encode()

def format_data_msg(to, data):
    message = {"to": client_send_to, "data": data}
    print('Sending Gradients ' + message['data'] + ' to ' + message['to'])
    return json.dumps(message).encode()

if __name__ == '__main__':
    client_program()