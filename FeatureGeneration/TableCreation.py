from dateutil.parser import parse
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql import Row

transactionFile = sc.textFile("E:/FP/Transactions.csv”)
sqlContext = SQLContext(sc)
schemaString = "CUSTOMER_ID CHAIN_ID DEPARTMENT_ID CATEGORY_ID COMPANY_ID BRAND_ID PURCHASE_DATE PRODUCT_SIZE PRODUCT_MEASURE PURCHASE_QTY PURCHASE_AMT"
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
fields[6].dataType = TimestampType()
fields[7].dataType = FloatType()
fields[9].dataType = FloatType()
fields[10].dataType = FloatType()
schema = StructType(fields)
header = transactionFile.filter(lambda line: "id" in line)
transactionFile = transactionFile.subtract(header)
transactions = transactionFile.map(lambda l: l.split(",")).map(lambda p: (p[0],p[1],p[2],p[3],p[4],p[5],parse(p[6]),float(p[7]),p[8],float(p[9]),float(p[10])))
transactions_df = sqlContext.createDataFrame(transactions, schema) 
transactions_df.registerTempTable("transactions")

offerFile = sc.textFile("E:/FP/Offers.csv”)
schemaString = "OFFER_ID CATEGORY_ID MIN_QTY_TO_PURCHASE COMPANY_ID OFFER_VALUE BRAND_ID"
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
fields[4].dataType = FloatType()
schema = StructType(fields)
header = offerFile.filter(lambda line: "offer" in line)
offerFile = offerFile.subtract(header)
offers = offerFile.map(lambda l: l.split(",")).map(lambda p: (p[0],p[1],p[2],p[3],float(p[4]),p[5]))
offers_df = sqlContext.createDataFrame(offers, schema) 
offers_df.registerTempTable("offers")

trainFile = sc.textFile("E:/FP/TrainHistory.csv”)
schemaString = "CUSTOMER_ID CHAIN_ID OFFER_ID MARKET_ID REPEAT_TRIPS REPEATER OFFER_DATE"
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
fields[6].dataType = TimestampType()
schema = StructType(fields)
header = trainFile.filter(lambda line: "id" in line)
trainFile = trainFile.subtract(header)
train = trainFile.map(lambda l: l.split(",")).map(lambda p: (p[0],p[1],p[2],p[3],p[4],p[5],parse(p[6])))
train_df = sqlContext.createDataFrame(train, schema) 
train_df.registerTempTable("train")

has_bought_times_by_customer = sqlContext.sql(""" SELECT TH.CUSTOMER_ID CUSTOMER_ID, OFF.COMPANY_ID COMPANY_ID, COUNT (1) PURCHASE_TIMES
                                      FROM train TH, offers OFF, transactions TR
                                      WHERE TH.CUSTOMER_ID = TR.CUSTOMER_ID AND TH.OFFER_ID = OFF.OFFER_ID
                                      AND OFF.COMPANY_ID = TR.COMPANY_ID AND TR.CUSTOMER_ID = 86246
                                      GROUP BY TH.CUSTOMER_ID, OFF.COMPANY_ID""")

has_bought_times_by_customer.show()
