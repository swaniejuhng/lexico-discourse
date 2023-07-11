
# Lexico-Discourse model

This is the official repository for the ACL 2023 short paper [Discourse-Level Representations can Improve Prediction of Degree of Anxiety](empty). It contains manual to extracting embeddings required to predict the degree of anxiety as well as making predictions.

# Model / Representations request
You can make a request for our models and/or representations here: https://docs.google.com/forms/d/e/1FAIpQLSc6kqSqJQvNODesSVX_NLNzGRyKfHnXuNmscb2O11N4dlGV2w/viewform?usp=sf_link


# Setup
**0.  Conda environment**
Clone this repository and run the following commands:
```
conda create --name lexdisc --file requirements.txt
conda activate lexdisc
```

**1. Create a directory (and do everything here)**
```
mkdir lexico-discourse
cd lexico-discourse
```

**2. Install TweeboParser** (https://github.com/ikekonglp/TweeboParser)
```
git clone https://github.com/ikekonglp/TweeboParser.git
cd TweeboParser
python setup.py install
cd ..
```

**3. Install DLATK** (https://github.com/dlatk/dlatk)
```
git clone https://github.com/dlatk/dlatk.git
cd dlatk
python setup.py install
cd ..
```

**4. Replace strings**
Replace "{DB_NAME}", "{MSG_TABLE_NAME}", "{USER_TABLE_NAME}" within files in the **scripts** directory with their actual names.
```
find . -type f -exec sed -i 's/{DB_NAME}/actual_db_name/g' {} +
find . -type f -exec sed -i 's/{MSG_TABLE_NAME}/actual_msg_table_name/g' {} +
find . -type f -exec sed -i 's/{USER_TABLE_NAME}/actual_user_table_name/g' {} +
```

**5. (Optional) If GPUs are not set up**
If you do not have GPUs set up, remove the string "CUDA_VISIBLE_DEVICES=0" from **scripts/extract_roberta.sh** file and run the command (doing so will extract RoBERTa embeddings using CPU and thus be slower).

# Data Format
You need two tables in mySQL: user table (contains information about users and their anxiety scores) and message table (contains messages as well as meta data)

**1. user table**
Field       |            Type               | Key           |
----------- | ----------------------------- | ------------- |
user_id     | varchar(45)                   | PRI           |
anx_score   | double                        |               |

Create index on **user_id.**
> Keep in mind that the anx_score is a rational number between 1 and 5, representing the Anxiety facet as a subscale of the Neuroticism factor from IPIP NEO-PI (Costa and McCrae, 1992).

**2. message table**
Field       |            Type               | Key           |
----------- | ----------------------------- | ------------- |
message_id  | int(11)                       | PRI           |
message     | text                          |               |
user_id     | varchar(45)                   |               |
time_updated| datetime                      |               |
autoinc_id  | int(11), auto increment       |               |

Create index on **user_id, message_id, autoinc_id.**

# Experiment!

You can run the experiment by entering the following command:
```
./run.sh
```

# Contact
If you have any questions, feel free to contact me via email **(sjuhng {at} cs.stonybrook {at} edu)**