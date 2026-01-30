#!/usr/bin/env bash
#
# init-versioning.sh - Initialize versioning for projects that lack it
#
# Usage:
#   init-versioning.sh [--version VERSION] [--type TYPE] [--dry-run]
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

log_info() {
    echo -e "${BLUE}[i]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[!]${NC} $*"
}

log_error() {
    echo -e "${RED}[✗]${NC} $*"
}

# Default values
VERSION="${VERSION:-0.1.0}"
PROJECT_TYPE=""
DRY_RUN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --version|-v)
            VERSION="$2"
            shift 2
            ;;
        --type|-t)
            PROJECT_TYPE="$2"
            shift 2
            ;;
        --dry-run|-n)
            DRY_RUN=true
            shift
            ;;
        --help|-h)
            cat <<EOF
init-versioning.sh - Initialize versioning for projects

USAGE:
    init-versioning.sh [OPTIONS]

OPTIONS:
    --version, -v VERSION    Starting version (default: 0.1.0)
    --type, -t TYPE          Project type (auto-detected if omitted)
    --dry-run, -n            Show what would be done without making changes
    --help, -h               Show this help

EXAMPLES:
    init-versioning.sh --version 1.0.0
    init-versioning.sh --type python
    init-versioning.sh --dry-run

SUPPORTED TYPES:
    python, go, node, rust, java, dotnet, ruby, php, multi
EOF
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run detect-project to get project info
DETECT_OUTPUT=$(bash ~/.claude/skills/release-runbook/scripts/detect-project.sh)
eval "$DETECT_OUTPUT"

if [[ -z "$PROJECT_TYPE" ]]; then
    PROJECT_TYPE="$PROJECT_TYPE"
fi

if [[ "$PROJECT_TYPE" == "unknown" ]]; then
    log_error "Could not detect project type. Please specify with --type."
    exit 1
fi

log_info "Project type: $PROJECT_TYPE"
log_info "Languages: $LANGUAGES"
log_info "Initializing version: $VERSION"

# Validate version format (SemVer)
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$ ]]; then
    log_error "Invalid version format: $VERSION (expected SemVer like 1.2.3)"
    exit 1
fi

# Function to create file with content
create_file() {
    local file="$1"
    local content="$2"
    local backup="$file.bak"

    if [[ -f "$file" ]]; then
        log_warn "File $file already exists, backing up to $backup"
        if [[ "$DRY_RUN" == false ]]; then
            cp "$file" "$backup"
        fi
    fi

    log_info "Creating $file"
    if [[ "$DRY_RUN" == false ]]; then
        echo "$content" > "$file"
        log_success "Created $file"
    else
        echo "    Content:"
        echo "$content" | sed 's/^/    /'
    fi
}

# Function to append to file
append_to_file() {
    local file="$1"
    local content="$2"

    if [[ -f "$file" ]]; then
        # Check if content already exists
        if grep -qF "$(echo "$content" | head -1)" "$file"; then
            log_info "Content already exists in $file, skipping"
            return
        fi
        log_info "Appending to $file"
        if [[ "$DRY_RUN" == false ]]; then
            echo "" >> "$file"
            echo "$content" >> "$file"
            log_success "Appended to $file"
        else
            echo "    Content to append:"
            echo "$content" | sed 's/^/    /'
        fi
    fi
}

# Initialize Python versioning
init_python() {
    # Check for pyproject.toml
    if [[ -f "pyproject.toml" ]]; then
        log_info "Found pyproject.toml, ensuring version is set"
        if [[ "$DRY_RUN" == false ]]; then
            if grep -q "^version = " pyproject.toml; then
                sed -i "s/^version = .*/version = \"$VERSION\"/" pyproject.toml
            else
                # Add version after [project] section
                sed -i "/^\[project\]/a version = \"$VERSION\"" pyproject.toml
            fi
            log_success "Updated pyproject.toml"
        fi
    else
        log_info "Creating pyproject.toml"
        create_file "pyproject.toml" "[project]
name = \"$(basename "$(pwd)")\"
version = \"$VERSION\"
description = \"\"
readme = \"README.md\"
requires-python = \">=3.8\"
dependencies = []
"
    fi

    # Create __init__.py with version if src layout
    if [[ -d "src/$(basename "$(pwd)")" ]]; then
        local pkg_dir="src/$(basename "$(pwd)")"
        mkdir -p "$pkg_dir"
        create_file "$pkg_dir/__init__.py" "\"\"\"$(basename "$(pwd)")\"\"\n\n__version__ = \"$VERSION\"\n"
    fi

    # Create __version__.py
    create_file "$(basename "$(pwd)")/_version.py" "\"\"\"Version information.\"\"\"\n\n__version__ = \"$VERSION\"\n"

    log_info "Python version: $VERSION"
}

# Initialize Go versioning
init_go() {
    create_file "VERSION" "$VERSION"

    # If go.mod exists, add version comment
    if [[ -f "go.mod" ]]; then
        if ! grep -q "version" go.mod; then
            log_info "Adding version comment to go.mod"
            if [[ "$DRY_RUN" == false ]]; then
                echo "" >> go.mod
                echo "// version is the version of the binary" >> go.mod
                echo "const version = \"$VERSION\"" >> go.mod
                log_success "Added version to go.mod"
            fi
        fi
    fi

    # Create cmd/version.go if it doesn't exist
    local cmd_dir="cmd"
    if [[ -d "cmd" ]]; then
        # Find main package
        local main_file
        main_file=$(find cmd -name "main.go" 2>/dev/null | head -1)
        if [[ -n "$main_file" ]]; then
            local main_dir
            main_dir=$(dirname "$main_file")
            if [[ ! -f "$main_dir/version.go" ]]; then
                create_file "$main_dir/version.go" "package main

var Version = \"$VERSION\"
"
            fi
        fi
    fi

    log_info "Go version: $VERSION"
}

# Initialize Node.js versioning
init_node() {
    if [[ -f "package.json" ]]; then
        log_info "Found package.json, ensuring version is set"
        if [[ "$DRY_RUN" == false ]]; then
            # Update version in package.json
            if command -v jq &>/dev/null; then
                jq ".version = \"$VERSION\"" package.json > package.json.tmp && mv package.json.tmp package.json
            else
                # Fallback to sed
                sed -i "s/\"version\":\s*\"[^\"]*\"/\"version\": \"$VERSION\"/" package.json
            fi
            log_success "Updated package.json"
        fi
    else
        log_info "Creating package.json"
        create_file "package.json" "{
  \"name\": \"$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')\",
  \"version\": \"$VERSION\",
  \"description\": \"\",
  \"main\": \"index.js\",
  \"scripts\": {
    \"test\": \"echo \\\"Error: no test specified\\\" && exit 1\"
  },
  \"keywords\": [],
  \"author\": \"\",
  \"license\": \"MIT\"
}
"
    fi

    log_info "Node.js version: $VERSION"
}

# Initialize Rust versioning
init_rust() {
    if [[ -f "Cargo.toml" ]]; then
        log_info "Found Cargo.toml, ensuring version is set"
        if [[ "$DRY_RUN" == false ]]; then
            sed -i "s/^version = .*/version = \"$VERSION\"/" Cargo.toml
            log_success "Updated Cargo.toml"
        fi
    else
        log_info "Creating Cargo.toml"
        create_file "Cargo.toml" "[package]
name = \"$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')\"
version = \"$VERSION\"
edition = \"2021\"

[dependencies]
"
    fi

    log_info "Rust version: $VERSION"
}

# Initialize Java versioning
init_java() {
    if [[ -f "pom.xml" ]]; then
        log_info "Found pom.xml, ensuring version is set"
        if [[ "$DRY_RUN" == false ]]; then
            # Update version in pom.xml
            sed -i "s|<version>.*</version>|<version>$VERSION</version>|g" pom.xml
            log_success "Updated pom.xml"
        fi
    elif [[ -f "build.gradle" || -f "build.gradle.kts" ]]; then
        log_info "Found Gradle build file, ensure version is set"
        local gradle_file="build.gradle"
        [[ -f "build.gradle.kts" ]] && gradle_file="build.gradle.kts"
        log_warn "Please manually set version in $gradle_file"
    else
        log_info "Creating pom.xml"
        create_file "pom.xml" "<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<project xmlns=\"http://maven.apache.org/POM/4.0.0\"
         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"
         xsi:schemaLocation=\"http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd\">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]')</artifactId>
    <version>$VERSION</version>
    <packaging>jar</packaging>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
</project>
"
    fi

    log_info "Java version: $VERSION"
}

# Initialize .NET versioning
init_dotnet() {
    local csproj
    csproj=$(find . -maxdepth 3 -name "*.csproj" 2>/dev/null | head -1)

    if [[ -n "$csproj" ]]; then
        log_info "Found $csproj, ensuring version is set"
        if [[ "$DRY_RUN" == false ]]; then
            if grep -q "<Version>" "$csproj"; then
                sed -i "s|<Version>.*</Version>|<Version>$VERSION</Version>|g" "$csproj"
            elif grep -q "<VersionPrefix>" "$csproj"; then
                sed -i "s|<VersionPrefix>.*</VersionPrefix>|<VersionPrefix>$VERSION</VersionPrefix>|g" "$csproj"
            else
                # Add Version property to first PropertyGroup
                sed -i "0,/<PropertyGroup>/s/<PropertyGroup>/<PropertyGroup>\n    <Version>$VERSION<\/Version>/" "$csproj"
            fi
            log_success "Updated $csproj"
        fi
    else
        log_warn "No .csproj file found. Please create one manually."
    fi

    log_info ".NET version: $VERSION"
}

# Initialize Ruby versioning
init_ruby() {
    local gemspec
    gemspec=$(find . -maxdepth 2 -name "*.gemspec" 2>/dev/null | head -1)

    if [[ -n "$gemspec" ]]; then
        log_info "Found $gemspec, ensuring version is set"
        if [[ "$DRY_RUN" == false ]]; then
            sed -i "s|s.version.*=.*|s.version = '$VERSION'|g" "$gemspec"
            log_success "Updated $gemspec"
        fi
    else
        log_info "Creating lib/version.rb"
        mkdir -p lib
        create_file "lib/version.rb" "# frozen_string_literal: true

module $(basename "$(pwd)" | sed 's/./\u&/')
  VERSION = '$VERSION'
end
"
    fi

    log_info "Ruby version: $VERSION"
}

# Initialize PHP versioning
init_php() {
    if [[ -f "composer.json" ]]; then
        log_info "Found composer.json, ensuring version is set"
        if [[ "$DRY_RUN" == false ]]; then
            if command -v jq &>/dev/null; then
                jq ".version = \"$VERSION\"" composer.json > composer.json.tmp && mv composer.json.tmp composer.json
            else
                # Check if version key exists
                if grep -q '"version"' composer.json; then
                    sed -i "s/\"version\":\s*\"[^\"]*\"/\"version\": \"$VERSION\"/" composer.json
                fi
            fi
            log_success "Updated composer.json"
        fi
    else
        log_info "Creating composer.json"
        create_file "composer.json" "{
    \"name\": \"$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')/package\",
    \"description\": \"\",
    \"type\": \"library\",
    \"version\": \"$VERSION\",
    \"require\": {
        \"php\": \">=8.0\"
    },
    \"autoload\": {
        \"psr-4\": {
            \"App\\\\\": \"src/\"
        }
    }
}
"
    fi

    log_info "PHP version: $VERSION"
}

# Initialize multi-language versioning
init_multi() {
    # Create VERSION file as source of truth
    create_file "VERSION" "$VERSION"

    # Also initialize for each language detected
    IFS=',' read -ra LANGS <<< "$LANGUAGES"
    for lang in "${LANGS[@]}"; do
        case "$lang" in
            python) init_python ;;
            go) init_go ;;
            node) init_node ;;
            rust) init_rust ;;
            java) init_java ;;
            dotnet) init_dotnet ;;
            ruby) init_ruby ;;
            php) init_php ;;
        esac
    done

    log_info "Multi-language version: $VERSION (synchronized across all projects)"
}

# Main
log_info "Initializing versioning for $PROJECT_TYPE project..."
log_info "Setting version to: $VERSION"

case "$PROJECT_TYPE" in
    python) init_python ;;
    go) init_go ;;
    node) init_node ;;
    rust) init_rust ;;
    java) init_java ;;
    dotnet) init_dotnet ;;
    ruby) init_ruby ;;
    php) init_php ;;
    multi) init_multi ;;
    *)
        log_error "Unsupported project type: $PROJECT_TYPE"
        log_info "Supported types: python, go, node, rust, java, dotnet, ruby, php, multi"
        exit 1
        ;;
esac

# Create .versionrc for semantic-release if it's a Node project
if [[ "$PROJECT_TYPE" == "node" || "$LANGUAGES" == *"node"* ]]; then
    create_file ".versionrc" "{
  \"types\": [
    {\"type\": \"feat\", \"section\": \"Features\"},
    {\"type\": \"fix\", \"section\": \"Bug Fixes\"},
    {\"type\": \"chore\", \"hidden\": true},
    {\"type\": \"docs\", \"section\": \"Documentation\"},
    {\"type\": \"style\", \"hidden\": true},
    {\"type\": \"refactor\", \"section\": \"Refactor\"},
    {\"type\": \"perf\", \"section\": \"Performance\"},
    {\"type\": \"test\", \"hidden\": true}
  ]
}
"
fi

# Summary
echo ""
log_success "Versioning initialized!"
log_info "Version: $VERSION"
log_info "Type: $PROJECT_TYPE"

if [[ "$DRY_RUN" == true ]]; then
    log_warn "Dry run mode - no files were actually created"
    log_info "Run without --dry-run to apply changes"
fi

echo ""
log_info "Next steps:"
echo "  1. Review the generated files"
echo "  2. Customize version flags in your code if needed"
echo "  3. Commit the changes:"
echo "     git add -A && git commit -m 'chore: initialize versioning'"
echo "  4. Run release to create the first release:"
echo "     ~/.claude/skills/release-runbook/scripts/release.sh --version $VERSION"
