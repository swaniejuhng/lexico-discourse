CUDA_VISIBLE_DEVICES=0 \
python3 ./dlatk/dlatkInterface.py \
-d {DB_NAME} \
-t {MSG_TABLE_NAME} \
-c user_id \
--add_emb_feat --emb_model roberta-large \
--word_aggregation mean \
--emb_layers 23