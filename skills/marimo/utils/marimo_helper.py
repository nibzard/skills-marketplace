#!/usr/bin/env python3
"""
Marimo Notebook Helper Utilities
Helper functions and tools for marimo notebook development and debugging
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import json

def check_marimo_installation():
    """Check if marimo is installed and return version info"""
    try:
        import marimo
        version = getattr(marimo, '__version__', 'unknown')
        return {
            'installed': True,
            'version': version,
            'location': marimo.__file__
        }
    except ImportError:
        return {
            'installed': False,
            'version': None,
            'location': None,
            'suggestion': 'Install with: pip install marimo or uv add marimo'
        }

def validate_marimo_notebook(file_path: str) -> Dict:
    """Validate marimo notebook syntax and structure"""
    issues = []
    warnings = []

    if not Path(file_path).exists():
        return {'valid': False, 'error': f'File not found: {file_path}'}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for marimo import
        if 'import marimo' not in content:
            issues.append('Missing marimo import')

        # Check for app creation
        if 'marimo.App()' not in content:
            issues.append('Missing marimo.App() creation')

        # Check for @app.cell decorators
        if '@app.cell' not in content:
            issues.append('Missing @app.cell decorators')

        # Check for main execution
        if 'if __name__ == "__main__":' not in content:
            warnings.append('Missing main execution block')

        # Check for syntax errors
        try:
            compile(content, file_path, 'exec')
        except SyntaxError as e:
            issues.append(f'Syntax error: {e}')

        # Analyze cell dependencies
        cells = re.findall(r'@app\.cell\s*\ndef\s+__([a-zA-Z0-9_]+)\([^)]*\):', content)
        if not cells:
            issues.append('No valid cell definitions found')

        # Check for potential circular dependencies
        dependencies = {}
        for i, cell_name in enumerate(cells):
            # Find function definition
            cell_pattern = rf'@app\.cell\s*\def\s+__{re.escape(cell_name)}\([^)]*\):(.*?)(?=@app\.cell|\Z)'
            cell_match = re.search(cell_pattern, content, re.DOTALL)
            if cell_match:
                cell_code = cell_match.group(1)
                # Find variable references
                var_refs = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', cell_code)
                dependencies[cell_name] = var_refs

        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'cells': len(cells),
            'dependencies': dependencies
        }

    except Exception as e:
        return {'valid': False, 'error': f'Validation failed: {e}'}

def analyze_marimo_notebook(file_path: str) -> Dict:
    """Analyze marimo notebook structure and components"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract imports
        imports = re.findall(r'^(?:from\s+(\S+)\s+)?import\s+(.+)', content, re.MULTILINE)

        # Extract UI elements
        ui_elements = re.findall(r'(\w+)\.ui\.\w+', content)
        ui_types = re.findall(r'\.ui\.\w+', content)

        # Extract plotly/visualization elements
        plot_elements = re.findall(r'px\.|plt\.|fig\.|plotly', content)

        # Extract database operations
        db_operations = re.findall(r'sql|pd\.read_sql|execute|query', content, re.IGNORECASE)

        # Extract file operations
        file_ops = re.findall(r'\.read_csv|\.to_csv|\.read_excel|\.to_excel', content)

        return {
            'imports': imports,
            'ui_elements': list(set(ui_elements)),
            'ui_types': list(set(ui_types)),
            'visualizations': len(plot_elements),
            'database_operations': len(db_operations),
            'file_operations': len(file_ops),
            'complexity_score': len(ui_elements) + len(plot_elements) + len(db_operations)
        }
    except Exception as e:
        return {'error': f'Analysis failed: {e}'}

def run_marimo_notebook(file_path: str, mode: str = 'edit', port: int = 8080) -> Dict:
    """Run marimo notebook with specified mode"""
    if not Path(file_path).exists():
        return {'success': False, 'error': f'File not found: {file_path}'}

    try:
        cmd = ['marimo', mode, file_path]
        if mode == 'run':
            cmd.extend(['--port', str(port)])

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        return {
            'success': True,
            'pid': process.pid,
            'command': ' '.join(cmd),
            'mode': mode,
            'port': port if mode == 'run' else None
        }
    except FileNotFoundError:
        return {
            'success': False,
            'error': 'marimo command not found. Install with: pip install marimo'
        }
    except Exception as e:
        return {'success': False, 'error': f'Failed to run notebook: {e}'}

def create_marimo_project(project_name: str, template_type: str = 'basic') -> Dict:
    """Create a new marimo project structure"""
    project_dir = Path(project_name)

    try:
        project_dir.mkdir(exist_ok=True)

        # Create basic notebook template
        notebook_content = f'''import marimo

app = marimo.App(
    title="{project_name.replace('_', ' ').title()}",
    width="full"
)

@app.cell
def __(load_libraries):
    """Load necessary libraries"""
    import pandas as pd
    import numpy as np
    return pd, np

@app.cell
def __(setup_data):
    """Setup your data here"""
    # Replace with your data source
    # df = pd.read_csv("your_data.csv")
    # df = pd.read_excel("your_data.xlsx")

    # Sample data for demonstration
    sample_data = pd.DataFrame({{
        'x': range(10),
        'y': [i**2 for i in range(10)]
    }})
    return sample_data

@app.cell
def __(create_visualization, setup_data):
    """Create your visualization"""
    import plotly.express as px

    fig = px.line(setup_data, x='x', y='y', title="Your Data Visualization")
    return fig

@app.cell
def __(create_ui_controls):
    """Create interactive controls"""
    slider = marimo.ui.slider(1, 100, value=50)
    text_input = marimo.ui.text("Enter text here")
    return slider, text_input

if __name__ == "__main__":
    app.run()
'''

        notebook_path = project_dir / f"{project_name}.py"
        with open(notebook_path, 'w', encoding='utf-8') as f:
            f.write(notebook_content)

        # Create README
        readme_content = f'''# {project_name.replace('_', ' ').title()}

Marimo notebook project created with marimo-notebook skill.

## Getting Started

1. Install marimo:
   ```bash
   pip install marimo
   ```

2. Run the notebook in edit mode:
   ```bash
   marimo edit {project_name}.py
   ```

3. Run as web app:
   ```bash
   marimo run {project_name}.py
   ```

## Project Structure

- `{project_name}.py`: Main marimo notebook
- `README.md`: This file

## Customization

Edit the notebook to:
- Load your own data sources
- Create custom visualizations
- Add interactive UI elements
- Implement your specific analysis

## Resources

- [Marimo Documentation](https://docs.marimo.io)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/)
'''

        readme_path = project_dir / 'README.md'
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)

        return {
            'success': True,
            'project_path': str(project_dir),
            'notebook_path': str(notebook_path),
            'readme_path': str(readme_path)
        }
    except Exception as e:
        return {'success': False, 'error': f'Failed to create project: {e}'}

def get_marimo_snippet(snippet_type: str) -> str:
    """Get commonly used marimo code snippets"""
    snippets = {
        'basic_app': '''import marimo

app = marimo.App(width="full")

@app.cell
def __():
    """Your first cell"""
    import marimo as mo
    return mo.md("Hello, Marimo!")

if __name__ == "__main__":
    app.run()
''',

        'ui_controls': '''@app.cell
def __(create_controls):
    """Create interactive controls"""
    import marimo as mo

    # Dropdown selection
    category = mo.ui.dropdown(
        options=["Option 1", "Option 2", "Option 3"],
        value="Option 1"
    )

    # Slider control
    value = mo.ui.slider(1, 100, value=50)

    # Text input
    text = mo.ui.text("Enter text here")

    # Button
    button = mo.ui.button("Click me")

    return category, value, text, button
''',

        'data_processing': '''@app.cell
def __(process_data):
    """Process data with common operations"""
    import pandas as pd
    import numpy as np

    # Load data
    df = pd.read_csv("data.csv")

    # Basic operations
    df = df.dropna()  # Remove missing values
    df['new_column'] = df['column'] * 2  # Create new column
    filtered_df = df[df['value'] > 0]  # Filter data

    return filtered_df
''',

        'visualization': '''@app.cell
def __(create_chart):
    """Create interactive visualization"""
    import plotly.express as px
    import pandas as pd

    # Sample data
    df = pd.DataFrame({
        'x': range(100),
        'y': np.random.randn(100),
        'category': np.random.choice(['A', 'B', 'C'], 100)
    })

    # Create chart
    fig = px.scatter(
        df,
        x='x',
        y='y',
        color='category',
        title="Interactive Scatter Plot"
    )

    return fig
''',

        'sql_integration': '''@app.cell
def __(sql_integration):
    """Integrate SQL queries"""
    import marimo as mo
    from marimo.sql import sql
    import sqlite3
    import pandas as pd

    # Create database connection
    conn = sqlite3.connect(":memory:")

    # Load data into database
    df = pd.read_csv("data.csv")
    df.to_sql("table_name", conn, index=False, if_exists="replace")

    # SQL query
    query = """
        SELECT
            column1,
            column2,
            COUNT(*) as count
        FROM table_name
        WHERE condition = 'value'
        GROUP BY column1, column2
    """

    result = sql(query, conn)
    return result
'''
    }

    return snippets.get(snippet_type, f"Snippet '{snippet_type}' not found")

def suggest_optimizations(file_path: str) -> List[str]:
    """Suggest optimizations for marimo notebook"""
    suggestions = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for common patterns
        if content.count('print(') > 3:
            suggestions.append("Consider using marimo UI elements instead of multiple print statements")

        if 'import matplotlib.pyplot as plt' in content and 'plt.show()' in content:
            suggestions.append("Consider using plotly for better interactivity with marimo")

        if 'pd.read_csv(' in content:
            suggestions.append("Add caching for expensive data loading operations with @marimo.cache")

        if content.count('@app.cell') > 20:
            suggestions.append("Consider breaking large notebooks into smaller, focused ones")

        if 'while True:' in content:
            suggestions.append("Avoid infinite loops in reactive notebooks")

        if len(content) > 10000:  # Large file
            suggestions.append("Consider extracting utility functions to separate modules")

        return suggestions
    except Exception as e:
        return [f"Failed to analyze for optimizations: {e}"]

def main():
    """CLI interface for marimo helper utilities"""
    if len(sys.argv) < 2:
        print("Usage: python marimo_helper.py <command> [options]")
        print("Commands:")
        print("  check           Check marimo installation")
        print("  validate <file> Validate marimo notebook")
        print("  analyze <file>  Analyze notebook structure")
        print("  run <file>     Run marimo notebook")
        print("  create <name>   Create new marimo project")
        print("  snippet <type>  Get code snippet")
        print("  optimize <file> Suggest optimizations")
        return

    command = sys.argv[1]

    if command == 'check':
        result = check_marimo_installation()
        print(json.dumps(result, indent=2))

    elif command == 'validate' and len(sys.argv) > 2:
        result = validate_marimo_notebook(sys.argv[2])
        print(json.dumps(result, indent=2))

    elif command == 'analyze' and len(sys.argv) > 2:
        result = analyze_marimo_notebook(sys.argv[2])
        print(json.dumps(result, indent=2))

    elif command == 'run' and len(sys.argv) > 2:
        mode = sys.argv[3] if len(sys.argv) > 3 else 'edit'
        port = int(sys.argv[4]) if len(sys.argv) > 4 else 8080
        result = run_marimo_notebook(sys.argv[2], mode, port)
        print(json.dumps(result, indent=2))

    elif command == 'create' and len(sys.argv) > 2:
        result = create_marimo_project(sys.argv[2])
        print(json.dumps(result, indent=2))

    elif command == 'snippet' and len(sys.argv) > 2:
        snippet = get_marimo_snippet(sys.argv[2])
        print(snippet)

    elif command == 'optimize' and len(sys.argv) > 2:
        suggestions = suggest_optimizations(sys.argv[2])
        for suggestion in suggestions:
            print(f"• {suggestion}")

    else:
        print(f"Invalid command or missing arguments: {' '.join(sys.argv)}")

if __name__ == "__main__":
    main()