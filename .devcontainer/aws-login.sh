#!/bin/bash
# AWS environment login helper
# Usage: aws-login <environment>
#
# Calls gimme-aws-creds with a pre-configured Okta profile (no interactive role
# selection menu) and exports AWS_PROFILE into the current shell.
#
# Requires ~/.okta_aws_login_config to have a matching named profile with
# aws_rolename set. Example profile:
#
#   [arch-poc]
#   inherits = DEFAULT
#   aws_rolename = arn:aws:iam::303907944320:role/sso-powerusers
#   cred_profile = arch-poc

aws-login() {
    local env="${1:-}"

    if [[ -z "${env}" ]]; then
        echo "Usage: aws-login <environment>"
        echo ""
        echo "Available environments:"
        echo "  arch-poc    hmh-data-arch (303907944320)  role: sso-powerusers"
        echo "  arch-cost   hmh-it (418762722837)         role: sso-cost-monitor"
        echo "  arch-it     hmh-it (418762722837)         role: sso-hmh-it-arch-readonly"
        return 0
    fi

    case "${env}" in
        arch-poc|arch-cost|arch-it) ;;
        *)
            echo "Unknown environment: '${env}'"
            echo "Run 'aws-login' with no arguments to see available environments."
            return 1
            ;;
    esac

    gimme-aws-creds --profile "${env}" || return 1

    export AWS_PROFILE="${env}"

    echo ""
    echo "✅ Active environment: ${env}  (AWS_PROFILE=${env})"
    aws sts get-caller-identity
}
