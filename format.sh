#!/bin/bash
# Format and lint code using Black and Ruff

set -e

echo "🔍 Running Ruff linter..."
ruff check app/ --fix

echo "✨ Formatting code with Black..."
black app/

echo "✅ Code formatting complete!"
