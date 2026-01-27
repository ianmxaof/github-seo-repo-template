# GitHub Directory

This directory contains GitHub-specific configuration and templates.

## Structure

- `workflows/` - GitHub Actions workflows for CI/CD
- `ISSUE_TEMPLATE/` - Issue templates for bug reports and feature requests
- `PULL_REQUEST_TEMPLATE.md` - Template for pull requests

## Workflows

### validate-readme.yml

Validates that README.md follows the recommended structure:
- Checks for H1 title
- Verifies presence of key sections
- Provides warnings for missing recommended sections

**Usage**: Runs automatically on pull requests that modify README.md, or manually via workflow_dispatch.

### lint-metadata.yml

Placeholder workflow for repository metadata validation. Can be extended to:
- Check repository description length
- Validate topic tags
- Ensure proper repository naming conventions

**Usage**: Runs weekly on schedule or manually via workflow_dispatch.

## Customization

When using this template:

1. **Enable workflows**: Uncomment or customize workflows as needed
2. **Add project-specific checks**: Extend workflows with your project's requirements
3. **Update issue templates**: Customize templates for your project's needs
4. **Configure branch protection**: Set up rules that require these checks to pass

## Best Practices

- Keep workflows minimal and focused
- Make validation checks opt-in where possible
- Document what each workflow does
- Test workflows before enforcing them
