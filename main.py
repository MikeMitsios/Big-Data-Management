# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import argparse
import os
import random
import string


#a function that produces a random string with a specific length
def get_random_string(length):
    word_len=random.randint(1, length)
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(word_len))
    return "\""+result_str+"\""
    # print("Random string of length", length, "is:", result_str)

def isnumber(value):
    ivalue = int(value)
    return ivalue
#based on the type of the function produce a random value
def rand_value_creation(rand_type):
    if rand_type=="string":
        return get_random_string(args.l)
    elif rand_type=="int":
        return random.randint(1, 100)
    else:
        return random.uniform(1, 100)

#pick a random feature from the keyFile
def pick_rand_feature(array):
    rand_pick_pos = random.randint(0, len(array)-1)
    # print(rand_pick)
    rand_pick=array.pop(rand_pick_pos)
    return rand_pick[0],rand_pick[1]

#building the dictionary into diction
def my_dictionary(diction,max_deapth,features):
    available_features = features.copy()
    max_length = random.randint(0, args.m)
    for i in range(max_length):
        #flip a coin to see if the key can go deeper or simple has a value
        deapth = random.randint(0, 1)
        rand_name, rand_type=pick_rand_feature(available_features)
        #if the deapth is 1 then the key will have as value another dictionary
        #we have to check not to exceed the max deapth we have defined
        if deapth==1 and max_deapth>0:
            # print("MPHKA")
            diction[rand_name]={}
            #and we create this nested dictionary calling again the same function
            my_dictionary(diction[rand_name], max_deapth-1,features)
        else:
            #in the other case where we dont have to create a dictionary we just create the random value
            diction[rand_name]=rand_value_creation(rand_type)
        # print("DICT: ",diction)
    # diction["alpha"] = 1

#function that write the dictionary into the open file
def write_my_dict(diction,f):
    counter = len(diction.items())-1
    for key,value in diction.items():
        # print(key,value)
        # print(type(value))
        # print(counter)
        if isinstance(value, dict):
            f.write("\""+str(key) + "\":{")
            write_my_dict(diction[key], f)
            f.write("}")
        else:
            f.write("\""+str(key)+"\":"+str(value))

        if counter != 0:
            f.write("; ")
        counter -= 1



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    mydict={}
    #get the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-k",action='store',required=True)
    parser.add_argument("-n",action='store', required=True, type=isnumber)
    parser.add_argument("-d",action='store', required=True, type=isnumber)
    parser.add_argument("-l",action='store', required=True, type=isnumber)
    parser.add_argument("-m", action='store', required=True, type=isnumber)
    args = parser.parse_args()

    #get the file with the keys_name and the values
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    key_file = open(os.path.join(__location__, args.k))
    print(args.l)
    # print(args.m)
    print(args.k)



    # key_file = open(args.k, 'r')
    Lines = key_file.readlines()
    #a check to see that the arguments inside the keyFile are NOT less than the m(the maximum arguments a key can have)
    Lines2 = [x.strip().split() for x in Lines]
    if args.m>len(Lines2):
        print("PLZ THE NUMBER OF MAXIMUM ELEMENTS SHOULD NOT BE BIGGER THAN THE NUMBER OF FEATURES IN THE GIVEN FILE")
        exit(1)
    #we continue for each line
    for i in range(args.n):
        # print(i)
        key_v="key_"+str(i)
        print(key_v)
        mydict[key_v]={}
        max_length=random.randint(0,args.m)
        max_deapth = random.randint(0, args.d)
        my_dictionary(mydict[key_v],max_deapth, Lines2)


    #we open-create the my_output.txt file to write all the keys
    output = open("my_output.txt", "w+")
    len_dict=len(mydict.items())-1
    count=0
    for k,v in mydict.items():
        # print(k,v)
        output.write((str(k) + " : {"))
        write_my_dict(mydict[k], output)
        #a counter for not putting in the end of the file the \n
        if len_dict!=count:
            output.write("}\n")
        else:
            output.write("}")
        count+=1
