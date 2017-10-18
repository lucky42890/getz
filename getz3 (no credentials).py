#from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
from pyzillow import ZillowWrapper, GetDeepSearchResults
import quickbase

url = "xxxx"
token = "xxx"  #Create app Token in Manage Application Tokens Section on qb
files_db_table  = 'xxx'                 #This is the encoded reference to the table "Files" in qb
comparables_qb_table = 'xxxx'      #This is the encoded reference to the table "Comparables" in qb
username = 'xxxxxx'
password = 'xxxxxx'
YOUR_ZILLOW_API_KEY = "xxxx"  #Zillow access Key (attached to jmeza@brightsystems.net)
zcounter = 0                # zillow API calls counter
zlimit = 1                  # number of API calls to make to Zillow (limit is 1000/day)

record_id = 0               #qbc fid = 3 (Numeric)  <-- This is the recird key for files_db_table
zestimate = 0.0               #qbc fid = 202 (Currency)
bathrooms = 0               #qbc fid = 293 (Numeric)
bedrooms = 0                #qbc fid = 294 (Numeric)
comp_score = 0              #qbc fid = 297 (Numeric)
finishedSqFt = 0            #qbc fid = 292 (Numeric)
lastSoldDate = "1/1/1900"   #qbc fid = 295 (Date)
lastSoldPrice = 0.0         #qbc fid = 296 (Currency)
lotSizeSqFt = 0             #qbc fid = 291 (Numeric)
taxAssessment = 0.0         #qbc fid = 289 (Currency)
taxAssessmentYear = 0       #qbc fid = 288 (Numeric)
tax_value = 0.0              #qbc fid = 204 (Currency)
tax_value_date = "1/1/1900"  #qbc fid = 205 (Date)
yearBuilt = 0               #qbc fid = 290 (Numeric)
zestimate_last_updated = "1/1/1900"  #qbc fid = 286 (Date)
rentzestimate_last_updated = "1/1/1900"  #qbc fid = 287 (Date)
rentzestimate = 0.0         #qbc fid = 203 (Currency)

comparables_url = "http://zillow.com"  #qbc fid = 6 (URL)  comparables <-- Report Link fid 298
servicerloanno = 0 #qbc fid = 8 (Numeric) in comparables_qb_table and fid = 15 in files_db_table


zillow_data = ZillowWrapper(YOUR_ZILLOW_API_KEY)
qbc = quickbase.Client(username,password,database=files_db_table,apptoken=token, base_url=url)

qbr = qbc.do_query(query="{'202'.EX.''}", columns='a',database=files_db_table)     # Pull all records where zestimate is BLANK
#qbr = qbc.do_query(query="{'7'.CT.'ST'}", columns='a',database=files_db_table)       #Pull all records that contain "ST" in the address1 line

print("=====================================================")                  #DEBUG

for  record in qbr:
    record_id      = record["3"]  #qbc fid = 3 (Numeric)  <-- This is the recird key for files_db_table
    address        = record["7"]
    zipcode        = record["11"]
    servicerloanno = record["15"]
    zestimate_last_updated = record["286"]  #qbc fid = 286 (Date)
    rentzestimate_last_updated = record["287"]  #qbc fid = 287 (Date)
    taxAssessmentYear = record["288"]       #qbc fid = 288 (Numeric)
    taxAssessment  = record["289"]         #qbc fid = 289 (Currency)
    yearBuilt      = record["290"]               #qbc fid = 290 (Numeric)
    zestimate      = record["202"]               #qbc fid = 202 (Currency)
    rentzestimate  = record["203"]    #qbc fid = 203 (Currency)
    lotSizeSqFt    = record["291"]            #qbc fid = 291 (Numeric)
    finishedSqFt   = record["292"]    #qbc fid = 292 (Numeric)
    bathrooms      = record["293"]    #qbc fid = 293 (Numeric)
    bedrooms       = record["294"]    #qbc fid = 294 (Numeric)
    lastSoldDate   = record["295"]    #qbc fid = 295 (Date)
    lastSoldPrice  = record["296"]  #qbc fid = 296 (Currency)
    comp_score     = record["297"]   #qbc fid = 297 (Numeric)

    if zipcode != "" and len(zipcode) == 5 and zcounter < zlimit:
        deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
        print("--> deep_search_response:", deep_search_response)
        result = GetDeepSearchResults(deep_search_response)
#        result.zillow_id                                            # zillow id, needed for the GetUpdatedPropertyDetails

        zestimate = result.zestimate_amount
        bathrooms = result.bathrooms
        bedrooms = result.bedrooms
        finishedSqFt = result.home_size
        lastSoldDate = result.last_sold_date
        lastSoldPrice = result.last_sold_price
        lotSizeSqFt = result.property_size
        taxAssessment = result.tax_value
        taxAssessmentYear = result.tax_year
        yearBuilt = result.year_built
        zestimate_last_updated = result.zestimate_last_updated

        comp_score = 99999                       # Need to get the data from zillow
        rentzestimate_last_updated = "1/1/1900"  # Need to get the data from zillow
        rentzestimate = 0.0                      ## Need to get the data from zillow

        zcounter = zcounter + 1
#        print("Rec ID: %s ->  %s + Zip: %s --> Zestimate: %s" % (record["3"], record["7"], record["11"],result.zestimate_amount))
        print("Rec ID: %s -> %s  %s + Zip: %s " % (record_id, servicerloanno, address, zipcode))
        qbc.edit_record(rid=record["3"], fields={"202":zestimate,
                                                 "286":zestimate_last_updated,
                                                 "287":rentzestimate_last_updated,
                                                 "288":taxAssessmentYear,
                                                 "289":taxAssessment,
                                                 "290":yearBuilt,
                                                 "203":rentzestimate,
                                                 "291":lotSizeSqFt,
                                                 "292":finishedSqFt,
                                                 "293":bathrooms,
                                                 "294":bedrooms,
                                                 "295":lastSoldDate,
                                                 "296":lastSoldPrice,
                                                 "297":comp_score
                                                 }, named=False, database=files_db_table)
        #Need to develop code to wipeout the current entries for the comparables_url in the comparables_qb_table
        qbc.add_record(fields={"6":(comparables_url+record_id),
                               "8":record_id,
                               "7":servicerloanno}, named=False, database=comparables_qb_table)
