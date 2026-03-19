import json
import os

class FullAIAgent:
    def __init__(self, task_type):
        self.task_type = task_type
        self.specialized_prompts = {
            'CODE_REVIEW': 'Please review the following code:',
            'DOCUMENTATION': 'Please provide documentation for the following topic:',
            'SUMMARY': 'Please summarize the following content:',
            'TESTING': 'Please generate tests for the following code:',
            'CUSTOM': 'Please perform the following task:'
        }

    def detect_task(self, task_description):
        # Placeholder for detecting task type based on description
        # For now, return a fixed task type
        return self.task_type

    def analyze_files(self, files):
        results = []
        for file in files:
            results.append(self.process_file(file))
        return results

    def process_file(self, file):
        # Placeholder for file processing logic
        # This can include reading, analyzing, and generating insights
        return f'Processed {file}'

    def split_response(self, response):
        # Split response based on some criteria (e.g., length)
        return response.split('\n')  # Split on new lines

    def generate_prompt(self):
        return self.specialized_prompts.get(self.task_type, self.specialized_prompts['CUSTOM'])

# Example usage:
task_type = 'CODE_REVIEW'
agent = FullAIAgent(task_type)
description = 'Review the following implementation.'
task = agent.detect_task(description)

files = ['script1.py', 'script2.py']
results = agent.analyze_files(files)
response = agent.split_response('This is a response\nSplit me!')

prompt = agent.generate_prompt() 
print(prompt)
print(results)
print(response)