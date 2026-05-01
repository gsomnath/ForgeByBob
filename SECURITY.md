# Security Guidelines

## Sensitive Information Protection

This document outlines how sensitive information is protected in this project and best practices for developers.

## 🔒 What is Protected

### 1. Environment Variables (.env)
- **Location**: `.env` file in project root
- **Protection**: Excluded via `.gitignore`
- **Contains**:
  - API keys (Gemini AI, Google Cloud)
  - Secret keys for session management
  - Database credentials
  - Service URLs with authentication

### 2. Runtime Data
- **Location**: `data/` directory
- **Protection**: Excluded via `.gitignore`
- **Contains**:
  - `settings.json` - Stores API keys and configuration
  - Database files (*.db, *.sqlite)
  - User-generated content

### 3. Credentials Files
- **Patterns**: `*credentials*.json`, `*.pem`, `*.key`, `*.p12`
- **Protection**: Excluded via `.gitignore`
- **Contains**: Google Cloud service account credentials, SSL certificates

### 4. Generated Content
- **Location**: `blogs/`, `generated_images/`
- **Protection**: Excluded via `.gitignore`
- **Reason**: User-generated content, may contain sensitive information

## ✅ Safe Practices

### For Developers

1. **Never commit `.env` files**
   ```bash
   # Always use .env.example as template
   cp .env.example .env
   # Then edit .env with your actual values
   ```

2. **Generate secure secret keys**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **Check before committing**
   ```bash
   # Review what will be committed
   git status
   git diff --cached
   
   # Ensure no sensitive files are staged
   git ls-files | grep -E '\.(env|key|pem|credentials)'
   ```

4. **Use environment variables in code**
   ```python
   # ✅ GOOD - Load from environment
   from shared.config import settings
   api_key = settings.gemini_api_key
   
   # ❌ BAD - Hardcoded
   api_key = "AIzaSyABC123..."
   ```

### For API Responses

The application automatically masks sensitive data in API responses:

```python
# In settings_service/main.py
if settings_data.get("gemini_api_key"):
    settings_data["gemini_api_key"] = "***masked***"
```

## 🚨 What to Do If Secrets Are Exposed

### If you accidentally commit sensitive data:

1. **Immediately rotate the exposed credentials**
   - Generate new API keys
   - Update `.env` file
   - Update any deployed instances

2. **Remove from Git history**
   ```bash
   # For recent commits
   git reset --soft HEAD~1
   git reset HEAD .env
   git commit -m "Remove sensitive data"
   
   # For older commits, use git-filter-repo or BFG Repo-Cleaner
   ```

3. **Force push (if already pushed)**
   ```bash
   git push --force-with-lease
   ```

4. **Notify team members** to pull the updated history

## 📋 Pre-Commit Checklist

Before committing code, verify:

- [ ] No `.env` files in staged changes
- [ ] No hardcoded API keys or secrets
- [ ] No credential files (*.json, *.pem, *.key)
- [ ] No database files with sensitive data
- [ ] `.gitignore` is up to date
- [ ] Only `.env.example` with placeholder values

## 🔍 Automated Checks

Consider adding pre-commit hooks:

```bash
# .git/hooks/pre-commit
#!/bin/bash
if git diff --cached --name-only | grep -E '\.(env|key|pem|credentials)'; then
    echo "ERROR: Attempting to commit sensitive files!"
    exit 1
fi
```

## 📚 Additional Resources

- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [12-Factor App: Config](https://12factor.net/config)

## 🆘 Support

If you discover a security vulnerability, please email security@example.com (do not create a public issue).