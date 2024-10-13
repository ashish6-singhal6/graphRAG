import pickle

with open("papers_metadata_2023.pkl", "rb") as f_obj:
    results = pickle.load(f_obj)

authors = []
duplicate_count = 0
for key, value in results.items():
    for author in value["authors"]:
        if author in authors:
            duplicate_count += 1
        else:
            authors.append(author)

print(f"Total number of authors: {len(authors)}")
print(f"Total number of duplicate authors: {duplicate_count}")