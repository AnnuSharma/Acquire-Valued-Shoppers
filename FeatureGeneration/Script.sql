alter table TRAIN_HISTORY add repeat_customer number(1);

update TRAIN_HISTORY set repeat_customer = 1 where repeater = 't';
update TRAIN_HISTORY set repeat_customer = 0 where repeater = 'f' ;

ALTER TABLE TRAIN_HISTORY drop column repeater; 

DELETE FROM transactions
      WHERE    PURCHASE_AMT = 0
            OR PURCHASE_AMT IS NULL
            OR PURCHASE_QTY = 0
            OR PURCHASE_QTY IS NULL
            OR CATEGORY_ID IS NULL
            OR COMPANY_ID IS NULL
            OR BRAND_ID IS NULL;
---------------------------------------------------------------

ALTER TABLE TRAIN_HISTORY
  ADD PURCHASE_TIMES_COMPANY NUMBER(10) DEFAULT 0;

CREATE TABLE PURCHASE_TIMES_COMPANY
AS
     SELECT TH.TRAIN_HISTORY_ID CUSTOMER_ID,
            OFF.COMPANY_ID COMPANY_ID,
            COUNT (1) PURCHASE_TIMES
       FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
      WHERE     TH.TRAIN_HISTORY_ID = TR.TRANSACTION_ID
            AND TH.OFFER_ID = OFF.OFFER_ID
            AND OFF.COMPANY_ID = TR.COMPANY_ID
   GROUP BY TH.TRAIN_HISTORY_ID, OFF.COMPANY_ID;

MERGE INTO TRAIN_HISTORY TH
     USING (SELECT CUSTOMER_ID, COMPANY_ID, PURCHASE_TIMES
              FROM PURCHASE_TIMES_COMPANY) PTC
        ON (TH.TRAIN_HISTORY_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.PURCHASE_TIMES_COMPANY = PTC.PURCHASE_TIMES;

DROP TABLE PURCHASE_TIMES_COMPANY;

---------------------------------------------------------

ALTER TABLE TRAIN_HISTORY
   ADD PURCHASE_VALUE_COMPANY NUMBER (10) DEFAULT 0;

CREATE TABLE PURCHASE_VALUE_COMPANY
AS
     SELECT TH.TRAIN_HISTORY_ID CUSTOMER_ID,
            OFF.COMPANY_ID COMPANY_ID,
            SUM (PURCHASE_AMT) PURCHASE_AMT
       FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
      WHERE     TH.TRAIN_HISTORY_ID = TR.TRANSACTION_ID
            AND TH.OFFER_ID = OFF.OFFER_ID
            AND OFF.COMPANY_ID = TR.COMPANY_ID
   GROUP BY TH.TRAIN_HISTORY_ID, OFF.COMPANY_ID;

MERGE INTO TRAIN_HISTORY TH
     USING (SELECT CUSTOMER_ID, COMPANY_ID, PURCHASE_AMT
              FROM PURCHASE_VALUE_COMPANY) PTC
        ON (TH.TRAIN_HISTORY_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.PURCHASE_VALUE_COMPANY = PTC.PURCHASE_AMT;

DROP TABLE PURCHASE_VALUE_COMPANY;

---------------------------------------------------

ALTER TABLE TRAIN_HISTORY
   ADD PURCHASE_QUANTITY_COMPANY NUMBER (10) DEFAULT 0;
   
CREATE TABLE PURCHASE_QTY_COMPANY
AS
     SELECT TH.TRAIN_HISTORY_ID CUSTOMER_ID,
            OFF.COMPANY_ID COMPANY_ID,
            SUM (PURCHASE_QTY) PURCHASE_QTY
       FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
      WHERE     TH.TRAIN_HISTORY_ID = TR.TRANSACTION_ID
            AND TH.OFFER_ID = OFF.OFFER_ID
            AND OFF.COMPANY_ID = TR.COMPANY_ID
   GROUP BY TH.TRAIN_HISTORY_ID, OFF.COMPANY_ID;

MERGE INTO TRAIN_HISTORY TH
     USING (SELECT CUSTOMER_ID, COMPANY_ID, PURCHASE_QTY
              FROM PURCHASE_QTY_COMPANY) PTC
        ON (TH.TRAIN_HISTORY_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.PURCHASE_QUANTITY_COMPANY = PTC.PURCHASE_QTY;

DROP TABLE PURCHASE_QTY_COMPANY;

-------------------------------------------------------------

ALTER TABLE TRAIN_HISTORY
   ADD NEVER_BOUGHT_COMPANY NUMBER (1) DEFAULT 0;
   
CREATE TABLE NEVER_BOUGHT_COMPANY
AS
     SELECT TH.TRAIN_HISTORY_ID CUSTOMER_ID,
         OFF.COMPANY_ID COMPANY_ID,
         DECODE (COUNT (1), 0, 1, 0) NOT_PURCHASED_BEFORE
    FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE     TH.TRAIN_HISTORY_ID = TR.TRANSACTION_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.COMPANY_ID = TR.COMPANY_ID
GROUP BY TH.TRAIN_HISTORY_ID,
         OFF.COMPANY_ID;

MERGE INTO TRAIN_HISTORY TH
     USING (SELECT CUSTOMER_ID, COMPANY_ID, NOT_PURCHASED_BEFORE
              FROM NEVER_BOUGHT_COMPANY) PTC
        ON (TH.TRAIN_HISTORY_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.NEVER_BOUGHT_COMPANY = PTC.NOT_PURCHASED_BEFORE;
   
DROP TABLE NEVER_BOUGHT_COMPANY;