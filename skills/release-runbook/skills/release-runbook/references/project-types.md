# Project Types Reference

This document describes version file patterns, bump methods, and test commands for various ecosystems.

## Python

### Version Files

| File | Format | Priority |
|------|--------|----------|
| `pyproject.toml` | `version = "1.2.3"` under `[project]` or `[tool.poetry]` | 1 |
| `setup.py` | `version="1.2.3"` in setup() call | 2 |
| `setup.cfg` | `version = 1.2.3` under `[metadata]` | 3 |
| `__version__.py` | `__version__ = "1.2.3"` | 4 |
| `_version.py` | `__version__ = "1.2.3"` | 5 |
| `VERSION` | Just the version string | 6 |

### Bump Methods

**Manual:**
```bash
# Edit pyproject.toml directly
sed -i 's/^version = .*/version = "1.2.3"/' pyproject.toml

# Using bump2version
pip install bump2version
bump2version minor  # bumps 1.0.0 -> 1.1.0

# Using bump-my-version
pip install bump-my-version
bump-my-version bump minor
```

### Test Commands

| Command | When Used |
|---------|-----------|
| `pytest` | Has pytest.ini, tests/, or pyproject.toml with pytest config |
| `python -m pytest` | Same as above but explicit |
| `python -m unittest discover` | Has tests/ with unittest tests |
| `tox` | Has tox.ini |
| `make test` | Has Makefile with test target |

### Build Commands

| Command | When Used |
|---------|-----------|
| `python -m build` | Modern Python packaging (pyproject.toml) |
| `python setup.py sdist bdist_wheel` | Legacy setup.py |
| `poetry build` | Poetry projects |

### Publish Commands

```bash
# PyPI
python -m build
twine upload dist/*

# Poetry
poetry publish

# Flit
flit publish
```

---

## Node.js / TypeScript

### Version Files

| File | Format | Priority |
|------|--------|----------|
| `package.json` | `"version": "1.2.3"` | 1 |
| `lerna.json` | `"version": "1.2.3"` (monorepo) | 2 |

### Bump Methods

**Using npm:**
```bash
npm version major   # 1.0.0 -> 2.0.0
npm version minor   # 1.0.0 -> 1.1.0
npm version patch   # 1.0.0 -> 1.0.1

# With pre-release
npm version premajor    # 1.0.0 -> 2.0.0-0
npm version preminor    # 1.0.0 -> 1.1.0-0
npm version prepatch    # 1.0.0 -> 1.0.1-0
npm version prerelease  # 1.0.0-0 -> 1.0.0-1
```

**Using yarn:**
```bash
yarn version --major
yarn version --minor
yarn version --patch
```

**Using pnpm:**
```bash
pnpm version major
pnpm version minor
pnpm version patch
```

**Manual (jq):**
```bash
jq '.version = "1.2.3"' package.json > package.json.tmp && mv package.json.tmp package.json
```

### Test Commands

| Command | When Used |
|---------|-----------|
| `npm test` | package.json has test script |
| `npm run test` | Alternative test script call |
| `yarn test` | Yarn projects |
| `pnpm test` | pnpm projects |
| `jest` | Direct jest |
| `mocha` | Direct mocha |
| `vitest` | Vitest projects |

### Build Commands

| Command | When Used |
|---------|-----------|
| `npm run build` | Has build script |
| `tsc` | TypeScript projects |
| `webpack` | Webpack bundler |
| `vite build` | Vite projects |
| `next build` | Next.js projects |

### Publish Commands

```bash
# npm
npm publish

# yarn
yarn publish

# pnpm
pnpm publish

# With OTP
npm publish --otp 123456
```

---

## Go

### Version Files

| File | Format | Priority |
|------|--------|----------|
| `VERSION` | Just the version string | 1 |
| `go.mod` | Version as comment | 2 |
| `cmd/*/version.go` | `var Version = "1.2.3"` | 3 |

### Bump Methods

**Manual:**
```bash
# Update VERSION file
echo "1.2.3" > VERSION

# Update version.go
sed -i 's/var Version = .*/var Version = "1.2.3"/' cmd/myapp/version.go
```

**Using gopkgs:**
```bash
go install github.com/psampaz/go-mod-version@latest
go-mod-version bump minor
```

### Test Commands

| Command | When Used |
|---------|-----------|
| `go test ./...` | Standard Go testing |
| `go test -v ./...` | Verbose output |
| `go test -race ./...` | Race detection |
| `go test -cover ./...` | With coverage |
| `make test` | Has Makefile with test target |

### Build Commands

| Command | When Used |
|---------|-----------|
| `go build` | Simple build |
| `go build ./cmd/myapp` | Build specific binary |
| `go build -o myapp ./cmd/myapp` | With output name |
| `go build -ldflags "-X main.Version=1.2.3"` | With version injected |

### Version Injection Pattern

```go
// main.go
package main

var (
    Version   = "dev"
    Commit    = "unknown"
    BuildTime = "unknown"
)

func main() {
    if flagVersion {
        fmt.Printf("version %s (commit %s, built at %s)\n", Version, Commit, BuildTime)
        os.Exit(0)
    }
}
```

Build with:
```bash
go build -ldflags \
  "-X main.Version=$(git describe --tags --always) \
   -X main.Commit=$(git rev-parse HEAD) \
   -X main.BuildTime=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

---

## Rust

### Version Files

| File | Format | Priority |
|------|--------|----------|
| `Cargo.toml` | `version = "1.2.3"` | 1 |

### Bump Methods

**Using cargo-edit:**
```bash
cargo install cargo-edit
cargo bump minor  # 1.0.0 -> 1.1.0
cargo bump major
cargo bump patch
cargo bump 1.2.3  # specific version

# With beta
cargo bump minor --beta
```

**Manual:**
```bash
sed -i 's/^version = .*/version = "1.2.3"/' Cargo.toml
```

### Test Commands

| Command | When Used |
|---------|-----------|
| `cargo test` | Standard Rust testing |
| `cargo test --all` | Test all packages (workspace) |
| `cargo test --workspace` | Workspace testing |
| `cargo nextest run` | Using nextest |

### Build Commands

| Command | When Used |
|---------|-----------|
| `cargo build --release` | Release build |
| `cargo build` | Debug build |

### Publish Commands

```bash
# crates.io
cargo publish

# Dry run first
cargo publish --dry-run

# With registry token
cargo publish --token $CRATES_IO_TOKEN
```

---

## Java

### Version Files

| File | Format | Priority |
|------|--------|----------|
| `pom.xml` | `<version>1.2.3</version>` | 1 |
| `build.gradle` | `version = "1.2.3"` | 2 |
| `build.gradle.kts` | `version = "1.2.3"` | 3 |
| `gradle.properties` | `version=1.2.3` | 4 |

### Bump Methods

**Maven (pom.xml):**
```bash
# Using Maven Versions Plugin
mvn versions:set -DnewVersion=1.2.3

# Manual
sed -i 's|<version>.*</version>|<version>1.2.3</version>|g' pom.xml
```

**Gradle (build.gradle):**
```bash
# Update gradle.properties
echo "version=1.2.3" > gradle.properties
```

### Test Commands

| Command | When Used |
|---------|-----------|
| `mvn test` | Maven projects |
| `gradle test` | Gradle projects |
| `./gradlew test` | Gradle wrapper |
| `mvn verify` | Maven with integration tests |

### Build Commands

| Command | When Used |
|---------|-----------|
| `mvn package` | Maven |
| `mvn clean package` | Maven clean build |
| `gradle build` | Gradle |
| `./gradlew build` | Gradle wrapper |

---

## .NET (C#, F#)

### Version Files

| File | Format | Priority |
|------|--------|----------|
| `*.csproj` | `<Version>1.2.3</Version>` | 1 |
| `*.fsproj` | `<Version>1.2.3</Version>` | 2 |
| `Directory.Build.props` | `<Version>1.2.3</Version>` | 3 |

### Bump Methods

**Manual:**
```bash
# Update .csproj
sed -i 's|<Version>.*</Version>|<Version>1.2.3</Version>|g' MyProject.csproj

# Update Directory.Build.props
sed -i 's|<Version>.*</Version>|<Version>1.2.3</Version>|g' Directory.Build.props
```

**Using NerdBank.GitVersioning:**
```xml
<PackageReference Include="Nerdbank.GitVersioning" Version="3.6.133" />
```

### Test Commands

| Command | When Used |
|---------|-----------|
| `dotnet test` | Standard |
| `dotnet test --no-build` | Without building |
| `vstest.console.exe` | Legacy |

### Build Commands

| Command | When Used |
|---------|-----------|
| `dotnet build` | Standard |
| `dotnet build -c Release` | Release configuration |
| `msbuild MyProject.sln` | MSBuild |

---

## Ruby

### Version Files

| File | Format | Priority |
|------|--------|----------|
| `*.gemspec` | `s.version = "1.2.3"` | 1 |
| `lib/version.rb` | `VERSION = "1.2.3"` | 2 |
| `lib/*_version.rb` | `VERSION = "1.2.3"` | 3 |
| `VERSION` | Just the version string | 4 |

### Bump Methods

**Manual:**
```bash
# Update gemspec
sed -i "s|s.version.*=.*|s.version = '$VERSION'|g" mygem.gemspec

# Update version.rb
sed -i "s|VERSION.*=.*|VERSION = '$VERSION'|" lib/version.rb
```

### Test Commands

| Command | When Used |
|---------|-----------|
| `rake test` | Rake-based |
| `rspec` | RSpec |
| `minitest` | Minitest |

### Build Commands

| Command | When Used |
|---------|-----------|
| `gem build mygem.gemspec` | Build gem |
| `rake build` | Rake build task |

### Publish Commands

```bash
# RubyGems
gem build mygem.gemspec
gem push mygem-1.2.3.gem

# With credentials
gem push mygem-1.2.3.gem --key $RUBYGEMS_API_KEY
```

---

## PHP

### Version Files

| File | Format | Priority |
|------|--------|----------|
| `composer.json` | `"version": "1.2.3"` | 1 |
| `VERSION` | Just the version string | 2 |

### Bump Methods

**Manual:**
```bash
# Update composer.json
jq '.version = "1.2.3"' composer.json > composer.json.tmp && mv composer.json.tmp composer.json
```

### Test Commands

| Command | When Used |
|---------|-----------|
| `phpunit` | PHPUnit |
| `./vendor/bin/phpunit` | PHPUnit local |
| `./vendor/bin/pest` | Pest |
| `composer test` | Composer script |

### Build Commands

| Command | When Used |
|---------|-----------|
| `composer install` | Install dependencies |
| `composer dump-autoload` | Regenerate autoloader |

---

## Multi-Language Projects

### Strategy

For projects with multiple languages:

1. **Single Source of Truth**: Use a `VERSION` file as the primary version reference
2. **Synchronized Updates**: Update all version files atomically
3. **Unified Tagging**: Single git tag for all components
4. **Testing**: Run tests for all language components
5. **Building**: Build all artifacts before release

### Version File Priority

1. `VERSION` - Source of truth
2. Language-specific files (pyproject.toml, package.json, etc.)

### Example Structure

```
myproject/
├── VERSION              # Source of truth: "1.2.3"
├── pyproject.toml       # Synced from VERSION
├── package.json         # Synced from VERSION
├── go.mod              # May reference VERSION in comments
└── Makefile            # Orchestrates multi-language build
```

### Makefile Example

```makefile
VERSION := $(shell cat VERSION)

# Update all version files from VERSION file
sync-version:
    sed -i 's/^version = .*/version = "$(VERSION)"/' pyproject.toml
    jq '.version = "$(VERSION)"' package.json > package.json.tmp && mv package.json.tmp package.json

# Run all tests
test:
    pytest
    go test ./...
    npm test

# Build all artifacts
build:
    python -m build
    go build -o bin/myapp ./cmd/myapp
    npm run build

# Release
release: sync-version test build
    git add -A
    git commit -m "chore: release v$(VERSION)"
    git tag -a v$(VERSION) -m "Release v$(VERSION)"
    git push origin main --tags
```

---

## Docker

### Version Files

| File | Format | Priority |
|------|--------|----------|
| `VERSION` | Just the version string | 1 |
| `Dockerfile` | `ARG VERSION=1.2.3` | 2 |

### Build Commands

```bash
# Build with version
docker build --build-arg VERSION=1.2.3 -t myapp:1.2.3 .

# Tag as latest
docker tag myapp:1.2.3 myapp:latest

# Push to registry
docker push myregistry/myapp:1.2.3
docker push myregistry/myapp:latest
```

---

## Version Format Standards

### Semantic Versioning (SemVer)

Format: `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible functionality
- **PATCH**: Backward-compatible bug fixes
- **PRERELEASE**: `alpha`, `beta`, `rc.1`, etc.
- **BUILD**: Build metadata (ignored for ordering)

Examples:
- `1.0.0` - First stable release
- `1.2.3` - Stable release
- `2.0.0-alpha` - Alpha version of 2.0.0
- `2.0.0-beta.1` - First beta
- `2.0.0-rc.1` - First release candidate
- `2.0.0-rc.2` - Second release candidate

### Calendar Versioning (CalVer)

Format: `YYYY.MM.DD` or `YYYY.MM`

Examples:
- `2024.01.15` - January 15, 2024
- `2024.01` - January 2024

---

## Detection Patterns

### Language Indicators

| Language | Files/Directories |
|----------|-------------------|
| Python | `*.py`, `pyproject.toml`, `setup.py`, `requirements.txt`, `tests/` |
| Node.js | `*.js`, `*.ts`, `package.json`, `node_modules/`, `*.lock` |
| Go | `*.go`, `go.mod`, `go.sum` |
| Rust | `*.rs`, `Cargo.toml`, `Cargo.lock` |
| Java | `*.java`, `pom.xml`, `build.gradle`, `src/main/java/` |
| .NET | `*.cs`, `*.csproj`, `*.fs`, `*.fsproj` |
| Ruby | `*.rb`, `Gemfile`, `*.gemspec`, `Rakefile` |
| PHP | `*.php`, `composer.json`, `vendor/` |

### Build System Indicators

| Build System | Files |
|--------------|-------|
| Make | `Makefile` |
| Just | `justfile` |
| Task | `Taskfile.yml` |
| CMake | `CMakeLists.txt` |
| Meson | `meson.build` |
| Ninja | `*.ninja` |

### Package Manager Indicators

| Manager | Files |
|---------|-------|
| pip | `pyproject.toml`, `setup.py`, `requirements.txt` |
| npm | `package.json`, `package-lock.json` |
| yarn | `yarn.lock` |
| pnpm | `pnpm-lock.yaml` |
| cargo | `Cargo.toml` |
| maven | `pom.xml` |
| gradle | `build.gradle` |
| composer | `composer.json` |
| brew | `Brewfile`, `.github/workflows/*.yml` (with brew) |

---

## Testing Strategies by Ecosystem

### Python

- `pytest` for most projects
- `unittest` for standard library projects
- `tox` for multi-environment testing
- `nox` for modern session management

### Node.js

- `jest` for JavaScript/TypeScript
- `mocha` + `chai` for older projects
- `vitest` for Vite projects
- `ava` for fast testing

### Go

- `go test` standard
- `testify` for assertions
- `gomock` for mocking

### Rust

- `cargo test` built-in
- `tokio-test` for async

### Java

- JUnit for unit tests
- TestNG for alternative
- Mockito for mocking

### Ruby

- RSpec for behavior-driven
- Minitest for standard library

### PHP

- PHPUnit for most projects
- Pest for modern syntax

---

## CI/CD Integration

### GitHub Actions

Release workflow:
```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: make test
      - name: Build
        run: make build
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            dist/*
            bin/*
```

### GitLab CI

```yaml
release:
  stage: release
  script:
    - make test
    - make build
    - gh release create $CI_COMMIT_TAG
  only:
    - tags
```

---

## Additional Resources

- [Semantic Versioning 2.0.0](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [How to Publish a Python Package](https://realpython.com/pypi-publish-python-package/)
- [npm Publishing](https://docs.npmjs.com/cli/v9/commands/npm-publish)
