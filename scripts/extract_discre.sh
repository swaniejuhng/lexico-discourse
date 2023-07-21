wget https://nlp.stanford.edu/data/glove.twitter.27B.zip

unzip glove.twitter.27B.zip
rm glove.twitter.27B.50d.txt
rm glove.twitter.27B.100d.txt
rm glove.twitter.27B.200d.txt

python3 ./scripts/convert_glove.py

mv ./util/tokenize_and_tag_only_1.sh TweeboParser/
mv ./util/ConvertFromTaggingResToConll_1.py TweeboParser/scripts/

cd TweeboParser
./tokenize_and_tag_only_1.sh ../data/{MSG_TABLE_NAME}.txt
cd ..

python3 ./discre/discourseParsing/ArgumentExtractor.py \
./data/{MSG_TABLE_NAME}.txt_tagger.out \
n
# outputs:
# data/{MSG_TABLE_NAME}.txt_tagger.out_a_pos.tsv
# data/{MSG_TABLE_NAME}.txt_tagger.out_args.csv
# data/{MSG_TABLE_NAME}.txt_tagger.out_args_train_meta.csv
# data/{MSG_TABLE_NAME}.txt_tagger.out_dup_errors.txt
# data/{MSG_TABLE_NAME}.txt_tagger.out_t_pos.tsv

python3 ./discre/discourseParsing/utils/InputMaker.py \
./data/{MSG_TABLE_NAME}.txt_tagger.out_args.csv \
./data/{MSG_TABLE_NAME}.txt_tagger.out_args_train_meta.csv
# output: 
# data/{MSG_TABLE_NAME}.txt_tagger.out_args.dict

CUDA_VISIBLE_DEVICES=0 \
python ./discre/predict.py \
--test_file ./data/{MSG_TABLE_NAME}.txt_tagger.out_args.dict \
--split_one_arg \
--cuda \
--input_dim 200 \
--hidden_dim 200 \
--word_embedding_dict /data1/glove/glove_200.dict \
--attn_act ReLU \
--model models/DiscRE_200.ptstdict
# output:
# ./avgDump_SOA_DiscRE_200.ptstdict{MSG_TABLE_NAME}.txt_tagger.out_args.dict.dict

mv ./avgDump_SOA_DiscRE_200.ptstdict{MSG_TABLE_NAME}.txt_tagger.out_args.dict.dict data/

python3 ./util/avgToSparse.py \
./data/avgDump_SOA_DiscRE_200.ptstdict{MSG_TABLE_NAME}.txt_tagger.out_args.dict.dict
# output:
# data/avgDump_SOA_DiscRE_200.ptstdict{MSG_TABLE_NAME}.txt_tagger.out_args_sparse.csv_sparse.csv

python2 ./util/csv2mySQL.py \
./data/avgDump_SOA_DiscRE_200.ptstdict{MSG_TABLE_NAME}.txt_tagger.out_args_sparse.csv_sparse.csv \
{DB_NAME} \
'feat$discre${MSG_TABLE_NAME}$autoinc_id' \
'(id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, group_id INT(11), feat VARCHAR(11), value INT(11), group_norm DOUBLE)'