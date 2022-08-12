import time
import json
from api_handling import get_api_json

def get_author_profiles() -> list:

    """
    Returns a list of author profiles from Colombian institutions with at least one paper

    Each author profile is an url to an api
    """
    
    #  since the whole document fits within a single access, 
    #  and the latency is quite high, we will try to access as
    #  few times as possible the api

    college_api_url = "https://inspirehep.net/api/institutions?q=colombia&size=1000"

    college_data = get_api_json(college_api_url)

    colleges_with_papers = []


    for college in college_data["hits"]["hits"]:
        if college["metadata"]["number_of_papers"] > 0:
            colleges_with_papers.append(college)
            #print(college["metadata"]["legacy_ICN"])


    ## literature data

    first_split_url = "https://inspirehep.net/api/literature?sort=mostrecent&amp;page=1&amp;q=aff+"
    third_split_url = "+and+ac+1->+10"

    article_list_by_college = []

    ## we look only for authors from these colleges
    for college in colleges_with_papers:
        ## we replace white spaces with a '+' symbol
        second_split_url = college["metadata"]["legacy_ICN"].replace(" ", "+")
        ## we concatenate the three strings to get the final api url
        literature_api_url = first_split_url + second_split_url + third_split_url
        print("Accessing this api... \t\t", literature_api_url)
        article_list_by_college.append(get_api_json(literature_api_url)["hits"]["hits"])
 
    time.sleep(2)
    print("--------")


    author_profile_list = []

    ## we traverse the institutions that hold the papers
    for articles_list_info in article_list_by_college:
        print("Searching profiles...")
        ## we search each article within the list of articles
        for article in articles_list_info:
            ## we traverse the list of authors of each article      
            for authors in article["metadata"]["authors"]:
                print(authors["record"]["$ref"])
                ## we check that the author its not yet in our list of author profiles.
                if authors["record"]["$ref"] not in author_profile_list:
                    author_profile_list.append(authors["record"]["$ref"])

    return author_profile_list


def create_profiles():

    author_profile_list = get_author_profiles()


    collection_authors = []


    for author_url in author_profile_list:
        author_document = {}
        profile_json = get_api_json(author_url)

        if author_url == "https://inspirehep.net/api/authors/1010271":
            input("aparecio Fazio")

        if "name" in profile_json["metadata"].keys():
            if "value" in profile_json["metadata"]["name"]:
                author_document["Nombre Completo"] =  profile_json["metadata"]["name"].get("value","")
        else:
            author_document["Nombre Completo"] = ""

        if "email_addresses" in profile_json["metadata"].keys():
            if len(profile_json["metadata"]["email_addresses"]) != 0:
                author_document["Correo electronico"] = profile_json["metadata"]["email_addresses"][0].get("value","")
        else:
            author_document["Correo electronico"] = ""

        if "positions" in profile_json["metadata"].keys():
            if len(profile_json["metadata"]["positions"]) != 0:
                author_document["rango"] = profile_json["metadata"]["positions"][0].get("rank", "")
                author_document["institucion"] = profile_json["metadata"]["positions"][0].get("institution", "")
                author_document["fecha de inicio"] = profile_json["metadata"]["positions"][0].get("start_date", "")     
                author_document["fecha de finalizacion"] = profile_json["metadata"]["positions"][0].get("end_date", "Sigue vinculado")
        else:
            author_document["rango"] = ""
            author_document["institucion"] = ""
            author_document["fecha de inicio"] = ""
            author_document["fecha de finalizacion"] = ""
        
        collection_authors.append(author_document)


    serialized_json_authors = json.dumps(collection_authors,indent=4)

    print(serialized_json_authors)

    print("Number of authors in json dumps", len(serialized_json_authors))

    with open("summary_authors.json", "w") as outfile:
        outfile.write(serialized_json_authors)
        outfile.close()
    
    return collection_authors