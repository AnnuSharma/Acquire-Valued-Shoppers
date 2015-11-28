/* Formatted on 24/11/2015 19:32:08 (QP5 v5.287) */
--has_bought_times_by_customer_from_the_offer_company

  SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.COMPANY_ID COMPANY_ID,
         COUNT (1) PURCHASE_TIMES
    FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.COMPANY_ID = TR.COMPANY_ID
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID;

--has_bought_amount_by_customer_from_the_offer_company

  SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.COMPANY_ID COMPANY_ID,
         SUM (PURCHASE_AMT) PURCHASE_AMT
    FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.COMPANY_ID = TR.COMPANY_ID
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID;

--has_bought_quantity_by_customer_from_the_offer_company

  SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.COMPANY_ID COMPANY_ID,
         SUM (PURCHASE_QTY) PURCHASE_QTY
    FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.COMPANY_ID = TR.COMPANY_ID
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID;

--has_bought_times_by_customer_from_the_offer_company_in_last_180_days

  SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.COMPANY_ID COMPANY_ID,
         COUNT (1) PURCHASE_TIMES
    FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.COMPANY_ID = TR.COMPANY_ID
         AND TO_DATE (TR.PURCHASE_DATE, 'dd/mm/yyyy') BETWEEN   TO_DATE (
                                                                   TH.OFFER_DATE,
                                                                   'dd/mm/yyyy')
                                                              - 180
                                                          AND TO_DATE (
                                                                 TH.OFFER_DATE,
                                                                 'dd/mm/yyyy')
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID;

--has_never_bought_by_customer_from_the_offer_company

  SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.COMPANY_ID COMPANY_ID,
         DECODE (COUNT (1), 0, 'T', 'F') NOT_PURCHASED_BEFORE
    FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
	 AND OFF.COMPANY_ID = TR.COMPANY_ID
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID;

--has_bought_times_by_customer_from_the_offer_category_company_brand

  SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.CATEGORY_ID CATEGORY_IDANY_ID,
         OFF.COMPANY_ID COMPANY_ID,
         OFF.BRAND_ID BRAND_ID,
         COUNT (1) PURCHASE_TIMES
    FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.CATEGORY_ID = TR.CATEGORY_ID
         AND OFF.COMPANY_ID = TR.COMPANY_ID
         AND OFF.BRAND_ID = TR.BRAND_ID
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID,
         OFF.CATEGORY_ID,
         OFF.COMPANY_ID,
         OFF.BRAND_ID;

--has_never_bought_by_customer_from_the_offer_category_company_brand

  SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.CATEGORY_ID CATEGORY_IDANY_ID,
         OFF.COMPANY_ID COMPANY_ID,
         OFF.BRAND_ID BRAND_ID,
         DECODE (COUNT (1), 0, 'T', 'F') NOT_PURCHASED_BEFORE
    FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.CATEGORY_ID = TR.CATEGORY_ID
         AND OFF.COMPANY_ID = TR.COMPANY_ID
         AND OFF.BRAND_ID = TR.BRAND_ID
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID,
         OFF.CATEGORY_ID,
         OFF.COMPANY_ID,
         OFF.BRAND_ID;

--total_amount_spent_by_customer

  SELECT TH.CUSTOMER_ID CUSTOMER_ID, SUM (PURCHASE_AMT) TOTAL_AMT_SPENT
    FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID;

—-has_bought_times_by_customer_offer_category

SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.CATEGORY_ID CATEGORY_ID,
         COUNT (*) PURCHASE_TIMES
FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.CATEGORY_ID = TR.CATEGORY_ID
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID, OFF.CATEGORY_ID;

—-has_never_bought_category

SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.CATEGORY_ID CATEGORY_ID,
         DECODE (COUNT (1), 0, 'T', 'F') NOT_PURCHASED_BEFORE
   FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID, OFF.CATEGORY_ID;

—-total_amount_spent_on category

SELECT TH.CUSTOMER_ID CUSTOMER_ID, OFF.CATEGORY_ID CATEGORY_ID,
	SUM (PURCHASE_AMT) TOTAL_AMT_SPENT
   FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
	 AND OFF.CATEGORY_ID = TR.CATEGORY_ID
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID, OFF.CATEGORY_ID;


-—has_never_bought_company_and_brand

SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.COMPANY_ID COMPANY_ID,
         OFF.BRAND_ID BRAND_ID
         DECODE (COUNT (1), 0, 'T', 'F') NOT_PURCHASED_BEFORE
   FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.COMPANY_ID = TR.COMPANY_ID
         AND OFF.BRAND_ID = TR.BRAND_ID
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID;

—-has_bought_times_company_and_brand

SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.COMPANY_ID COMPANY_ID,
	 OFF.BRAND_ID BRAND_ID,
         COUNT (*) PURCHASE_TIMES
FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.COMPANY_ID = TR.COMPANY_ID
	 AND OFF.BRAND_ID = TR.BRAND_ID
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID, OFF.CATEGORY_ID;

--has_bought_times_by_customer_from_the_offer_company_in_last_60_days

  SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.COMPANY_ID COMPANY_ID,
         COUNT (1) PURCHASE_TIMES
    FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
    WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.COMPANY_ID = TR.COMPANY_ID
         AND TO_DATE (TR.PURCHASE_DATE, 'dd/mm/yyyy') BETWEEN   TO_DATE (
                                                                   TH.OFFER_DATE,
                                                                   'dd/mm/yyyy')
                                                              - 60
                                                          AND TO_DATE (
                                                                 TH.OFFER_DATE,
                                                                 'dd/mm/yyyy')
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID;

--has_bought_times_by_customer_from_the_offer_company_in_last_30_days

  SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.COMPANY_ID COMPANY_ID,
         COUNT (1) PURCHASE_TIMES
    FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
    WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.COMPANY_ID = TR.COMPANY_ID
         AND TO_DATE (TR.PURCHASE_DATE, 'dd/mm/yyyy') BETWEEN   TO_DATE (
                                                                   TH.OFFER_DATE,
                                                                   'dd/mm/yyyy')
                                                              - 30
                                                          AND TO_DATE (
                                                                 TH.OFFER_DATE,
                                                                 'dd/mm/yyyy')
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID;


--has_bought_times_by_customer_from_the_offer_category_in_last_180_days

  SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.CATEGORY_ID CATEGORY_ID,
         COUNT (1) PURCHASE_TIMES
    FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
    WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.CATEGORY_ID = TR.CATEGORY_ID
         AND TO_DATE (TR.PURCHASE_DATE, 'dd/mm/yyyy') BETWEEN   TO_DATE (
                                                                   TH.OFFER_DATE,
                                                                   'dd/mm/yyyy')
                                                              - 60
                                                          AND TO_DATE (
                                                                 TH.OFFER_DATE,
                                                                 'dd/mm/yyyy')
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID, OFF.CATEGORY_ID;

--has_bought_times_by_customer_from_the_offer_category_in_last_60_days

  SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.CATEGORY_ID CATEGORY_ID,
         COUNT (1) PURCHASE_TIMES
    FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
    WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.CATEGORY_ID = TR.CATEGORY_ID
         AND TO_DATE (TR.PURCHASE_DATE, 'dd/mm/yyyy') BETWEEN   TO_DATE (
                                                                   TH.OFFER_DATE,
                                                                   'dd/mm/yyyy')
                                                              - 60
                                                          AND TO_DATE (
                                                                 TH.OFFER_DATE,
                                                                 'dd/mm/yyyy')
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID, OFF.CATEGORY_ID;

--has_bought_times_by_customer_from_the_offer_category_in_last_30_days

  SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.CATEGORY_ID CATEGORY_ID,
         COUNT (1) PURCHASE_TIMES
    FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
    WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.CATEGORY_ID = TR.CATEGORY_ID
         AND TO_DATE (TR.PURCHASE_DATE, 'dd/mm/yyyy') BETWEEN   TO_DATE (
                                                                   TH.OFFER_DATE,
                                                                   'dd/mm/yyyy')
                                                              - 60
                                                          AND TO_DATE (
                                                                 TH.OFFER_DATE,
                                                                 'dd/mm/yyyy')
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID, OFF.CATEGORY_ID;

—-has_bought_times_offer_brand

SELECT TH.CUSTOMER_ID CUSTOMER_ID,
	 OFF.BRAND_ID BRAND_ID,
         COUNT (*) PURCHASE_TIMES
FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
WHERE    TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
	 AND OFF.BRAND_ID = TR.BRAND_ID
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID, OFF.BRAND_ID;


-—has_never_bought_brand

SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.BRAND_ID BRAND_ID
         DECODE (COUNT (1), 0, 'T', 'F') NOT_PURCHASED_BEFORE
   FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.BRAND_ID = TR.BRAND_ID
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID;

—-given_offer_value

SELECT TH.CUSTOMER_ID CUSTOMER_ID,
       OFF.OFFER_VALUE OFFER_VALUE,
   FROM TRAIN_HISTORY TH, OFFERS OFF
   WHERE  TR.CUSTOMER_ID = 101623425;

—-min_quantity_to_avail_offer_value

SELECT TH.CUSTOMER_ID CUSTOMER_ID,
       OFF.MIN_QTY_TO_PURCHASE MIN_QTY,
   FROM TRAIN_HISTORY TH, OFFERS OFF
   WHERE  TR.CUSTOMER_ID = 101623425;


—- freqency_visits_to_market_and_chain_on_offer

SELECT TH.CUSTOMER_ID CUSTOMER_ID,
	 TH.MARKET_ID = TR.MARKET_ID,
         TH.CHAIN_ID = TR.CHAIN_ID,
         COUNT (*) PURCHASE_TIMES
FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
WHERE    TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
	 AND TH.MARKET_ID = TR.MARKET_ID
	 AND TH.CHAIN_ID = TR.CHAIN_ID 
         AND TR.CUSTOMER_ID = 101623425
GROUP BY TH.CUSTOMER_ID;

-—has_previously_returned_category_and_company_on_offer

SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.CATEGORY_ID CATEGORY_ID,
	 OFF.COMPANY_ID COMPANY_ID,
         DECODE (COUNT (1), 0, 'T', 'F') RETURNED_CATEGORY_BEFORE
   FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.CATEGORY_ID = OFF.CATEGORY_ID
         AND OFF.COMPANY_ID = TR.COMPANY_ID
         AND TR.CUSTOMER_ID = 101623425
	 AND TR.PURCHASE_AMT < 0;
GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID, OFF.CATEGORY_ID;



—-ratio_of_returned_category_company_over_bought_category_company
—-ranking_market_and_chain_on_offer_for_category_company_brand
—-has_bought_ratio_offer_category_over_all_transactions
-—discount_on_the_original_price







