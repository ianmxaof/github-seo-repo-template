# GitHub Topic Taxonomy Guide

This guide helps you choose the right topics for your repository to maximize discoverability.

## Topic Selection Strategy

Choose 5-10 topics that cover:
1. **Technology stack** (2-3 topics)
2. **Platform/ecosystem** (1-2 topics)
3. **Use case/domain** (2-3 topics)
4. **Project type** (1-2 topics)

## Technology Stack Topics

### Programming Languages
- `javascript`, `typescript`, `python`, `java`, `go`, `rust`, `php`, `ruby`, `swift`, `kotlin`, `csharp`, `cpp`, `c`

### Frameworks & Libraries
- `react`, `vue`, `angular`, `svelte`, `nextjs`, `nuxt`, `express`, `fastapi`, `django`, `flask`, `spring`, `laravel`, `rails`

### Build Tools & Runtimes
- `nodejs`, `deno`, `bun`, `webpack`, `vite`, `rollup`, `esbuild`

## Platform & Ecosystem Topics

### Code Editors & IDEs
- `vscode-extension`, `vim-plugin`, `sublime-text`, `jetbrains-plugin`, `atom-package`

### Package Managers
- `npm-package`, `python-package`, `ruby-gem`, `rust-crate`, `go-module`, `nuget-package`

### CI/CD & DevOps
- `github-action`, `gitlab-ci`, `jenkins-plugin`, `terraform-module`, `ansible-role`, `docker-image`, `kubernetes`

### Content Management
- `wordpress-plugin`, `wordpress-theme`, `drupal-module`, `jekyll-theme`, `hugo-theme`

### Cloud Platforms
- `aws`, `azure`, `gcp`, `vercel`, `netlify`, `cloudflare`

## Use Case & Domain Topics

### Developer Tools
- `developer-tools`, `cli-tool`, `api-wrapper`, `sdk`, `library`, `framework`

### Web Development
- `web-development`, `frontend`, `backend`, `fullstack`, `responsive-design`, `pwa`

### Data & Analytics
- `data-analysis`, `machine-learning`, `ai`, `data-visualization`, `analytics`

### Security
- `security`, `authentication`, `authorization`, `encryption`, `vulnerability-scanner`

### SEO & Marketing
- `seo`, `marketing`, `analytics`, `tracking`, `optimization`

### Automation
- `automation`, `scraping`, `testing`, `monitoring`, `scheduling`

### Documentation
- `documentation`, `docs`, `tutorial`, `guide`, `examples`

## Project Type Topics

### Open Source
- `open-source`, `hacktoberfest`, `first-contributions`

### Templates & Boilerplates
- `template`, `boilerplate`, `starter-kit`, `generator`

### Learning & Education
- `learning`, `tutorial`, `education`, `beginner-friendly`, `examples`

### Utilities
- `utility`, `helper`, `tool`, `script`

## Topic Combinations by Project Type

### VS Code Extension
```
vscode-extension, typescript, developer-tools, markdown, productivity
```

### WordPress Plugin
```
wordpress-plugin, php, seo, marketing, cms
```

### GitHub Action
```
github-action, javascript, ci-cd, automation, devops
```

### NPM Package
```
npm-package, javascript, typescript, utility, developer-tools
```

### CLI Tool
```
cli-tool, python, automation, developer-tools, productivity
```

### React Component Library
```
react, typescript, components, ui, frontend
```

## Best Practices

1. **Be Specific**: Prefer `vscode-extension` over `extension`
2. **Use Official Topics**: GitHub has a taxonomy - use existing topics when possible
3. **Balance Breadth**: Mix general (`developer-tools`) and specific (`vscode-extension`) topics
4. **Avoid Overlap**: Don't use `javascript` and `js` - pick one
5. **Update Regularly**: Add new topics as your project evolves

## Finding Related Topics

1. **Browse Similar Projects**: Check topics used by similar repositories
2. **GitHub Explore**: Visit github.com/topics to discover popular topics
3. **Search Autocomplete**: GitHub suggests topics as you type
4. **Community Standards**: Follow conventions in your ecosystem

## Topic Validation

Before finalizing topics, ask:
- ✅ Would someone searching for this topic find my project?
- ✅ Does this topic accurately describe my project?
- ✅ Is this topic commonly used in my ecosystem?
- ✅ Do I have the right mix of general and specific topics?

## Examples

### Good Topic Sets

**VS Code Markdown Extension:**
```
vscode-extension, markdown, typescript, productivity, developer-tools
```

**WordPress SEO Plugin:**
```
wordpress-plugin, seo, php, marketing, cms, optimization
```

**GitHub Action for Linting:**
```
github-action, linting, ci-cd, automation, code-quality
```

### Poor Topic Sets

**Too Generic:**
```
tool, useful, awesome, cool
```

**Too Specific (Niche):**
```
my-personal-project, internal-tool-v2, test-repo
```

**Overlapping:**
```
javascript, js, node, nodejs, npm
```

## Resources

- [GitHub Topics Documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-topics)
- [GitHub Topics Explorer](https://github.com/topics)
- [Topic Search](https://github.com/search/advanced) - Use "Topic" filter
