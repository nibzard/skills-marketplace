#!/usr/bin/env bash
#
# release.sh - Universal release automation script
#
# Supports: Python, Go, Node.js, Rust, Java, .NET, Ruby, PHP, and multi-language projects
#
# Usage:
#   release.sh [OPTIONS]
#
# Options:
#   --version VERSION       Version to release (required unless --interactive)
#   --major                 Bump major version
#   --minor                 Bump minor version
#   --patch                 Bump patch version (default)
#   --interactive           Prompt for version and confirmation
#   --dry-run               Show what would happen without making changes
#   --skip-tests            Skip running tests
#   --test-command CMD      Custom test command
#   --no-commit             Don't create release commit
#   --no-tag                Don't create git tag
#   --no-push               Don't push to remote
#   --no-release            Don't create GitHub release
#   --draft                 Create GitHub release as draft
#   --pre-release TAG       Mark as pre-release with tag (e.g., beta, rc)
#   --notes FILE            Release notes from file
#   --title TITLE           Custom release title
#   --help                  Show help message
#

set -euo pipefail

# Color output
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BLUE='\033[0;34m'
    CYAN='\033[0;36m'
    BOLD='\033[1m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    CYAN=''
    BOLD=''
    NC=''
fi

# Logging functions
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

log_step() {
    echo -e "${CYAN}[→]${NC} ${BOLD}$*${NC}"
}

# Default values
VERSION=""
BUMP_TYPE="patch"
INTERACTIVE=false
DRY_RUN=false
SKIP_TESTS=false
TEST_COMMAND=""
NO_COMMIT=false
NO_TAG=false
NO_PUSH=false
NO_RELEASE=false
DRAFT=false
PRERELEASE=""
NOTES_FILE=""
TITLE=""

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Detect project
eval "$(bash "$SCRIPT_DIR/detect-project.sh")"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --version|-v)
            VERSION="$2"
            shift 2
            ;;
        --major)
            BUMP_TYPE="major"
            shift
            ;;
        --minor)
            BUMP_TYPE="minor"
            shift
            ;;
        --patch)
            BUMP_TYPE="patch"
            shift
            ;;
        --interactive|-i)
            INTERACTIVE=true
            shift
            ;;
        --dry-run|-n)
            DRY_RUN=true
            shift
            ;;
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --test-command)
            TEST_COMMAND="$2"
            shift 2
            ;;
        --no-commit)
            NO_COMMIT=true
            shift
            ;;
        --no-tag)
            NO_TAG=true
            shift
            ;;
        --no-push)
            NO_PUSH=true
            shift
            ;;
        --no-release)
            NO_RELEASE=true
            shift
            ;;
        --draft)
            DRAFT=true
            shift
            ;;
        --pre-release)
            PRERELEASE="$2"
            shift 2
            ;;
        --notes)
            NOTES_FILE="$2"
            shift 2
            ;;
        --title)
            TITLE="$2"
            shift 2
            ;;
        --help|-h)
            cat <<EOF
release.sh - Universal release automation

USAGE:
    release.sh [OPTIONS]

OPTIONS:
    --version, -v VERSION    Version to release (e.g., 1.2.3)
    --major                   Bump major version (X.0.0)
    --minor                   Bump minor version (x.X.0)
    --patch                   Bump patch version (x.x.X) [default]
    --interactive, -i         Interactive mode with prompts
    --dry-run, -n             Show actions without executing
    --skip-tests              Skip test execution
    --test-command CMD        Custom test command
    --no-commit               Skip creating release commit
    --no-tag                  Skip creating git tag
    --no-push                 Skip pushing to remote
    --no-release              Skip GitHub release creation
    --draft                   Create release as draft
    --pre-release TAG         Pre-release tag (beta, rc, etc.)
    --notes FILE              Release notes from file
    --title TITLE             Custom release title
    --help, -h                Show this help

EXAMPLES:
    # Automated release with specific version
    release.sh --version 1.2.3

    # Interactive mode
    release.sh --interactive

    # Bump patch version and release
    release.sh --patch

    # Dry run to see what would happen
    release.sh --dry-run --version 1.2.3

    # Custom test command
    release.sh --version 1.2.3 --test-command "make test-integration"

DETECTED PROJECT:
    Type: $PROJECT_TYPE
    Languages: $LANGUAGES
    Version Files: $VERSION_FILES
    Test Commands: $TEST_COMMANDS
EOF
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Preflight checks
preflight_checks() {
    log_step "Running preflight checks..."

    local errors=0

    # Check if we're in a git repo
    if ! git rev-parse --git-dir &>/dev/null; then
        log_error "Not a git repository"
        ((errors++))
    fi

    # Check for uncommitted changes
    if [[ $errors -eq 0 ]] && ! git diff-index --quiet HEAD --; then
        log_error "Uncommitted changes detected. Please commit or stash first."
        git status --short
        ((errors++))
    fi

    # Check if gh CLI is installed
    if [[ $errors -eq 0 ]] && [[ "$NO_RELEASE" == false ]] && ! command -v gh &>/dev/null; then
        log_error "GitHub CLI (gh) not found. Install from https://cli.github.com/"
        ((errors++))
    fi

    # Check gh auth
    if [[ $errors -eq 0 ]] && [[ "$NO_RELEASE" == false ]] && ! gh auth status &>/dev/null; then
        log_error "GitHub CLI not authenticated. Run: gh auth login"
        ((errors++))
    fi

    # Check for remote
    if [[ $errors -eq 0 ]] && [[ "$NO_PUSH" == false ]]; then
        if ! git remote get-url origin &>/dev/null; then
            log_error "No git remote 'origin' found"
            ((errors++))
        fi
    fi

    # Check for version files
    if [[ $errors -eq 0 ]]; then
        IFS=',' read -ra files <<< "$VERSION_FILES"
        if [[ ${#files[@]} -eq 0 ]]; then
            log_warn "No version files detected. Consider running init-versioning.sh first."
            if [[ "$INTERACTIVE" == true ]]; then
                read -p "Initialize versioning now? [y/N] " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    bash "$SCRIPT_DIR/init-versioning.sh" --version "${VERSION:-0.1.0}"
                    # Re-detect after init
                    eval "$(bash "$SCRIPT_DIR/detect-project.sh")"
                fi
            fi
        fi
    fi

    if [[ $errors -gt 0 ]]; then
        log_error "Preflight checks failed. Please fix the errors above."
        exit 1
    fi

    log_success "Preflight checks passed"
}

# Determine version
determine_version() {
    log_step "Determining version..."

    if [[ -n "$VERSION" ]]; then
        log_info "Using specified version: $VERSION"
        return
    fi

    # Get current version
    local current="$CURRENT_VERSION"

    if [[ -z "$current" ]]; then
        log_warn "No current version detected, using 0.0.0"
        current="0.0.0"
    else
        log_info "Current version: $current"
    fi

    # Parse current version
    IFS='.' read -ra parts <<< "$current"
    local major="${parts[0]:-0}"
    local minor="${parts[1]:-0}"
    local patch="${parts[2]:-0}"

    # Strip prerelease if any
    patch="${patch%%-*}"

    # Bump version
    case "$BUMP_TYPE" in
        major)
            ((major++))
            minor=0
            patch=0
            ;;
        minor)
            ((minor++))
            patch=0
            ;;
        patch)
            ((patch++))
            ;;
    esac

    VERSION="$major.$minor.$patch"

    # Add prerelease tag if specified
    if [[ -n "$PRERELEASE" ]]; then
        VERSION="$VERSION-$PRERELEASE"
    fi

    log_info "New version: $VERSION"

    if [[ "$INTERACTIVE" == true ]]; then
        read -p "Enter version (default: $VERSION): " -r input
        if [[ -n "$input" ]]; then
            VERSION="$input"
        fi
    fi
}

# Bump version in files
bump_version() {
    log_step "Bumping version in files..."

    local updated=false
    IFS=',' read -ra files <<< "$VERSION_FILES"

    for file in "${files[@]}"; do
        [[ ! -f "$file" ]] && continue

        log_info "Updating $file"

        case "$file" in
            pyproject.toml)
                update_pyproject_toml "$file"
                ;;
            package.json)
                update_package_json "$file"
                ;;
            Cargo.toml)
                update_cargo_toml "$file"
                ;;
            VERSION)
                update_version_file "$file"
                ;;
            setup.py)
                update_setup_py "$file"
                ;;
            go.mod)
                update_go_mod "$file"
                ;;
            pom.xml)
                update_pom_xml "$file"
                ;;
            build.gradle|build.gradle.kts)
                update_gradle "$file"
                ;;
            *.csproj|*.fsproj)
                update_dotnet_proj "$file"
                ;;
            *.gemspec)
                update_gemspec "$file"
                ;;
            composer.json)
                update_composer_json "$file"
                ;;
            *)
                update_generic "$file"
                ;;
        esac

        updated=true
    done

    if [[ "$updated" == true ]]; then
        log_success "Version bumped to $VERSION"
    else
        log_warn "No version files were updated"
    fi
}

update_pyproject_toml() {
    local file="$1"
    if [[ "$DRY_RUN" == false ]]; then
        # Try project.version first (PEP 621), then tool.poetry.version
        if grep -q "^version = " "$file"; then
            sed -i "s|^version = .*|version = \"$VERSION\"|" "$file"
        else
            log_warn "Could not find version in $file"
        fi
    fi
}

update_package_json() {
    local file="$1"
    if [[ "$DRY_RUN" == false ]]; then
        if command -v jq &>/dev/null; then
            jq ".version = \"$VERSION\"" "$file" > "$file.tmp" && mv "$file.tmp" "$file"
        else
            sed -i 's/"version":\s*"[^"]*"/"version": "'"$VERSION"'"/' "$file"
        fi
    fi
}

update_cargo_toml() {
    local file="$1"
    if [[ "$DRY_RUN" == false ]]; then
        sed -i 's/^version = .*/version = "'"$VERSION"'"/' "$file"
    fi
}

update_version_file() {
    local file="$1"
    if [[ "$DRY_RUN" == false ]]; then
        echo "$VERSION" > "$file"
    fi
}

update_setup_py() {
    local file="$1"
    if [[ "$DRY_RUN" == false ]]; then
        sed -i "s/version=['\"][^'\"]*['\"]/version='$VERSION'/" "$file"
    fi
}

update_go_mod() {
    local file="$1"
    if [[ "$DRY_RUN" == false ]]; then
        # Go version is usually a comment, update it if present
        if grep -q "version" "$file"; then
            sed -i "s|//.*version.*|// version $VERSION|" "$file"
        fi
    fi
}

update_pom_xml() {
    local file="$1"
    if [[ "$DRY_RUN" == false ]]; then
        # Update first version occurrence (project version)
        sed -i "0,/<version>/s|<version>[^<]*</version>|<version>$VERSION</version>|" "$file"
    fi
}

update_gradle() {
    local file="$1"
    log_warn "Please manually update version in $file to $VERSION"
}

update_dotnet_proj() {
    local file="$1"
    if [[ "$DRY_RUN" == false ]]; then
        if grep -q "<Version>" "$file"; then
            sed -i "s|<Version>[^<]*</Version>|<Version>$VERSION</Version>|g" "$file"
        elif grep -q "<VersionPrefix>" "$file"; then
            sed -i "s|<VersionPrefix>[^<]*</VersionPrefix>|<VersionPrefix>$VERSION</VersionPrefix>|g" "$file"
        fi
    fi
}

update_gemspec() {
    local file="$1"
    if [[ "$DRY_RUN" == false ]]; then
        sed -i "s|s.version.*=.*|s.version = '$VERSION'|g" "$file"
    fi
}

update_composer_json() {
    local file="$1"
    if [[ "$DRY_RUN" == false ]]; then
        if command -v jq &>/dev/null; then
            jq ".version = \"$VERSION\"" "$file" > "$file.tmp" && mv "$file.tmp" "$file"
        elif grep -q '"version"' "$file"; then
            sed -i 's/"version":\s*"[^"]*"/"version": "'"$VERSION"'"/' "$file"
        fi
    fi
}

update_generic() {
    local file="$1"
    if [[ "$DRY_RUN" == false ]]; then
        # Generic pattern: look for version = or version: with quotes
        sed -i -E "s/(version|VERSION)[[:space:]]*[=:][[:space:]]*[\"']?[0-9]+\.[0-9]+\.[0-9]+/\1 = \"$VERSION\"/" "$file" 2>/dev/null || true
    fi
}

# Run tests
run_tests() {
    if [[ "$SKIP_TESTS" == true ]]; then
        log_warn "Skipping tests (--skip-tests)"
        return
    fi

    log_step "Running tests..."

    local test_cmd="$TEST_COMMAND"

    # Auto-detect test command if not specified
    if [[ -z "$test_cmd" ]]; then
        IFS=',' read -ra cmds <<< "$TEST_COMMANDS"
        if [[ ${#cmds[@]} -gt 0 ]]; then
            test_cmd="${cmds[0]}"
        fi
    fi

    if [[ -z "$test_cmd" ]]; then
        log_warn "No test command found, skipping tests"
        return
    fi

    log_info "Running: $test_cmd"

    if [[ "$DRY_RUN" == true ]]; then
        log_info "[DRY RUN] Would run: $test_cmd"
        return
    fi

    if eval "$test_cmd"; then
        log_success "Tests passed"
    else
        log_error "Tests failed. Aborting release."
        exit 1
    fi
}

# Commit changes
commit_changes() {
    if [[ "$NO_COMMIT" == true ]]; then
        log_warn "Skipping commit (--no-commit)"
        return
    fi

    log_step "Committing version changes..."

    local commit_msg="chore: release v$VERSION"

    if [[ "$DRY_RUN" == true ]]; then
        log_info "[DRY RUN] Would commit with message: $commit_msg"
        return
    fi

    # Stage version files
    IFS=',' read -ra files <<< "$VERSION_FILES"
    for file in "${files[@]}"; do
        if [[ -f "$file" ]]; then
            git add "$file"
        fi
    done

    if git diff-index --quiet HEAD --; then
        log_warn "No changes to commit"
        return
    fi

    git commit -m "$commit_msg"
    log_success "Committed: $commit_msg"
}

# Create tag
create_tag() {
    if [[ "$NO_TAG" == true ]]; then
        log_warn "Skipping tag creation (--no-tag)"
        return
    fi

    log_step "Creating git tag..."

    local tag_name="v$VERSION"
    local tag_msg="Release $VERSION"

    if [[ "$DRY_RUN" == true ]]; then
        log_info "[DRY RUN] Would create tag: $tag_name"
        return
    fi

    # Check if tag already exists
    if git rev-parse "$tag_name" &>/dev/null; then
        log_error "Tag $tag_name already exists. Delete it first or use a different version."
        exit 1
    fi

    git tag -a "$tag_name" -m "$tag_msg"
    log_success "Created tag: $tag_name"
}

# Push to remote
push_to_remote() {
    if [[ "$NO_PUSH" == true ]]; then
        log_warn "Skipping push (--no-push)"
        return
    fi

    log_step "Pushing to remote..."

    local branch
    branch=$(git branch --show-current 2>/dev/null || echo "HEAD")
    local remote
    remote=$(git config --get "branch.${branch}.remote" 2>/dev/null || echo "origin")

    if [[ "$DRY_RUN" == true ]]; then
        log_info "[DRY RUN] Would push to $remote $branch"
        log_info "[DRY RUN] Would push tag v$VERSION to $remote"
        return
    fi

    git push "$remote" "$branch"
    git push "$remote" "v$VERSION"
    log_success "Pushed to $remote"
}

# Generate release notes
generate_release_notes() {
    local last_tag
    last_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

    local notes="## Release v$VERSION\n\n"

    if [[ -n "$last_tag" ]]; then
        notes+="### Changes since $last_tag\n\n"
        notes+="Full changelog: https://github.com/$GITHUB_REPO/compare/$last_tag...v$VERSION\n\n"
        notes+="### Commits\n\n"
        git log "$last_tag..HEAD" --pretty=format:"- %s (%h)" | head -20
    else
        notes+="Initial release.\n\n"
        notes+="### Commits\n\n"
        git log --pretty=format:"- %s (%h)" | head -20
    fi

    echo -e "$notes"
}

# Create GitHub release
create_github_release() {
    if [[ "$NO_RELEASE" == true ]]; then
        log_warn "Skipping GitHub release (--no-release)"
        return
    fi

    log_step "Creating GitHub release..."

    local tag_name="v$VERSION"
    local release_title="${TITLE:-v$VERSION}"
    local release_notes

    if [[ -n "$NOTES_FILE" ]]; then
        release_notes=$(cat "$NOTES_FILE")
    else
        release_notes=$(generate_release_notes)
    fi

    if [[ "$DRY_RUN" == true ]]; then
        log_info "[DRY RUN] Would create GitHub release:"
        log_info "  Tag: $tag_name"
        log_info "  Title: $release_title"
        log_info "  Draft: $DRAFT"
        [[ -n "$PRERELEASE" ]] && log_info "  Pre-release: $PRERELEASE"
        echo ""
        echo "$release_notes"
        return
    fi

    local gh_args=(
        "$tag_name"
        --title "$release_title"
        --notes "$release_notes"
    )

    [[ "$DRAFT" == true ]] && gh_args+=(--draft)
    [[ -n "$PRERELEASE" ]] && gh_args+=(--prerelease)

    gh release create "${gh_args[@]}"
    log_success "Created GitHub release: $tag_name"
}

# Main workflow
main() {
    log_info "Starting release workflow..."
    echo ""
    log_info "Detected project:"
    log_info "  Type: $PROJECT_TYPE"
    log_info "  Languages: $LANGUAGES"
    log_info "  Version files: $VERSION_FILES"
    [[ -n "$CURRENT_VERSION" ]] && log_info "  Current version: $CURRENT_VERSION"
    echo ""

    if [[ "$INTERACTIVE" == true ]]; then
        echo ""
        read -p "Continue? [Y/n] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            log_info "Aborted by user"
            exit 0
        fi
    fi

    preflight_checks
    determine_version
    bump_version
    run_tests
    commit_changes
    create_tag
    push_to_remote
    create_github_release

    echo ""
    log_success "Release v$VERSION complete!"

    # Post-release info
    echo ""
    log_info "Next steps:"

    if [[ -n "$GITHUB_REPO" ]]; then
        log_info "  - View release: https://github.com/$GITHUB_REPO/releases/tag/v$VERSION"
    fi

    # Package manager info
    case "$PROJECT_TYPE" in
        python)
            if [[ -f "pyproject.toml" ]] && grep -q "\[project.urls\]" pyproject.toml; then
                log_info "  - Publish to PyPI: python -m build && twine upload dist/*"
            fi
            ;;
        node)
            if [[ -f "package.json" ]] && grep -q "publishConfig" package.json; then
                log_info "  - Publish to npm: npm publish"
            fi
            ;;
        rust)
            if [[ -f "Cargo.toml" ]] && grep -q "registry" Cargo.toml; then
                log_info "  - Publish to crates.io: cargo publish"
            fi
            ;;
    esac
}

main "$@"
