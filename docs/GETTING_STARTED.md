# 🚀 Getting Started with HPC/AI Tools

This guide will help you get started with the HPC/AI Content Generation and Publishing Tools.

## 📋 Prerequisites

Before you begin, ensure you have:

- Python 3.11 or higher
- Git (for version control)
- X/Twitter Developer Account (for automated publishing)
- Basic familiarity with command line

## 🏗️ Project Setup

### 1. Clone the Repository

```bash
# Clone the repository
git clone https://github.com/last-kakas-1989/hpc-ai-tools.git
cd hpc-ai-tools
```

### 2. Set Up Python Environment

We recommend using Conda for environment management:

```bash
# Create and activate conda environment
conda create -n hpc-ai python=3.11 -y
conda activate hpc-ai

# Or use virtualenv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install in development mode
pip install -e .[dev]

# Or install production dependencies only
pip install -e .
```

### 4. Configure Environment Variables

```bash
# Copy example configuration
cp .env.example .env

# Edit .env file with your credentials
# You'll need X/Twitter API credentials from developer.twitter.com
```

## 🔧 Configuration

### X/Twitter API Setup

1. Visit [developer.twitter.com](https://developer.twitter.com/)
2. Create a developer account and project
3. Generate API keys and access tokens
4. Add them to your `.env` file:

```bash
X_API_KEY=your_api_key_here
X_API_SECRET=your_api_secret_here
X_ACCESS_TOKEN=your_access_token_here
X_ACCESS_TOKEN_SECRET=your_access_token_secret_here
```

### Content Configuration

You can customize content generation in the `.env` file:

```bash
# Content language (en/zh)
LANGUAGE=en

# Content theme
CONTENT_THEME=hpc_ai

# Tweet length limit
MAX_TWEET_LENGTH=280

# Schedule settings
GENERATE_MORNING_AT=08:00
GENERATE_AFTERNOON_AT=14:00
```

## 🚀 Quick Start Examples

### Generate Content

```bash
# Generate morning and afternoon content
hpc-ai-tools generate

# Generate only morning content
hpc-ai-tools generate --time morning

# Generate and save to file
hpc-ai-tools generate --output content.txt
```

### Test Publishing

```bash
# Test publishing in mock mode (no actual posting)
hpc-ai-tools post --mock

# Real publishing (requires API keys)
hpc-ai-tools post --real
```

### Run Tests

```bash
# Run all tests
pytest

# Run specific component tests
hpc-ai-tools test --component generator
hpc-ai-tools test --component poster
hpc-ai-tools test --component config
```

## 📅 Daily Automation

### Manual Automation

```bash
# Run the daily automation script
./run_daily_automation.sh
```

This script will:
1. Activate the conda environment
2. Generate morning and afternoon content
3. Save content to files
4. Create logs and reports
5. Prepare content for manual publishing

### OpenClaw Integration

For advanced automation with OpenClaw:

```json
{
  "systemEvents": {
    "handlers": {
      "run_hpc_ai_daily": {
        "type": "exec",
        "command": "/path/to/hpc-ai-tools/run_daily_automation.sh",
        "description": "Daily HPC/AI content generation"
      }
    }
  }
}
```

## 📁 Project Structure

```
hpc-ai-tools/
├── src/hpc_ai_tools/          # Source code
│   ├── __init__.py           # Package initialization
│   ├── cli.py               # Command-line interface
│   ├── content_generator.py  # Content generation engine
│   └── x_poster.py          # X/Twitter publishing
├── tests/                   # Test files
├── docs/                   # Documentation
├── output/                 # Generated content
├── logs/                   # Application logs
├── scripts/                # Automation scripts
├── .env.example            # Configuration template
├── pyproject.toml         # Modern project config
├── setup.py               # Traditional setup
├── requirements.txt       # Python dependencies
└── README.md              # Project overview
```

## 🔍 Understanding the Codebase

### Content Generation

The `ContentGenerator` class in `src/hpc_ai_tools/content_generator.py`:

- Uses template-based generation
- Supports multiple languages (English/Chinese)
- Includes HPC and AI topic databases
- Validates content length and format
- Provides content statistics

### X/Twitter Publishing

The `XPoster` class in `src/hpc_ai_tools/x_poster.py`:

- Supports both mock and real posting modes
- Validates content before posting
- Handles media uploads (images)
- Provides comprehensive logging
- Includes error handling and recovery

### Command-Line Interface

The CLI in `src/hpc_ai_tools/cli.py`:

- Provides intuitive command structure
- Includes help and documentation
- Supports verbose output for debugging
- Validates arguments and inputs

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=hpc_ai_tools --cov-report=html

# Run specific test file
pytest tests/test_content_generator.py -v
```

### Test Structure

- `tests/test_content_generator.py`: Content generation tests
- Additional tests can be added for other components

## 🐛 Troubleshooting

### Common Issues

1. **"tweepy not installed" warning**
   - Run `pip install tweepy` or use mock mode

2. **Missing API credentials**
   - Ensure `.env` file exists and contains valid credentials
   - Use mock mode for testing: `hpc-ai-tools post --mock`

3. **Content too long for X/Twitter**
   - The system automatically truncates content to 280 characters
   - Check logs for warnings

4. **Permission errors**
   - Ensure scripts are executable: `chmod +x *.sh`
   - Check directory permissions

### Debug Mode

Enable verbose output for debugging:

```bash
# Generate with verbose output
hpc-ai-tools generate --verbose

# Post with verbose output
hpc-ai-tools post --mock --verbose

# Test with verbose output
hpc-ai-tools test --verbose
```

## 📈 Monitoring and Logs

### Log Files

- `logs/hpc_ai_tools.log`: Application logs
- `logs/tweet_log.txt`: Tweet posting history
- `logs/post_errors.log`: Error logs
- `logs/report_YYYYMMDD.md`: Daily execution reports

### Generated Content

- `output/`: Generated content files
- `tweets/`: Content ready for publishing

## 🔄 Maintenance

### Updating Dependencies

```bash
# Update all packages
pip list --outdated | cut -d' ' -f1 | xargs -n1 pip install -U

# Update project dependencies
pip install -e .[dev] --upgrade
```

### Backup and Recovery

```bash
# Backup environment configuration
conda env export > environment_backup.yml

# Backup project configuration
cp .env .env.backup.$(date +%Y%m%d)
```

## 🎯 Next Steps

### Advanced Configuration

1. **Custom Content Templates**
   - Extend the `ContentGenerator` class
   - Add new template methods
   - Update configuration

2. **Additional Publishing Platforms**
   - Implement new publisher classes
   - Add platform-specific configuration
   - Update CLI commands

3. **Enhanced Analytics**
   - Add engagement tracking
   - Implement A/B testing
   - Create dashboards

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

- **Documentation**: Check the `docs/` directory
- **Issues**: Report bugs on GitHub
- **Questions**: Contact last.kakas.1989@gmail.com
- **Community**: Join discussions on project forums

---

**Happy coding!** 🚀

If you encounter any issues or have questions, please don't hesitate to reach out.