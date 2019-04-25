import socket # for connecting to the server
import json # to enconde and decode the data
import time

relay_server_host = '127.0.0.1'  # as both code is running on same pc
relay_server_port = 5000  # socket server port number

client_id = 'MIT'
client_send_to = 'HARVARD'

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

    # waiting for HARVARD to finish the first forward propagation
    msgRaw = client_socket.recv(1024).decode()
    partial_activation_functions = json.loads(msgRaw)  # receive response
    
    ############ Runs last layers layers of Forward propagation ##########
    print('Received Activation Functions ' + partial_activation_functions['data'] + ' from ' + partial_activation_functions['from'])

    ############ Evaluates results ##########
    finish_forward_prop(partial_activation_functions['data'])

    ############ Runs Backprogatation ##########
    partial_gradients = start_backward_prop()

    # send to HARVARD to finish the process. 
    client_socket.send(format_data_msg(client_send_to, partial_gradients))  # send message

    client_socket.close()  # close the connection

def finish_forward_prop(data):
    return ""

def start_backward_prop():
    return "ZXCVZXVCZXVZXCVZXVC"

def format_client_id_msg(client_id):
    return json.dumps({"client_id": client_id}).encode()

def format_data_msg(to, data):
    message = {"to": client_send_to, "data": data}
    print('Sending Gradients ' + message['data'] + ' to ' + message['to'])
    return json.dumps(message).encode()

if __name__ == '__main__':
    client_program()