#from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
from pyzillow import ZillowWrapper, GetDeepSearchResults
import quickbase

url = "https://xxxxx"                    #quickbooks app url
token = "xxxxxxxxxxxxxx"                 #Create app Token in Manage Application Tokens Section on qb
database = 'xxxxxxxxxxx'                 #This is teh encoded reference to the table in qb
username = 'xxxxxxx'                     #quickbooks logind ID
password = 'xxxxxxxxx'                   #quickbooks pass
YOUR_ZILLOW_API_KEY = "xxxxxxx"          #Zillow API access Key
zcounter = 0                             # zillow API calls counter
zlimit = 1                               # number of API calls to make to Zillow (limit is 1000/day)

zillow_data = ZillowWrapper(YOUR_ZILLOW_API_KEY)
qbc = quickbase.Client(username,password,database=database,apptoken=token, base_url=url)

qbr = qbc.do_query(query="{'202'.EX.''}", columns='a',database=database)        # Pull all records where zestimate is BLANK
#qbr = qbc.do_query(query="{'7'.CT.'ST'}", columns='a',database=database)       #Pull all records that contain "ST" in the address1 line

print("=====================================================")                  #DEBUG

for  record in qbr:
    address = record["7"]                                                       
    zipcode = record["11"]
    if zipcode != "" and len(zipcode) == 5 and zcounter < zlimit:
        deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
        print("--> deep_search_response:", deep_search_response)                #DEBUG
        result = GetDeepSearchResults(deep_search_response)
        result.zillow_id                                                        # zillow id, needed for the GetUpdatedPropertyDetails
        zcounter = zcounter + 1
        print("Rec ID: %s ->  %s + Zip: %s --> Zestimate: %s" % (record["3"], record["7"], record["11"],result.zestimate_amount))
        qbc.edit_record(rid=record["3"], fields={"202":result.zestimate_amount}, named=False, database=database)
