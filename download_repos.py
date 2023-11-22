'''
download_repos.py
Downloads all the repositories listed in repo_names.csv
'''

import os
import csv
from tqdm import tqdm
from joblib import Parallel, delayed

def download_repo(repo, verbose=False):
    file_name = repo.split("/")[-1]
    if file_name not in os.listdir("/data/github-repos/"):
        # Use " > /dev/null 2>&1" to suppress output
        os.system(f'git clone --depth 1 --single-branch git@github.com:{repo} /data/github-repos/{file_name}' + ('' if verbose else ' > /dev/null 2>&1'))

with open('github_repositories.csv', 'r') as f:
    csv_reader = csv.reader(f)
    repositories = list(map(tuple, csv_reader))

if not os.path.exists('/data/github-repos/'):
    os.makedirs('/data/github-repos/')


repo_names = [repo[0] for repo in repositories]
Parallel(n_jobs=40, prefer="threads")(
    delayed(download_repo)(name) for name in tqdm(repo_names))