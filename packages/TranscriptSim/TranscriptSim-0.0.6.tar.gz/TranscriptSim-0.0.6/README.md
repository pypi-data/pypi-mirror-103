# TranscriptSim: Automated NLP Document Similarity 

## What is it?

TranscriptSim is an automated NLP technique that quantifies the similarity of treatment transcripts to the treatment protocol. In order to quantify these differences each document first needs to be converted into a numeric form. Each document is converted into a numeric vector where each space in the vector indicates a unique word and the number can indicate the number of times the word appears in the document or the word weight. Two documents are similar if they both contain the same words. Document similarity can be used to detect plagiarism, identify authors, and in this instance measure how well someone is following a script. Once a group of documents have been converted to numeric vectors there are multiple ways to calculate their similarity. The method used by TranscriptSim is cosine similarity. Cosine similarity is the cosine of the angle between two points in a multidimensional space. Where the number of dimensions is equivalent to the number of unique words. Points with smaller angles are more similar. Points with larger angles are more different.

## Installation and Demo
Run the following code from your command line:
```
pip install TranscriptSim
```
After installation, you can call the functions from this package by
```
import TranscriptSim.Class
```
Then, you should be able to call on any function inside this package: 
```
# NOT RUN
# TranscriptSim.Class.DocSim()
```
Below is a quick demo on how to build a `DocSim` class and use the function `normal_comparison()`: 
```
import TranscriptSim.Class
import pandas

d1 = """films adapted from comic books have had plenty of success , whether 
        they're about superheroes ( batman , superman , spawn ) , or geared 
        toward kids ( casper ) or the arthouse crowd ( ghost world ) , 
        but there's never really been a comic book like from hell before . """
d2 = """films adapted from comic books have had plenty of success , whether 
        they're about superheroes ( batman , superman , spawn )"""

# Set up a example data frame      
data = {'document_id': ['123.txt','456.txt'],
        'study_id': ['Behavioral Study', 'Behavioral Study 1'], 
        'skill_id': [1, 1], 
        'type_id': ['script', 'transcript'],
        'raw_text': [d1, d2]}
data = pandas.DataFrame(data = data)

# Create the DocSim class object
DocSim1 = TranscriptSim.Class.DocSim(data = data, 
				     skill = 'skill_id', 
				     study = 'study_id',
				     doc_type = 'type_id',
				     doc_id = 'document_id',
				     text = 'raw_text')

# Running the normal_comparison function
output = DocSim1.normal_comparison(method = 'cosine', 
				   remove_stopwords = False,
				   filler_words = [], 
				   stem = False, 
				   tfidf = False, 
				   tfidf_level = 'skill',
				   lsa = False, 
				   lsa_n_components = 5)

# Preview
output.head()

# Successful
print('Installation is successful!')
```


______

## Repo File Structure 

```
.
├── build                   # Files automatically generated while building the package. 
|   └── lib
│       └── TranscriptSim   
├── src                     # Source files 
|   └── TranscriptSim         # Main Location to store all .py files
├── test                    # Unit tests files
├── .gitignore              # GitHub Note on ignored files
├── pyproject.toml          # Minimal Configuration File
├── setup.cfg               # Package Set Up Information
├── LICENSE
└── README.md
```
______

## Class Structure

## Class: PreprocessCorpusText

### Methods

- `collect_directory()`
  - Extract each line of each file in a directory [source_dir] of text documents. 
  - Returns a single dataframe of labeled lines from documents.
- `explode_lines()`
  - Given a column named [col_name] containing line breaks, explode the dataset so that every single line is a separate row. 
  - Returns new instance of the class object
- `copy()`
  - Create a new instance of PreprocessCorpusText with the same data as this instance.
- `extr_col()`
  - Function for Pandas Apply vectorizing. 
  - Extract from src text [x] to add to a separate column, if any match of the given regex [pattern]. 
  - If [mult]=True then extract multiple regex pattern group matches.
- `add_col_from_extract()`
  - Return the original given dataframe [df1] with a new column [newcolname] created from matches returned from the given regex pattern [regex] applied to a src column [colfrom]. 
  - If [mult]=True, returns list of all matches, not just first.
  - If from_prev_row, returns [regex] match from previous instead of current row.
  - Returns new instance of the class object.
- `add_column()`
  - Add a new column to the dataset, named [colname], and the values should be [contents].
  - If [contents] is a string and the name of an existing column, copy existing column [contents] to the new column. 
- `new_text_column()`
  - Create a new column of text to process named [new_text_col_name].
  - Automatically updates internal text col tracking.
  - Returns new instance of the class object.
- `join_dataset()`
  - Join current dataset with new dataset [newdf], assuming inner join.
  - Join on the column named [join_on_col] which must exist in both datasets.
  - For the benefit of the object, set column named [assign_text_col] as text analysis target.
  - Returns new instance of the class object.
- `colon_delim_timestamp_to_second()`
  - Apply vectorizer function, accepts raw text like timestamp.
  - Returns number of hours, minutes, and seconds converted to a single numeric seconds value.
- `regex_replace_from_dict()`
  - Accepts dictionary where each key is a regex group to find and each value is what should replace the found group.
  - Returns new instance of the class object

### Attribute

1. `data_Source`: PreprocessCorpusText accepts as its primary input either a directory of txt files, or an existing Pandas dataframe of documents
2. `text_col`: The column name which contains document texts which may be compared for similarity. This could be any name, not restricted. 
2. `df`: PreprocessCorpusText at its core is just a Pandas dataframe which is being carefully manipulated. 
  - all other techniques are working to clean the text of this dataframe either in place or by removing characters and appending them in a new column. 
  - this df will reliably contain the following columns:
 	* data_sources: see #1 above
	* doc_id: a unique identifier of each document described by a row of the dataframe
	* rawtext: the original unchanged version of text_col
	* collected: datetime that each document record in the dataframe was added to this object

## Class: DocSim

### Initialization

- `DocSim()`: Declare class object
  - `data`: a Pandas data frame. For example, 

    |File_Name|Doc_Type|Study|Skill|Raw_Text|
    |-|-|-|-|-|
    |Classroom_Management_Model_Script_1.txt|script|-|1|This is what script 2 says|
    |52-2C.txt|transcript|Behavior Study 1|1|This is what script 1 states|
  - `doc_id`: column name of the ID of each document
    - In the example table above, `doc_id = 'File_Name'`
  - `study`: column name of the study ID of each document
    - In the example table above, `study = 'Study'`
  - `skill`: column name of the skill ID of each document
    - In the example table above, `skill = 'Skill'`
  - `doc_type`: column name of the document type for each document
    - In the example table above, `doc_type = 'Doc_Type'`
    - **Please note that only “transcript” and "script" are acceptable entries for this column.**
  - `text`: column name of the raw text for each document
    - In the example table above, `text = 'Raw_Text'`

### Methods

  - `preprocessing()`: NLP preprocessing step for stopwords, stemming, tf-idf, and LSA
    - Expected Input:
      - `self`: it will take `self.data` as the input.
      - `remove_stopwords`: True or False
      - `filler_words`: List of additional words that should be removed from transcripts and scripts. 
      - `stem`: True or False, whether to enable stemming
      - `lemm`: True or False, whether to enable lemmantizing. Note: You can only use either `stem` or `lemm`, not both at the same time.
      - `tfidf`: True of False, whether to use TF-IDF on transcripts
      - `tfidf_level`: 'full', 'skill', 'study' or 'document'. Define the level of hierarchy to apply TF-IDF
      - `lsa`: True or False, whether to enable Latent Semantic Analysis
      - `lsa_n_components`: integer, the number of LSA topics to include
      - `ngram`: integer, the number of N-Gram to use.

    - Expected Output: `clean_vectroized_text` column is appended to the Pandas Data Frame which contains the cleaned and vectorized documents. For example,
    
      |File_Name|Doc_Type|Study|Skill|Raw_Text|clean_vectroized_text|
      |-|-|-|-|-|-|
      |Classroom_Management_Model_Script_1.txt|script|-|1|This is what script 2 says|[1, 1, 1, 1, 1, 1, 0, 0]|
      |52-2C.txt|transcript|Behavior Study 1|1|This is what script 1 states|[1, 1, 1, 1, 0, 0, 1, 1]|
  
  - `get_preprocessed_text()`: 
    - Expected Input: `self`
    - Expected Output: A list of the cleaned and vectorized numbers. For example, 
    
    ```
    [[1, 1, 1, 1, 1, 1, 0, 0], 
     [1, 1, 1, 1, 0, 0, 1, 1]]
    ```
  
  - `get_feature_names()`: 
    - Expected Input: `self`
    - Expected Output: A list of the cleaned and vectorized words. For example, 
    
    ```
    [['This', 'is', 'what', 'script', '2', 'says'], 
     ['This', 'is', 'what', 'script', '1', 'states']]
    ```
  
  - `get_skill()`: 
    - Expected Input: `self`
    - Expected Output: A list of *unique* skills within the data. For example, 
    
    ```
    ['1', '2', '3']
    ```
  
  - `get_doc_type()`: 
    - Expected Input: `self`
    - Expected Output: A list of *unique* document type within the data. For example, 
    
    ```
    ['transcript', 'script']
    ```
  
  - `get_study()`: 
    - Expected Input: 
      - `self`
      - `skill_id`, a list of skills to extract study IDs. For example, `skill_id = ['1', '2']`.
    - Expected Output: A list of *unique* study IDs within certain skills. For example, 
    
    ```
    ['Behavior Study 1', 'Behavior Study 2']
    ```
  
  - `check_preprocessing_input()`: Check if the inputs for `preprocessing()` meet the requirements
    - Expected Input: all inputs for `preprocessing()`. 
    - Expected Output: None

  - `create_sparse_matrix()`: create a sparse matrix of the vectorized column
    - Expected Input: 
      - `data`: the data frame contains the vectorized column
      - `col`: column name of the vectorized column 
    - Expected Output: A sparse matrix
  
  - `normal_comparison()`: **Calculate the similarity score between scripts and transcripts by skill**
    - Expected Input: 
      - `method`: 'cosine'. Currently, we only support calculating cosine similarity scores 
      - all `preprocessing()` inputs

    - Expected Output: A Pandas Data Frame with only *transcripts* will be created along with an additional column called `similarity_score`. 

    |File_Name|Doc_Type|Study|Skill|Raw_Text|clean_vectroized_text|similarity_score|
    |-|-|-|-|-|-|-|
    |52-2C.txt|transcript|Behavior Study 1|1|This is what script 1 states|[1, 1, 1, 1, 0, 0, 1, 1]|0.6667|
	
  - `pairwise_comparison()`: **Calculate the similarity score among transcripts within the same skill**
    - Expected Input:
      - `method`: 'cosine'. Currently, we only support calculating cosine similarity scores 
      - all `preprocessing()` inputs

    - Expected Output: A Pandas Data Frame with only *transcripts* will be created along with an additional column called `similarity_score`. 

    |File_Name|Doc_Type|Study|Skill|Raw_Text|clean_vectroized_text|similarity_score|
    |-|-|-|-|-|-|-|
    |52-2C.txt|transcript|Behavior Study 1|1|This is what script 1 states|[1, 1, 1, 1, 0, 0, 1, 1]|0.6667|

  - `within_study_normal_average()`: **Calculate the average similarity score for all transcripts compared with script within the same study**
    - Expected Input:
      - `method`: 'cosine'. Currently, we only support calculating cosine similarity scores 
      - all `preprocessing()` inputs
    - Expected Output: A Pandas Data Frame of two columns will be generated. 
	
    |Study|similarity_score|
    |-|-|
    |Behavior Study 1|0.1234|
    |Behavior Study 2|0.5678|
  
  - `across_study_normal_average()`: **Calculate the average similarity score for each transcript compared with all transcripts in other studies**
    - Given this function is relatively complex, here is the process breakdown
      - Check Preprocessing Inputs 
      - Perform NLP Preprocessing
      - Loop through each skill
      - Loop through each study within the same skill
	- Identify the transcripts in the current study 
	- Identify the transcripts in the rest of studies
	- **Calculate the cosine similarity for each transcrtips in the current study against the transcripts in the rest of the studies**
    - Expected Input:
      - `method`: 'cosine'. Currently, we only support calculating cosine similarity scores 
      - all `preprocessing()` inputs
    - Expected Output: A Pandas Data Frame with only *transcripts* will be created along with an additional column called `similarity_score`. 

### Attribute

1. `data`: a Pandas data frame
2. `doc_id`: column name of the ID of each document
3. `skill`: column name of the skill ID of each document
4. `study`: column name of the study ID of each document
5. `doc_type`: column name of the document type for each document
6. `text`: Column name of the raw text within the Document Matrix
7. `vectorized_documents`: List of weights for each factor
8. `tfidf_factors`: List of tokenized words from TF-IDF 
9. `lsa_factors`: List of tokenized words from LSA
10. `document_matrix`: Expected output of `preprocessing()`

______

## Author:
- Ashley Scurlock
- Kip McCharen
- Latifa Hasan
- Congxin (David) Xu

## Acknowledgement
Thank you to our sponsors Kylie Anglin, Vivian Wong, and Todd Hall, as well as our advisor Brian Wright!
