#!/usr/bin/env python3
"""
Marimo Notebook Converter
Converts Jupyter notebooks to Marimo notebooks and vice versa
"""

import json
import re
import sys
import argparse
from pathlib import Path
try:
    import nbformat
except ImportError:
    print("Warning: nbformat not installed. Install with: pip install nbformat")
    nbformat = None

def extract_imports_from_cell(code):
    """Extract import statements from a cell"""
    imports = []
    lines = code.split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(('import ', 'from ')):
            imports.append(stripped)
    return imports

def extract_variables_from_cell(code):
    """Extract variable assignments from a cell"""
    variables = []
    # Simple regex for variable assignment
    pattern = r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*='
    lines = code.split('\n')
    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            variables.append(match.group(1))
    return variables

def convert_jupyter_to_marimo(notebook_path, output_path=None):
    """Convert Jupyter notebook to Marimo notebook"""
    if nbformat is None:
        raise ImportError("nbformat is required for Jupyter conversion")

    notebook_path = Path(notebook_path)
    if output_path is None:
        output_path = notebook_path.with_suffix('.py')

    # Load Jupyter notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Initialize Marimo code
    marimo_code = """import marimo

app = marimo.App()

"""

    # Track all imports and variables
    all_imports = []
    all_variables = []

    # Convert each cell
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            source = cell.source.strip()
            if not source:
                continue

            # Extract imports from this cell
            cell_imports = extract_imports_from_cell(source)
            all_imports.extend(cell_imports)

            # Extract variables from this cell
            cell_variables = extract_variables_from_cell(source)
            all_variables.extend(cell_variables)

            # Create marimo cell
            marimo_code += f"@app.cell\ndef __cell_{i}():\n"
            marimo_code += f'    """Cell {i+1}: {cell.get("metadata", {}).get("name", "")}"""\n'

            # Add the code
            for line in source.split('\n'):
                marimo_code += f'    {line}\n'

            # Return variables that might be used by other cells
            if cell_variables:
                vars_str = ', '.join(cell_variables)
                marimo_code += f'    return {vars_str}\n\n'

    # Add main execution
    marimo_code += """
if __name__ == "__main__":
    app.run()
"""

    # Write the marimo notebook
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(marimo_code)

    print(f"✅ Converted {notebook_path} to {output_path}")
    print(f"📊 Found {len(nb.cells)} cells")
    print(f"📦 Extracted {len(set(all_imports))} unique imports")
    return output_path

def extract_marimo_cells(file_path):
    """Extract cell content from Marimo notebook"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all cell functions
    cell_pattern = r'@app\.cell\s*\ndef\s+__([a-zA-Z0-9_]+)\([^)]*\):\s*"""([^"]*)"""\s*(.*?)(?=\s*@app\.cell|\s*if\s+__name__|\s*$)'

    cells = []
    matches = re.findall(cell_pattern, content, re.DOTALL)

    for i, (cell_name, docstring, cell_code) in enumerate(matches):
        # Clean up the cell code
        cell_code = cell_code.strip()
        # Remove extra indentation
        lines = cell_code.split('\n')
        dedented_lines = []
        for line in lines:
            if line.strip():  # Skip empty lines
                # Remove 4 spaces of indentation
                dedented_lines.append(line[4:] if line.startswith('    ') else line)
            else:
                dedented_lines.append('')

        cleaned_code = '\n'.join(dedented_lines)

        # Remove return statements at the end if they exist
        return_pattern = r'return\s+.*$'
        cleaned_lines = []
        for line in cleaned_code.split('\n'):
            if not re.match(return_pattern, line.strip()):
                cleaned_lines.append(line)

        final_code = '\n'.join(cleaned_lines).strip()

        cells.append({
            'cell_type': 'code',
            'source': final_code,
            'metadata': {'name': docstring.strip() or f'Cell {i+1}'}
        })

    return cells

def convert_marimo_to_jupyter(marimo_path, output_path=None):
    """Convert Marimo notebook to Jupyter notebook"""
    if nbformat is None:
        raise ImportError("nbformat is required for Jupyter conversion")

    marimo_path = Path(marimo_path)
    if output_path is None:
        output_path = marimo_path.with_suffix('.ipynb')

    # Extract cells from Marimo notebook
    cells = extract_marimo_cells(marimo_path)

    # Create Jupyter notebook structure
    nb = nbformat.v4.new_notebook()
    nb.cells = cells

    # Write the Jupyter notebook
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

    print(f"✅ Converted {marimo_path} to {output_path}")
    print(f"📊 Created {len(cells)} cells")
    return output_path

def analyze_marimo_notebook(file_path):
    """Analyze Marimo notebook and provide insights"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract cells
    cells = extract_marimo_cells(file_path)

    # Analyze imports
    all_imports = []
    for cell in cells:
        cell_imports = extract_imports_from_cell(cell['source'])
        all_imports.extend(cell_imports)

    unique_imports = list(set(all_imports))

    # Analyze UI elements
    ui_elements = []
    ui_patterns = [
        r'marimo\.ui\.\w+',
        r'mo\.\w+',
        r'\.ui\.\w+'
    ]

    for cell in cells:
        for pattern in ui_patterns:
            matches = re.findall(pattern, cell['source'])
            ui_elements.extend(matches)

    unique_ui = list(set(ui_elements))

    # Print analysis
    print(f"📊 Marimo Notebook Analysis: {file_path}")
    print(f"🔢 Total cells: {len(cells)}")
    print(f"📦 Unique imports: {len(unique_imports)}")

    if unique_imports:
        print("\n📦 Imports found:")
        for imp in sorted(unique_imports):
            print(f"  • {imp}")

    if unique_ui:
        print(f"\n🎛️  UI elements found: {len(unique_ui)}")
        for ui in sorted(unique_ui):
            print(f"  • {ui}")

    # Check for common issues
    issues = []

    # Check for print statements
    for i, cell in enumerate(cells):
        if 'print(' in cell['source']:
            issues.append(f"Cell {i+1}: Contains print statement (consider using marimo UI)")

    # Check for hardcoded file paths
    for i, cell in enumerate(cells):
        if '.csv"' in cell['source'] or '.json"' in cell['source']:
            issues.append(f"Cell {i+1}: Hardcoded file path detected")

    if issues:
        print(f"\n⚠️  Potential issues:")
        for issue in issues:
            print(f"  • {issue}")

    return {
        'cells': len(cells),
        'imports': unique_imports,
        'ui_elements': unique_ui,
        'issues': issues
    }

def create_marimo_template(template_type, output_path):
    """Create a Marimo notebook template"""

    templates = {
        'basic': '''
import marimo

app = marimo.App()

@app.cell
def __():
    """Load libraries and setup"""
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    return pd, np, plt

@app.cell
def __(pd):
    """Load data"""
    # Replace with your data source
    df = pd.read_csv("your_data.csv")
    return df

@app.cell
def __(df):
    """Process data"""
    # Add your data processing here
    processed_df = df.copy()
    return processed_df

@app.cell
def __(df, plt):
    """Create visualization"""
    plt.figure(figsize=(10, 6))
    plt.plot(df['x'], df['y'])
    plt.title("Your Data Visualization")
    plt.xlabel("X axis")
    plt.ylabel("Y axis")
    plt.show()

if __name__ == "__main__":
    app.run()
''',
        'dashboard': '''
import marimo

app = marimo.App(width="full")

@app.cell
def __():
    """Import libraries"""
    import pandas as pd
    import plotly.express as px
    import marimo as mo
    return pd, px, mo

@app.cell
def __(mo):
    """Create UI controls"""
    category = mo.ui.dropdown(
        options=["Option 1", "Option 2", "Option 3"],
        value="Option 1"
    )
    slider = mo.ui.slider(1, 100, value=50)
    return category, slider

@app.cell
def __(category, slider):
    """Process data based on UI controls"""
    import pandas as pd
    import numpy as np

    # Create sample data
    data = pd.DataFrame({
        'x': range(100),
        'y': np.random.randn(100) * slider.value,
        'category': [category.value] * 100
    })

    return data

@app.cell
def __(data, px):
    """Create visualization"""
    fig = px.scatter(data, x='x', y='y', color='category')
    fig.update_layout(title="Interactive Dashboard")
    return fig

if __name__ == "__main__":
    app.run()
''',
        'ml': '''
import marimo

app = marimo.App()

@app.cell
def __():
    """Import ML libraries"""
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error, r2_score
    import plotly.express as px
    return pd, np, train_test_split, LinearRegression, mean_squared_error, r2_score, px

@app.cell
def __(pd):
    """Load and prepare data"""
    # Sample data - replace with your dataset
    np.random.seed(42)
    n_samples = 1000
    X = np.random.randn(n_samples, 3)
    y = X[:, 0] * 2 + X[:, 1] * 0.5 + X[:, 2] * 1.5 + np.random.randn(n_samples) * 0.1

    df = pd.DataFrame(X, columns=['feature_1', 'feature_2', 'feature_3'])
    df['target'] = y
    return df

@app.cell
def __(df, train_test_split):
    """Split data"""
    X = df[['feature_1', 'feature_2', 'feature_3']]
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test

@app.cell
def __(X_train, y_train, LinearRegression):
    """Train model"""
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

@app.cell
def __(model, X_test, y_test, mean_squared_error, r2_score):
    """Evaluate model"""
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    metrics = {
        'MSE': mse,
        'R2': r2,
        'Intercept': model.intercept_,
        'Coefficients': model.coef_
    }

    return metrics, y_pred

@app.cell
def __(metrics):
    """Display metrics"""
    import marimo as mo

    metrics_df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Value'])
    return mo.ui.table(metrics_df)

if __name__ == "__main__":
    app.run()
'''
    }

    if template_type not in templates:
        print(f"❌ Unknown template type: {template_type}")
        print(f"Available templates: {list(templates.keys())}")
        return None

    template_content = templates[template_type]

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template_content)

    print(f"✅ Created {template_type} template: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description='Marimo Notebook Converter and Analyzer')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Convert Jupyter to Marimo
    j2m_parser = subparsers.add_parser('j2m', help='Convert Jupyter to Marimo')
    j2m_parser.add_argument('input', help='Input Jupyter notebook (.ipynb)')
    j2m_parser.add_argument('-o', '--output', help='Output Marimo notebook (.py)')

    # Convert Marimo to Jupyter
    m2j_parser = subparsers.add_parser('m2j', help='Convert Marimo to Jupyter')
    m2j_parser.add_argument('input', help='Input Marimo notebook (.py)')
    m2j_parser.add_argument('-o', '--output', help='Output Jupyter notebook (.ipynb)')

    # Analyze Marimo notebook
    analyze_parser = subparsers.add_parser('analyze', help='Analyze Marimo notebook')
    analyze_parser.add_argument('input', help='Marimo notebook to analyze')

    # Create template
    template_parser = subparsers.add_parser('template', help='Create Marimo template')
    template_parser.add_argument('type', choices=['basic', 'dashboard', 'ml'], help='Template type')
    template_parser.add_argument('-o', '--output', required=True, help='Output file path')

    args = parser.parse_args()

    if args.command == 'j2m':
        convert_jupyter_to_marimo(args.input, args.output)
    elif args.command == 'm2j':
        convert_marimo_to_jupyter(args.input, args.output)
    elif args.command == 'analyze':
        analyze_marimo_notebook(args.input)
    elif args.command == 'template':
        create_marimo_template(args.type, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()