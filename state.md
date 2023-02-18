Things are much easier to implement and predict if you just have one method call. 
One request and one response. You don't have an open connection and a reference to 
a remote object which executes on a remote server.
Look at all the dated protocols which are like a human conversation between a 
client and a server: SMTP, IMAP, FTP, ... Nobody wants the client and the server to
have a chatty dialog like this: 
```
Client: My name is Bob
Server: Hi Bob, nice to meet you.
Server: But are you really Bob?
Server: Please prove to me that you're Bob. You can use method foo, bar, blu for 
authentication
Client: I choose method "blu"
Server: Ok, then please tell send the magic blu token
Client: Here it is xyuasdusd8... I hope you like it.
Server: Fine, I accept this. Now I trust you. Now I know you are Bob
Client: Please show me the first message
Server: here it is:
Server:...
Client: looks like spam. Please delete this message
Server: Now I know that you want to delete this message. 
Server: But won't delete it now. Please send me EXPUNGE to execute the delete.
Client: grrrr, this is complicated. I already told you that I want the message to 
be deleted.
Client: EXPUNGE
...
```
Of course roughly the same needs to be done with HTTP. But HTTP you can cut the 
task into several smaller HTTP requests. This gives the service the chance of 
delegating request-1 to server-a and request-2 to server-b. In the cloud, 
environment containers get created and destroyed in seconds. It is easier without a
long-living connection.
In the above case (IMAP protocol) the EXPUNGE is like a COMMIT in relational 
databases. It is very handy to have a transactional database to implement a 
service. But it makes no sense to expose the transaction to the client.
Stateless is like IPO: Input-Processing-Output.
