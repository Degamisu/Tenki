import os
from flask import Flask, request
import github

app = Flask(__name__)

# Replace with your GitHub App credentials
app_id = '809572'
key_file_path = '.certs/github/kanshabot-key.pem'
with open(os.path.normpath(os.path.expanduser(key_file_path)), 'r') as cert_file:
    app_key = cert_file.read()

@app.route("/", methods=['POST'])
def bot():
    payload = request.json

    # Check if the event is a GitHub PR creation event
    if 'action' in payload and payload['action'] == 'opened' and 'pull_request' in payload:
        owner = payload['repository']['owner']['login']
        repo_name = payload['repository']['name']

        git_connection = github(
            login_or_token=app_key,
            oauth_token=app_key,  # Use the private key directly
            app_id=app_id,
            base_url="https://api.github.com",
        )
        repo = git_connection.get_repo(f"{owner}/{repo_name}")

        issue = repo.get_issue(number=payload['issue']['number'])

    # Comment
    issue.create_comment(f"""Hello! I'm a bot created by `Emi Yamashita` at Degamisu. Thank you for contributing to {repo_name}.
    ---
    In the meantime, check the Wiki to see if your error is documented.""")
    
    return "ok"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
