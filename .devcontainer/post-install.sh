#!/bin/bash
set -ex

WORKSPACE_DIR=$(pwd)

append_bashrc_line() {
	local line="$1"
	grep -Fqx "$line" "${HOME}/.bashrc" || echo "$line" >> "${HOME}/.bashrc"
}

##
## Bash aliases
##
append_bashrc_line 'alias ll="ls -alF"'
append_bashrc_line 'alias la="ls -A"'
append_bashrc_line 'alias l="ls -CF"'

# AWS convenience shortcuts
append_bashrc_line 'alias aws-whoami="aws sts get-caller-identity"'

# Source AWS environment login helper (awsl-login function)
append_bashrc_line "source ${WORKSPACE_DIR}/.devcontainer/aws-login.sh"

# Enable AWS CLI tab completion for bash when aws_completer is available.
append_bashrc_line 'if command -v aws_completer >/dev/null 2>&1; then complete -C "$(command -v aws_completer)" aws; fi'

##
## Python / project setup (uv-based)
##
pip install uv
uv sync
uv run pre-commit install

##
## AgentCore CLI (AWS Bedrock AgentCore)
##
npm install -g @aws/agentcore

echo ""
echo "=================================================="
echo "✅ DevContainer setup complete!"
echo "=================================================="
