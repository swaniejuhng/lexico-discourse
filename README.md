# Lexico-Discourse model

This is the official repository for the ACL 2023 short paper [Discourse-Level Representations can Improve Prediction of Degree of Anxiety](empty). It contains manual to extracting embeddings required to predict the degree of anxiety as well as making predictions.

# Model / Representations request
You can request our models and/or representations here: https://docs.google.com/forms/d/e/1FAIpQLSc6kqSqJQvNODesSVX_NLNzGRyKfHnXuNmscb2O11N4dlGV2w/viewform?usp=sf_link


# Setup
## DLATK
We use DLATK to extract embeddings and run experiments -- you can install it here: https://dlatk.wwbp.org/install.html


## Python requirements
Clone this repository and enter the following command:
```
pip install -r HaRT/requirements.txt
```
# Data Format
You need two tables in mySQL: user table (contains information about users and their anxiety scores)

**1. user table**
Field       |            Type               | Key           |
----------- | ----------------------------- | ------------- |
user_id     | varchar(45)                   | PRI           |
anx_score   | double                        |               |
> Keep in mind that the anx_score is a rational number between 1 and 5, representing the Anxiety facet as a subscale of the Neuroticism factor from IPIP NEO-PI (Costa and McCrae, 1992).

**2. message table**
Field       |            Type               | Key           |
----------- | ----------------------------- | ------------- |
message_id  | int(11)                       | PRI           |
message     | text                          |               |
user_id     | varchar(45)                   |               |
time_updated| datetime                      |               |
autoinc_id  | int(11), auto increment       |               |

# Extract Embeddings

Our lexico-discourse model requires three embeddings from RoBERTa-large, DiscRE, and Sentence-BERT. Use the following instructions to derive representations to use in prediction.

## RoBERTa-L23
write something here
```
CUDA_VISIBLE_DEVICES=0 \ # if you have gpu's to use
python ~/dlatk/dlatkInterface.py \
-d (db_name) \
-t (msg_table_name) \
-c user_id \
--add_emb_feat --emb_model  roberta-large \
--word_aggregation mean \
--emb_layers 23
```
>**Output table:** (database_name).feat\$bert\_la_meL23con\$(msg_table_name)$user\_id

## DiscRE

(to be updated)

## Sentence-BERT

**1. Export messages only and save into .csv file**
```
mysqlToCSV.bash \
(db_name) \
"SELECT message FROM (msg_table_name)" \
> (your_path)/(msgs_csv_name).txt
```
>**Output file:** (your_path)/(msg_table_name).txt

**2. Split each message into sentences**
```
python split_sentence.py (your_path)/(msgs_csv_name).txt
```
>**Output file:** (your_path)/(msg_table_name).sentence_split.csv

**3. Get Sentence-BERT embeddings in DLATK format**
```
python sbert_extract.py (your_path)/(msg_table_name).sentence_split.csv
```
> **Output file:** (your_path)/(msg_table_name).sbert.csv

**5. Insert the embeddings into message-level feature table**
```
python csv2mySQL.py \
(your_path)/(msg_table_name).sbert.csv \
(db_name) \
"feat$sbert$(msg_table_name)$autoinc_id" \
"(id INT UNSINGED NOT NULL AUTO_INCREMENT PRIMARY KEY, group_id INT(11), feat VARCHAR(11), value INT(11), group_norm DOUBLE)"
```
>**Output table:** (database_name).feat\$sbert\$(msg\_table_name)\$autoinc_id

**6. Aggregate embeddings into user-level**
```
(in MYSQL)
-- change engine
ALTER TABLE feat$sbert$(msg_table_name)$autoinc_id
	ENGINE = MyISAM;

-- create indices on message-level feature table
CREATE INDEX fdex ON feat$sbert$(msg_table_name)$autoinc_id (feat);
CREATE INDEX gdex ON feat$sbert$(msg_table_name)$autoinc_id (group_id);

-- create user-level feature table
CREATE TABLE feat$sbert$(msg_table_name)$user_id
	LIKE feat$sbert$(msg_table_name)$autoinc_id;
ALTER TABLE feat$sbert$(msg_table_name)$user_id
	CHANGE COLUMN group_id group_id VARCHAR(45);
ALTER TABLE feat$sbert$(msg_table_name)$user_id
	ENGINE = MyISAM;

-- aggregate message-level embeddings into user-level
INSERT INTO feat$sbert$(msg_table_name)$user_id
	(group_id, feat, value, group_norm)
	SELECT user_id, feat, AVG(value), AVG(group_norm)
	FROM feat$sbert$(msg_table_name)$autoinc_id AS a,
	(msg_table_name) AS b
	WHERE a.group_id = b.autoinc_id
	GROUP BY user_id, feat;

-- create indices
CREATE INDEX fdex ON feat$sbert$(msg_table_name)$user_id (feat);
CREATE INDEX gdex ON feat$sbert$(msg_table_name)$user_id (group_id);
```
>**Output table:** (database_name).feat\$sbert\$(msg\_table_name)\$user_id

# Make prediction
Use the following command to see the result on metrics:
```
python ~/dlatk/dlatkInterface.py \
-d (db_name) \
-t (msg_table_name) \
-c user_id \
-f 'feat$roberta_la_meL23con$(msg_table_name)$user_id' \
'feat$sbert$(msg_table_name)$user_id' \
'feat$LDE_split$200$(msg_table_name)$user_id' \
--outcome_table (user_table_name) \
--outcomes anx_score \
--predict_regression --model mlp \
--load_model --picklefile (your_path)/lexico_discourse_model.pickle
```
This command lets you see the actual predicted output:
```
python3  ~/dlatk/dlatkInterface.py \
-d wwbp_dep_anx \
-t msgsEnUs_anxpred_train \
-c user_id \
-f 'feat$roberta_la_meL23con$(msg_table_name)$user_id' \
'feat$sbert$(msg_table_name)$user_id' \
'feat$LDE_split$200$(msg_table_name)$user_id' \
--outcome_table (user_table_name) \
--outcomes anx_score \
--predict_regression_to_outcome_table '(msg_table_name)$roberta_sbert_discre' --model mlp \
--load_model --picklefile (your_path)/lexico_discourse_model.pickle
```
