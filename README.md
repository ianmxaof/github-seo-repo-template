# GitHub Account Presentation Optimizer Template

A CLI-first GitHub Account Presentation Optimizer that analyzes all repositories in a GitHub account and scores how clearly they present themselves to humans, while also serving as an SEO-optimized template for developer-facing projects.

## What This Project Provides

This repository contains a **concrete product** and a **reusable template**:

- A **GitHub Account Presentation Optimizer** that:
  - Scans a GitHub account using a Personal Access Token (PAT)
  - Evaluates repo names, descriptions, topics, and READMEs
  - Produces structured, explainable presentation scores (and, later, suggestions)
- An **SEO-focused repository template** that demonstrates:
  - Clear README structure and metadata best practices
  - GitHub Actions workflows for lightweight checks
  - Topic taxonomy guidance for discoverability

## Who This Is For

- Developers who want their GitHub presence to read like a coherent portfolio
- Open-source maintainers who care how projects look to newcomers and sponsors
- Indie hackers and product builders using GitHub as a discovery surface
- Developer tooling authors who want a strong, SEO-aware repo template

## Quick Start (Using the Analyzer)

> Note: The analyzer implementation is evolving toward v0.1. The interface below describes the intended CLI shape.

1. Generate a GitHub Personal Access Token (PAT) with minimal read scopes
2. Export it in your shell: `export GITHUB_TOKEN=ghp_xxx` (or use `--token`)
3. Run the CLI:
   - `gh-visibility scan --user your-username --preset indie-hacker --output table`
4. Inspect the scores and explanations per repository
5. Manually apply any improvements you agree with

See `PRODUCT_INTENT.md` for the detailed product definition and `RULES.md` for hard scope constraints.

### Dashboard (optional)

A read-only web view is in `web/index.html`. Run the CLI with `--output json`, save the output to a file, then open the HTML file and paste the JSON to view scores and suggestions in the browser. No server or GitHub auth in the browser.

### Configuration (PAT-based auth)

- **Token**: Set `GITHUB_TOKEN` in your environment, or pass `--token ghp_xxx` to the CLI.
- **Scopes**: Use a Personal Access Token with minimal read scope:
  - For public repos only: no special scopes (or `public_repo` if needed).
  - For private repos: `repo` scope.
- **Install (development)**: From the repo root, run `pip install -e ".[dev]"` then `gh-visibility scan --user <username>`.

## Using This Repository as a Template

You can also use this repository purely as a **GitHub SEO-optimized template**:

1. Click **“Use this template”** on GitHub to create a new repository
2. Replace the analyzer-specific content with your own project details
3. Follow the README structure guidelines below for your own README
4. Update repository topics and description in GitHub settings
5. Customize `.github/workflows/` for your project’s CI/CD needs

For deeper guidance:

- See `TEMPLATE_USAGE.md` for step-by-step template usage
- See `TOPIC_TAXONOMY.md` for topic selection strategies

## README Structure Guidelines

### Required Sections

Your README should include these sections in order:

1. **H1 Title** - Repository name that matches search intent
2. **First Paragraph** - WHAT + WHO + PLATFORM (one sentence each)
3. **What This [Project] Provides** - Clear value proposition
4. **Who Should Use This** - Target audience
5. **Installation/Getting Started** - How to begin
6. **Usage/Examples** - Practical examples
7. **Configuration** - If applicable
8. **Contributing** - How others can help
9. **License** - Legal information

### SEO Best Practices

- **Repository name**: Use literal, searchable terms (e.g., `vscode-markdown-preview` not `md-preview`)
- **Description**: Include primary keywords in the first 160 characters
- **Topics**: Add 5-10 relevant topics from GitHub's taxonomy
- **Headings**: Use H1 for title, H2 for major sections, H3 for subsections
- **Code examples**: Include real, runnable examples
- **Links**: Link to related projects, documentation, and resources

## Project Philosophy & Scope

This project is intentionally **read-only and advisory-only**:

- It analyzes repository presentation, it does not mutate repositories by default
- It explains *why* something is scored a certain way
- It keeps humans in the loop for all actual changes

Core intent and guardrails are documented in:

- `PRODUCT_INTENT.md` — product intent, non-goals, and philosophy
- `RULES.md` — project rules, scope constraints, and contribution expectations

Any new feature should be checked against these documents before implementation.

## Repository Metadata

### GitHub Topics

Add topics that match your project's:
- **Technology stack** (e.g., `javascript`, `python`, `typescript`)
- **Use case** (e.g., `cli-tool`, `api-wrapper`, `vscode-extension`)
- **Domain** (e.g., `seo`, `developer-tools`, `automation`)
- **Platform** (e.g., `github-action`, `npm-package`, `wordpress-plugin`)

### Repository Description

Keep the description under 160 characters and include:
- Primary keyword
- What it does
- Target platform/ecosystem

Example: `A VS Code extension that provides enhanced Markdown preview with live reload and custom CSS support.`

## CI/CD Structure

The `.github/` directory includes:

- `workflows/` - GitHub Actions workflows for:
  - README structure validation (optional)
  - Metadata linting (optional)
  - Automated checks for best practices

### Workflow Templates

Workflows are provided as templates that you can enable or customize:

- `validate-readme.yml` - Checks README structure and required sections
- `lint-metadata.yml` - Validates repository topics and description

## Customization Guide

### For Plugin Authors

1. Add installation instructions specific to your platform
2. Include screenshots or demos
3. Document configuration options
4. Link to marketplace listings

### For Library Maintainers

1. Add API documentation links
2. Include code examples for common use cases
3. Document version compatibility
4. Link to changelog and migration guides

### For SaaS/Developer Tools

1. Add signup/onboarding links
2. Include pricing information (if applicable)
3. Document API endpoints
4. Link to status page and support

## Next Steps

- **Dogfood**: Run the CLI on your own GitHub account regularly. See [docs/dogfooding.md](docs/dogfooding.md).
- **v0.1 usage**: See [docs/v0.1.md](docs/v0.1.md) for sample output and usage.
- **Monetization**: Only after real usage signal; see [docs/dogfooding.md](docs/dogfooding.md#monetization-only-after-signal).

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request with a clear description

## License

This template is provided under the MIT License. See [LICENSE](LICENSE) for details.

## Related Resources

- [GitHub's Guide to Repository Discovery](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-topics)
- [SEO Best Practices for Open Source Projects](https://opensource.guide/)
- [Writing Great Documentation](https://www.writethedocs.org/guide/)

---

**Note**: This template is designed to evolve. As GitHub introduces new features and SEO best practices emerge, this template will be updated to reflect current recommendations.
