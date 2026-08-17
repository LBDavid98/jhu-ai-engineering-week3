# AGENTS.md

## Critical Context

Project requirements, where we are, and punch list: [`PROJECT_SPEC.MD`](PROJECT_SPEC.MD). 

## Rules
1. Requests involving code must be made using the prompts in /Users/davidhook/school/jhu-ai-engineer/week3/docs/prompt_templates.md. If a request to build something comes in a different format, recommend the correct prompt and wait for the user to confirm.
2. After completing a code task, log the completion in `AI_USAGE_LOG.MD`. Record the prompt **verbatim** from [`docs/prompt_templates.md`](docs/prompt_templates.md) or the user’s exact send. Do not paraphrase, summarize, or replace it with a label such as “Template 3 SM1”.
3. Follow instructions rather strictly. If you're told to annotate something specific and you think you need to add something extra, ask first.

## Roles

The user plays three roles in this project:

- **Navigator.** Set the direction and goal. Break work into clear, small steps. Keep the big picture in focus.
- **Reviewer.** Inspect every AI-generated output. Ask: Does this do what was asked? Spot gaps, errors, or drift from intent.
- **Decision-Maker.** Accept, reject, or redirect AI output. Own the final quality of the work. You are always accountable.

