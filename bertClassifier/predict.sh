#!/usr/bin/env bash
python run_classifier.py \
  --task_name=my \
  --do_predict=true \
  --data_dir=data \
  --vocab_file=chinese_L-12_H-768_A-12/vocab.txt \
  --bert_config_file=chinese_L-12_H-768_A-12/bert_config.json \
  --init_checkpoint=my_model \
  --max_seq_length=70 \
  --output_dir=output

