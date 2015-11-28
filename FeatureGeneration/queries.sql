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
-- let me know if it is taking more time in spark
SELECT CUSTOMER_ID,
         (CASE
             WHEN BOUGHT_COUNT > 0 THEN RETURN_COUNT / BOUGHT_COUNT
             ELSE 0
          END)
            RATIO
    FROM (  SELECT TR.CUSTOMER_ID CUSTOMER_ID,
                   COUNT (CASE WHEN TR.PURCHASE_AMT < 0 THEN 1 END) RETURN_COUNT,
                   COUNT (CASE WHEN TR.PURCHASE_AMT > 0 THEN 1 END) BOUGHT_COUNT
              FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
             WHERE TH.CUSTOMER_ID = TR.CUSTOMER_ID
                   AND TH.OFFER_ID = OFF.OFFER_ID
                   AND OFF.CATEGORY_ID = TR.CATEGORY_ID
                   AND OFF.COMPANY_ID = TR.COMPANY_ID
          --AND TR.CUSTOMER_ID = 217526800
          GROUP BY TR.CUSTOMER_ID --ORDER BY BOUGHT_COUNT DESC
         )
ORDER BY RATIO DESC;

—-ranking_market_and_chain_on_offer_for_category_company_brand

--Generated chainwise ranking for each market
-- if ranking is needed individually for market as well as chain remove the partition and generate rank
SELECT MARKET_ID,
       CHAIN_ID,
       MARKET_TXN_CNT,
       RANK () OVER (PARTITION BY MARKET_ID ORDER BY MARKET_TXN_CNT DESC) "RANK"
  FROM (  SELECT TH.MARKET_ID MARKET_ID,
                 TH.CHAIN_ID CHAIN_ID,
                 COUNT (1) MARKET_TXN_CNT
            FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
           WHERE TH.CUSTOMER_ID = TR.CUSTOMER_ID
                 AND TH.OFFER_ID = OFF.OFFER_ID
                 AND OFF.CATEGORY_ID = TR.CATEGORY_ID
                 AND OFF.COMPANY_ID = TR.COMPANY_ID
                 AND OFF.BRAND_ID = TR.BRAND_ID
        GROUP BY TH.MARKET_ID, TH.CHAIN_ID)
		
—-has_bought_ratio_offer_category_over_all_transactions

  SELECT CUSTOMER_ID,
         (CASE WHEN NO_OFFER_CNT > 0 THEN OFFER_CNT / NO_OFFER_CNT ELSE 0 END)
            RATIO
    FROM (SELECT CUSTOMER_ID2 CUSTOMER_ID,
                 NVL (CNT1, 0) OFFER_CNT,
                 NVL (CNT2, 0) NO_OFFER_CNT
            FROM ( (  SELECT TR.CUSTOMER_ID CUSTOMER_ID1, COUNT (1) CNT1
                        FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
                       WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
                             AND TH.OFFER_ID = OFF.OFFER_ID
                             AND OFF.CATEGORY_ID = TR.CATEGORY_ID
                    GROUP BY TR.CUSTOMER_ID) A
                  FULL OUTER JOIN
                  (  SELECT TR.CUSTOMER_ID CUSTOMER_ID2, COUNT (1) CNT2
                       FROM TRANSACTIONS TR
                   GROUP BY TR.CUSTOMER_ID) B
                     ON A.CUSTOMER_ID1 = B.CUSTOMER_ID2))
ORDER BY RATIO DESC

-—discount_on_the_original_price
   
   need to check this







