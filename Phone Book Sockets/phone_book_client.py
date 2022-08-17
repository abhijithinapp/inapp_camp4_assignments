import json
import socket
import re
phoneNumbers = {}
class Utils:
    def getInt(*msg):
        while(True):
            try:
                value = int(input(*msg))
                return value
            except:
                print("Enter a valid number")
                continue

    def getNumber(*msg):
        while(True):
                value = input(*msg)
                if re.match(r'\+[0-9]*', value):
                    return value
                else:
                    print("Enter a valid number")
                    continue


def listAllContacts():
    msgJson = {"option" : 1, "params":None}
    return msgJson

def addContact():
    msg = {}
    name = input("Enter name: ")
    phoneNumber = Utils.getNumber("Enter Phone Number: ")
    msgJson = {"option":2, "params":{"name":name,"phn":phoneNumber}}
    return msgJson



def deleteContact():
    
    nameToBeDeleted = input("Enter the name to be deleted: ")
    msgJson = {"option":3, "params":{"name":nameToBeDeleted}}
    return msgJson

def searchByName():
    name = input("Enter the name to be searched: ")
    msgJson = {"option":4, "params":{"name":name}}
    return msgJson

def searchbyNumber():
    phn = Utils.getNumber("Enter the phone number: ")
    msgJson = {"option":5, "params":{"phn":phn}}
    return msgJson


def actionToSelectedOption(option):
    global msg
    msg = ""
    match(option):
        case 1: msg = listAllContacts()
        case 2: msg = addContact()
        case 3: msg = deleteContact()
        case 4: msg = searchByName()
        case 5: msg = searchbyNumber()
        case 6: msg = exit()
        case _: print("Wrong choice")
    return json.dumps(msg)
            
def handleReply(msgString):
    msg = json.loads(msgString)
    print(msg['status'])
    if (msg['value']):
        print(msg['value'])

def client_program():
    host = socket.gethostname() #get the hostname
    #since both server and client are in the same machine we can get the loopback address as the server addres
    port = 5000 #initiate port no above 1024 till 65535
    #HOST = "127.0.0.1" #statndard loopback interface address ( or localhost)
    #PORT = 65432 #port to listen on (non-priveleged ports are > 1024)
    
    #get instance of socket
    client_socket = socket.socket() 

    #instead of binding, client we are connecting to server
    client_socket.connect((host,port)) #host & port as tuple
    
    #getting the msg to send to the server
    

    while True:
        option = Utils.getInt("""
    Choose the required option
    1. List all contacts
    2. Add a new contact
    3. Delete a contact
    4. Search by name
    5. Search by number
    6. exit
    
    """)
        message = actionToSelectedOption(option)
        if option == 6:
            break
        #if the msg is not 'exit', encode and send it to server
        client_socket.send(message.encode())
        #receive any reply from the server
        data = client_socket.recv(1024).decode()
        #printing the received data as text
        handleReply(data)
        #getting the msg to send to the server
        

    #close the socket connection once the while loop is exited
    print("closing connection ...")
    client_socket.close()

if __name__ == '__main__': 
    client_program()   


