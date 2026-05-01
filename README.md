# Gemini AI-Powered Blog Application

A microservice-based blog content generation application powered by Google's Gemini AI.

## Architecture

This application follows microservice architecture principles with the following services:

- **API Gateway** - Central entry point and request routing
- **Blog Service** - Handles blog content management and AI generation
- **Settings Service** - Manages configuration and user preferences
- **UI Service** - Frontend web interface

## Services

### API Gateway (Port 8000)
- Routes requests to appropriate microservices
- Handles authentication and authorization
- Provides unified API interface

### Blog Service (Port 8001)
- Blog content creation and management
- Gemini AI integration for content generation
- File and folder management for blog projects
- Versioning system for blog drafts

### Settings Service (Port 8002)
- Configuration management (API keys, source folders)
- User preferences and publication settings
- Secure storage of sensitive data

### UI Service (Port 8003)
- Web-based user interface
- Blog creation and editing interface
- Settings management interface
- Blog browsing and management

## Getting Started

### Prerequisites
- Python 3.11+
- Google Gemini AI API key

### Installation

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Edit .env and add your actual values:
# - GEMINI_API_KEY: Get from https://makersuite.google.com/app/apikey
# - SECRET_KEY: Use the generated key from above
# - Other settings: Adjust as needed
```

**⚠️ IMPORTANT**: Never commit the `.env` file to version control!

5. Start the services:
```bash
# Start all services (run each in separate terminal)
python -m services.api_gateway.main
python -m services.blog_service.main
python -m services.settings_service.main
python -m services.ui_service.main
```

6. Access the application:
- Main UI: http://localhost:8003
- API Gateway: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Project Structure

```
BLOGWRITER/
├── services/
│   ├── api_gateway/          # API Gateway service
│   ├── blog_service/         # Blog management service
│   ├── settings_service/     # Configuration service
│   └── ui_service/          # Frontend service
├── shared/                  # Shared utilities and models
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Features

- **Blog Creation**: Create new blog projects with organized folder structure
- **AI Content Generation**: Leverage Gemini AI for content creation and updates
- **Version Management**: Track and manage different versions of blog drafts
- **Reference Management**: Store and organize reference materials
- **Multi-platform Publishing**: Configure publication to different platforms
- **Settings Management**: Centralized configuration management

## API Documentation

Once the services are running, visit http://localhost:8000/docs for complete API documentation.

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black .
flake8 .
mypy .
```

### Security Best Practices

**Before committing code:**

1. **Install pre-commit hooks** (recommended):
   ```bash
   pip install pre-commit
   pre-commit install
   ```
   This will automatically check for sensitive data before each commit.

2. **Manual security check**:
   ```bash
   # Verify no .env files are staged
   git status | grep .env
   
   # Check for credential files
   git ls-files | grep -E '\.(key|pem|credentials)'
   ```

3. **Review the SECURITY.md file** for detailed guidelines on protecting sensitive information.

## Security

See [SECURITY.md](SECURITY.md) for detailed information about:
- What sensitive data is protected
- How to handle API keys and secrets
- Pre-commit security checks
- What to do if secrets are exposed

## License

This project is licensed under the MIT License.
