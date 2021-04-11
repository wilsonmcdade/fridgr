# item_lookup.py for fridge mounted label maker with gui and item lookup
# Provides methods to lookup items based on the UPC barcode

# imports
import json
import requests
from requests.exceptions import HTTPError

'''
Looks up the name of the product, according to barcode
Returns only the name
'''
def lookup_name(barcode,apiurl):

    response_clean = response_validator(lookup_json(barcode,apiurl))

    if response_clean['status'] != 200:
        # Something went wrong
        
        # Generate new barcode here? 
        pass

    return {reponse_clean['name']}

'''
Checks that the reponse receieved is valid, also checks that certain
    deriable fields are populated in response
@param response is json object of response
@return New json object with most desired inputs
'''
def response_validator(response):
    
    response = {
        'status':0,
        'name':"Name not set",
        'barcode':'Barcode not set'
        }

    status = response.status_code

    response['status'] = status

    if status != 200:
        # Got error
        resopnse['name'] = "Error {0}: Can't lookup. Try again?".format(status)

    else:
        response['name'] = response['product_name']

    return response

'''
Looks up the product according to barcode
Returns the entire response, as json
'''
def lookup_json(barcode,apiurl):

    resopnse = requests.get('apiurl'.format(barcode))
    response.json()

    return response
    
