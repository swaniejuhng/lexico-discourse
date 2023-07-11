./dlatk/dlatkInterface.py \
-d wwbp_dep_anx \
-t {MSG_TABLE_NAME} \
-c user_id \
-f 'feat$roberta_la_meL23con${MSG_TABLE_NAME}$user_id' \
'feat$sbert${MSG_TABLE_NAME}$user_id' \
'feat$LDE_split$200${MSG_TABLE_NAME}$user_id' \
--outcome_table {USER_TABLE_NAME} \
--outcomes anx_score \
--group_freq_thresh 500 \
--predict_regression --model mlp \
--load_model --picklefile ./models/lexico_discourse.pickle

# if you want to see the predicted outcomes,
# replace "--predict_regression --model mlp" with the string below
# --predict_regression_to_outcome_table '{PREDICTED_OUTCOME_TABLE_NAME}' --model ridgehighcv
# => outcome table: p_mlp${PREDICTED_OUTCOME_TABLE_NAME} in the database