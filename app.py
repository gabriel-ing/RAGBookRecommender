from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import irisnative

app = Flask(__name__)
table_name = "BookRecommender.Books"

conversation_history = []


@app.route('/')
def homepage():
    """
    Create homepage by ren the index.html file at the application root. 
    """
    return render_template('index.html')

@app.route('/prompt', methods=["POST"])
def submit():
    '''
    Handles the messaging logic. A message comes in as a POST request to /prompt. 
    It returns a json message containing the models response and the results of the vector search.

    '''
    prompt = request.form['prompt']
    search = request.form.get('search-database')
    search_results = []
    if search=="on":
        response, search_results = rag_chatbot(prompt)
    else:
        print("Not searching database")
        response = text_model_query(prompt, [])
    conversation_history.append({"User Prompt":prompt, "Your response":response})
    return jsonify(message=f"{response}", searchResults = search_results)



def vector_search(user_prompt,num_results = 3):
    '''
    Performs the vector search on the database. 

    The user's prompt is encoded into a vector (same method as used in the database).
    The IRIS-SQL database is then searched
    '''

    search_vector =  model.encode(user_prompt, normalize_embeddings=True).tolist() 
    
    searchSQL = f"""
        SELECT TOP ? title, authors, average_rating AS GoodReads_rating, description
        FROM {table_name}
        ORDER BY VECTOR_COSINE(description_vector, TO_VECTOR(?,double)) DESC
    """
    cursor.execute(searchSQL,[num_results,str(search_vector)])
    
    results = cursor.fetchall()
    return results

def text_model_query(user_prompt, results ):
    '''
    Creates a prompt with:
    - System prompt - this is used to direct the model in certain ways, including how to format the results and to use the search information
    - Search Results - Results of the database vector search
    - Conversation history - This gives the model memory.
    '''

    system_query = """Answer the following prompt using the search results provided below. 
    Use only the information provided in the search results when describing the book.
     Mention at least two options when recommending. 
    Do not refer directly to the search itself, but use the results.
     Please format the response as html.Do not preface the response with anything. Begin the html at the start of the response. Don't add anything additional at the end.
     """
    results_string = "Search Results: "+str(results)
    
    conversation_history_string = "This is the history of your conversation: " + str(conversation_history)

    model_query =  system_query + results_string + conversation_history_string+"Chat prompt: What kind of book would you like? User prompt: " + user_prompt  + "/*/*/"
    

    ## For debugging purposes a shorter query will give a faster response. 
    # Uncomment the following line to use a short placeholder query
    # model_query = "this is a filler query /*/*/"
    
    output = text_model(model_query)

    response = output[0]["generated_text"].split("/*/*/")[1]
    
    return response


def rag_chatbot(user_prompt):
    """
    Combines the vector search and LLM model query into a single function. 
    """
    search_results = vector_search(user_prompt)
    print(search_results)
    output = text_model_query(user_prompt, search_results)
    return output, search_results



if __name__ == '__main__':

    conn = irisnative.createConnection("localhost", 1972, "USER", "SuperUser", "SYS")
    cursor = conn.cursor()
    text_model = pipeline(task="text-generation", model="Qwen/Qwen2.5-1.5B-Instruct")
    # text_model = pipeline(task="text-generation", model="gpt2")
    model = SentenceTransformer('all-MiniLM-L6-v2') 

    app.run(debug=True,host='0.0.0.0', port=5010)