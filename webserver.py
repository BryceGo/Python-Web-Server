#Python 2.7.3

#Created by: Bryce Golamco
#bgolamco@sfu.ca

#To use the webserver, Start the server by typing "python webserver.py"
#Open the browser with the following:
#localhost:5000     or      localhost:5000/home
#Default port is curently at 5000
#The root html is within this python code under the string named welcome_page.
#For files other than the /home or root however, you would need to place an html file on the same folder as the web server
#Then you can access it by doing localhost:5000/hello.html  - Assuming hello.html file was the added file
#Sending a request for versions other than HTTP/1.1 will issue a 505 Error (Assuming that a 404 has not yet been issued)



from socket import *
import os

listen_port = 5000                              #Port number of the listening socket, change this number to change the port
listen_socket = socket(AF_INET,SOCK_STREAM)     #The Socket
listen_socket.bind(('',listen_port))            #Binds the socket with port number
listen_socket.listen(5)                         #Listens for 5 parralel connection

#The welcome page html of the server
welcome_page = """

<html>
<h1>
This is the welcome page of the server.
</h1>
<li> Created by: Bryce Golamco </li>
<li> Student Number: ******* </li>
<li> Email: bgolamco@sfu.ca </li>

</html>
"""

#The Error 404 page of the server
error_404 = """

<html>
<h1>ERROR 404, PAGE NOT FOUND</h1>
</html>
"""

#The Error 505 page of the server
error_505 = """

<html>
<h1>ERROR 505, HTTP Version Not Supported
</html>
"""

#Prints out the port number listening from out to the console
print ("Server waiting for requests on port number: " + str(listen_port))

while True:
    connect_socket, connect_addr = listen_socket.accept()
    request = connect_socket.recv(1024)

    if len(request) < 5:                       #Sometimes recieves a request with nothing inside, this prevents the server from crashing
        continue
    
    request = request.split("\n")               #separates the message by line
    status_line = request[0].split(" ")         #splits the status line so we can get the HTTP method, PATH and HTTP version
    request_message = status_line[0]            #HTTP Method
    path = status_line[1]                       #Path 
    version_r = status_line[2].split("\r")      #HTTP Version with /r at the very end
    version = version_r[0]                      #Sets the http version without the \r in the string

    if request_message == "GET":                #Has to be a GET request, otherwise 400 Bad Request is given
        if os.path.isfile("." + path):          #Checks to see if there is a file on the system that the server is asking for.
            if version == "HTTP/1.1":           #Note that the file has to be in the same folder as the web server
                filename = path.strip("/")
                file = open(filename, "r")
                response = "HTTP/1.1 200 OK\n\n" + file.read()
                file.close()
            else:
                response = "HTTP/1.1 505 HTTP Version Not Supported" + error_505    #Issues a 505 error   
        elif path == "/" or path == "/home":    #Checks to see if it requests the home or root path which gives it the welcome page of the server (Assuming It doesn't get an error later)
            if version == "HTTP/1.1":           #Has to be of version HTTP/1.1 otherwise an error 505 is given
                response = "HTTP/1.1 200 OK" + welcome_page     #If Request,Path and Version are ok, it sends the welcome page with a 200 
            else:                               
                response = "HTTP/1.1 505 HTTP Version Not Supported" + error_505 
        else:
            response = "HTTP/1.1 404 Not Found" + error_404
    else:
        response = "HTTP/1.1 400 Bad Request"
    

    connect_socket.send(response)
    connect_socket.close()
