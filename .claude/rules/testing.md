---
name: testing
description: Testing standards and conventions for all test code
globs:
  - "**/test_*.py"
  - "**/*_test.py"
  - "**/tests/**/*.py"
  - "**/*.test.js"
  - "**/*.test.ts"
  - "**/*.spec.js"
  - "**/*.spec.ts"
---

# Testing Conventions

Standards for writing and organizing tests across all projects.

## Test Framework

### Python
- **Framework**: pytest (NOT unittest)
- **Coverage**: pytest-cov
- **Mocking**: pytest-mock or unittest.mock

### JavaScript/TypeScript
- **Framework**: Jest or Vitest
- **E2E**: Playwright
- **Mocking**: Jest mocks or Sinon

## Test Organization

### Directory Structure
```
project/
├── src/
│   ├── module.py
│   └── utils.py
└── tests/
    ├── unit/
    │   ├── test_module.py
    │   └── test_utils.py
    ├── integration/
    │   └── test_api.py
    ├── e2e/
    │   └── test_user_flow.py
    └── conftest.py          # Shared fixtures
```

### File Naming
- Test files: `test_*.py` or `*_test.py`
- Test functions: `test_descriptive_name()`
- Test classes: `TestFeatureName`

## Test Structure (AAA Pattern)

```python
def test_user_login():
    # Arrange - Set up test data and preconditions
    user = User(username="test", password="pass123")
    db.add(user)

    # Act - Execute the code being tested
    result = login(username="test", password="pass123")

    # Assert - Verify the results
    assert result.success is True
    assert result.user_id == user.id
```

**Rules:**
- Clear separation between Arrange, Act, Assert
- One assertion concept per test (can have multiple asserts)
- Test one thing at a time

## Naming Tests

### Descriptive Names
```python
# Good - describes what is being tested
def test_login_with_valid_credentials_returns_success():
    pass

def test_login_with_invalid_password_returns_error():
    pass

def test_user_cannot_login_when_account_disabled():
    pass

# Bad - vague names
def test_login():
    pass

def test_case1():
    pass
```

**Pattern**: `test_<what>_<condition>_<expected_result>`

## Fixtures (pytest)

### Basic Fixtures
```python
import pytest

@pytest.fixture
def user():
    """Create a test user."""
    return User(username="test", email="test@example.com")

@pytest.fixture
def db_session():
    """Create database session for testing."""
    session = create_test_session()
    yield session
    session.close()

def test_create_user(db_session, user):
    db_session.add(user)
    db_session.commit()
    assert user.id is not None
```

### Fixture Scopes
```python
@pytest.fixture(scope="function")  # Default - run per test
def per_test_fixture():
    pass

@pytest.fixture(scope="class")  # Run once per test class
def per_class_fixture():
    pass

@pytest.fixture(scope="module")  # Run once per module
def per_module_fixture():
    pass

@pytest.fixture(scope="session")  # Run once per test session
def per_session_fixture():
    pass
```

### conftest.py
Shared fixtures in `tests/conftest.py`:
```python
import pytest

@pytest.fixture(scope="session")
def browser():
    """Playwright browser for all tests."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.fixture
def context(browser):
    """New browser context per test."""
    context = browser.new_context()
    yield context
    context.close()
```

## Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("Test123", "TEST123"),
])
def test_uppercase(input, expected):
    assert input.upper() == expected

@pytest.mark.parametrize("username,password,should_succeed", [
    ("valid_user", "valid_pass", True),
    ("valid_user", "wrong_pass", False),
    ("invalid_user", "any_pass", False),
])
def test_login_scenarios(username, password, should_succeed):
    result = login(username, password)
    assert result.success == should_succeed
```

**Benefits:**
- Run same test with different inputs
- Easier to add new test cases
- Clear relationship between inputs and outputs

## Mocking

### When to Mock
- External APIs
- Database calls (in unit tests)
- File system operations
- Time-dependent code
- Third-party services

### When NOT to Mock
- Code being tested
- Simple data structures
- Internal utilities
- Integration tests

### Mock Example
```python
from unittest.mock import patch, MagicMock

def test_fetch_user_data():
    # Arrange
    mock_response = {"id": 1, "name": "John"}

    # Act
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_response
        result = fetch_user_data(user_id=1)

    # Assert
    assert result["name"] == "John"
    mock_get.assert_called_once_with("https://api.example.com/users/1")

@patch('time.sleep')  # Skip actual sleep
def test_retry_logic(mock_sleep):
    result = function_with_retry()
    assert result is not None
    assert mock_sleep.call_count == 2  # Verify retries happened
```

## Assertions

### Good Assertions
```python
# Specific and clear
assert user.is_active is True
assert len(results) == 3
assert "error" in response.json()
assert response.status_code == 200

# With helpful messages
assert user.role == "admin", f"Expected admin role, got {user.role}"
```

### pytest Assertions
```python
# Exception testing
with pytest.raises(ValueError) as exc_info:
    invalid_function()
assert "invalid input" in str(exc_info.value)

# Approximate comparisons
import pytest
assert result == pytest.approx(3.14, rel=0.01)

# Warnings
with pytest.warns(UserWarning):
    function_that_warns()
```

## Test Coverage

### Coverage Goals
- **Overall**: Minimum 80%
- **Critical paths**: 100%
- **New code**: 90%+

### Running Coverage
```bash
# Run with coverage report
pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

# See HTML report
open htmlcov/index.html

# Check specific module
pytest tests/ --cov=src.module --cov-report=term-missing
```

### Coverage Rules
- Don't chase 100% mindlessly
- Focus on business logic
- Skip trivial code (getters, setters)
- Skip generated code
- Test edge cases and error paths

## Test Types

### Unit Tests
```python
def test_calculate_total():
    """Test calculation logic in isolation."""
    items = [
        {"price": 10, "quantity": 2},
        {"price": 5, "quantity": 3},
    ]
    total = calculate_total(items)
    assert total == 35
```

**Characteristics:**
- Fast (milliseconds)
- No external dependencies
- Test single function/method
- Use mocks for dependencies

### Integration Tests
```python
def test_create_and_fetch_user(db_session):
    """Test database operations together."""
    # Create user
    user = User(username="test")
    db_session.add(user)
    db_session.commit()

    # Fetch user
    fetched = db_session.query(User).filter_by(username="test").first()
    assert fetched.username == "test"
```

**Characteristics:**
- Slower (seconds)
- Test multiple components together
- Use real dependencies (test database)
- Verify integration points

### E2E Tests
```python
def test_complete_login_flow(page):
    """Test full user login workflow."""
    page.goto("https://app.example.com")
    page.fill("#username", "test_user")
    page.fill("#password", "test_pass")
    page.click("button[type=submit]")

    # Verify redirected to dashboard
    assert page.url == "https://app.example.com/dashboard"
    assert page.is_visible("text=Welcome, test_user")
```

**Characteristics:**
- Slowest (seconds to minutes)
- Test complete user flows
- Use real environment
- Verify system behavior

## Test Data

### Factory Pattern
```python
# factories.py
class UserFactory:
    @staticmethod
    def create(**kwargs):
        defaults = {
            "username": "test_user",
            "email": "test@example.com",
            "is_active": True,
        }
        defaults.update(kwargs)
        return User(**defaults)

# In tests
def test_with_custom_user():
    user = UserFactory.create(username="custom", is_active=False)
    assert user.username == "custom"
```

### Fixtures for Test Data
```python
@pytest.fixture
def sample_users():
    return [
        User(username="alice", role="admin"),
        User(username="bob", role="user"),
        User(username="charlie", role="user"),
    ]

def test_filter_admins(sample_users):
    admins = [u for u in sample_users if u.role == "admin"]
    assert len(admins) == 1
```

## Debugging Tests

### Print Statements
```python
def test_complex_calculation():
    result = complex_function(input_data)
    print(f"Result: {result}")  # Will show with -s flag
    assert result > 0
```

Run with: `pytest tests/test_file.py -v -s`

### Debugging
```python
def test_with_debugging():
    result = function()
    import pdb; pdb.set_trace()  # Pause here
    assert result == expected
```

### Screenshots (E2E)
```python
def test_login_flow(page):
    page.goto("https://app.example.com")
    page.screenshot(path="screenshots/login_page.png")

    page.fill("#username", "test")
    page.fill("#password", "test")
    page.screenshot(path="screenshots/before_submit.png")

    page.click("button[type=submit]")
    page.screenshot(path="screenshots/after_submit.png")
```

## Test Performance

### Fast Tests
```python
# Good - fast, isolated
def test_validation():
    result = validate_email("test@example.com")
    assert result is True

# Bad - slow, depends on network
def test_api_call():
    response = requests.get("https://api.example.com/users")
    assert response.status_code == 200
```

### Skip Slow Tests
```python
@pytest.mark.slow
def test_expensive_operation():
    """Takes 30 seconds to run."""
    pass

# Run fast tests only
# pytest tests/ -m "not slow"

# Run all tests including slow
# pytest tests/
```

## What NOT to Test

- ❌ Third-party library code
- ❌ Framework code
- ❌ Trivial getters/setters
- ❌ Generated code
- ❌ Configuration files
- ❌ Constants

## Test Checklist

Before committing:
- [ ] All tests pass locally
- [ ] New code has tests
- [ ] Tests follow AAA pattern
- [ ] Test names are descriptive
- [ ] No commented-out tests
- [ ] No print statements (use logging)
- [ ] Coverage meets minimum threshold
- [ ] Tests run fast (< 5 seconds for unit tests)

## Running Tests

### Basic
```bash
# Run all tests
pytest tests/

# Run specific file
pytest tests/test_module.py

# Run specific test
pytest tests/test_module.py::test_function

# Run with verbose output
pytest tests/ -v

# Run with print statements
pytest tests/ -s

# Run with verbose + prints
pytest tests/ -v -s
```

### Advanced
```bash
# Stop on first failure
pytest tests/ -x

# Show local variables on failure
pytest tests/ -l

# Run only failed tests from last run
pytest tests/ --lf

# Run tests matching pattern
pytest tests/ -k "login"

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

---

*Good tests are your safety net for refactoring*
