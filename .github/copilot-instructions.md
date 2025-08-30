# Morpholyzer - Japanese Morphological Analysis Application

Morpholyzer is a Django web application for Japanese morphological analysis using MeCab. It provides both a web interface and REST API for analyzing Japanese text into morphemes with detailed linguistic information.

**ALWAYS reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Prerequisites and Environment Setup
- MeCab is already installed system-wide with mecab-ipadic-utf8 dictionary
- Python 3.12 is available at `/usr/bin/python3`
- Docker and Docker Compose (v2 syntax) are available

### Bootstrap and Build the Repository
**NEVER CANCEL builds or long-running commands. Wait for completion.**

```bash
# 1. Install Python dependencies - takes ~6 seconds
pip install -r requirements.txt

# 2. Run database migrations - takes ~0.5 seconds  
python manage.py migrate

# 3. Run all tests - takes ~1 second. NEVER CANCEL.
python manage.py test
# Expected: "Ran 13 tests in 0.XXXs OK"

# 4. Run specific app tests - takes ~0.5 seconds
python manage.py test morpholyzer
```

### Running the Application

#### Local Development Server
```bash
# Start development server - starts in ~2 seconds
python manage.py runserver
# Access at: http://localhost:8000
# API endpoint: http://localhost:8000/api/analyze/
```

#### Docker Environment
```bash
# Build Docker image - takes ~23 seconds. NEVER CANCEL. Set timeout to 60+ seconds.
docker compose build web

# Run production container - starts in ~5 seconds
docker compose up web
# Access at: http://localhost:8000

# Run development container (with volume mounts)
docker compose up dev
# Note: May fail due to container runtime issues in some environments
```

### Testing and Quality Assurance

#### Test Commands
```bash
# Run all tests with timing
time python manage.py test
# Expected time: ~1 second. NEVER CANCEL.

# Run with coverage analysis
pip install coverage
coverage run --source='.' manage.py test morpholyzer
coverage report
# Expected: ~90% coverage, runs in ~1 second
```

#### API Testing
```bash
# Test API endpoint with sample Japanese text
curl -X POST -d "text=これはテストです。" http://localhost:8000/api/analyze/
# Expected: JSON response with morphemes array and pos_summary
```

## Validation Scenarios

**ALWAYS run through these validation scenarios after making changes:**

### 1. Basic Functionality Test
1. Start development server: `python manage.py runserver`
2. Navigate to http://localhost:8000
3. Enter Japanese text: `これは日本語形態素解析のテストです。`
4. Click submit button
5. Verify analysis results appear with:
   - 品詞統計 (POS statistics)
   - 解析情報 (Analysis information)
   - Complete morpheme breakdown table

### 2. API Validation Test  
```bash
# Test valid input
curl -X POST -d "text=テスト文章" http://localhost:8000/api/analyze/

# Test empty input (should return 400 error)
curl -X POST -d "text=" http://localhost:8000/api/analyze/

# Test invalid method (should return 405 error)
curl -X GET http://localhost:8000/api/analyze/
```

### 3. Test Suite Validation
```bash
# All tests must pass
python manage.py test
# Expected output: "Ran 13 tests in X.XXXs OK"
```

## Common Tasks and File Locations

### Key Application Components
- **Main app**: `morpholyzer/` - Core morphological analysis logic
- **MeCab integration**: `morpholyzer/analyzer.py` - MorphologicalAnalyzer class
- **Web views**: `morpholyzer/views.py` - Django views for web and API
- **Templates**: `morpholyzer/templates/morpholyzer/index.html` - Web interface
- **Tests**: `morpholyzer/tests.py` - 13 comprehensive test cases
- **Forms**: `morpholyzer/forms.py` - Text input validation
- **Settings**: `morpholyzer_project/settings.py` - Django configuration

### Project Structure Reference
```
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies (Django 5.2.4, mecab-python3)
├── Dockerfile               # Container definition
├── docker-compose.yml       # Docker services (web, dev)
├── morpholyzer/            # Main Django app
│   ├── analyzer.py         # MeCab morphological analysis
│   ├── views.py           # Web and API endpoints  
│   ├── tests.py           # Test suite (13 tests)
│   ├── forms.py           # Input validation
│   └── templates/         # HTML templates
└── morpholyzer_project/   # Django project settings
    ├── settings.py        # Configuration
    └── urls.py           # URL routing
```

### Database Information
- **Engine**: SQLite3 (development default)
- **Location**: `db.sqlite3` (auto-created)
- **Migrations**: Standard Django auth and session tables only
- **No custom models**: Application is stateless for morphological analysis

### API Specification
- **Endpoint**: `POST /api/analyze/`
- **Input**: `text` parameter (max 1000 characters)
- **Output**: JSON with morphemes array, pos_summary, and metadata
- **Error codes**: 400 (empty text), 405 (wrong method), 500 (analysis error)

## Timing Expectations and Timeouts

**CRITICAL: NEVER CANCEL any of these operations:**

- **Dependencies install**: ~6 seconds (set timeout: 60+ seconds)
- **Database migration**: ~0.5 seconds (set timeout: 30+ seconds) 
- **Test execution**: ~1 second (set timeout: 30+ seconds)
- **Docker build**: ~23 seconds (set timeout: 60+ seconds)
- **Server startup**: ~2 seconds (set timeout: 30+ seconds)
- **Coverage analysis**: ~1 second (set timeout: 30+ seconds)

## Troubleshooting

### MeCab Issues
If you encounter MeCab initialization errors:
1. Verify MeCab installation: `mecab --version`
2. Check dictionary: `ls /usr/share/mecab/dic/`
3. MeCab is pre-installed system-wide - do not reinstall

### Docker Issues  
- Use `docker compose` (v2 syntax), not `docker-compose`
- Development container may fail due to runtime issues - use production container instead
- Warning about obsolete version attribute in docker-compose.yml is harmless

### Port Conflicts
- Default port 8000 may be in use
- Use alternative port: `python manage.py runserver 127.0.0.1:8001`

### Test Failures
- All 13 tests should pass consistently
- If tests fail, check MeCab installation and Japanese text encoding
- Test database is created/destroyed automatically

## Development Notes

### Code Style and Standards
- Application uses Japanese language for UI text and comments
- Follow existing Django patterns and conventions  
- MeCab analyzer handles UTF-8 Japanese text encoding automatically
- Error messages are in Japanese to match UI language

### Making Changes
- Always run full test suite after modifications: `python manage.py test`
- Test both web interface and API endpoints manually
- Verify MeCab analysis still works with sample Japanese text
- Check that morpheme parsing returns expected linguistic features

### Dependencies
- **Django 5.2.4**: Web framework
- **mecab-python3 1.0.10**: MeCab binding for morphological analysis
- **No linting tools**: Project does not include ESLint, Flake8, etc.
- **No CI/CD**: No GitHub Actions workflows configured

### Known Working Commands Summary
```bash
# Complete validation sequence (run all commands):
pip install -r requirements.txt              # ~6s
python manage.py migrate                     # ~0.5s  
python manage.py test                        # ~1s
python manage.py runserver                   # starts in ~2s
curl -X POST -d "text=テスト" http://localhost:8000/api/analyze/  # API test
docker compose build web                     # ~23s
docker compose up web                        # starts in ~5s
```