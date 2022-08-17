
import re
import socket
import json
phoneNumbers = {}

def addContact(params):
    name = params['name']
    phoneNumber = params['phn']
    phoneNumbers[name] = phoneNumber 
    msg = json.dumps({"status" : "Contact added successfully",
    "value" :None})
    return msg
    

def listAllContacts():
    value = ""
    for i,x in enumerate(phoneNumbers):
        value += "\n{}. Name: {} Phonenumber: {}".format(i+1,x,phoneNumbers[x])
    msg = json.dumps({"status" : "Found Contacts",
    "value" :value})
    return msg
    
def deleteContact(params):
    
    nameToBeDeleted = params['name']
    if nameToBeDeleted in phoneNumbers.keys():
        del phoneNumbers[nameToBeDeleted]
        status = "Number Deleted!"
    else: 
        status = "Name not found"
    msg = json.dumps({"status" : status,
    "value" :None})
    return msg

def searchByName(params):
    name = params['name']
    if name in phoneNumbers.keys():
        status = "Name found"
        value = "Name: {}     Phone Number: {}".format(name,phoneNumbers[name])
    else:
        status = "Name not found"
        value = None
    msg = json.dumps({"status" : status,
    "value" :value})
    return msg


def searchbyNumber(params):
    phn = params['phn']
    if phn in phoneNumbers.values():
        for name,phn_number in phoneNumbers.items():
            if phn_number == phn:
                status = "Name found"
                value = "Name : {} Phone Number: {}".format(name,phn_number)
    else:
        status = "Phone number not found"
        value = None
    msg = json.dumps({"status" : status,
    "value" :value})
    return msg

def actionToSelectedOption(option, params):
    global msg
    msg = ""
    match(option):
        case 1: msg = listAllContacts()
        case 2: msg =  addContact(params)
        case 3: msg = deleteContact(params)
        case 4: msg = searchByName(params)
        case 5: msg = searchbyNumber(params)
        case 6: msg = exit()
        case _: msg =print("Wrong choice")
    return msg   

def handlerequest(jsonString):
    message = json.loads(jsonString)
    msg = actionToSelectedOption(message["option"],message["params"],)
    return msg

    
def server_program():
    host = socket.gethostname() # getting the ip of host
    port = 5000
    server_socket = socket.socket()
    server_socket.bind((host,port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection accepted from " + str(address))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("Message from client" + str(address) + " : " + str(data))
        msg = handlerequest(str(data))
        conn.send(msg.encode())
    conn.close()

if __name__ == '__main__':
    server_program()