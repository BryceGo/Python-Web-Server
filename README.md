# Python Web Server
This script uses the http get methods from browsers to return html files
Use localhost:5000/home to start the server
Default port is curently at 5000.
The root html is within this python code under the string named welcome_page.
For files other than the /home or root however, you would need to place an html file on the same folder as the web server
Then you can access it by doing localhost:5000/hello.html  - Assuming hello.html file was the added file
Sending a request for versions other than HTTP/1.1 will issue a 505 Error (Assuming that a 404 has not yet been issued)
