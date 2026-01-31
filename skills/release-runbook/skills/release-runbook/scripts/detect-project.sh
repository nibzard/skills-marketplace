#!/usr/bin/env bash
#
# detect-project.sh - Auto-detect project type, languages, version files, and test commands
#
# Outputs key=value pairs that can be sourced or parsed
#
# Usage:
#   source <(detect-project.sh)  # Shell mode
#   detect-project.sh            # JSON-like output mode
#

set -euo pipefail

# Color output
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
fi

# Detect function - checks for file existence
detect_file() {
    local file="$1"
    [[ -f "$file" ]]
}

# Detect function - checks for directory existence
detect_dir() {
    local dir="$1"
    [[ -d "$dir" ]]
}

# Output function - prints key=value (with proper quoting for eval)
output() {
    local key="$1"
    local value="${2:-}"
    # Escape single quotes in value and wrap in single quotes for safe eval
    local escaped_value="${value//\'/\'\\\'\'}"
    printf '%s='"'"'%s'"'"'\n' "$key" "$escaped_value"
}

# Main detection
detect_project() {
    local project_dir="${1:-.}"
    cd "$project_dir"

    local languages=()
    local version_files=()
    local build_systems=()
    local test_commands=()
    local package_managers=()

    # --- Language Detection ---

    # Python
    if detect_file "pyproject.toml" || detect_file "setup.py" || detect_file "setup.cfg" || \
       detect_file "requirements.txt" || detect_dir "src" && find . -name "*.py" -quit | grep -q .; then
        languages+=("python")
        if detect_file "pyproject.toml"; then
            version_files+=("pyproject.toml")
        fi
        if detect_file "setup.py"; then
            version_files+=("setup.py")
        fi
        # Look for __version__.py in common locations
        local version_py
        version_py=$(find . -name "__version__.py" -o -name "_version.py" 2>/dev/null | head -1)
        if [[ -n "$version_py" ]]; then
            version_files+=("$version_py")
        fi
    fi

    # Node.js
    if detect_file "package.json" || detect_dir "node_modules" || \
       detect_file "yarn.lock" || detect_file "pnpm-lock.yaml" || detect_file "package-lock.json"; then
        languages+=("node")
        if detect_file "package.json"; then
            version_files+=("package.json")
        fi
        if detect_file "package-lock.json"; then
            build_systems+=("npm")
        elif detect_file "yarn.lock"; then
            build_systems+=("yarn")
        elif detect_file "pnpm-lock.yaml"; then
            build_systems+=("pnpm")
        fi
    fi

    # Go
    if detect_file "go.mod" || detect_file "go.sum" || \
       find . -maxdepth 3 -name "*.go" -quit | grep -q .; then
        languages+=("go")
        if detect_file "go.mod"; then
            # Check if version is in go.mod (as comment)
            if grep -q "version" go.mod 2>/dev/null; then
                version_files+=("go.mod")
            fi
        fi
        # VERSION file is common for Go CLIs
        if detect_file "VERSION"; then
            version_files+=("VERSION")
        fi
    fi

    # Rust
    if detect_file "Cargo.toml" || detect_file "Cargo.lock" || detect_dir ".cargo" || \
       find . -name "*.rs" -quit | grep -q .; then
        languages+=("rust")
        if detect_file "Cargo.toml"; then
            version_files+=("Cargo.toml")
        fi
    fi

    # Java
    if detect_file "pom.xml" || detect_file "build.gradle" || detect_file "build.gradle.kts" || \
       detect_file "gradlew" || detect_dir "src/main/java"; then
        languages+=("java")
        if detect_file "pom.xml"; then
            version_files+=("pom.xml")
            build_systems+=("maven")
        fi
        if detect_file "build.gradle" || detect_file "build.gradle.kts"; then
            version_files+=("build.gradle")
            build_systems+=("gradle")
        fi
    fi

    # .NET
    if find . -name "*.csproj" -quit | grep -q . || \
       find . -name "*.fsproj" -quit | grep -q . || \
       detect_file "Directory.Build.props"; then
        languages+=("dotnet")
        local csproj
        csproj=$(find . -maxdepth 3 -name "*.csproj" -o -name "*.fsproj" 2>/dev/null | head -1)
        if [[ -n "$csproj" ]]; then
            version_files+=("$csproj")
        fi
        if detect_file "Directory.Build.props"; then
            version_files+=("Directory.Build.props")
        fi
    fi

    # Ruby
    if detect_file "Gemfile" || detect_file "*.gemspec" || detect_dir "lib" || \
       detect_file "Rakefile"; then
        languages+=("ruby")
        local gemspec
        gemspec=$(find . -maxdepth 2 -name "*.gemspec" 2>/dev/null | head -1)
        if [[ -n "$gemspec" ]]; then
            version_files+=("$gemspec")
        fi
        if detect_file "lib/version.rb"; then
            version_files+=("lib/version.rb")
        fi
    fi

    # PHP
    if detect_file "composer.json" || detect_file "composer.lock" || \
       detect_dir "vendor" || find . -name "*.php" -quit | grep -q .; then
        languages+=("php")
        if detect_file "composer.json"; then
            version_files+=("composer.json")
        fi
    fi

    # Standalone VERSION file
    if detect_file "VERSION"; then
        # Only add if not already added by Go detection
        if [[ ! " ${version_files[*]} " =~ " VERSION " ]]; then
            version_files+=("VERSION")
        fi
    fi

    # --- Build System Detection ---

    if detect_file "Makefile"; then
        build_systems+=("make")
    fi

    if detect_file "justfile"; then
        build_systems+=("just")
    fi

    if detect_file "Taskfile.yml"; then
        build_systems+=("task")
    fi

    if detect_file "CMakeLists.txt"; then
        build_systems+=("cmake")
    fi

    if detect_file "meson.build"; then
        build_systems+=("meson")
    fi

    # --- Test Command Discovery ---

    # Check Makefile for test target
    if detect_file "Makefile"; then
        if grep -q "^test:" Makefile || grep -q "^.PHONY.*test" Makefile; then
            test_commands+=("make test")
        fi
    fi

    # Check justfile for test recipe
    if detect_file "justfile"; then
        if grep -q "^test:" justfile; then
            test_commands+=("just test")
        fi
    fi

    # Check Taskfile.yml for test task
    if detect_file "Taskfile.yml"; then
        if grep -q "test:" Taskfile.yml; then
            test_commands+=("task test")
        fi
    fi

    # Language-specific test commands
    if [[ " ${languages[*]} " =~ " python " ]]; then
        # Check for pytest first
        if detect_file "pytest.ini" || detect_file "pyproject.toml" && grep -q "pytest" pyproject.toml || \
           detect_file "setup.cfg" && grep -q "pytest" setup.cfg || \
           detect_dir "tests" && find tests -name "test_*.py" -quit | grep -q .; then
            test_commands+=("pytest")
        fi
        # Check for unittest
        if detect_dir "tests" && find tests -name "test_*.py" -quit | grep -q .; then
            test_commands+=("python -m unittest discover")
        fi
    fi

    if [[ " ${languages[*]} " =~ " go " ]]; then
        test_commands+=("go test ./...")
    fi

    if [[ " ${languages[*]} " =~ " node " ]]; then
        if detect_file "package.json"; then
            # Extract test script from package.json
            local test_script
            test_script=$(grep -A 10 '"scripts"' package.json | grep '"test"' | cut -d'"' -f4 || true)
            if [[ -n "$test_script" ]]; then
                test_commands+=("npm test")
            fi
        fi
    fi

    if [[ " ${languages[*]} " =~ " rust " ]]; then
        test_commands+=("cargo test")
    fi

    if [[ " ${languages[*]} " =~ " java " ]]; then
        if detect_file "pom.xml"; then
            test_commands+=("mvn test")
        fi
        if detect_file "build.gradle" || detect_file "build.gradle.kts"; then
            test_commands+=("gradle test")
        fi
    fi

    if [[ " ${languages[*]} " =~ " dotnet " ]]; then
        test_commands+=("dotnet test")
    fi

    if [[ " ${languages[*]} " =~ " ruby " ]]; then
        if detect_file "Rakefile"; then
            test_commands+=("rake test")
        fi
        if detect_file "spec" && find spec -name "*_spec.rb" -quit | grep -q .; then
            test_commands+=("rspec")
        fi
    fi

    if [[ " ${languages[*]} " =~ " php " ]]; then
        if detect_file "phpunit.xml" || detect_dir "tests" && find tests -name "*Test.php" -quit | grep -q .; then
            test_commands+=("phpunit")
        fi
        if detect_file "composer.json" && grep -q "pest" composer.json; then
            test_commands+=("./vendor/bin/pest")
        fi
    fi

    # --- Package Manager Detection ---

    if [[ " ${languages[*]} " =~ " python " ]]; then
        if detect_file "pyproject.toml" && grep -q "\[project\]" pyproject.toml; then
            package_managers+=("pip")
        fi
        if detect_file "setup.py"; then
            package_managers+=("pip")
        fi
    fi

    if [[ " ${languages[*]} " =~ " node " ]]; then
        if detect_file "package.json"; then
            package_managers+=("npm")
        fi
    fi

    if [[ " ${languages[*]} " =~ " rust " ]]; then
        if detect_file "Cargo.toml"; then
            package_managers+=("cargo")
        fi
    fi

    if detect_file "Brewfile" || detect_file ".homebrew" || \
       detect_dir ".github/workflows" && grep -r "homebrew" .github/workflows &>/dev/null; then
        package_managers+=("brew")
    fi

    # --- Determine Project Type ---

    local project_type
    if [[ ${#languages[@]} -eq 0 ]]; then
        project_type="unknown"
    elif [[ ${#languages[@]} -eq 1 ]]; then
        project_type="${languages[0]}"
    else
        project_type="multi"
    fi

    # --- Build Command Discovery ---

    local build_commands=()

    if detect_file "Makefile" && grep -q "^build:" Makefile; then
        build_commands+=("make build")
    fi

    if [[ " ${languages[*]} " =~ " python " ]]; then
        if detect_file "pyproject.toml"; then
            build_commands+=("python -m build")
        fi
        if detect_file "setup.py"; then
            build_commands+=("python setup.py sdist bdist_wheel")
        fi
    fi

    if [[ " ${languages[*]} " =~ " go " ]]; then
        build_commands+=("go build")
    fi

    if [[ " ${languages[*]} " =~ " node " ]]; then
        if detect_file "package.json" && grep -q '"build"' package.json; then
            build_commands+=("npm run build")
        fi
    fi

    if [[ " ${languages[*]} " =~ " rust " ]]; then
        build_commands+=("cargo build --release")
    fi

    if [[ " ${languages[*]} " =~ " java " ]]; then
        if detect_file "pom.xml"; then
            build_commands+=("mvn package")
        fi
        if detect_file "build.gradle" || detect_file "build.gradle.kts"; then
            build_commands+=("gradle build")
        fi
    fi

    if [[ " ${languages[*]} " =~ " dotnet " ]]; then
        build_commands+=("dotnet build")
    fi

    # --- Output Results ---

    # Join arrays with commas
    local languages_str
    local version_files_str
    local build_systems_str
    local test_commands_str
    local package_managers_str
    local build_commands_str

    languages_str=$(IFS=','; echo "${languages[*]}")
    version_files_str=$(IFS=','; echo "${version_files[*]}")
    build_systems_str=$(IFS=','; echo "${build_systems[*]}")
    test_commands_str=$(IFS=','; echo "${test_commands[*]}")
    package_managers_str=$(IFS=','; echo "${package_managers[*]}")
    build_commands_str=$(IFS=','; echo "${build_commands[*]}")

    # Output as key=value pairs
    output "PROJECT_TYPE" "$project_type"
    output "LANGUAGES" "$languages_str"
    output "VERSION_FILES" "$version_files_str"
    output "BUILD_SYSTEMS" "$build_systems_str"
    output "TEST_COMMANDS" "$test_commands_str"
    output "PACKAGE_MANAGERS" "$package_managers_str"
    output "BUILD_COMMANDS" "$build_commands_str"

    # Get current version if possible
    local current_version
    current_version=$(detect_current_version "$version_files_str")
    if [[ -n "$current_version" ]]; then
        output "CURRENT_VERSION" "$current_version"
    fi

    # Get repo info
    if git rev-parse --git-dir &>/dev/null; then
        local branch
        local remote
        local origin_url

        branch=$(git branch --show-current 2>/dev/null || echo "HEAD")
        remote=$(git config --get "branch.${branch}.remote" 2>/dev/null || echo "origin")
        origin_url=$(git remote get-url "$remote" 2>/dev/null || echo "")

        output "GIT_BRANCH" "$branch"
        output "GIT_REMOTE" "$remote"
        output "GIT_ORIGIN_URL" "$origin_url"

        # Extract repo owner/name from URL
        if [[ "$origin_url" =~ github\.com[/:]([^/]+)/(.+)(\.git)?$ ]]; then
            output "GITHUB_REPO" "${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
        fi
    fi
}

# Detect current version from version files
detect_current_version() {
    local version_files="$1"
    IFS=',' read -ra files <<< "$version_files"

    for file in "${files[@]}"; do
        [[ ! -f "$file" ]] && continue

        case "$file" in
            pyproject.toml)
                # Try project.version first, then tool.poetry.version
                grep -E "^version = " "$file" | head -1 | sed -E 's/^version = ["'\'']?([^"'"\'']+)["'\'']?.*/\1/' | grep -v "^version = " || true
                ;;
            package.json)
                grep -E '"version"' "$file" | head -1 | sed -E 's/.*"version":\s*"([^"]+)".*/\1/'
                ;;
            Cargo.toml)
                grep -E '^version = ' "$file" | head -1 | sed -E 's/^version = "(.+)"/\1/'
                ;;
            VERSION)
                cat "$file"
                ;;
            setup.py)
                grep -E "version=" "$file" | head -1 | sed -E "s/.*version=['\"]([^'\"]+)['\"].*/\1/"
                ;;
            go.mod)
                # Go modules don't have versions, but some projects add them as comments
                grep -i "//.*version" "$file" | head -1 | sed -E 's|.*[Vv]ersion[^0-9]*([0-9.]+).*|\1|' | grep -E "^[0-9]"
                ;;
            pom.xml)
                grep -A 1 "<version>" "$file" | head -1 | sed -E 's/.*<version>(.+)<\/version>.*/\1/' | grep -E "^[0-9]"
                ;;
            *.gemspec)
                grep -E "version\s*=" "$file" | head -1 | sed -E "s/.*version\s*=\s*['\"]([^'\"]+)['\"].*/\1/"
                ;;
            composer.json)
                grep -E '"version"' "$file" | head -1 | sed -E 's/.*"version":\s*"([^"]+)".*/\1/'
                ;;
            *)
                # Generic: look for version= or version: patterns
                grep -iE "version[=:]" "$file" 2>/dev/null | head -1 | sed -E 's/.*[Vv]ersion[=:]["'\'']?([0-9]+\.[0-9]+\.[0-9]+)[-a-zA-Z0-9.]*["'\'']?.*/\1/' | grep -E "^[0-9]"
                ;;
        esac | head -1
    done | grep -E "^[0-9]+\.[0-9]" | head -1
}

# Main
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    detect_project "$@"
else
    SOURCING=1
    detect_project "$@"
fi
