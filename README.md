# 🚀 HPC/AI Content Generation Tools

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A professional toolset for automated HPC (High Performance Computing) and AI content generation, curation, and publishing.

## ✨ Features

- **🤖 AI-Powered Content Generation**: Automatically generate HPC/AI-related content using intelligent templates
- **📰 Multi-Source Content Aggregation**: Fetch and curate content from HPCWire, DOE, Argonne, ORNL, and other authoritative sources
- **🐦 X/Twitter Integration**: Automated publishing with intelligent scheduling
- **📊 Content Analytics**: Track engagement and optimize content strategy
- **⚡ High Performance**: Optimized for speed and reliability
- **🔧 Extensible Architecture**: Easy to add new content sources and publishing platforms

## 🏗️ Project Structure

```
hpc-ai-tools/
├── src/
│   └── hpc_ai_tools/
│       ├── __init__.py
│       ├── content_generator.py    # Core content generation engine
│       ├── x_poster.py            # X/Twitter publishing interface
│       └── cli.py                 # Command-line interface
├── tests/
│   └── test_content_generator.py  # Unit tests
├── scripts/
│   └── run_daily.sh              # Daily automation script
├── docs/                         # Documentation
├── output/                       # Generated content storage
├── logs/                         # Application logs
├── pyproject.toml               # Modern Python project config
├── setup.py                     # Traditional setup configuration
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── LICENSE                      # MIT License
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Conda (recommended) or virtualenv
- X/Twitter Developer Account (for automated publishing)

### Installation

1. **Clone and setup environment:**
```bash
# Clone the repository
git clone https://github.com/last-kakas-1989/hpc-ai-tools.git
cd hpc-ai-tools

# Create and activate conda environment
conda create -n hpc-ai python=3.11 -y
conda activate hpc-ai

# Install dependencies
pip install -e .[dev]
```

2. **Configure environment variables:**
```bash
# Copy example configuration
cp .env.example .env

# Edit .env file with your credentials
# Required: X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET
```

3. **Test the installation:**
```bash
# Generate sample content
hpc-ai-tools generate

# Test publishing (mock mode)
hpc-ai-tools post --mock

# Run tests
pytest
```

## 📖 Usage

### Basic Commands

```bash
# Generate HPC/AI content
hpc-ai-tools generate

# Generate and save to file
hpc-ai-tools generate --output tweets/today.txt

# Publish to X (real mode - requires API keys)
hpc-ai-tools post --real

# Publish to X (mock mode - dry run)
hpc-ai-tools post --mock

# Show help
hpc-ai-tools --help
```

### Daily Automation

The project includes a complete automation script for daily content generation:

```bash
# Run daily automation (generates morning and afternoon content)
./scripts/run_daily.sh

# Or use the Python automation script
./run_daily_automation.sh
```

### Integration with OpenClaw

For advanced automation, integrate with OpenClaw:

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

## 🔧 Development

### Setting up Development Environment

```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run tests with coverage
pytest --cov=hpc_ai_tools --cov-report=html

# Code formatting
black src tests

# Linting
flake8 src tests

# Type checking
mypy src
```

### Adding New Content Sources

1. Extend the `ContentGenerator` class in `src/hpc_ai_tools/content_generator.py`
2. Add new template methods
3. Update configuration as needed
4. Write tests for the new functionality

### Project Architecture

- **Content Generation**: Template-based system with AI-assisted content creation
- **Publishing**: Abstract publisher interface with X/Twitter implementation
- **Configuration**: Environment-based configuration with sensible defaults
- **Logging**: Comprehensive logging for debugging and monitoring
- **Error Handling**: Robust error handling with graceful degradation

## 📊 Content Strategy

The tool generates content in two daily batches:

### Morning Content (HPC Focus)
- Latest HPC research and breakthroughs
- Supercomputing infrastructure updates
- Performance benchmarks and optimizations
- Industry news and partnerships

### Afternoon Content (AI Focus)
- AI research and model developments
- Machine learning applications in HPC
- AI infrastructure and tooling
- Ethical considerations and best practices

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write tests for new functionality
- Update documentation as needed
- Use meaningful commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- HPCWire, DOE, Argonne National Laboratory, Oak Ridge National Laboratory for content inspiration
- The open-source community for amazing tools and libraries
- All contributors who help improve this project

## 📞 Support

For support, questions, or feature requests:
- Open an issue on GitHub
- Contact: last.kakas.1989@gmail.com

---

**Built with ❤️ for the HPC and AI communities**
