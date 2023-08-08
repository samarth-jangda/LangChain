# The following script is intended to use flask apis to recieve the call from frontend which will
# be send to the langchain library for getting response from the model
# The expected response from the frontend will be properly validated along woth the responses
    # 1) 204 Response: If the response is successful
    # 2) 408 Response: If there is a client side error
    # 3) 500 Response: If these is a server side error

import subprocess    
from flask import Flask, jsonify, request, Response

app = Flask(__name__)

# getting all the saved queries
@app.route("/ask_query", methods=['GET'])
def get_query():
    """
    The following function is used to get the queries saved in the past
    """
    data='Past Queries'
    return jsonify({'data':data})

# posting new query
@app.route("/post_query", methods=['POST'])
def post_query():
    """
    The following function is used to post the query to the lang chain model and get the corresponding response
    """    
    # the response being posted by the user
    data = request.get_json()
    if data !=  None:
        # now to post the following response to the lang chain model to get a response
        query_answer= subprocess.run([f'./data_validation.sh {data} exp/queries exp/responses'])
        # get the saved response in specified directory
        return jsonify({"Message":query_answer, "Response": Response(status=204)})
    else:
        # case if the user didn't pass any query
        print("Since the data is [None] hence sending the reply as 408 to the user")
        return jsonify({"Message":"No Query found", "Response": Response(status=408)})

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": 'Internal Server Error', "message": 'Something went wrong on the server.', "Response": Response(status=500)})   

if "__main__" == __name__:
    app.run(debug=True, port=5005)