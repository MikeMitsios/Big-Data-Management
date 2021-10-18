import socket
import argparse
import json

#class for creating the Trie structure
class TrieNode(object):
    def __init__(self, char: str):
        self.char = char
        #The children of each node
        self.children = []
        # Is it the last character of the word.`
        self.finished = False
        #if the node has a nested trie
        self.has_nested_trie=False
        #the nested trie structure
        self.nested_trie=None
        #the values of each key
        self.value=None

    #A function that helps printing the whole tree of the trie
    def __str__(self, level=0):
        if self.value is not None:
            ret = "\t" * level + repr(self.char)+ " -> "+repr(self.value) + "\n"
        else:
            ret = "\t" * level + repr(self.char) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
            if child.has_nested_trie:
                ret += child.nested_trie.__str__(level)
        return ret

#A function that adds a key and its value on the trie
def add_to_trie(root, word: str,val: str,value_is_dict=False):
    current=root
    #for each character on the key scans the childrens
    for ch in word:
        found = False
        for child in current.children:
            if ch==child.char:
                #if found go deeper
               current=child
               found = True
               break
        #if not found create a new node and add the missing character
        if not found:
            new_node = TrieNode(ch)
            current.children.append(new_node)
            current= new_node
    current.finished=True
    #if the value is a dictionary then insert a nested trie and add in the value the string form of the dictionary
    if value_is_dict:
        current.nested_trie=TrieNode('*')
        dict_to_trie(val, current.nested_trie)
        current.has_nested_trie=True
        current.value = write_my_dict(val)
    else:
        current.value=val

#A function that deletes a value
def delete_from_trie(root, word: str):
    current=root
    #for each character on the key scans the childrens
    for ch in word:
        found = False
        for child in current.children:
            if ch==child.char:
            #if found go deeper
               current=child
               found = True
               break
        #if not found return False
        if not found:
            return False
    #if it was found delete all the info
    if current.finished==True:
        current.finished=False
        current.has_nested_trie=False
        current.nested_trie=None
        current.value=None
        #and return true
        return True
    else:
        return False


#Search the trie based on the key and finds the value on the finish node
def search_trie(root, word:str):
    current = root
    if root is None:
        return None
    #same scan for each character in every child
    for ch in word:
        found = False
        for child in current.children:
            if ch == child.char:
                current = child
                found = True
                break
        if not found:
            return None
    if current.finished==True:
        return  current

#search a set of keys going deeper on the nested tries
def find_keys(keys, my_trie):
    current_root=my_trie
    for k in keys:
        #search each trie based on the current key we are
        result=search_trie(current_root,k)
        if result==None:
            return None
        else:
            current_root=result.nested_trie

    return result.value

#converts a distionary to trie (including the nested dictionaries)
def dict_to_trie(dictionr, my_trie):
    for key, value in dictionr.items():

        if isinstance(value, dict):
            add_to_trie(my_trie, key, value,True)
            # add_to_trie(my_trie, key, write_my_dict(value))
            # dict_to_trie(value, my_trie)

        else:
            add_to_trie(my_trie,key,value)


#a function that convert to int
def isnumber(value):
    ivalue = int(value)
    return ivalue

#function that converts a dictionary to string
def write_my_dict(diction,my_string=""):
    counter = len(diction.items())-1
    for key,value in diction.items():
        if isinstance(value, dict):
            my_string+="\""+str(key) + "\":{"
            my_string+=write_my_dict(value)
            my_string+="}"
        else:
            my_string+="\""+str(key)+"\":"+str(value)
        if counter != 0:
            my_string+="; "
        counter -= 1
    return my_string


if __name__ == '__main__':
    #manages the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-a",action='store',required=True)
    parser.add_argument("-p",action='store', required=True, type=isnumber)
    args = parser.parse_args()

    # next create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")


    #init the trie structure
    my_trie = TrieNode('*')
    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests
    # coming from other computers on the network
    s.bind((args.a, args.p))
    print("socket binded to %s" % (args.p))

    #a helpful string
    result_string = ""
    #the dictionary that will collect all the keys
    my_data={}

    while True:
        # put the socket into listening mode
        s.listen()
        print("socket is listening")
        # a forever loop until we interrupt it or
        # an error occurs
        # Establish connection with client.
        c, addr = s.accept()
        print('Got connection from', addr)

        while True:
            #first taking the messages that client send to check if the server is down or still up
            checking_connection = c.recv(1024).decode()
            c.send("YES".encode())
            #receive the command that the client is going to do
            command = c.recv(1024).decode()
            print(command)
            #ensures the command he got
            c.send((str(args.p) + ':TOOK COMMAND ' + command).encode())
            #if the command is exit the it leaves
            if command=="EXIT":
                my_data = {}
                my_trie = TrieNode('*')
                break
            #if a message is DATA starts the process  of reading all the keys
            elif command=="DATA":
                #receive the size of the bytes that the key will have
                data=c.recv(1024).decode()
                while data!="end":
                    num_bytes=int(data)
                    #send a thank you mess to client to ensure that he got the size
                    c.send((str(args.p)+':Thank you for MEGETHOS').encode())
                    #receive the key
                    key=c.recv(num_bytes).decode().replace(";",",").replace(" ","")
                    key_name,key_data = key.split(':', 1)
                    #add the key into the main data dictionary
                    my_data[key_name]=json.loads(key_data)
                    print(my_data)
                    # send a thank you message to the client that the key received
                    c.send((str(args.p)+':Thank you for KEY').encode())
                    data = c.recv(1024).decode()
                #convert the my_data dictionary that has all the keys into the trie structure
                dict_to_trie(my_data,my_trie)
                # print the trie that created
                # print(str(my_trie))
            elif command == "GET":
                #again get the bytes of the key
                num_bytes = int(c.recv(1024).decode())
                #ensure for taking the size
                c.send((str(args.p) + ':Thank you for MEGETHOS').encode())
                #receives the key that want to be returned
                key = c.recv(num_bytes).decode()
                #checks the existance of the key in the dictionary structure
                if key in my_data.keys():
                    result_string=write_my_dict(my_data[key])
                    #return the value of the key
                    c.send((str(args.p) +":"+key+"->{"+ result_string+"}" ).encode())
                else:
                    #else return that the key was not found
                    c.send((str(args.p) + ":The key->"+key+" NOT FOUND").encode())
            elif command == "DELETE":
                #the delete command that can only be done when all the servers are up
                num_bytes = int(c.recv(1024).decode())
                c.send((str(args.p) + ':Thank you for MEGETHOS').encode())
                key = c.recv(num_bytes).decode()
                delete_from_trie(my_trie,key)
                if my_data.pop(key, None):
                    c.send((str(args.p) + ":" + key + "->DELETED").encode())
                else:
                    c.send((str(args.p) + ":The key->" + key + " NOT FOUND").encode())
            elif command == "DO NOTHING":
                #do nothing is called when at least one server disconnects
                c.recv(32).decode()
                c.send((str(args.p) + ':Do NOTHING').encode())
            elif command == "QUERY":
                #the query command is a search on the trie structure
                #read the Bytes of the key set
                num_bytes = int(c.recv(1024).decode())
                c.send((str(args.p) + ':Thank you for MEGETHOS').encode())
                #get the key set
                key=c.recv(num_bytes).decode()
                #split the keys and then searches them on the trie
                keys = key.split(".")
                result_string=find_keys(keys,my_trie)
                if result_string is not None:
                    # result_string = write_my_dict(my_data[key])
                    # write_my_dict(my_data[key])
                    #the series of the keys was found
                    c.send((str(args.p) + ":" + key + "->{" + str(result_string) + "}").encode())
                else:
                    #the series of keys was not found
                    c.send((str(args.p) + ":The key->" + key + " NOT FOUND").encode())


        # Close the connection with the client
        print("closing connection")
        c.close()