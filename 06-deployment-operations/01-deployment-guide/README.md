# 01-Deployment-Guide Skill

## Objective

This skill produces a step-by-step deployment guide that defines pre-deployment checklists, numbered deployment steps with exact commands, database migration procedures, rollback instructions, and post-deployment verification. It serves as the authoritative deployment reference for operations teams per IEEE 1062.

## Execution Steps

1. Verify `projects/<ProjectName>/<phase>/<document>/HLD.md` and `projects/<ProjectName>/_context/tech_stack.md` exist. Optionally check for `projects/<ProjectName>/<phase>/<document>/Database_Design.md`. Halt if any required file is missing.
2. Invoke `logic.prompt` or trigger the skill. The skill generates pre-deployment checklists, deployment steps, rollback procedures, and post-deployment verification, then writes `projects/<ProjectName>/<phase>/<document>/Deployment_Guide.md`.
3. Review the deployment steps to confirm each step includes exact commands, expected duration, and success criteria.
4. Proceed to `02-runbook` and `03-monitoring-setup` which can run in parallel once this skill completes.

## Quality Reminder

Every deployment step shall include the literal command or action to execute with expected duration. Every deployment guide shall include a recovery decision for each deployment step, including how the operator preserves writes after an irreversible migration. Configuration shall distinguish dev, staging, and production environments explicitly. Flag deployment gaps rather than fabricating operational details.

## Standards

- IEEE 1062 (Software Acquisition)
