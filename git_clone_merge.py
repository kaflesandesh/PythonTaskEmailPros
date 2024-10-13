import git
import os

def git_clone_merge():
    # Clone the GitLab repository
    repo_url = "https://gitlab.fi.muni.cz/inject/papers/2024-iticse-from-paper-to-platform"
    repo_dir ="2024-iticse-from-paper-to-platform"

    if not os.path.exists(repo_dir):
        git.Repo.clone_from(repo_url, repo_dir)


    # Define the folder path containing the subfolders
    main_folder = "2024-iticse-from-paper-to-platform/logs-2023"
    target_file = "emails.jsonl"

    # Output file path/name
    output_file_path = "all_emails.jsonl"

    # Create/open the output file in write mode - 
    with open(output_file_path, 'w') as output_file:
        # Traverse through the main folder and subfolders
        for root, dirs, files in os.walk(main_folder):
            for file in files:
                if file == target_file:
                    file_path = os.path.join(root, file)
                    
                    # Read the content of the file and write it to the output file
                    with open(file_path, 'r') as f:
                        file_content = f.read()
                        # Output_file.write(f"\n--- Content from: {file_path} ---\n")
                        output_file.write(file_content)
                        output_file.write('\n')
