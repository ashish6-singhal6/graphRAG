from scholarly import scholarly as sch
from scholarly import ProxyGenerator
import pickle
from tqdm import tqdm

import time

def get_data_from_google_scholar(paper_title: str):
    """
    Steps this function does
    1. Search the publication on Google Scholar
    2. Get the publication details
    3. Get the author details
    4. Return the results
    """
    retries = 0
    parsed = False

    while not parsed and retries < 10:
        try:
            print("HERE")
            time.sleep(0.1)    
            search_query = sch.search_single_pub(paper_title)
            publication_result = search_query
            parsed = True
        except Exception as e:
            print(f"Error: {e}")
            retries += 1

    # Get the author details
    for each_author_id in search_query["author_id"]:
        if each_author_id not in author_dictionaries.keys():
            retries = 0
            parsed = False
            while not parsed and retries < 10:
                try:
                    time.sleep(0.1)
                    author = sch.search_author_id(each_author_id)
                    author_dictionaries[each_author_id] = author
                    parsed = True
                except Exception as e:
                    print(f"Error: {e}")
                    retries += 1

    return publication_result

if __name__ == "__main__":
    # Read the file containing list of papers
    with open("/ai/work/P_AI/graphRAG/dataset/arxiv_papers/ArXivQA-main/Papers-2023.md") as f_obj:
        files_lines = f_obj.readlines()

    # Refresh the proxies
    #pg = ProxyGenerator()
    #pg.FreeProxies()
    #sch.use_proxy(pg)


    results = {}
    author_dictionaries = {}
    counts = 0

    with tqdm(total=len(files_lines), desc="Processing items") as pbar:
        for each_line in files_lines:
            if each_line.startswith("-"):
                paper_title = each_line.split(" - [[Arxiv]")[0].strip(" -")
                result = get_data_from_google_scholar(paper_title)
                results[paper_title] = result
                counts += 1
            pbar.update(1)
            
            # Save the results to a file
            if counts % 100 == 0:
                with open(f"papers_metadata_{counts}.pkl", "wb") as f_obj:
                    pickle.dump(results, f_obj)

                with open(f"authors_metadata_{counts}.pkl", "wb") as f_obj:
                    pickle.dump(author_dictionaries, f_obj)
