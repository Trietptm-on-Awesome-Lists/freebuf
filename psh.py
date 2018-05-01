#!/user/bin/python2.7
import socket
import threading
import getopt
import subprocess
import sys
 
listen = False
command = False
upload = False
execute =""
target = ""
port = 0
upload_destination = ""
 
def use():
    print("Examples:")
    print("./tcp.py -l -t localhost -p 9999")
 
def client_sender(buffer):
    client  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((target,port))
        if len(buffer):
            client.send(buffer)
                     
        while True:
            recv_len = 1
            res = ""
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                res += data
                if recv_len < 4096:
                     break
            print(res)
            buffer = raw_input("")
            buffer += "\n"
            client.send(buffer)
    except:
        print("[*] Exception!!!!  exiting!!!!")
        client.close()
 
def run_command(command):
    command = command.rstrip()
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    except:
        output = "Failed to execute command.\r\n"
 
    return output
 
def loop_server():
    global target
    if not len(target):
        target = "0.0.0.0"
 
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(3)
    while True:
       client_socket,addr = server.accept()
        
     
       client_socket.send('hello i am server!!!')
       client_thread = threading.Thread(target=client_handler,args=(client_socket,))
       client_thread.start()
 
def client_handler(client_socket):
    global command
    if command:
        while True:
            client_socket.send("<BHP:#> ")
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
                resp = run_command(cmd_buffer)
                client_socket.send(resp)
         
 
 
 
def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
 
    if not len(sys.argv[1:]):
        use()
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",["help","listen","target","port","command","upload"])
    except getopt.GetoptError as err:
        print str(err)
        use()
    for o,a in opts:
        if o in ("-h","--help"):
            use()
        elif o in ("-l","--listen"):
            listen = True
        elif o in ("-t","--target"):
            target = a
        elif o in ("-p","--port"):
            port = int(a)
        elif o in ("-c","--command"):
            command = True
        else:
            assert False,"Not this Option!!!!"
 
    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()
        client_sender(buffer)
 
    if listen:
        loop_server()
 
 
main()