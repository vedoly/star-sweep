import traceback
import urllib3
import xmltodict
import numpy as np
import pandas as pd
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
    try:
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
    except:
        return []


def getDataframe(terms, amount):
    result = getArticle(terms, amount + 20)[:-20]
    print(len(result))

    data = {"pmid": [], "title": [], "abstract": [], "keywords": []}
    for e in result:
        try:
            data["pmid"].append(e["MedlineCitation"]["PMID"]["#text"])

        except:
            data["pmid"].append(np.nan)

        try:
            data["title"].append(e["MedlineCitation"]["Article"]["ArticleTitle"])
        except:
            data["title"].append(np.nan)

        try:
            try:
                try:
                    data["abstract"].append(
                        e["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0][
                            "#text"
                        ]
                    )

                except Exception as ee:

                    data["abstract"].append(
                        e["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][
                            "#text"
                        ]
                    )
            except:
                data["abstract"].append(
                    e["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]
                )
        except:
            data["abstract"].append(np.nan)

        try:
            data["keywords"].append(
                [k["#text"] for k in e["MedlineCitation"]["KeywordList"]["Keyword"]]
            )
        except:
            data["keywords"].append(np.nan)

    return pd.DataFrame.from_dict(data)


# print("x")
