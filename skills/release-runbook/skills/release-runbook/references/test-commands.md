# Test Commands Reference

This document describes common test commands and discovery patterns for various ecosystems.

## Test Discovery Priority

The release script follows this priority order when discovering test commands:

1. **Makefile targets** - `make test`, `make check`
2. **Taskfile tasks** - `task test`
3. **Just recipes** - `just test`
4. **Package.json scripts** - `npm test`, `npm run test`
5. **Language-specific** - pytest, go test, cargo test, etc.
6. **CI/CD detection** - Extract test commands from workflow files

## By Language

### Python

| Command | Description | When Detected |
|---------|-------------|---------------|
| `pytest` | pytest runner | pytest.ini exists, or `tests/` with `test_*.py` |
| `python -m pytest` | pytest as module | Same as above, explicit module |
| `pytest -v` | Verbose pytest | User preference |
| `pytest tests/` | Explicit tests dir | Has tests/ directory |
| `python -m unittest` | unittest runner | No pytest, has unittest tests |
| `python -m unittest discover` | Auto-discover unittest | Has tests/ directory |
| `tox` | Multi-env testing | tox.ini exists |
| `nox` | Modern testing | noxfile.py exists |
| `python setup.py test` | Legacy setup.py | Old-style packages |
| `make test` | Makefile target | Makefile has test target |
| `pytest --cov` | With coverage | Coverage configured |

**Detection Logic:**

```bash
# Check for pytest
if [[ -f "pytest.ini" ]] || \
   [[ -f "pyproject.toml" && grep -q "pytest" pyproject.toml ]] || \
   [[ -f "setup.cfg" && grep -q "pytest" setup.cfg ]] || \
   [[ -d "tests" ]] && find tests -name "test_*.py" -quit | grep -q .; then
    echo "pytest"
fi

# Check for unittest
if [[ -d "tests" ]] && find tests -name "test_*.py" -quit | grep -q .; then
    echo "python -m unittest discover"
fi
```

### Go

| Command | Description | When Detected |
|---------|-------------|---------------|
| `go test ./...` | Test all packages | Always for Go projects |
| `go test -v ./...` | Verbose output | User preference |
| `go test -race ./...` | Race detection | User preference |
| `go test -cover ./...` | With coverage | User preference |
| `go test ./... -run TestFoo` | Specific test | User specified |
| `make test` | Makefile target | Makefile has test target |
| `richgo test ./...` | Rich output | richgo installed |
| `gotestsum ./...` | JUnit output | gotestsum installed |

**Detection Logic:**

```bash
# Go projects almost always have go test
if [[ -f "go.mod" ]] || find . -name "*.go" -quit | grep -q .; then
    echo "go test ./..."
fi
```

### Node.js / TypeScript

| Command | Description | When Detected |
|---------|-------------|---------------|
| `npm test` | Run test script | package.json has test script |
| `npm run test` | Alternative syntax | Same as above |
| `npm t` | Shorthand | Same as above |
| `yarn test` | Yarn projects | yarn.lock exists |
| `pnpm test` | pnpm projects | pnpm-lock.yaml exists |
| `jest` | Direct jest | jest.config.* exists |
| `jest --coverage` | With coverage | Coverage configured |
| `mocha` | Direct mocha | mocha configured |
| `vitest` | Vite test runner | vitest.config.* exists |
| `ts-mocha` | TypeScript mocha | TS + mocha |
| `cypress run` | E2E tests | cypress configured |
| `playwright test` | E2E tests | playwright configured |

**Detection Logic:**

```bash
# Check package.json for test script
if [[ -f "package.json" ]]; then
    if grep -A 10 '"scripts"' package.json | grep -q '"test"'; then
        echo "npm test"
    fi
fi

# Check for specific test runners
if [[ -f "jest.config.js" ]] || [[ -f "jest.config.ts" ]]; then
    echo "jest"
fi
```

### Rust

| Command | Description | When Detected |
|---------|-------------|---------------|
| `cargo test` | Standard test | Always for Rust projects |
| `cargo test --all` | All packages | Workspace projects |
| `cargo test --workspace` | Workspace alternative | Workspace projects |
| `cargo nextest run` | Faster tests | nextest installed |
| `make test` | Makefile target | Makefile has test target |

**Detection Logic:**

```bash
if [[ -f "Cargo.toml" ]] || find . -name "*.rs" -quit | grep -q .; then
    echo "cargo test"
fi
```

### Java

| Command | Description | When Detected |
|---------|-------------|---------------|
| `mvn test` | Maven test | pom.xml exists |
| `mvn verify` | Maven + integration | Has integration tests |
| `mvn clean test` | Clean then test | User preference |
| `gradle test` | Gradle test | build.gradle exists |
| `./gradlew test` | Gradle wrapper | gradlew exists |
| `./gradlew clean test` | Clean then test | User preference |
| `make test` | Makefile target | Makefile has test target |

**Detection Logic:**

```bash
if [[ -f "pom.xml" ]]; then
    echo "mvn test"
elif [[ -f "build.gradle" ]] || [[ -f "build.gradle.kts" ]]; then
    if [[ -f "gradlew" ]]; then
        echo "./gradlew test"
    else
        echo "gradle test"
    fi
fi
```

### .NET (C#, F#)

| Command | Description | When Detected |
|---------|-------------|---------------|
| `dotnet test` | Standard test | *.csproj or *.fsproj exists |
| `dotnet test --no-build` | Without building | Already built |
| `dotnet test -c Release` | Release config | User preference |
| `vstest.console.exe` | Legacy | Old projects |
| `make test` | Makefile target | Makefile has test target |

**Detection Logic:**

```bash
if find . -name "*.csproj" -quit | grep -q . || find . -name "*.fsproj" -quit | grep -q .; then
    echo "dotnet test"
fi
```

### Ruby

| Command | Description | When Detected |
|---------|-------------|---------------|
| `rake test` | Rake test | Rakefile exists |
| `rspec` | RSpec | spec/ exists or .rspec configured |
| `rspec --format documentation` | Verbose RSpec | User preference |
| `ruby test/test_*.rb` | Direct test | Has test/ directory |
| `minitest` | Minitest | test/minitest_suite.rb |
| `cucumber` | Acceptance tests | features/ exists |
| `make test` | Makefile target | Makefile has test target |

**Detection Logic:**

```bash
if [[ -f "Rakefile" ]]; then
    echo "rake test"
elif [[ -d "spec" ]] || [[ -f ".rspec" ]]; then
    echo "rspec"
fi
```

### PHP

| Command | Description | When Detected |
|---------|-------------|---------------|
| `phpunit` | PHPUnit | phpunit.xml exists |
| `./vendor/bin/phpunit` | Local PHPUnit | Has vendor/bin/ |
| `./vendor/bin/pest` | Pest | Pest configured |
| `composer test` | Composer script | composer.json has test script |
| `phpstan` | Static analysis | User preference |
| `psalm` | Static analysis | User preference |
| `make test` | Makefile target | Makefile has test target |

**Detection Logic:**

```bash
if [[ -f "phpunit.xml" ]] || [[ -f "phpunit.xml.dist" ]]; then
    if [[ -f "vendor/bin/phpunit" ]]; then
        echo "./vendor/bin/phpunit"
    else
        echo "phpunit"
    fi
fi
```

## Build System Test Targets

### Makefile

Common test target patterns:

```makefile
# Simple test
test:
    pytest

# Test with coverage
test:
    pytest --cov=src

# Multiple test suites
test: test-unit test-integration

test-unit:
    pytest tests/unit

test-integration:
    pytest tests/integration

# Go test
test:
    go test ./...

# Multi-language
test:
    pytest && go test ./... && npm test
```

**Detection:**

```bash
if grep -q "^test:" Makefile; then
    echo "make test"
fi
```

### Taskfile (Task)

```yaml
# Taskfile.yml
version: '3'

tasks:
  test:
    desc: Run tests
    cmds:
      - pytest

  test:unit:
    desc: Run unit tests
    cmds:
      - pytest tests/unit

  test:integration:
    desc: Run integration tests
    cmds:
      - pytest tests/integration
```

**Detection:**

```bash
if [[ -f "Taskfile.yml" ]] && grep -q "test:" Taskfile.yml; then
    echo "task test"
fi
```

### Just (Justfile)

```just
# Justfile
test:
    pytest

test-unit:
    pytest tests/unit

test-integration:
    pytest tests/integration
```

**Detection:**

```bash
if [[ -f "justfile" ]] && grep -q "^test:" justfile; then
    echo "just test"
fi
```

## CI/CD Test Discovery

Extract test commands from CI/CD configuration files:

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Test

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest                    # Extract this
      - run: go test ./...              # Extract this too
```

**Detection:**

```bash
if grep -r "run:" .github/workflows/ 2>/dev/null | grep -q "test"; then
    grep -r "run:" .github/workflows/ | grep test | sed 's/.*run: *//' | head -1
fi
```

### GitLab CI

```yaml
# .gitlab-ci.yml
test:
  script:
    - pytest                           # Extract this
    - go test ./...
```

### CircleCI

```yaml
# .circleci/config.yml
jobs:
  test:
    steps:
      - run: pytest                    # Extract this
```

## Multi-Language Projects

For projects with multiple languages, run tests sequentially:

```bash
# Combined test command
pytest && go test ./... && npm test

# Or via Makefile
make test:
    @echo "Running Python tests..."
    pytest
    @echo "Running Go tests..."
    go test ./...
    @echo "Running Node tests..."
    npm test
```

## Test Command Shortcuts

| Shortcut | Full Command |
|----------|--------------|
| `npm t` | `npm test` |
| `npm run test` | `npm test` |
| `yarn test` | `yarn test` |
| `pnpm test` | `pnpm test` |
| `make test` | `make test` |
| `just test` | `just test` |
| `task test` | `task test` |

## Custom Test Commands

Override auto-detection with `--test-command`:

```bash
# Run specific test suite
~/.claude/skills/release-runbook/scripts/release.sh \
  --test-command "pytest tests/integration/" \
  --version 1.2.3

# Run with coverage
~/.claude/skills/release-runbook/scripts/release.sh \
  --test-command "pytest --cov=src --cov-report=term-missing" \
  --version 1.2.3

# Run multiple test suites
~/.claude/skills/release-runbook/scripts/release.sh \
  --test-command "pytest && go test ./..." \
  --version 1.2.3
```

## Skip Tests

Skip tests with `--skip-tests` (not recommended for production releases):

```bash
~/.claude/skills/release-runbook/scripts/release.sh \
  --skip-tests \
  --version 1.2.3
```

## Test Exit Codes

Standard exit codes:
- `0` - All tests passed
- `1` - Tests failed
- `2` - Test execution error

The release script exits on any non-zero test result.

## Test Environment Variables

Common environment variables for testing:

| Variable | Purpose |
|----------|---------|
| `CI` | Running in CI |
| `TEST_VERBOSE` | Verbose output |
| `TEST_COVERAGE` | Generate coverage |
| `RUSTFLAGS` | Rust flags (e.g., `-D warnings`) |
| `GOFLAGS` | Go flags |
| `NODE_ENV` | Node environment |

Example:

```bash
# Enable warnings as errors for Go
GOFLAGS="-race -count=1" go test ./...

# Rust with warnings as errors
RUSTFLAGS="-D warnings" cargo test

# Node test environment
NODE_ENV=test npm test
```

## Test Parallelization

For faster test execution:

```bash
# pytest with xdist
pytest -n auto

# Go tests are parallel by package
go test -parallel 4 ./...

# cargo tests are parallel by default
cargo test

# npm run with concurrent
npm-run-all --parallel test:*
```

## Test Docker Integration

Testing in Docker containers:

```makefile
# Makefile
test:
    docker-compose -f docker-compose.test.yml up --abort-on-container-exit

test-python:
    docker run -v $(PWD):/app python:3.11 pytest

test-go:
    docker run -v $(PWD):/app golang:1.21 go test ./...
```

## Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [Go testing](https://go.dev/doc/tutorial/add-a-test)
- [npm test scripts](https://docs.npmjs.com/cli/v9/using-npm/scripts)
- [cargo test](https://doc.rust-lang.org/cargo/commands/cargo-test.html)
- [Maven test](https://maven.apache.org/surefire/maven-surefire-plugin/examples/test.html)
- [Gradle test](https://docs.gradle.org/current/userguide/java_testing.html)
