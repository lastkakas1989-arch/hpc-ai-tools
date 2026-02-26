#!/bin/bash
# Push HPC/AI Tools to GitHub

set -e

echo "🚀 Pushing HPC/AI Tools to GitHub..."
echo "======================================"

# Configuration
GITHUB_USERNAME="last-kakas-1989"
REPO_NAME="hpc-ai-tools"
REPO_DESC="HPC/AI Content Generation and Publishing Tools"
REPO_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"
PROJECT_DIR="/Users/attaxu/.openclaw/workspace/python_projects/hpc_ai_tools"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored message
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
check_directory() {
    if [ ! -f "pyproject.toml" ] || [ ! -f "README.md" ]; then
        print_error "This doesn't look like the hpc-ai-tools project directory."
        print_error "Please run this script from: $PROJECT_DIR"
        exit 1
    fi
    print_info "Project directory verified"
}

# Check Git status
check_git_status() {
    if ! git status &> /dev/null; then
        print_error "Not a Git repository. Run 'git init' first."
        exit 1
    fi
    
    # Check for uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        print_warning "You have uncommitted changes."
        read -p "Do you want to commit them? (y/N): " COMMIT_CHOICE
        if [[ "$COMMIT_CHOICE" =~ ^[Yy]$ ]]; then
            git add .
            git commit -m "Auto-commit before pushing to GitHub"
            print_success "Changes committed"
        fi
    fi
    print_info "Git status checked"
}

# Check remote repository
check_remote() {
    if git remote | grep -q origin; then
        CURRENT_URL=$(git remote get-url origin)
        print_info "Remote 'origin' already exists: $CURRENT_URL"
        
        if [ "$CURRENT_URL" != "$REPO_URL" ]; then
            print_warning "Remote URL doesn't match expected URL"
            print_warning "Current: $CURRENT_URL"
            print_warning "Expected: $REPO_URL"
            read -p "Update remote URL? (y/N): " UPDATE_CHOICE
            if [[ "$UPDATE_CHOICE" =~ ^[Yy]$ ]]; then
                git remote set-url origin "$REPO_URL"
                print_success "Remote URL updated"
            fi
        fi
    else
        print_info "Adding remote repository: $REPO_URL"
        git remote add origin "$REPO_URL"
    fi
}

# Test GitHub connection
test_github_connection() {
    print_info "Testing connection to GitHub..."
    
    # Try to ping GitHub
    if ! curl --silent --head https://github.com > /dev/null; then
        print_error "Cannot connect to GitHub. Check your internet connection."
        exit 1
    fi
    
    # Check if repository exists
    if curl --silent --head "https://github.com/${GITHUB_USERNAME}/${REPO_NAME}" > /dev/null; then
        print_info "Repository already exists on GitHub"
        return 0
    else
        print_warning "Repository doesn't exist on GitHub yet"
        print_warning "You need to create it first at:"
        echo "    https://github.com/new"
        echo "    Name: $REPO_NAME"
        echo "    Description: $REPO_DESC"
        echo "    DO NOT initialize with README, .gitignore, or license"
        echo ""
        read -p "Have you created the repository? (y/N): " REPO_CREATED
        if [[ "$REPO_CREATED" =~ ^[Yy]$ ]]; then
            return 0
        else
            print_error "Please create the repository first and run this script again."
            print_info "You can use the manual instructions in PUSH_TO_GITHUB.md"
            exit 1
        fi
    fi
}

# Push to GitHub
push_to_github() {
    print_info "Pushing to GitHub..."
    
    # Try to push
    if git push -u origin main 2>/dev/null; then
        print_success "Successfully pushed to GitHub!"
        return 0
    fi
    
    # If push fails, try with force (after warning)
    print_warning "Push failed. Trying with --force..."
    read -p "Force push? This will overwrite remote history. (y/N): " FORCE_CHOICE
    if [[ "$FORCE_CHOICE" =~ ^[Yy]$ ]]; then
        if git push -u origin main --force; then
            print_success "Successfully force-pushed to GitHub!"
            return 0
        else
            print_error "Force push also failed"
            return 1
        fi
    else
        print_error "Push cancelled"
        return 1
    fi
}

# Show success message
show_success() {
    echo ""
    echo "======================================"
    print_success "🎉 HPC/AI Tools Successfully Pushed to GitHub!"
    echo ""
    echo "📊 Repository: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
    echo "📁 Files: $(git ls-files | wc -l) files committed"
    echo "📝 Commit: $(git log --oneline -1)"
    echo ""
    echo "🚀 Next Steps:"
    echo "   1. Visit your repository: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
    echo "   2. Add repository topics: hpc, ai, content-generation, automation, python"
    echo "   3. Set up GitHub Actions for CI/CD"
    echo "   4. Share your project!"
    echo ""
    echo "💡 Tip: Run './push_to_github.sh' again if you make more changes."
    echo "======================================"
}

# Main execution
main() {
    echo "🚀 HPC/AI Tools GitHub Push Script"
    echo "======================================"
    echo "GitHub User: $GITHUB_USERNAME"
    echo "Repository: $REPO_NAME"
    echo "URL: $REPO_URL"
    echo ""
    
    # Run steps
    check_directory
    check_git_status
    test_github_connection
    check_remote
    
    echo ""
    read -p "Ready to push to GitHub? (y/N): " PUSH_CHOICE
    if [[ ! "$PUSH_CHOICE" =~ ^[Yy]$ ]]; then
        print_error "Push cancelled by user"
        exit 0
    fi
    
    if push_to_github; then
        show_success
    else
        print_error "Failed to push to GitHub. Please check the errors above."
        print_info "Manual instructions are in PUSH_TO_GITHUB.md"
        exit 1
    fi
}

# Run main function
main "$@"