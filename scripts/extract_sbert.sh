./util/mysqlToCSV.bash \
{DB_NAME} \
"SELECT message FROM {MSG_TABLE_NAME}" \
> ./data/{MSG_TABLE_NAME}.csv

python3 ./util/message_only.py ./data/{MSG_TABLE_NAME}.csv

python3 ./util/split_sentence.py ./data/{MSG_TABLE_NAME}.txt

python3 ./util/sbert_extract.py ./data/{MSG_TABLE_NAME}.sentence_split.csv

python2 ./util/csv2mySQL.py \
./data/{MSG_TABLE_NAME}.sbert.csv \
{DB_NAME} \
'feat$sbert${MSG_TABLE_NAME}$autoinc_id' \
'(id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, group_id INT(11), feat VARCHAR(11), value INT(11), group_norm DOUBLE)'
