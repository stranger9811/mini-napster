# telnet program example
import socket, select, string, sys
from thread import *
 
file_name=""
shared_files={}
share_file=0
def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()
    
  
def uploadThread(conn,path,client,file_name):
    fil = open(path,'r')
    full_file = fil.read()
    i=0
    while i<len(full_file):
        if i+1000 < len(full_file):
            s.send("<GIVE "+ client +" " + file_name +" >"+full_file[i:i+1000])
        else:
            s.send("<GIVE "+ client +" " + file_name +" >"+full_file[i:len(full_file)+1])
        i=i+1000
        for j in range(0,10000):
            j=j+1
    

 
#main function
if __name__ == "__main__":
     
    if(len(sys.argv) < 3) :
        print 'Usage : python client.py hostname port'
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. Start sending messages'
    prompt()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    
                    if data.find("<FILE_FOUND>")!=-1:
                        data=data.split("xxx")
                        sys.stdout.write(data[1])
                        client_name = raw_input("Enter (yes/no) to get file\n")
                        if client_name=="yes":
                            
                            client_name = raw_input("Enter id\n")
                            
                            s.send("<DOWNLOAD "+ client_name +" " + file_name +" >") 
                        prompt() 
                        
                    elif data.find("<UPLOAD")!=-1:
                        header=data.split(" ")
                        #header[2] is file name header[1] is client who wants this file
                     
                        for path in shared_files[header[2]]:
                            try:
                               with open(path): pass
                               start_new_thread(uploadThread,(s,path,header[1],header[2]))
                            except IOError:
                               print 'Oh dear,'
                               prompt()
                                
                        
                    elif data.find("<TAKE")!=-1:
                        #header[1]=garbage
                        #header[2]=filename
                        header=data[:data.find(">")+1].split(" ")
                        data=data[data.find(">")+1:]
                        try:
                            fil=open(header[2],'a')
                            fil.write(data)
                        except:
                            sock.send("wrong username entered try again later\n")    
                               
                    else:   
                    #print data
                        sys.stdout.write(data)
                        prompt()
             
            #user entered a message
            else :
                
                msg = raw_input()
                if msg=="SHARE_FILES":
                    share_file=1
                elif msg=="QUERY":
                    share_file=0
                if share_file==1 and msg!="SHARE_FILES":
                    l=msg.split("\t")
                    if len(l)!=2:
                        break
                    try:
                        shared_files[l[0]].append(l[1])
                        
                    except:
                        shared_files[l[0]]=[]
                        shared_files[l[0]].append(l[1])
                    
                
                file_name = msg
                s.send(msg)
                prompt()