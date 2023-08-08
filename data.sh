# The following shell script is used to validate the response and also 
# saves the asked data in some directory along with the response

user_query=$1
query_directory=$2
response_directory=$3
gpt_api_key="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"
num_google_results=5

# checking if directory exist
if [ ! -d $query_directory ] && [ ! -d $response_directory ]; then
    echo "The given name $query_directory and $response_directory does not exist hence creating the directory "
    mkdir $query_directory
    mkdir $response_directory
else
    echo "The system found the specified path location and proceeding with same"

# sending the response to the lang_chain.py to get the response to query
python3 lang_chain.py --user-query=$user_query --openai-api-key=$gpt_api_key --num-google-results=$num_google_results --output-path=$out_response 