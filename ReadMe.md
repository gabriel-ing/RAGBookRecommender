# AI book recommender application using IRIS vector search

Example Python implementation vector search using IRIS vector search (using IRIS native for database querying). This example is based off the [hackathon-kit github](https://github.com/intersystems-community/hackathon-kit/tree/main) and uses a database downloadable from [kaggle](https://www.kaggle.com/datasets/dylanjcastillo/7k-books-with-metadata). I ran this from a community edition of iris, downloadable with docker. 

I opted to use a local LLM as this is free to download and use. As a result, this application uses a lot of drive space (the LMM model I use is ~4GB) and takes a long time to provide a response to the query. The responses are also poor compared to standard langauge models available - the model ignores a lot of the system prompt information provided and gives unpredicatable results. As this is for demonstration/learning purposes this is not an issue for me, but for real uses it would be best to use a better LLM.#

Please note, as this is based off of the demo linked above, I've gone into less detail about the process. Keep in mind that for more information you can look at https://github.com/intersystems-community/hackathon-kit/tree/main . 

## Demo

https://github.com/user-attachments/assets/7891c12c-da60-4a46-a774-fc95ad5720aa

## Usage 

1. Clone the repo
    git clone {repo name}

2. Install dependancies (ideally in a new python environment)

2. Download a community edition of iris using: 

    docker run --name IRIS -d --publish 1972:1972 --publish 52773:52773  -e IRISUSERNAME="SuperUser" -e IRISPASSWORD="SYS" -e IRISNAMESPACE="USER" containers.intersystems.com/intersystems/iris-community:latest

Note - you may need to enable service calling from within the management portal: 
    System Administration -> Security -> Services -> Go
    %Service_callin -> check box: Service Enabled

3. Download the dataset from https://www.kaggle.com/datasets/dylanjcastillo/7k-books-with-metadata and save it into the repo directory
    
4. Create the database. 

I recommend going through this step-by-step from the VectorSearchBookRecommender.ipynb, this way you can ensure it all works. You may need to change the credentials for iris login, or the books.csv location. If you are feeling brave though, you can try running it all from the python file: 

    python3 create_database.py

6. Start the application: 

    python3 app.py

7. Navigate to localhost:{Port} in a browser - the port number can be found within the terminal output. For me it defaults to 5010 (so localhost:5010).
