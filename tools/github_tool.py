import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

class GitHubTool:
    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        # Initialize client with token
        self.client = Github(token) if token else None

    def get_repo_details(self, repo_name: str):
        """
        Searches for a repository and returns its details (stars, forks, language).
        """
        if not self.client:
            return {"error": "GitHub Token not found in environment."}
        
        try:
            # If a full path like 'user/repo' is provided, get it directly
            if "/" in repo_name:
                repo = self.client.get_repo(repo_name.strip())
            else:
                # Otherwise, search for the most popular one
                repos = self.client.search_repositories(query=f"{repo_name} language:python")
                if repos.totalCount == 0:
                    return {"error": f"No repository found for '{repo_name}'"}
                repo = repos[0]

            return {
                "full_name": repo.full_name,
                "description": repo.description,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "language": repo.language,
                "url": repo.html_url
            }
        except Exception as e:
            return {"error": f"GitHub API error: {str(e)}"}