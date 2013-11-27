import socket, select
from thread import *
import sys

query={}
share={}
file_socket={}
ip={}
username={}
reverse_username={}


if __name__ == "__main__":
     
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 5000
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "mini napster has started at " + str(PORT)
 
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
     
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                query[sockfd]=0
                share[sockfd]=0
                file_socket[sockfd]=[]
                ip[sockfd]=addr[0]
                socket_id = str(sockfd)
                socket_id = socket_id[32:socket_id.find('>')]
                
                username[sockfd]=socket_id
                reverse_username[socket_id] = sockfd
            
                print "Client (%s, %s) connected" % addr
             
            #Some incoming message from a client
            else:
                data = sock.recv(RECV_BUFFER)
                
                if data:
                    
                    if data=="SHARE_FILES":
                        print "Client (%s, %s) wants to share files" % addr
                        share[sock]=1
                        query[sock]=0
                        
                    elif data=="QUERY_FILE":
                        print "Client (%s, %s) wants to query a file" % addr
                        share[sock]=0
                        query[sock]=1
                        
                    elif data.find("<DOWNLOAD")!=-1:
                        data=data.split(" ")
                        try:
                            reverse_username[data[1]].send("<UPLOAD"+" "+username[sock]+" "+data[2]+" >")
                        except:
                            sock.send("unable to tell client to upload file\n")
                        
                    elif data.find("<GIVE")!=-1:
                        header=data[:data.find(">")+1].split(" ")
                        data="<TAKE "+header[1]+" "+header[2]+" >"+data[data.find(">")+1:]
                        
                        try:
                            reverse_username[header[1]].send(data)
                        except:
                            print "TAKE command is not working \n"
                        
                        
                    elif data:
                        
                        if share[sock]:
                            if data.find("\t")==-1:
                                print "Client (%s, %s) mentioned incorrect format" % addr
                            else:
                                data = data.split("\t")
                                print "Client (%s, %s) shared %s having path = %s" % (addr[0],addr[1],data[0],data[1])
                                file_socket[sock].append(data)
                        if query[sock]:
                            query_answer="\nid\t\tpath\n"
                            flag=0
                            for socket_single in file_socket:
                                if sock==socket_single:
                                    continue
                                    
                                for file in file_socket[socket_single]:
                                    if file[0]==data:
                                        flag=1
                                        query_line=username[socket_single]+"\t"+file[1]+"\n"
                                        query_answer=query_answer+query_line
                        
                            if flag==0:
                                query_answer="\nOOPS!!!!! no such file found\n"
                            else:
                                query_answer="<FILE_FOUND>xxx"+query_answer+"\n"
                      
                            sock.send(query_answer)
                                   
                            
                else:
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    query.pop(sock)
                    share.pop(sock)
                    file_socket.pop(sock)
                    ip.pop(sock)
                    reverse_username.pop(username[sock])
                    username.pop(sock)
                    
                    CONNECTION_LIST.remove(sock)
                    continue
                                              
              
          
     
    server_socket.close()