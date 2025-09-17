import pandas as pd # Data handling
from sentence_transformers import SentenceTransformer ## vector generation
import irisnative # connection to iris


# Load the csv file - file can be downloaded from kaggle : https://www.kaggle.com/datasets/dylanjcastillo/7k-books-with-metadata
df = pd.read_csv('books.csv')

# View the data
print(df.head)
print(f"The dataset has {len(df)} entries.")

### remove entries with no description
df = df.fillna("")
df = df[df["description"]!=""& (df['description'] != None) ]
df = df[(df['average_rating'] != '') & (df['num_pages'] != '')]

df.drop(columns=["ratings_count"], inplace=True)

print(f"After removing entries with no description, there are now {len(df)} entries")


# Load a pre-trained sentence transformer model. This model's output vectors are of size 384

model = SentenceTransformer('all-MiniLM-L6-v2') 

# Generate embeddings for all descriptions at once. Batch processing makes it faster
embeddings = model.encode(df['description'].tolist(), normalize_embeddings=True)

# Add the embeddings to the DataFrame
df['description_vector'] = embeddings.tolist()


# Name the SQL table
table_name = "BookRecommender.Books"

# Make the table creation query. The schema of the table is given within this query. 
table_schema = '''(
  isbn13     VARCHAR(32),
  isbn10        VARCHAR(32),
  title          VARCHAR(1024) NOT NULL,
  subtitle            VARCHAR(1024),
  authors    VARCHAR(255),
  categories     VARCHAR(1024),
  thumbnail        VARCHAR(1024),
  description       LONGVARCHAR,
  published_year    INTEGER,
  average_rating    DOUBLE,
  num_pages     INTEGER ,
  description_vector   VECTOR(DOUBLE, 384)
)'''
create_table_query = 'CREATE TABLE {table_name} {table_schema}'


# Create connection to database 
conn = irisnative.createConnection("localhost", 1972, "USER", "SuperUser", "SYS")
cursor = conn.cursor()

##Call the create-table query
cursor.execute(create_table_query)

## Create function for adding rows to table
def add_row(row):
    ##sql query
    sql = f'Insert into {table_name} (isbn13, isbn10, title, subtitle, authors, categories, thumbnail, description, published_year, average_rating, num_pages, description_vector) values (?,?,?,?,?,?,?,?,?,?,?,TO_VECTOR(?))'
    ##values
    values = [row['isbn13'], row['isbn10'], row['title'], row['subtitle'], row['authors'], row['categories'], row['thumbnail'], row['description'], row['published_year'], row['average_rating'], row['num_pages'], str(row['description_vector'])]
    
    try:
        cursor.execute(sql, values)
    except:
        pass

#call the function
df.apply(add_row, axis=1)