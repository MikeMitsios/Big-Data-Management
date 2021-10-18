# Import socket module
import socket
import argparse
import os
import random


def byte_len(word):
    return len(word.encode())

#a function that convert to int
def isnumber(value):
    ivalue = int(value)
    return ivalue

#a function that checks with a send if the servers are still connected
def checking_Connection(cons):
    new_list = cons.copy()
    for s in new_list:
        try:
            # print("CHECKING...")
            s.send("ALL GOOD?".encode())
            mess=(s.recv(1024).decode())
            # print(mess)
            if mess!= "YES":
                cons.remove(s)
                continue
        except:
            print("A SERVER HAS BEEN DISCONNECTED")
            cons.remove(s)
            continue

#manages the arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s",action='store',required=True)
parser.add_argument("-i",action='store',required=True)
parser.add_argument("-k",action='store', required=True, type=isnumber)
args = parser.parse_args()
# Create a socket object



# filepath = sys.argv[1]
#open the file of the servers
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
servers_files = open(os.path.join(__location__, args.s))
data_file = open(os.path.join(__location__, args.i))

server_lines = servers_files.readlines()

print(server_lines)
IPS=[]
ports=[]
cons=[]
num_cons=0

for count,l in enumerate(server_lines):
    l2=l.strip().split(" ")
    print(l2)
    IPS.append(l2[0])
    ports.append(l2[1])
    one_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    one_con.connect((l2[0], int(l2[1])))
    #create all the connections
    cons.append(one_con)

#keep the number of connections that we started
total_cons=len(cons)

# IPS, ports=server_lines[:].split(' ')
#checking the connections
checking_Connection(cons)
for s in cons:
    #send data to all servers to set up the servers to receive the keys
    s.send("DATA".encode())
    print(s.recv(1024).decode())

for line in data_file:
    #take a random k-sample of our connections
    sample_cons=random.sample(cons, args.k)
    for s in sample_cons:
        s.send(str(byte_len(line)).encode())
        #print("ESTEILA MEGETHOS")
        s.recv(1024).decode()
        #send each line of the file with the keys
        s.send(line.encode())
        # receive data from the server
        s.recv(1024).decode()
        # s.close()
for s in cons:
    #send end to establish the end of the data trasfering
    s.send("end".encode())
    # print(s.recv(1024).decode())

while True:
    #a useful menu for the commands
    print("##################### MENU #####################")
    print("Write one of the following commands:")
    print("GET key: get informations about a high level key")
    print("DELETE key: Delete a high level key")
    print("QUERY key: Similar to get but it can return value of a subkey")
    print("EXIT: close the program")
    #take the command
    command_line=input()
    checking_Connection(cons)
    #if the servers that are up, are more than the k then keep going else stop
    if len(cons)<args.k:
        for s in cons:
            s.send("EXIT".encode())
            print(s.recv(1024).decode())
        print("the number of remain servers("+str(len(cons))+") is lower than k("+str(args.k)+")")
        break
    # print(total_cons-len(cons))
    #if we type exit then we leave
    if command_line=="EXIT":
        for s in cons:
            s.send("EXIT".encode())
            print(s.recv(1024).decode())
        break
    #wrong command format
    if len(command_line.split(' ', 1))<2:
        print("PLZ follow one of the following commands")
        continue
    #take the command and the parameters
    command_name, command_parameters = command_line.split(' ', 1)
    #if the command is get
    if command_name=="GET":
        for s in cons:
            s.send("GET".encode())
            s.recv(1024).decode()
            #send the byte len
            s.send(str(byte_len(command_parameters)).encode())
            s.recv(1024).decode()
            #send the parameters
            s.send(command_parameters.encode())
            #receives the useful informations
            print("######### "+s.recv(1024).decode())
    elif command_name=="DELETE":
        if total_cons!=len(cons):
            for s in cons:
                #if a server has been disconnected then send the command to "DO NOTHING"
                s.send("DO NOTHING".encode())
                s.recv(1024).decode()
                s.send("THANKS".encode())
                print("######### " + s.recv(1024).decode()+" Cannot Delete if at least one server is disconnected.")
                print("######### The Number of servers that has been disconnected: "+str(total_cons-len(cons)))
        else:
            for s in cons:
                #else if all servers are up then delete it normally
                s.send("DELETE".encode())
                s.recv(1024).decode()
                s.send(str(byte_len(command_parameters)).encode())
                s.recv(1024).decode()
                s.send(command_parameters.encode())
                print("######### "+s.recv(1024).decode())
    elif command_name=="QUERY":
        #send the query and a set of keys to search their values
        for s in cons:
            s.send("QUERY".encode())
            s.recv(1024).decode()
            s.send(str(byte_len(command_parameters)).encode())
            s.recv(1024).decode()
            s.send(command_parameters.encode())
            print("######### "+s.recv(1024).decode())
    else:
        print("PLZ follow one of the following commands")

for s in cons:
    # close all the connections
    s.close()