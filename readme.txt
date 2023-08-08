Write a code using Lang chain Library to take a query from an user and search its answer on 
google/gpt3.5 depending on some conditions. 
--If it is its a factual question-Ask google. 
--If it is an emotional question-Ask-Gpt         
--If , its both, scrape the first link of google and use it as context for Gpt and answer the query.

Create the entire code and make a Flask Api where the user sends json query and receives response 
as ("answer": Answer) 

It should send status code 204 when correct, 408 when client-side error and 500 when server side 
error. 
The server-side error must be handled and resolved so that the server does not stop.            
 