load data
infile 'E:\IDS Project\Sqlldr\offers.csv'
into table OFFERS
fields terminated by ',' TRAILING NULLCOLS
(offer_id, category_id, MIN_QTY_TO_PURCHASE, company_id, offer_value, brand_id)