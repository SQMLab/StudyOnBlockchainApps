from flask import Flask, jsonify, render_template, request
import csv
import requests
import pandas as pd
import os
import json
from github import Auth
from github import Github
import markdown

app = Flask(__name__)

filtered_repositories_path = "./Data/BlockchainAppRepositories-part1.csv"
repositories_path = "./Data/repository-part1.csv"

ACCESS_TOKEN = json.load(open("./config"))["access_token"]
auth = Auth.Token(ACCESS_TOKEN)
github = Github(auth=auth)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/topics")
def topics():
    return render_template("topics.html")

@app.route("/RepoPreviewer")
def RepoPreviewer():
    return render_template("RepoPreviewer.html")

@app.route("/getRepoList", methods=["GET"])
def get_repo_list():
    try:
        df = pd.read_csv(repositories_path)
        repo_list = df["full_name"].to_list()
        return jsonify(repo_list)
    except:
        return jsonify({"error": "Failed to fetch repos"}), 500

@app.route("/repo/<owner>/<repo_name>", methods=["GET"])
def get_repo(owner, repo_name):
    full_name = owner+"/"+repo_name

    df = pd.read_csv(repositories_path)
    df = df[df["full_name"]==full_name]
    df = df.fillna(" ")
    topics = df["topics"].iloc[0]
    description = df["description"].iloc[0]
    languages = df["language"].iloc[0]
    repo_url = df["repo_url"].iloc[0]

    repo = github.get_repo(full_name)
    readme = ''
    try:
        readme = repo.get_readme().decoded_content.decode()
    except:
        print("Failed to fetch ReadMe")
    

    is_app = False
    
    if os.path.exists(filtered_repositories_path):
        df = pd.read_csv(filtered_repositories_path)
        if full_name in df["full_name"].to_list():
            is_app = True

    return jsonify({
        "Name": owner+"/"+repo_name,
        "RepoUrl": repo_url,
        "Description": description,
        "Topics": topics,
        "Languages": languages,
        "Readme": markdown.markdown(readme),
        "IsApplication": is_app
    })

@app.route("/toggle_repo", methods=["POST"])
def toggle_repo():
    data = request.json
    repo = data.get("repo")
    if not repo:
        return jsonify({"error": "No repo provided"}), 400
    
    df = pd.read_csv(repositories_path)
    new_df = df[df["full_name"] == repo]

    if not os.path.exists(filtered_repositories_path):
        df = new_df
    else:
        df = pd.read_csv(filtered_repositories_path)
        if repo in df["full_name"].to_list():
            df = df[df["full_name"] != repo]
        else:
            df = pd.concat([df, new_df], ignore_index=True, sort=False)

    df.to_csv(filtered_repositories_path, index=False)

    return jsonify({"message": "Updated"})

@app.route("/getIssueList", methods=["GET"])
def get_issue_list():
    csv_filename = request.args.get("csv")
    if not csv_filename:
        return jsonify({"error": "CSV file name not provided"}), 400
    
    csv_path = os.path.join("./Data/Output-BERTopic/Topics", csv_filename)  # Ensure proper path
    if not os.path.exists(csv_path):
        return jsonify({"error": "CSV file not found"}), 404
    
    try:
        df = pd.read_csv(csv_path, dtype=str)
        issue_df =  df[["Repository", "IssueId", "Prob"]]
        issue_df = issue_df.sort_values(by="Prob", ascending=False)
        issues = issue_df.to_dict(orient="records")
        return jsonify(issues)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/getIssue/<filename>/<owner>/<repo>/<int:issue_id>", methods=["GET"])
def get_issue(filename, owner, repo, issue_id):
    try:
        df = pd.read_csv(os.path.join("./Data/Output-BERTopic/Topics", filename))
        issue = df.loc[(df["Repository"] == owner+"/"+repo) & (df["IssueId"] == issue_id)]
        issue = issue.iloc[0]
        return jsonify({
            "title": issue.Title,
            "body": issue.Body or "No description available",
            "comments": ["No comments available"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/getIssueComments/<owner>/<repo>/<int:issue_id>", methods=["GET"])
def get_issue_comments(owner, repo, issue_id):
    try:
        repo_obj = github.get_repo(owner+"/"+repo)
        issue = repo_obj.get_issue(number=issue_id)
        comments = [comment.body for comment in issue.get_comments()]
        
        return jsonify({
            "comments": comments or ["No comments available"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)
