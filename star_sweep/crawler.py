import traceback
import urllib3
import xmltodict
from urllib.parse import urlencode, quote

# from urllib.parse import urlencode # python3
from collections import OrderedDict


def getxml(url):
    http = urllib3.PoolManager()
    # print(url)
    response = http.request("GET", url)
    try:
        data = xmltodict.parse(response.data)
    except:
        print("Failed to parse xml from response (%s)" % traceback.format_exc())
    return data


def getPUID(terms):
    terms = terms.replace(" ", "+")
    query_string = urlencode(OrderedDict(term=terms))
    return getxml(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term="
        + terms
        + "&retmax=10000"
    )


def getArticle(terms, amount):
    puids = getPUID(terms)["eSearchResult"]["IdList"]["Id"]
    request_batch = [puids[i : i + 200] for i in range(0, amount, 200)]

    result = []
    for i, e in enumerate(request_batch):
        print(i)
        result.append(
            getxml(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id="
                + ",".join(e)
                + "&rettype=text"
            )
        )

    out = []
    for e in result:
        try:
            out += e["PubmedArticleSet"]["PubmedArticle"]
        except:
            pass
    return out


# print("x")
