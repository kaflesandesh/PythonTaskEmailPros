import json
from transformers import pipeline, T5ForConditionalGeneration, T5Tokenizer

print("Hello Friends!")

import git
import os

# Clone the GitLab repository
repo_url = "https://gitlab.fi.muni.cz/inject/papers/2024-iticse-from-paper-to-platform/logs-2023"
repo_dir = "./team-100"

if not os.path.exists(repo_dir):
    git.Repo.clone_from(repo_url, repo_dir)

