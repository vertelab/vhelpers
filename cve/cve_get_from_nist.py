#!/usr/bin/env python3
'''
Prototype fetching CVE data from NIST's NVD. The NIST JSON API contain the
vulnerability score. MITRE's / cve.org's standard database does not.

Additional reading
==================
https://cve.org
https://nvd.nist.gov/developers
https://nvd.nist.gov/developers/vulnerabilities

'''
#%%
import requests
import datetime

#%%
BASE_URL_CVE = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
APIKEY = "" # Empty unused placeholder. With an API key the rate limit is
            # reduced.

#%%
def get_cve_list(lastModStartDate=None, lastModEndDate=None):
    '''
    Prototype utility to get CVE's and their score if possible.

    Based on Nists API for their NVD.
    https://nvd.nist.gov/developers/vulnerabilities

    Parameters
    ==========
    Work in progress. See https://nvd.nist.gov/developers/vulnerabilities
    for params in API.

    Returns
    =======
    JSON
    '''
    if lastModStartDate:
        startdate = lastModStartDate # Modified date
    else:
        startdate = datetime.datetime.utcnow() + datetime.timedelta(days=-14)
    if lastModEndDate:
        enddate = lastModEndDate
    else:
        enddate = datetime.datetime.utcnow()
    if enddate < startdate:
        raise ValueError("End date can't be older than start date.")

    response = requests.get(BASE_URL_CVE, params={'lastModStartDate':startdate.isoformat(),
    'lastModEndDate':enddate.isoformat()})
    if response:
        return response.json()
    else:
        return response

#%%

#%%
if __name__ == '__main__':
    print(get_cve_list())
