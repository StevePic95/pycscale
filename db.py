import pymongo
import ssl
import constants as const

# DATABASE ACCESS - 'pcfadb'
client = pymongo.MongoClient(const.MONGODB_CLIENT_URL, ssl_cert_reqs=ssl.CERT_NONE)
database = client.get_database(const.MONGODB_DATABASE_NAME)

# COLLECTION ACCESS
customer_accounts_collection = database.get_collection('Customer Accounts')
tickets_collection = database.get_collection('Tickets')

# FUNCTIONS

def update_collection_from_df(df, collection):
    """Keep in mind that the df passed to this function must have an _id key to
    work properly."""
    data = df.to_dict(orient='records')
    for row in data:
        collection.update_one({"_id": row['_id']},{'$set': row}, upsert=True)