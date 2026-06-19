#!/bin/bash
# AWS SSO login helper
# Usage: aws-login [<environment>]
#
# <environment> is a profile name from ~/.aws/config (bind-mounted from the
# host machine, never tracked in git).
#
# Example ~/.aws/config profiles:
#   [profile main]    <- sso admin on the main account
#   [profile dev]     <- sso admin on the dev account

aws-login() {
    local env="${1:-}"

    if [[ -z "${env}" ]]; then
        echo "Usage: aws-login <environment>"
        echo ""
        echo "Available profiles:"
        aws configure list-profiles | sort
        return 0
    fi

    if [[ ! "${env}" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        echo "Invalid environment name: '${env}'"
        return 1
    fi

    aws sso login --profile "${env}" || return 1

    export AWS_PROFILE="${env}"

    echo ""
    echo "✅ Active environment: ${env}  (AWS_PROFILE=${env})"
    aws sts get-caller-identity
}
