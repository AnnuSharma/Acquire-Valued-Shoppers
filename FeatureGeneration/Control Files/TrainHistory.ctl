load data
infile 'E:\IDS Project\Sqlldr\trainHistory.csv'
into table TRAIN_HISTORY
fields terminated by ',' TRAILING NULLCOLS
(TRAIN_HISTORY_ID, chain_id, offer_id, market_id, repeat_trips, repeater, offer_date DATE 'yyyy-mm-dd')