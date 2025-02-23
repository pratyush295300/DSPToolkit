# Contributing to DSPToolkit

Thank you for your interest in contributing to DSPToolkit! This document outlines the guidelines for contributing to this project.

## Security Guidelines

1. Input Validation
- Always validate signal parameters
- Check array bounds
- Verify sampling rates
- Validate frequency ranges

2. Memory Safety
- Implement size checks for large arrays
- Use secure memory handling
- Avoid buffer overflows
- Clean up resources properly

3. Random Number Generation
- Use cryptographically secure RNG
- Avoid predictable sequences
- Validate random data quality

4. Error Handling
- Implement proper exception handling
- Log errors securely
- Don't expose sensitive information

## Code Style

1. Python Standards
- Follow PEP 8 guidelines
- Use type hints
- Document functions with docstrings
- Keep functions focused and small

2. Documentation
- Update README.md for new features
- Document security implications
- Include usage examples
- Update requirements.txt

3. Testing
- Write unit tests for new features
- Include security test cases
- Test edge cases
- Verify memory usage

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add/update tests
5. Update documentation
6. Submit a pull request

## Development Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
python -m pytest tests/
```

## Contact

For questions or discussions:
- GitHub: [pratyush295300](https://github.com/pratyush295300)
- Email: pratyushpadhi04@gmail.com

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Follow security best practices
- Maintain professional communication
