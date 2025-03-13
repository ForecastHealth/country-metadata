# country-metadata Project Guidelines

## Build & Test Commands
- Install package: `pip install .` 
- Run all tests: `python -m unittest`
- Run a single test: `python -m unittest tests.test_api.TestAPI.test_get_country` (replace test_get_country with specific test)

## Code Style Guidelines

### Python Style
- Use snake_case for functions/variables: `get_country`, `country_code`
- Use CamelCase for classes: `Country`, `Tag`
- Use UPPER_CASE for constants: `ACCEPTED_TAGS`

### Type Hints
- All function signatures must include type hints
- Use typing module: Union, Optional, List, Dict, Tuple
- Explicitly declare return types

### Imports
- Group imports: standard library first, then internal
- Use relative imports for internal modules: `from .tags import ...`

### Error Handling
- Use Optional types for functions that might return None
- Raise ValueError with descriptive messages for invalid inputs
- Return None for lookups with no match

### Documentation
- Use triple-quoted docstrings for modules and functions
- Explain purpose and parameters in docstrings