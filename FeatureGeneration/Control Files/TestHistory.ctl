load data
infile 'E:\IDS Project\Sqlldr\testHistory.csv'
into table TEST_HISTORY
fields terminated by ',' TRAILING NULLCOLS
(CUSTOMER_ID, chain_id, offer_id, market_id, offer_date DATE 'yyyy-mm-dd')