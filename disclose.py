import urllib.request, json

# source https://portal.api.business.govt.nz/api-details#api=disclose-public&operation=DisclosePublic code generator
try:
    url = "https://api.business.govt.nz/sandbox/companies-office/disclose-register/DisclosePublic/v3/"

    hdr ={
    # Request headers
    'Content-Type': 'text/xml',
    'Cache-Control': 'no-cache',
    'Ocp-Apim-Subscription-Key': '1234',   # key goes here I think
    }

    req = urllib.request.Request(url, headers=hdr)

    req.get_method = lambda: 'POST'
    response = urllib.request.urlopen(req)
    print(response.getcode())
    print(response.read())
except Exception as e:
    print(e)

# Parsing
print('Next part')
import xmltodict
# open file that has a sample SOAP response as an example on API website
with open('response.txt') as f:
    response = f.read()
results = xmltodict.parse(response)
print(results)
print('Example per item...')
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