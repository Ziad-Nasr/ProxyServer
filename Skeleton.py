from socket import *
import sys
if len(sys.argv) <= 1:
    print ('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
TCP_IP = sys.argv[1]
My_PORT = 8888
tcpSerSock.bind((TCP_IP, My_PORT))
tcpSerSock.listen(5)
print(TCP_IP)
# Fill in end.

while 1:
    # Start receiving data from the client
    print ('\n\nServer is Ready...')
    tcpCliSock, addr = tcpSerSock.accept()
    print ('Received a connection from:', addr)
    # Fill in start.
    message = tcpCliSock.recv(1024)
    urlText = open("Filter.txt", "r")
    blocked = urlText.readlines()
    urlText.close()
    # Fill in end.
    if (len(message) > 0):
        print ("Message:\n", message)
        filename = message.split()[1].decode("utf-8").partition("/")[2]
    # Extract the filename from the given message
        print (message.split()[1])
    #el mafrod akteb hena conidition en law el url blocked
        if not (message.split()[1].decode("utf-8") in blocked):
            print ("FileName: \n",filename)
            fileExist = "false"
            filetouse = "/" + filename
            print ("filetouse")
            print (filetouse)
            print ("filetouse")
            try:
                # Check wether the file exist in the cache
                f = open(filetouse[1:], "rb")
                outputdata = f.readlines()
                fileExist = "true"
                # ProxyServer finds a cache hit and generates a response message
                tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")
                tcpCliSock.send(b"Content-Type:text/html\r\n")
                # Fill in start.
                for items in outputdata:
                    tcpCliSock.send(items)
                f.close()
                # Fill in end.
                
                print ('Read from cache')
            #Error handling for file not found in cache
            except IOError:
                if fileExist == "false":
                    # Create a socket on the proxyserver
                    # Fill in start. 
                    c = socket(AF_INET, SOCK_STREAM)
                    # Fill in end.

                    try:
                        hostn = filename.replace("www.","",1)
                        # hostn = message.split()[4].decode("utf-8")
                        # hostn = "10.5.50.253"
                        print("hostn")
                        print(hostn)
                        # Connect to the socket to port 80
                        # Fill in start.
                        print("c.connect((hostn,80))")
                        c.connect((hostn,80))
                        print("c.connect((hostn,80))")
                        # Fill in end.
                        # Create a temporary file on this socket and ask port 80 for the file requested by the client
                        print ("Test")
                        fileobj = c.makefile('w', None)
                        print ("Test")
                        
                        print("File is caching... Estana")
                        fileobj.write("GET "+"http://" + filename + " HTTP/1.0\n\n")
                        fileobj.close()
                        print("File is Cached... Yalla")
                        # Read the response into buffer
                        # Fill in start.
                        print("Testrb")
                        fileobj2 = c.makefile("rb", None)
                        Read = fileobj2.readlines()
                        print("Read")
                        # Fill in end.
                        # Create a new file in the cache for the requested file.
                        # Also send the response in the buffer to client socket and the corresponding file in the cache
                        print("tmpFile")
                        tmpFile = open("./" + filename,"wb+")
                        # Fill in start.
                        print("Loop")
                        for items in Read:
                            tmpFile.write(items)
                            tcpCliSock.send(items)
                        print("EndLoop")
                        tmpFile.close()
                        c.close()
                        # Fill in end.
                    except:
                        print ("Illegal request")
                        tcpCliSock.send(b"HTTP/1.0 404 Not Found\r\n")
                        tcpCliSock.send(b"Content-Type:text/html\r\n")
                        tcpCliSock.send(b"\r\n\r\n")
                        tcpCliSock.send(b"<h1>404 Not Found</h1>")        
                        tcpCliSock.send(b"<h2>File is Not Found</h2>")        
        else:
            print("Blocked")
            tcpCliSock.send(b"HTTP/1.0 403 Blocked\r\n")
            tcpCliSock.send(b"Content-Type:text/html\r\n")
            tcpCliSock.send(b"\r\n\r\n")
            tcpCliSock.send(b"<h1>This URL is Blocked</h1>")
    else:
        # HTTP response message for file not found
        # Fill in start.
        # tcpCliSock.send("HTTP/1.0 404")
        # Fill in end.
        # Close the client and the server sockets
        tcpCliSock.shutdown(SHUT_RDWR)
        tcpCliSock.close()
        # Fill in start.
        # Fill in end
