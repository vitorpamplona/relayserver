import socket # for connecting to the server
import _thread # to manage multiple clients
import json # to enconde and decode the data

host = '127.0.0.1'
port = 5000  # initiate port no above 1024

clients = {}

def server_program():
    print('Starting Relay Server at ' + host + ':' + str(port))  # show in terminal
    print('Waiting for clients...')

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many clients the server can listen simultaneously
    server_socket.listen(2)

    while True:
        conn, address = server_socket.accept()  # accept new connection
        _thread.start_new_thread(on_new_client,(conn, address)) #puts into a thread. 

    server_socket.close()  # close the connection

def on_new_client(clientsocket, addr):
    # print("Connection from: " + str(addr))
    # print("Waiting for client name...")

    # wait for the first message. 
    msgRaw = clientsocket.recv(1024).decode()
    # print("Message received: " + msgRaw)
    
    # Register the socket name at a list. 
    msgDict = json.loads(msgRaw)
    print(msgDict['client_id'] + " connected")
    clients[msgDict['client_id']] = clientsocket

    wait_for_next_message(clientsocket, msgDict['client_id'])

def wait_for_next_message(clientsocket, client_id): 
    # wait for a message. 
    msgRaw = clientsocket.recv(1024).decode()

    while msgRaw:      
        print("Message received from " + client_id + ": " + msgRaw)
        msgDict = json.loads(msgRaw)

        if msgDict['to'] in clients.keys():
            #reformat the message    
            formattedMsg = json.dumps({'from': client_id, 'data': msgDict['data']})
            # sending it to the next partner   
            clients[msgDict['to']].send(formattedMsg.encode())  # send data to the client
        else:
            print(msgDict['to'] + ' is not connected')
            # could not find the other socket 
            formattedMsg = json.dumps({'error':msgDict['to']+ ' not found'})
            # sending error message back.
            clientsocket.send(formattedMsg.encode())  # send data to the client

        #wait for next message
        msgRaw = clientsocket.recv(1024).decode()

    clientsocket.close()

if __name__ == '__main__':
    server_program()