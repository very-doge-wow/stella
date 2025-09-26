# Automated Release Workflow

This repository uses semantic-release for fully automated releases. Here's how it works:

## Workflow Overview

1. **Developer pushes to `main` branch** → `Release Orchestrator` workflow starts
2. **Tests run in parallel**: `Unittests` and `Linters` workflows execute simultaneously  
3. **GitHub Pages deploys**: Documentation is built and deployed independently
4. **Semantic release waits**: Only runs after **both** test workflows complete successfully
5. **Automated release**: `semantic-release` analyzes commits and if needed:
   - Calculates new version using ALL conventional commit types
   - Creates and pushes git tag
   - Generates and publishes GitHub release with changelog
   - Builds and publishes Docker images with version tags

## Conventional Commit Format

The versioning follows [Conventional Commits](https://www.conventionalcommits.org/) specification completely via semantic-release:

### Version Bumps:
- **Major (1.0.0 → 2.0.0)**: `BREAKING CHANGE:` in body or `!` after type (e.g., `feat!:`)
- **Minor (1.0.0 → 1.1.0)**: `feat:` - New features  
- **Patch (1.0.0 → 1.0.1)**: `fix:`, `perf:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`

### Supported Types (all trigger patch releases unless marked breaking):
- `feat:` - New features (minor)
- `fix:` - Bug fixes  
- `perf:` - Performance improvements
- `docs:` - Documentation changes
- `style:` - Code style/formatting
- `refactor:` - Code refactoring
- `test:` - Test changes
- `chore:` - Maintenance tasks
- `ci:` - CI/CD changes
- `build:` - Build system changes

### Examples:
```
feat: add new chart validation feature
fix: resolve template parsing issue
perf: optimize chart processing speed
docs: update README with new examples
feat!: remove deprecated API endpoints
fix: resolve parsing issue

BREAKING CHANGE: API endpoint structure changed
```

## Workflow Files

### Orchestrator Workflows
- **`.github/workflows/release-orchestrator.yml`** - Main orchestrator for `main` branch pushes
- **`.github/workflows/pr-validation.yml`** - Orchestrator for pull requests

### Reusable Workflows
- **`.github/workflows/unittest.yml`** - Runs Python unit tests with coverage
- **`.github/workflows/lint.yml`** - Runs markdown and Dockerfile linting
- **`.github/workflows/auto-version.yml`** - Uses semantic-release for complete release automation
- **`.github/workflows/docker-build.yml`** - Builds feature branch Docker images (no push)
- **`.github/workflows/github-pages.yml`** - Deploys example documentation to GitHub Pages

### Workflow Dependencies
```
Release Orchestrator (main push):
├── unittests ──┐
├── linters ────┼─→ auto-version-and-release (semantic-release)
└── github-pages

PR Validation (pull requests only):
├── unittests
├── linters  
└── docker-build
```

## Docker Image Tags

- `latest` - Latest stable release (semantic-release)
- `bleeding` - Latest stable release (same as latest, updated on releases)  
- `1.2.3` - Specific version tags (semantic-release)
- `abcd1234-stella-test` - Feature branch builds (PR only, not pushed)

## Manual Release

You can manually trigger workflows in several ways:

1. **Manual versioning**: Go to Actions → "Auto Version and Tag" → "Run workflow"
2. **Manual orchestration**: Go to Actions → "Release Orchestrator" → "Run workflow"
3. **Individual workflows**: Each reusable workflow can be triggered manually for testing

This modular approach makes it easy to test individual components and debug issues.

## Changelog Generation

GitHub releases automatically include categorized changelogs:
- 💥 Breaking Changes
- ✨ Features  
- 🐛 Bug Fixes
- 🔧 Other Changes

## Version Scheme

Simple semantic versioning: `v1.2.3`
- Major: Breaking changes
- Minor: New features
- Patch: Bug fixes and improvements