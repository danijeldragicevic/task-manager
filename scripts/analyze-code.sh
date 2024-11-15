#!/bin/bash

# Ensure the script exits if any command fails
set -e

# Define the instructions to be sent to ChatGPT
INSTRUCTIONS="
Context:
  This code is part of a Flask application that manages tasks stored in a MongoDB database.
  The app provides basic CRUD endpoints for tasks (Create, Read, Update, Delete).
  Here is a code diff that includes changes made to the original code derived from the head branch.

Goal:
  Please review the provided code diff to ensure:
  - Functionality: Does the refactored code work correctly for the described scenarios?
  - Python Best Practices: Is the code clear, maintainable, and consistent with Python and Flask conventions?
  - Error Handling and Edge Cases: Are there any missed scenarios or better ways to manage exceptions?

Diff:"

# Read the PR diff content from the workflow
DIFF_CONTENT=$(cat pr_diff.txt)

# Combine the instructions and the diff content into a single prompt
FULL_PROMPT="$INSTRUCTIONS\n\n$DIFF_CONTENT"
echo "$FULL_PROMPT"

# Create a JSON payload for the OpenAI API request
MESSAGES_JSON=$(jq -n --arg body "$FULL_PROMPT" '[{"role": "user", "content": $body}]')

# Call the OpenAI API to get a response based on the provided prompt
RESPONSE=$(curl -s -X POST "https://api.openai.com/v1/chat/completions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"model\": \"gpt-3.5-turbo\", \"messages\": $MESSAGES_JSON, \"max_tokens\": 500}")

# Extract the summary from the API response
SUMMARY=$(echo "$RESPONSE" | jq -r '.choices[0].message.content')

# Save the extracted summary to a file
echo "$SUMMARY" > summary.txt

# a JSON payload for the GitHub API request to post a comment
comment_body=$(jq -n --arg body "$(cat summary.txt)" '{body: $body}')

# Post the summary as a comment on the pull request using the GitHub API
curl -s -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$comment_body" \
  "https://api.github.com/repos/$REPO/issues/$PR_NUMBER/comments"