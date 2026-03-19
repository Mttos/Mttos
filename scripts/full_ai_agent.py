import os
import openai
import transformers
import requests

# Function to read issues from a GitHub repository
def read_issues(repo_owner, repo_name):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'
    response = requests.get(url)
    return response.json()

# Function to analyze files in the repository
def analyze_files(repo_path):
    files_data = {}
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            with open(os.path.join(root, file), 'r') as f:
                files_data[file] = f.read()
    return files_data

# Function to generate responses using Hugging Face transformers
def generate_response(prompt):
    model = transformers.AutoModelForCausalLM.from_pretrained('gpt2')
    tokenizer = transformers.AutoTokenizer.from_pretrained('gpt2')
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=150)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example usage of the functions
def main():
    repo_owner = 'Mttos'
    repo_name = 'Mttos'
    issues = read_issues(repo_owner, repo_name)
    print("Issues:", issues)
    # You would also provide the repo path to analyze files
    # repo_path = './path_to_repo'
    # files_data = analyze_files(repo_path)
    # print("Files Data:", files_data)
    prompt = "Write a short summary of the current issues in the repository."
    response = generate_response(prompt)
    print("Generated Response:", response)

if __name__ == '__main__':
    main()