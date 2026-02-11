from github import Github
from config import GITHUB_TOKEN

def load_repo_tf_files(repo_name: str):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo_name)

    contents = repo.get_contents("")
    tf_files = []

    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        elif file_content.path.endswith(".tf"):
            tf_files.append(file_content.decoded_content.decode())

    return tf_files
