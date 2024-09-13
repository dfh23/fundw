import urllib.request, json
import os
import xmltodict

soap_query = '''\
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sear="http://data.business.govt.nz/services/FMCR/Disc
 losePublic/SearchOffers" xmlns:com="http://data.business.govt.nz/services/FMCR/CommonTypes"> 
   <soapenv:Header/> 
   <soapenv:Body> 
      <sear:SearchOffers> 
         <sear:SchemaVersion>1.0</sear:SchemaVersion> 
         <sear:Request> 
            <sear:Criteria> 
                 <sear:OfferNameNumber>{query}</sear:OfferNameNumber> 
                 </sear:Criteria> 
         </sear:Request> 
      </sear:SearchOffers> 
   </soapenv:Body> 
</soapenv:Envelope>\
'''

URL = "https://api.business.govt.nz/sandbox/companies-office/disclose-register/DisclosePublic/v3/"
sub_key = '1234' # add your key in here or (best pratice) patch to use an ENVIRONMENT variable
hdr ={
    # Request headers
    'Content-Type': 'text/xml',
    'Cache-Control': 'no-cache',
    'Ocp-Apim-Subscription-Key': sub_key,
    }
soap_url = 'http://data.business.govt.nz/services/FMCR/DisclosePublic/DisclosePublicServicePort/SearchOffers'


def call_url(url, hdr, body=None):
    # source https://portal.api.business.govt.nz/api-details#api=disclose-public&operation=DisclosePublic code generator
    try:
        req = urllib.request.Request(url, headers=hdr, data=body)

        req.get_method = lambda: 'POST'
        response = urllib.request.urlopen(req)
        # Success
        print("Success with code: ", response.getcode())
        print(response.read())
        return response

    except Exception as e:
        print('Exception thrown')
        print(e)
        print(e.__dict__)
    return False

# Check authentication
print("Checking authentication...")
response = call_url(URL, hdr)

# If success then run a query
query_response = None
if response:
    print("Now calling a query...")
    query_text = 'kiwisaver test'  # adjust as necessary
    soap_body = soap_query.format(query=query_text)
    soap_body = soap_body.encode('utf-8')
    print('SOAP body: ', soap_body)
    # Add a soap url in header
    hdr['SOAPAction'] = soap_url
    print("Header: ", hdr)
    query_response = call_url(URL, hdr, soap_body)
    print("Query_response:", query_response)


# Parsing
# If no query response then load up from sample file
print("No query response; sourcing sample data to parse...")
if not query_response:
    # open file that has a sample SOAP response as an example on API website
    with open('response.txt') as f:
        query_response = f.read()

print('Now attempting parsing...')
results = xmltodict.parse(query_response)
print(results)
print('Example per item...')
# deep dive into the nested dicts
nested_results = (results['SOAP-ENV:Envelope']
    ['SOAP-ENV:Body']
    ['sear:SearchOffersResponse']
    ['sear:Response']
    ['sear:FmcOfferSearchWebServiceResults']
    ['sear:OfferSummary'])
print("This should be a list: ", type(nested_results))
print(nested_results)

# we can iterate over the list
for r in nested_results:
    print(r['sear:OfferIdentification']['sear:CurrentName'])