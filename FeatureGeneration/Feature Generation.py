from dateutil.parser import parse
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql import Row
import os

path = os.getcwd()
transactionFile = sc.textFile(path+"/reducedFile.csv")
sqlContext = SQLContext(sc)
schemaString = "CUSTOMER_ID CHAIN_ID DEPARTMENT_ID CATEGORY_ID COMPANY_ID BRAND_ID PURCHASE_DATE PRODUCT_SIZE PRODUCT_MEASURE PURCHASE_QTY PURCHASE_AMT"
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
fields[6].dataType = TimestampType()
fields[7].dataType = FloatType()
fields[9].dataType = FloatType()
fields[10].dataType = FloatType()
schema = StructType(fields)
transactions = transactionFile.map(lambda l: l.split(",")).map(lambda p: (p[0],p[1],p[2],p[3],p[4],p[5],parse(p[6]),float(p[7]),p[8],float(p[9]),float(p[10])))
transactions_df = sqlContext.createDataFrame(transactions, schema) 
transactions_df.registerTempTable("transactions")

#Cleaning the values in transactionsDF
transactions_df = sqlContext.sql("select * from transactions where PURCHASE_AMT != 0 or PURCHASE_AMT !=null or PURCHASE_QTY != 0 or PURCHASE_QTY != null or CATEGORY_ID != null or COMPANY_ID != null or BRAND_ID != null")
transactions_df.registerTempTable("transactions")


offerFile = sc.textFile(path+"/offers.csv")
schemaString = "OFFER_ID CATEGORY_ID MIN_QTY_TO_PURCHASE COMPANY_ID OFFER_VALUE BRAND_ID"
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
fields[2].dataType = FloatType()
fields[4].dataType = FloatType()
schema = StructType(fields)
header = offerFile.filter(lambda line: "offer" in line)
offerFile = offerFile.subtract(header)
offers = offerFile.map(lambda l: l.split(",")).map(lambda p: (p[0],p[1],float(p[2]),p[3],float(p[4]),p[5]))
offers_df = sqlContext.createDataFrame(offers, schema) 
offers_df.registerTempTable("offers")

trainFile = sc.textFile(path+"/trainHistory.csv")
schemaString = "CUSTOMER_ID CHAIN_ID OFFER_ID MARKET_ID REPEAT_TRIPS REPEATER OFFER_DATE"
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
fields[4].dataType = FloatType()
fields[6].dataType = TimestampType()
schema = StructType(fields)
header = trainFile.filter(lambda line: "id" in line)
trainFile = trainFile.subtract(header)
train = trainFile.map(lambda l: l.split(",")).map(lambda p: (p[0],p[1],p[2],p[3],float(p[4]),p[5],parse(p[6])))
train_df = sqlContext.createDataFrame(train, schema) 
train_df.registerTempTable("train")

CREATE TABLE OFFERS
(
   OFFER_ID              NUMBER (10) NOT NULL,
   CATEGORY_ID           NUMBER (10) NOT NULL,
   MIN_QTY_TO_PURCHASE   NUMBER (5),
   COMPANY_ID            NUMBER (20) NOT NULL,
   OFFER_VALUE           NUMBER (10, 4),
   BRAND_ID              NUMBER (10) NOT NULL,
   CONSTRAINT OFFERS_PK PRIMARY KEY (OFFER_ID)
) TABLESPACE USERS ;

CREATE TABLE TRAIN_HISTORY
(
   TRAIN_HISTORY_ID   NUMBER (10) NOT NULL,
   CHAIN_ID           NUMBER (10) NOT NULL,
   OFFER_ID           NUMBER (10) NOT NULL,
   MARKET_ID          NUMBER (10),
   REPEAT_TRIPS       NUMBER (10),
   REPEATER           VARCHAR2 (1),
   OFFER_DATE         DATE
) TABLESPACE USERS ;

CREATE TABLE TRANSACTIONS 
(
   TRANSACTION_ID   NUMBER (10) NOT NULL,
   CHAIN_ID         NUMBER (10) NOT NULL,
   DEPARTMENT_ID    NUMBER (10) NOT NULL,
   CATEGORY_ID      NUMBER (10) NOT NULL,
   COMPANY_ID       NUMBER (20) NOT NULL,
   BRAND_ID         NUMBER (10) NOT NULL,
   PURCHASE_DATE    DATE,
   PROD_SIZE        NUMBER (10, 4),
   PROD_MEASURE     VARCHAR2 (20),
   PURCHASE_QTY     NUMBER (10),
   PURCHASE_AMT     NUMBER (10, 4)
)  TABLESPACE USERS ;

CREATE TABLE TEST_HISTORY
(
   CUSTOMER_ID        NUMBER (10) NOT NULL,
   CHAIN_ID           NUMBER (10) NOT NULL,
   OFFER_ID           NUMBER (10) NOT NULL,
   MARKET_ID          NUMBER (10),
   OFFER_DATE         DATE
) TABLESPACE USERS ;

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
			
CREATE TABLE TRAIN_HIST
AS
   SELECT TRAIN_HISTORY_ID,
          TH.OFFER_ID,
          TH.CHAIN_ID,
          TH.MARKET_ID,
          TH.REPEAT_TRIPS,
          TH.REPEATER,
          TH.OFFER_DATE,
          OFF.CATEGORY_ID,
          OFF.MIN_QTY_TO_PURCHASE,
          OFF.COMPANY_ID,
          OFF.OFFER_VALUE,
          OFF.BRAND_ID
     FROM TRAIN_HISTORY TH, OFFERS OFF
    WHERE TH.OFFER_ID = OFF.OFFER_ID;
	
DROP TABLE TRAIN_HISTORY;

ALTER TABLE TRAIN_HIST
   RENAME TO
   TRAIN_HISTORY;
   
CREATE TABLE TEST_HIST
AS
   SELECT CUSTOMER_ID,
          TH.OFFER_ID,
          TH.CHAIN_ID,
          TH.MARKET_ID,
          TH.OFFER_DATE,
          OFF.CATEGORY_ID,
          OFF.MIN_QTY_TO_PURCHASE,
          OFF.COMPANY_ID,
          OFF.OFFER_VALUE,
          OFF.BRAND_ID
     FROM TEST_HISTORY TH, OFFERS OFF
    WHERE TH.OFFER_ID = OFF.OFFER_ID;

DROP TABLE TEST_HISTORY;
	
ALTER TABLE TEST_HIST
   RENAME TO
   TEST_HISTORY;
      
---------------------------------------------------------------

ALTER TABLE TRAIN_HISTORY
  ADD PURCHASE_TIMES_COMPANY NUMBER(10) DEFAULT 0;

CREATE TABLE TR_PURCHASE_TIMES_COMPANY
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
              FROM TR_PURCHASE_TIMES_COMPANY) PTC
        ON (TH.TRAIN_HISTORY_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.PURCHASE_TIMES_COMPANY = PTC.PURCHASE_TIMES;

DROP TABLE TR_PURCHASE_TIMES_COMPANY;

ALTER TABLE TEST_HISTORY
  ADD PURCHASE_TIMES_COMPANY NUMBER(10) DEFAULT 0;
  
CREATE TABLE TE_PURCHASE_TIMES_COMPANY
AS
     SELECT TH.CUSTOMER_ID CUSTOMER_ID,
            OFF.COMPANY_ID COMPANY_ID,
            COUNT (1) PURCHASE_TIMES
       FROM TEST_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
      WHERE     TH.CUSTOMER_ID = TR.TRANSACTION_ID
            AND TH.OFFER_ID = OFF.OFFER_ID
            AND OFF.COMPANY_ID = TR.COMPANY_ID
   GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID;

MERGE INTO TEST_HISTORY TH
     USING (SELECT CUSTOMER_ID, COMPANY_ID, PURCHASE_TIMES
              FROM TE_PURCHASE_TIMES_COMPANY) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.PURCHASE_TIMES_COMPANY = PTC.PURCHASE_TIMES;

DROP TABLE TE_PURCHASE_TIMES_COMPANY;
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

ALTER TABLE TEST_HISTORY
   ADD PURCHASE_VALUE_COMPANY NUMBER (10) DEFAULT 0;

CREATE TABLE PURCHASE_VALUE_COMPANY
AS
     SELECT TH.CUSTOMER_ID CUSTOMER_ID,
            OFF.COMPANY_ID COMPANY_ID,
            SUM (PURCHASE_AMT) PURCHASE_AMT
       FROM TEST_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
      WHERE     TH.CUSTOMER_ID = TR.TRANSACTION_ID
            AND TH.OFFER_ID = OFF.OFFER_ID
            AND OFF.COMPANY_ID = TR.COMPANY_ID
   GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID;

MERGE INTO TEST_HISTORY TH
     USING (SELECT CUSTOMER_ID, COMPANY_ID, PURCHASE_AMT
              FROM PURCHASE_VALUE_COMPANY) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
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

ALTER TABLE TEST_HISTORY
   ADD PURCHASE_QUANTITY_COMPANY NUMBER (10) DEFAULT 0;
   
CREATE TABLE PURCHASE_QTY_COMPANY
AS
     SELECT TH.CUSTOMER_ID CUSTOMER_ID,
            OFF.COMPANY_ID COMPANY_ID,
            SUM (PURCHASE_QTY) PURCHASE_QTY
       FROM TEST_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
      WHERE     TH.CUSTOMER_ID = TR.TRANSACTION_ID
            AND TH.OFFER_ID = OFF.OFFER_ID
            AND OFF.COMPANY_ID = TR.COMPANY_ID
   GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID;

MERGE INTO TEST_HISTORY TH
     USING (SELECT CUSTOMER_ID, COMPANY_ID, PURCHASE_QTY
              FROM PURCHASE_QTY_COMPANY) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.PURCHASE_QUANTITY_COMPANY = PTC.PURCHASE_QTY;

DROP TABLE PURCHASE_QTY_COMPANY;
-------------------------------------------------------------

ALTER TABLE TRAIN_HISTORY
   ADD OFFER_COMPANY_180 NUMBER (10) DEFAULT 0;
   
CREATE TABLE OFFER_COMPANY_180
AS
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
GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID;

MERGE INTO TRAIN_HISTORY TH
     USING (SELECT CUSTOMER_ID, COMPANY_ID, PURCHASE_TIMES
              FROM OFFER_COMPANY_180) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.OFFER_COMPANY_180 = PTC.PURCHASE_TIMES;

DROP TABLE OFFER_COMPANY_180;

ALTER TABLE TEST_HISTORY
   ADD OFFER_COMPANY_180 NUMBER (10) DEFAULT 0;
   
CREATE TABLE OFFER_COMPANY_180
AS
     SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.COMPANY_ID COMPANY_ID,
         COUNT (1) PURCHASE_TIMES
    FROM TEST_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
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
GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID;

MERGE INTO TEST_HISTORY TH
     USING (SELECT CUSTOMER_ID, COMPANY_ID, PURCHASE_TIMES
              FROM OFFER_COMPANY_180) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.OFFER_COMPANY_180 = PTC.PURCHASE_TIMES;

DROP TABLE OFFER_COMPANY_180;

-------------------------------------------------------------
ALTER TABLE TRAIN_HISTORY
   ADD OFFER_COMPANY_60 NUMBER (10) DEFAULT 0;
   
CREATE TABLE OFFER_COMPANY_60
AS
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
GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID;

MERGE INTO TRAIN_HISTORY TH
     USING (SELECT CUSTOMER_ID, COMPANY_ID, PURCHASE_TIMES
              FROM OFFER_COMPANY_60) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.OFFER_COMPANY_60 = PTC.PURCHASE_TIMES;

DROP TABLE OFFER_COMPANY_60;

ALTER TABLE TEST_HISTORY
   ADD OFFER_COMPANY_60 NUMBER (10) DEFAULT 0;
   
CREATE TABLE OFFER_COMPANY_60
AS
     SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.COMPANY_ID COMPANY_ID,
         COUNT (1) PURCHASE_TIMES
    FROM TEST_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
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
GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID;

MERGE INTO TEST_HISTORY TH
     USING (SELECT CUSTOMER_ID, COMPANY_ID, PURCHASE_TIMES
              FROM OFFER_COMPANY_60) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.OFFER_COMPANY_60 = PTC.PURCHASE_TIMES;

DROP TABLE OFFER_COMPANY_60;
-----------------------------------------------------------------

ALTER TABLE TRAIN_HISTORY
   ADD OFFER_COMPANY_30 NUMBER (10) DEFAULT 0;
   
CREATE TABLE OFFER_COMPANY_30
AS
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
GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID;

MERGE INTO TRAIN_HISTORY TH
     USING (SELECT CUSTOMER_ID, COMPANY_ID, PURCHASE_TIMES
              FROM OFFER_COMPANY_30) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.OFFER_COMPANY_30 = PTC.PURCHASE_TIMES;

DROP TABLE OFFER_COMPANY_30;

ALTER TABLE TEST_HISTORY
   ADD OFFER_COMPANY_30 NUMBER (10) DEFAULT 0;
   
CREATE TABLE OFFER_COMPANY_30
AS
     SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.COMPANY_ID COMPANY_ID,
         COUNT (1) PURCHASE_TIMES
    FROM TEST_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
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
GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID;

MERGE INTO TEST_HISTORY TH
     USING (SELECT CUSTOMER_ID, COMPANY_ID, PURCHASE_TIMES
              FROM OFFER_COMPANY_30) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.OFFER_COMPANY_30 = PTC.PURCHASE_TIMES;

DROP TABLE OFFER_COMPANY_30;

-----------------------------------------------------------------

ALTER TABLE TRAIN_HISTORY
   ADD PURCHASE_TIMES_CCB NUMBER (10) DEFAULT 0;
   
CREATE TABLE PURCHASE_TIMES_CCB
AS
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
GROUP BY TH.CUSTOMER_ID,
         OFF.CATEGORY_ID,
         OFF.COMPANY_ID,
         OFF.BRAND_ID;

MERGE INTO TRAIN_HISTORY TH
     USING (SELECT CUSTOMER_ID, COMPANY_ID, PURCHASE_TIMES
              FROM PURCHASE_TIMES_CCB) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.PURCHASE_TIMES_CCB = PTC.PURCHASE_TIMES;

DROP TABLE PURCHASE_TIMES_CCB;

ALTER TABLE TEST_HISTORY
   ADD PURCHASE_TIMES_CCB NUMBER (10) DEFAULT 0;
   
CREATE TABLE PURCHASE_TIMES_CCB
AS
     SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.CATEGORY_ID CATEGORY_IDANY_ID,
         OFF.COMPANY_ID COMPANY_ID,
         OFF.BRAND_ID BRAND_ID,
         COUNT (1) PURCHASE_TIMES
    FROM TEST_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.CATEGORY_ID = TR.CATEGORY_ID
         AND OFF.COMPANY_ID = TR.COMPANY_ID
         AND OFF.BRAND_ID = TR.BRAND_ID
GROUP BY TH.CUSTOMER_ID,
         OFF.CATEGORY_ID,
         OFF.COMPANY_ID,
         OFF.BRAND_ID;

MERGE INTO TEST_HISTORY TH
     USING (SELECT CUSTOMER_ID, COMPANY_ID, PURCHASE_TIMES
              FROM PURCHASE_TIMES_CCB) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.PURCHASE_TIMES_CCB = PTC.PURCHASE_TIMES;

DROP TABLE PURCHASE_TIMES_CCB;

-------------------------------------------------------------------------

ALTER TABLE TRAIN_HISTORY
   ADD NEVER_BOUGHT_CCB NUMBER (1) DEFAULT NULL; 
   
CREATE TABLE NEVER_BOUGHT_CCB
AS
     SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.CATEGORY_ID CATEGORY_IDANY_ID,
         OFF.COMPANY_ID COMPANY_ID,
         OFF.BRAND_ID BRAND_ID,
         DECODE (COUNT (1), 0, 1, 0) NOT_PURCHASED_BEFORE
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

MERGE INTO TRAIN_HISTORY TH
     USING (SELECT CUSTOMER_ID, COMPANY_ID, NOT_PURCHASED_BEFORE
              FROM NEVER_BOUGHT_CCB) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.NEVER_BOUGHT_CCB = PTC.NOT_PURCHASED_BEFORE;

DROP TABLE NEVER_BOUGHT_CCB;

ALTER TABLE TEST_HISTORY
   ADD NEVER_BOUGHT_CCB NUMBER (1) DEFAULT NULL;    
   
CREATE TABLE NEVER_BOUGHT_CCB
AS
     SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.CATEGORY_ID CATEGORY_IDANY_ID,
         OFF.COMPANY_ID COMPANY_ID,
         OFF.BRAND_ID BRAND_ID,
         DECODE (COUNT (1), 0, 1, 0) NOT_PURCHASED_BEFORE
    FROM TEST_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.CATEGORY_ID = TR.CATEGORY_ID
         AND OFF.COMPANY_ID = TR.COMPANY_ID
         AND OFF.BRAND_ID = TR.BRAND_ID
GROUP BY TH.CUSTOMER_ID,
         OFF.CATEGORY_ID,
         OFF.COMPANY_ID,
         OFF.BRAND_ID;

MERGE INTO TEST_HISTORY TH
     USING (SELECT CUSTOMER_ID, COMPANY_ID, NOT_PURCHASED_BEFORE
              FROM NEVER_BOUGHT_CCB) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.NEVER_BOUGHT_CCB = PTC.NOT_PURCHASED_BEFORE;

DROP TABLE NEVER_BOUGHT_CCB;

---------------------------------------------------------

ALTER TABLE TRAIN_HISTORY
   ADD PURCHASE_TIMES_CAT NUMBER (10) DEFAULT 0;
   
CREATE TABLE PURCHASE_TIMES_CAT
AS
     SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.CATEGORY_ID CATEGORY_ID,
         COUNT (*) PURCHASE_TIMES
FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.CATEGORY_ID = TR.CATEGORY_ID
GROUP BY TH.CUSTOMER_ID, OFF.CATEGORY_ID;

MERGE INTO TRAIN_HISTORY TH
     USING (SELECT CUSTOMER_ID, CATEGORY_ID, PURCHASE_TIMES
              FROM PURCHASE_TIMES_CAT) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.PURCHASE_TIMES_CAT = PTC.PURCHASE_TIMES;

DROP TABLE PURCHASE_TIMES_CAT;

ALTER TABLE TEST_HISTORY
   ADD PURCHASE_TIMES_CAT NUMBER (10) DEFAULT 0;
   
CREATE TABLE PURCHASE_TIMES_CAT
AS
     SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.CATEGORY_ID CATEGORY_ID,
         COUNT (*) PURCHASE_TIMES
FROM TEST_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.CATEGORY_ID = TR.CATEGORY_ID
GROUP BY TH.CUSTOMER_ID, OFF.CATEGORY_ID;

MERGE INTO TEST_HISTORY TH
     USING (SELECT CUSTOMER_ID, CATEGORY_ID, PURCHASE_TIMES
              FROM PURCHASE_TIMES_CAT) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.PURCHASE_TIMES_CAT = PTC.PURCHASE_TIMES;

DROP TABLE PURCHASE_TIMES_CAT;

-----------------------------------------------------------------

ALTER TABLE TRAIN_HISTORY
   ADD NEVER_BOUGHT_CAT NUMBER (1); 
   
CREATE TABLE NEVER_BOUGHT_CAT
AS
     SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.CATEGORY_ID CATEGORY_ID,
         DECODE (COUNT (1), 0, 1, 0) NOT_PURCHASED_BEFORE
   FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
GROUP BY TH.CUSTOMER_ID, OFF.CATEGORY_ID;

MERGE INTO TRAIN_HISTORY TH
     USING (SELECT CUSTOMER_ID, CATEGORY_ID, NOT_PURCHASED_BEFORE
              FROM NEVER_BOUGHT_CAT) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.NEVER_BOUGHT_CAT = PTC.NOT_PURCHASED_BEFORE;

DROP TABLE NEVER_BOUGHT_CAT;

ALTER TABLE TEST_HISTORY
   ADD NEVER_BOUGHT_CAT NUMBER (1); 
   
CREATE TABLE NEVER_BOUGHT_CAT
AS
     SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.CATEGORY_ID CATEGORY_ID,
         DECODE (COUNT (1), 0, 1, 0) NOT_PURCHASED_BEFORE
   FROM TEST_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
GROUP BY TH.CUSTOMER_ID, OFF.CATEGORY_ID;

MERGE INTO TEST_HISTORY TH
     USING (SELECT CUSTOMER_ID, CATEGORY_ID, NOT_PURCHASED_BEFORE
              FROM NEVER_BOUGHT_CAT) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.NEVER_BOUGHT_CAT = PTC.NOT_PURCHASED_BEFORE;

DROP TABLE NEVER_BOUGHT_CAT;

----------------------------------------------------------------
ALTER TABLE TRAIN_HISTORY
   ADD AMOUNT_SPENT_CAT NUMBER (10) DEFAULT 0;
   
CREATE TABLE AMOUNT_SPENT_CAT
AS
    SELECT TH.CUSTOMER_ID CUSTOMER_ID, OFF.CATEGORY_ID CATEGORY_ID,
	SUM (PURCHASE_AMT) TOTAL_AMT_SPENT
   FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
	 AND OFF.CATEGORY_ID = TR.CATEGORY_ID
GROUP BY TH.CUSTOMER_ID, OFF.CATEGORY_ID;

MERGE INTO TRAIN_HISTORY TH
     USING (SELECT CUSTOMER_ID, CATEGORY_ID, TOTAL_AMT_SPENT
              FROM AMOUNT_SPENT_CAT) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.AMOUNT_SPENT_CAT = PTC.TOTAL_AMT_SPENT;

DROP TABLE AMOUNT_SPENT_CAT;

ALTER TABLE TEST_HISTORY
   ADD AMOUNT_SPENT_CAT NUMBER (10) DEFAULT 0;
   
CREATE TABLE AMOUNT_SPENT_CAT
AS
    SELECT TH.CUSTOMER_ID CUSTOMER_ID, OFF.CATEGORY_ID CATEGORY_ID,
	SUM (PURCHASE_AMT) TOTAL_AMT_SPENT
   FROM TEST_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
   WHERE TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
	 AND OFF.CATEGORY_ID = TR.CATEGORY_ID
GROUP BY TH.CUSTOMER_ID, OFF.CATEGORY_ID;

MERGE INTO TEST_HISTORY TH
     USING (SELECT CUSTOMER_ID, CATEGORY_ID, TOTAL_AMT_SPENT
              FROM AMOUNT_SPENT_CAT) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.AMOUNT_SPENT_CAT = PTC.TOTAL_AMT_SPENT;

DROP TABLE AMOUNT_SPENT_CAT;

------------------------------------------------------------

ALTER TABLE TRAIN_HISTORY
   ADD BOUGHT_CATEGORY_30 NUMBER (10) DEFAULT 0;
   
CREATE TABLE BOUGHT_CATEGORY_30
AS
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
                                                              - 30
                                                          AND TO_DATE (
                                                                 TH.OFFER_DATE,
                                                                 'dd/mm/yyyy')
GROUP BY TH.CUSTOMER_ID, OFF.CATEGORY_ID;

MERGE INTO TRAIN_HISTORY TH
     USING (SELECT CUSTOMER_ID, CATEGORY_ID, PURCHASE_TIMES
              FROM BOUGHT_CATEGORY_30) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.BOUGHT_CATEGORY_30 = PTC.PURCHASE_TIMES;

DROP TABLE BOUGHT_CATEGORY_30;

ALTER TABLE TEST_HISTORY
   ADD BOUGHT_CATEGORY_30 NUMBER (10) DEFAULT 0;
   
CREATE TABLE BOUGHT_CATEGORY_30
AS
     SELECT TH.CUSTOMER_ID CUSTOMER_ID,
         OFF.CATEGORY_ID CATEGORY_ID,
         COUNT (1) PURCHASE_TIMES
    FROM TEST_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
    WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
         AND TH.OFFER_ID = OFF.OFFER_ID
         AND OFF.CATEGORY_ID = TR.CATEGORY_ID
         AND TO_DATE (TR.PURCHASE_DATE, 'dd/mm/yyyy') BETWEEN   TO_DATE (
                                                                   TH.OFFER_DATE,
                                                                   'dd/mm/yyyy')
                                                              - 30
                                                          AND TO_DATE (
                                                                 TH.OFFER_DATE,
                                                                 'dd/mm/yyyy')
GROUP BY TH.CUSTOMER_ID, OFF.CATEGORY_ID;

MERGE INTO TEST_HISTORY TH
     USING (SELECT CUSTOMER_ID, CATEGORY_ID, PURCHASE_TIMES
              FROM BOUGHT_CATEGORY_30) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.BOUGHT_CATEGORY_30 = PTC.PURCHASE_TIMES;

DROP TABLE BOUGHT_CATEGORY_30;

-----------------------------------------------------------------

ALTER TABLE TRAIN_HISTORY
   ADD CHAIN_VISIT_FREQ NUMBER (10) DEFAULT 0;
   
CREATE TABLE CHAIN_VISIT_FREQ
AS
    
  SELECT CUSTOMER_ID, CHAIN_ID, COUNT(PURCHASE_TIMES) PURCHASE_TIMES
    FROM (  SELECT TH.CUSTOMER_ID CUSTOMER_ID,
                   TH.CHAIN_ID CHAIN_ID,
                   TR.PURCHASE_DATE,
                   COUNT (*) PURCHASE_TIMES
              FROM TRAIN_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
             WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
                   AND TH.OFFER_ID = OFF.OFFER_ID
                   AND TH.CHAIN_ID = TR.CHAIN_ID
          GROUP BY TH.CUSTOMER_ID, TH.CHAIN_ID, TR.PURCHASE_DATE)
GROUP BY CUSTOMER_ID, CHAIN_ID;

MERGE INTO TRAIN_HISTORY TH
     USING (SELECT CUSTOMER_ID, CHAIN_ID, PURCHASE_TIMES
              FROM CHAIN_VISIT_FREQ) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.CHAIN_VISIT_FREQ = PTC.PURCHASE_TIMES;

DROP TABLE CHAIN_VISIT_FREQ;

ALTER TABLE TEST_HISTORY
   ADD CHAIN_VISIT_FREQ NUMBER (10) DEFAULT 0;
   
CREATE TABLE CHAIN_VISIT_FREQ
AS    
  SELECT CUSTOMER_ID, CHAIN_ID, COUNT(PURCHASE_TIMES) PURCHASE_TIMES
    FROM (  SELECT TH.CUSTOMER_ID CUSTOMER_ID,
                   TH.CHAIN_ID CHAIN_ID,
                   TR.PURCHASE_DATE,
                   COUNT (*) PURCHASE_TIMES
              FROM TEST_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
             WHERE     TH.CUSTOMER_ID = TR.CUSTOMER_ID
                   AND TH.OFFER_ID = OFF.OFFER_ID
                   AND TH.CHAIN_ID = TR.CHAIN_ID
          GROUP BY TH.CUSTOMER_ID, TH.CHAIN_ID, TR.PURCHASE_DATE)
GROUP BY CUSTOMER_ID, CHAIN_ID;

MERGE INTO TEST_HISTORY TH
     USING (SELECT CUSTOMER_ID, CHAIN_ID, PURCHASE_TIMES
              FROM CHAIN_VISIT_FREQ) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.CHAIN_VISIT_FREQ = PTC.PURCHASE_TIMES;

DROP TABLE CHAIN_VISIT_FREQ;

--------------------------------------------------------------

ALTER TABLE TRAIN_HISTORY
   ADD RATIO_RET_BGHT_CC NUMBER (10) DEFAULT 0;
   
CREATE TABLE RATIO_RET_BGHT_CC
AS
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
          	   GROUP BY TR.CUSTOMER_ID 
         );

MERGE INTO TRAIN_HISTORY TH
     USING (SELECT CUSTOMER_ID, RATIO
              FROM RATIO_RET_BGHT_CC) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.RATIO_RET_BGHT_CC = PTC.RATIO;

DROP TABLE RATIO_RET_BGHT_CC;

ALTER TABLE TEST_HISTORY
   ADD RATIO_RET_BGHT_CC NUMBER (10) DEFAULT 0;
   
CREATE TABLE RATIO_RET_BGHT_CC
AS
     SELECT CUSTOMER_ID,
         (CASE
             WHEN BOUGHT_COUNT > 0 THEN RETURN_COUNT / BOUGHT_COUNT
             ELSE 0
          END)
            RATIO
    FROM (  SELECT TR.CUSTOMER_ID CUSTOMER_ID,
                   COUNT (CASE WHEN TR.PURCHASE_AMT < 0 THEN 1 END) RETURN_COUNT,
                   COUNT (CASE WHEN TR.PURCHASE_AMT > 0 THEN 1 END) BOUGHT_COUNT
              FROM TEST_HISTORY TH, OFFERS OFF, TRANSACTIONS TR
             WHERE TH.CUSTOMER_ID = TR.CUSTOMER_ID
                   AND TH.OFFER_ID = OFF.OFFER_ID
                   AND OFF.CATEGORY_ID = TR.CATEGORY_ID
                   AND OFF.COMPANY_ID = TR.COMPANY_ID
          	   GROUP BY TR.CUSTOMER_ID 
         );

MERGE INTO TEST_HISTORY TH
     USING (SELECT CUSTOMER_ID, RATIO
              FROM RATIO_RET_BGHT_CC) PTC
        ON (TH.CUSTOMER_ID = PTC.CUSTOMER_ID)
WHEN MATCHED
THEN
   UPDATE SET TH.RATIO_RET_BGHT_CC = PTC.RATIO;

DROP TABLE RATIO_RET_BGHT_CC;