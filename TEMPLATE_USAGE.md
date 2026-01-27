# Using This Template

This guide explains how to use this repository as a GitHub template and customize it for your project.

## Creating a Repository from This Template

### Method 1: GitHub Web Interface

1. Navigate to this repository on GitHub
2. Click the green "Use this template" button
3. Choose "Create a new repository"
4. Fill in your repository details:
   - **Name**: Use a literal, searchable name (e.g., `vscode-markdown-preview`, `wordpress-seo-plugin`)
   - **Description**: Keep under 160 characters, include primary keyword
   - **Visibility**: Choose public or private
5. Click "Create repository from template"

### Method 2: GitHub CLI

```bash
gh repo create my-new-repo --template owner/github-seo-repo-template --public
cd my-new-repo
```

### Method 3: Manual Clone

```bash
git clone https://github.com/owner/github-seo-repo-template.git my-new-repo
cd my-new-repo
rm -rf .git
git init
git add .
git commit -m "Initial commit from template"
```

## Customization Checklist

After creating your repository, customize these elements:

### 1. README.md

- [ ] Replace template title with your project name
- [ ] Update first paragraph (WHAT + WHO + PLATFORM)
- [ ] Customize "What This Provides" section
- [ ] Define your target audience in "Who Should Use This"
- [ ] Add installation/quick start instructions
- [ ] Include usage examples
- [ ] Add configuration documentation (if applicable)
- [ ] Update license information
- [ ] Add links to your documentation, website, or marketplace

### 2. Repository Settings

- [ ] Set repository description (under 160 characters)
- [ ] Add 5-10 relevant topics (see TOPIC_TAXONOMY.md)
- [ ] Enable "Template repository" if you want others to use yours
- [ ] Configure branch protection rules (optional)
- [ ] Set up repository secrets for CI/CD (if needed)

### 3. GitHub Workflows

- [ ] Review `.github/workflows/validate-readme.yml`
- [ ] Customize or disable workflows as needed
- [ ] Add project-specific CI/CD workflows
- [ ] Test workflows on a test branch

### 4. Additional Files

- [ ] Update `LICENSE` with your license choice
- [ ] Customize `CONTRIBUTING.md` for your project
- [ ] Update issue templates if needed
- [ ] Add project-specific documentation

## SEO Optimization Steps

1. **Repository Name**: Ensure it matches search intent
   - ✅ Good: `vscode-markdown-preview`, `wordpress-seo-plugin`
   - ❌ Bad: `md-preview`, `seo-thing`

2. **Description**: Include primary keyword in first 160 characters
   - Example: `A VS Code extension that provides enhanced Markdown preview with live reload and custom CSS support.`

3. **Topics**: Add 5-10 relevant topics
   - Technology: `javascript`, `typescript`, `python`
   - Platform: `vscode-extension`, `wordpress-plugin`, `github-action`
   - Use case: `developer-tools`, `seo`, `automation`

4. **README Structure**: Follow the template's heading hierarchy
   - H1 for title
   - H2 for major sections
   - H3 for subsections

5. **Content**: Write for zero-context readers
   - Assume readers arrive from search engines
   - Use clear, literal language
   - Include practical examples

## Platform-Specific Customization

### For VS Code Extensions

- Add `vscode-extension` topic
- Include installation instructions from VS Code marketplace
- Add screenshots or animated GIFs
- Link to marketplace listing
- Document configuration options in `.vscode/settings.json`

### For WordPress Plugins

- Add `wordpress-plugin` topic
- Include installation via WordPress admin
- Document hooks and filters
- Add screenshots of admin interface
- Link to WordPress.org plugin directory (if applicable)

### For GitHub Actions

- Add `github-action` topic
- Include action.yml or action.yaml
- Document inputs and outputs
- Provide usage examples in workflows
- Link to GitHub Marketplace (if published)

### For NPM Packages

- Add `npm-package` topic
- Include installation via npm/yarn/pnpm
- Document API/exports
- Add usage examples
- Link to npm package page

## Testing Your Setup

1. **Validate README**: Run the validate-readme workflow
2. **Check Topics**: Ensure topics are relevant and searchable
3. **Test Links**: Verify all links work
4. **Review on Mobile**: Check README readability on mobile
5. **Search Test**: Search for your repository using expected keywords

## Next Steps

- Set up continuous integration for your project
- Add code examples and demos
- Create documentation site (if needed)
- Submit to relevant marketplaces
- Share in developer communities

## Getting Help

- Review the main README.md for structure guidelines
- Check TOPIC_TAXONOMY.md for topic suggestions
- Open an issue in this template repository for questions
