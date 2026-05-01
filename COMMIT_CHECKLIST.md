# Pre-Commit Security Checklist

Before committing code to the repository, verify the following:

## 🔒 Sensitive Data Check

### Files to NEVER Commit
- [ ] No `.env` files (only `.env.example` is allowed)
- [ ] No `data/` directory or `*.db`, `*.sqlite` files
- [ ] No `blogs/` directory (user-generated content)
- [ ] No credential files (`*credentials*.json`, `*.pem`, `*.key`)
- [ ] No API keys or tokens in code
- [ ] No passwords or secrets in configuration files

### Quick Verification Commands

```bash
# Check what will be committed
git status

# Verify no sensitive files are staged
git ls-files | grep -E '\.(env|db|sqlite|key|pem)$'

# Check for hardcoded secrets in staged files
git diff --cached | grep -iE '(api[_-]?key|secret|password|token)'

# List all staged files
git diff --cached --name-only
```

## ✅ Code Quality Check

- [ ] Code follows project style guidelines
- [ ] No debug print statements or commented-out code
- [ ] All imports are used
- [ ] No TODO comments without issue references
- [ ] Tests pass (if applicable)

## 📝 Commit Message Guidelines

- [ ] Clear, descriptive commit message
- [ ] Follows conventional commits format (optional)
- [ ] References issue number if applicable

## 🛡️ Automated Checks

If pre-commit hooks are installed, they will automatically check:
- Sensitive file detection
- Hardcoded secrets scanning
- Code formatting (black, flake8)
- Security issues (bandit)

### Install Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

## 🚨 If You Accidentally Commit Sensitive Data

1. **DO NOT PUSH** to remote repository
2. Remove the sensitive data from the file
3. Amend the commit:
   ```bash
   git add .
   git commit --amend --no-edit
   ```
4. If already pushed, follow the incident response in SECURITY.md

## ✨ Safe to Commit

Once all checks pass:

```bash
git commit -m "Your descriptive commit message"
```

## 📚 Additional Resources

- See [SECURITY.md](SECURITY.md) for detailed security guidelines
- See [.gitignore](.gitignore) for list of excluded files
- See [README.md](README.md) for project setup instructions