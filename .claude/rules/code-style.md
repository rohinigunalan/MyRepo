---
name: code-style
description: Code formatting and style conventions for all projects
globs:
  - "**/*.py"
  - "**/*.js"
  - "**/*.ts"
---

# Code Style Conventions

General code style rules that apply across all projects under Main.

## Python Style (PEP 8)

### Formatting
- **Line length**: 88 characters (Black default)
- **Indentation**: 4 spaces (never tabs)
- **Encoding**: UTF-8
- **Line endings**: LF (Unix style)

### Imports
```python
# Standard library
import os
import sys

# Third-party
import pytest
import playwright

# Local
from src.module import function
```

**Rules:**
- One import per line (except `from x import a, b`)
- Alphabetical order within groups
- No wildcard imports (`from module import *`)
- Remove unused imports

### Naming Conventions
```python
# Variables and functions: snake_case
user_name = "John"
def calculate_total():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3
API_URL = "https://api.example.com"

# Classes: PascalCase
class UserProfile:
    pass

# Private: _leading_underscore
def _internal_function():
    pass
```

### Strings
- Use double quotes `"` for regular strings
- Use single quotes `'` for dict keys and short literals
- Use f-strings for formatting:
  ```python
  # Good
  message = f"Hello {name}, you have {count} messages"

  # Bad
  message = "Hello %s, you have %d messages" % (name, count)
  message = "Hello {}, you have {} messages".format(name, count)
  ```

### Docstrings
```python
def function_name(param1: str, param2: int) -> bool:
    """Brief one-line description.

    Longer explanation if needed. Describe behavior,
    edge cases, and important details.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When input is invalid
    """
    pass
```

**Rules:**
- Use triple double-quotes `"""`
- Required for public functions/classes
- Optional for simple private functions
- Use Google style docstrings

### Comments
```python
# Good - explains WHY
# Retry 3 times because the API is flaky under load
for attempt in range(3):
    try:
        response = api_call()
        break
    except APIError:
        time.sleep(1)

# Bad - explains WHAT (obvious from code)
# Loop 3 times
for attempt in range(3):
    pass
```

**Rules:**
- Explain "why", not "what"
- Keep comments up-to-date with code
- Remove commented-out code before committing
- Use `# TODO:` for temporary notes

### Whitespace
```python
# Good
def function(arg1, arg2):
    x = 1 + 2
    result = function(a, b)
    return result

# Bad
def function( arg1,arg2 ):
    x=1+2
    result = function (a,b)
    return result
```

**Rules:**
- One blank line between functions
- Two blank lines between classes
- No trailing whitespace
- File ends with single newline

### Functions
```python
# Good - single responsibility
def validate_email(email: str) -> bool:
    """Check if email format is valid."""
    return "@" in email and "." in email.split("@")[1]

def send_email(to: str, subject: str, body: str) -> None:
    """Send email to recipient."""
    # Implementation

# Bad - doing too much
def validate_and_send_email(email: str, subject: str, body: str):
    if "@" not in email:
        return False
    # Send email logic...
    return True
```

**Rules:**
- Functions should do ONE thing
- Keep functions under 50 lines
- Max 5 parameters (use dataclass/dict if more)
- Prefer explicit over implicit

### Error Handling
```python
# Good - specific exceptions
try:
    user = get_user(user_id)
except UserNotFoundError:
    logger.error(f"User {user_id} not found")
    raise
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    # Handle or re-raise

# Bad - bare except
try:
    user = get_user(user_id)
except:  # Never do this!
    pass
```

**Rules:**
- Catch specific exceptions
- Never use bare `except:`
- Log errors before re-raising
- Don't swallow exceptions silently

## JavaScript/TypeScript Style

### Formatting
- **Line length**: 100 characters
- **Indentation**: 2 spaces
- **Semicolons**: Always use
- **Quotes**: Single quotes `'` for strings

### Naming
```javascript
// Variables/functions: camelCase
const userName = 'John';
function calculateTotal() {}

// Constants: UPPER_SNAKE_CASE
const MAX_RETRIES = 3;

// Classes: PascalCase
class UserProfile {}

// Private: #prefix (ES2022+)
class MyClass {
  #privateField;
}
```

### Modern Syntax
```javascript
// Use const/let, not var
const items = [1, 2, 3];
let count = 0;

// Arrow functions
const add = (a, b) => a + b;

// Destructuring
const { name, age } = user;
const [first, ...rest] = array;

// Template literals
const message = `Hello ${name}`;

// Optional chaining
const city = user?.address?.city;

// Nullish coalescing
const value = input ?? defaultValue;
```

## General Principles

### DRY (Don't Repeat Yourself)
- Extract repeated code into functions
- Use loops instead of copy-paste
- Create reusable utilities

### KISS (Keep It Simple, Stupid)
- Simple solutions over clever ones
- Readable over concise
- Avoid premature optimization

### YAGNI (You Aren't Gonna Need It)
- Don't add features you don't need now
- Don't over-engineer for hypothetical future
- Build for current requirements

### Code Organization
```
# Good structure
if condition:
    do_something()
    do_another_thing()
else:
    do_alternative()

# Bad nesting
if condition1:
    if condition2:
        if condition3:
            if condition4:
                do_something()
```

**Rules:**
- Max 3 levels of nesting
- Early returns to reduce nesting
- Extract complex conditions to variables/functions

### Magic Numbers
```python
# Bad
if retries > 3:
    pass

# Good
MAX_RETRIES = 3
if retries > MAX_RETRIES:
    pass
```

### Type Hints (Python)
```python
# Good
def process_user(user_id: int, active: bool = True) -> dict:
    """Process user data."""
    pass

# Better with complex types
from typing import Optional, List, Dict

def get_users(
    ids: List[int],
    filters: Optional[Dict[str, str]] = None
) -> List[dict]:
    """Get multiple users."""
    pass
```

**Rules:**
- Use type hints for function signatures
- Use `Optional[T]` for nullable values
- Use `List[T]`, `Dict[K, V]` for collections
- Not required for simple internal functions

## Tools

### Formatters
- **Python**: Black (`black src/ tests/`)
- **JavaScript**: Prettier (`prettier --write src/`)

### Linters
- **Python**: flake8, pylint
- **JavaScript**: ESLint

### Pre-commit Checks
Run before every commit:
```bash
# Format code
black src/ tests/

# Check style
flake8 src/ tests/

# Run tests
pytest tests/
```

## When to Break Rules

Rules are guidelines. Break them when:
- Following the rule makes code less readable
- There's a strong performance reason
- External API/library requires different style
- Team agrees on exception

**But**: Document why you broke the rule!

---

*Style consistency matters more than personal preference*
