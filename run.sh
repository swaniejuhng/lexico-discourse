./scripts/extract_roberta.sh
./scripts/extract_sbert.sh
./scripts/extract_discre.sh
mysql < ./scripts/db.sql
./scripts/predict.sh