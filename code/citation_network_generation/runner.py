from concurrent.futures import ThreadPoolExecutor, as_completed
import arxiv
from tqdm import tqdm
import pickle

def get_papers_metadata(paper_id: list):
    client = arxiv.Client()
    search_by_id = arxiv.Search(id_list=paper_id)
    results = next(client.results(search_by_id))

    return_dictionary = {
        "paper_id": paper_id[0],
        "title": results.title,
        "authors": [each_author.name for each_author in results.authors],
        "summary": results.summary,
        "primary_category": results.primary_category,
        "categories": results.categories
    }

    return return_dictionary

if __name__ == "__main__":
    # Read the file containing list of papers
    with open("/ai/work/P_AI/graphRAG/dataset/arxiv_papers/ArXivQA-main/Papers-2023.md") as f_obj:
        files_lines = f_obj.readlines()

    results = {}
    with ThreadPoolExecutor(max_workers=30) as executor:
        
        # Submit the tasks to the executor
        future_to_item = {}
        for each_line in files_lines:
            if each_line.startswith("-"):
                paper_id = each_line.split("https://arxiv.org/abs/")[1].split(")] [[QA]")[0]
                future = executor.submit(get_papers_metadata, [paper_id])
                future_to_item[future] = paper_id
        
        print("Submitted all the tasks")

        # Get the results from the executor
        with tqdm(total=len(future_to_item), desc="Processing items") as pbar:
            for future in as_completed(future_to_item):
                paper_id = future_to_item[future]
                try:
                    response = future.result()
                    results[paper_id] = response
                except Exception as exc:
                    print(f"Paper ID: {paper_id} generated an exception: {exc}")
                pbar.update(1)

    # Save the results to a file
    with open("papers_metadata_2023.pkl", "wb") as f_obj:
        pickle.dump(results, f_obj)