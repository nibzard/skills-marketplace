"""
Marimo Notebook Patterns Library
Common patterns and code structures for marimo notebooks
"""

class MarimoPatterns:
    """Collection of reusable marimo notebook patterns"""

    # BASIC PATTERNS
    BASIC_APP = '''
import marimo

app = marimo.App(
    title="Your App Title",
    width="full"
)

@app.cell
def __():
    """Load libraries and setup"""
    import pandas as pd
    import numpy as np
    import plotly.express as px
    return pd, np, px

@app.cell
def __(pd):
    """Load or create data"""
    # Replace with your data source
    data = pd.DataFrame({
        'x': range(100),
        'y': np.random.randn(100)
    })
    return data

if __name__ == "__main__":
    app.run()
'''

    # DATA LOADING PATTERNS
    CSV_LOADER = '''
@app.cell
def __(pd):
    """Load CSV data"""
    df = pd.read_csv("data.csv")
    return df
'''

    EXCEL_LOADER = '''
@app.cell
def __(pd):
    """Load Excel data"""
    df = pd.read_excel("data.xlsx", sheet_name="Sheet1")
    return df
'''

    SQL_LOADER = '''
@app.cell
def __(conn):
    """Load data from SQL"""
    query = "SELECT * FROM table_name WHERE condition = ?"
    df = pd.read_sql(query, conn, params=["value"])
    return df
'''

    API_LOADER = '''
@app.cell
def __(requests, pd):
    """Load data from API"""
    import requests

    response = requests.get("https://api.example.com/data")
    data = response.json()
    df = pd.DataFrame(data)
    return df
'''

    # UI CONTROL PATTERNS
    BASIC_CONTROLS = '''
@app.cell
def __(mo):
    """Create basic UI controls"""
    slider = mo.ui.slider(1, 100, value=50, label="Value")
    dropdown = mo.ui.dropdown(["A", "B", "C"], value="A", label="Choice")
    text_input = mo.ui.text(value="", label="Enter text")
    checkbox = mo.ui.checkbox(value=True, label="Enable")

    return slider, dropdown, text_input, checkbox
'''

    FILTER_CONTROLS = '''
@app.cell
def __(mo, df):
    """Create data filtering controls"""
    categories = mo.ui.multiselect(
        options=list(df['category'].unique()),
        value=list(df['category'].unique()),
        label="Categories"
    )

    date_range = mo.ui.date_range(
        start=df['date'].min().date(),
        end=df['date'].max().date(),
        label="Date Range"
    )

    threshold = mo.ui.slider(
        start=df['value'].min(),
        end=df['value'].max(),
        value=df['value'].min(),
        label="Minimum Value"
    )

    return categories, date_range, threshold
'''

    # DATA PROCESSING PATTERNS
    DATA_CLEANING = '''
@app.cell
def __(df):
    """Clean and preprocess data"""
    # Remove duplicates
    df = df.drop_duplicates()

    # Handle missing values
    df = df.dropna()  # or df.fillna(value)

    # Convert data types
    df['date_column'] = pd.to_datetime(df['date_column'])
    df['category'] = df['category'].astype('category')

    # Create derived columns
    df['new_column'] = df['col1'] + df['col2']

    return df
'''

    DATA_FILTERING = '''
@app.cell
def __(df, categories, date_range, threshold):
    """Filter data based on UI controls"""
    filtered_df = df.copy()

    # Category filter
    if categories.value:
        filtered_df = filtered_df[filtered_df['category'].isin(categories.value)]

    # Date filter
    start_date, end_date = date_range.value
    filtered_df = filtered_df[
        (filtered_df['date'].dt.date >= start_date) &
        (filtered_df['date'].dt.date <= end_date)
    ]

    # Threshold filter
    filtered_df = filtered_df[filtered_df['value'] >= threshold.value]

    return filtered_df
'''

    AGGREGATION = '''
@app.cell
def __(filtered_df):
    """Aggregate data for analysis"""
    # Group by category
    category_summary = filtered_df.groupby('category').agg({
        'value': ['sum', 'mean', 'count'],
        'amount': 'sum'
    }).round(2)

    category_summary.columns = ['Total', 'Average', 'Count', 'Amount']

    # Time-based aggregation
    daily_data = filtered_df.groupby(filtered_df['date'].dt.date).agg({
        'value': 'sum',
        'amount': 'sum'
    }).reset_index()

    return category_summary, daily_data
'''

    # VISUALIZATION PATTERNS
    PLOTLY_LINE = '''
@app.cell
def __(px, daily_data):
    """Create line chart with Plotly"""
    fig = px.line(
        daily_data,
        x='date',
        y='value',
        title="Daily Trends",
        labels={'date': 'Date', 'value': 'Value'}
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Value",
        hovermode='x unified'
    )

    return fig
'''

    PLOTLY_BAR = '''
@app.cell
def __(px, category_summary):
    """Create bar chart with Plotly"""
    fig = px.bar(
        category_summary.reset_index(),
        x='category',
        y=['Total', 'Average'],
        title="Category Comparison",
        barmode='group',
        labels={'category': 'Category', 'value': 'Amount'}
    )

    fig.update_layout(
        xaxis_title="Category",
        yaxis_title="Amount"
    )

    return fig
'''

    PLOTLY_SCATTER = '''
@app.cell
def __(px, df):
    """Create scatter plot with Plotly"""
    fig = px.scatter(
        df,
        x='x_column',
        y='y_column',
        color='category_column',
        size='size_column',
        title="Scatter Plot Analysis",
        hover_data=['additional_info']
    )

    fig.update_layout(
        xaxis_title="X Variable",
        yaxis_title="Y Variable"
    )

    return fig
'''

    # INTERACTIVE DASHBOARD PATTERNS
    DASHBOARD_LAYOUT = '''
@app.cell
def __(mo, chart1, chart2, summary_table):
    """Create dashboard layout"""
    dashboard = mo.md(
        f"""
        # 📊 Interactive Dashboard

        ## 📈 Key Metrics
        {summary_table}

        ## 📊 Charts
        {chart1}

        {chart2}
        """
    )

    return dashboard
'''

    TABS_LAYOUT = '''
@app.cell
def __(mo, data_tab, analysis_tab, settings_tab):
    """Create tabbed layout"""
    tabs = mo.tabs(
        {
            "📊 Data": data_tab,
            "📈 Analysis": analysis_tab,
            "⚙️ Settings": settings_tab
        }
    )

    return tabs
'''

    ACCORDION_LAYOUT = '''
@app.cell
def __(mo, info_content, chart_content, table_content):
    """Create accordion layout"""
    accordion = mo.accordion(
        {
            "📋 Overview": info_content,
            "📊 Visualization": chart_content,
            "📋 Data": table_content
        }
    )

    return accordion
'''

    # SQL INTEGRATION PATTERNS
    SQL_QUERY_PATTERN = '''
@app.cell
def __(conn, sql):
    """Execute SQL query with marimo.sql"""
    query = """
        SELECT
            category,
            COUNT(*) as transactions,
            SUM(amount) as total_amount,
            AVG(amount) as avg_amount
        FROM sales
        WHERE date BETWEEN ? AND ?
        GROUP BY category
        ORDER BY total_amount DESC
    """

    start_date, end_date = date_range.value  # Assuming date_range from UI

    result = sql(query, conn, params=[start_date, end_date])
    return result
'''

    SQL_TABLE_CREATION = '''
@app.cell
def __(df, conn):
    """Create and populate SQL table from DataFrame"""
    # Create table from DataFrame
    df.to_sql('table_name', conn, index=False, if_exists='replace')

    # Verify table creation
    verification_query = "SELECT COUNT(*) FROM table_name"
    count = sql(verification_query, conn)

    return count
'''

    # MACHINE LEARNING PATTERNS
    ML_DATA_PREP = '''
@app.cell
def __(df):
    """Prepare data for machine learning"""
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler

    # Select features and target
    features = df[['feature1', 'feature2', 'feature3']]
    target = df['target']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler
'''

    ML_MODEL_TRAINING = '''
@app.cell
def __(X_train, y_train):
    """Train machine learning model"""
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_squared_error, r2_score

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    return model
'''

    ML_MODEL_EVALUATION = '''
@app.cell
def __(model, X_test, y_test):
    """Evaluate machine learning model"""
    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Create results DataFrame
    results = pd.DataFrame({
        'Actual': y_test,
        'Predicted': y_pred,
        'Error': y_test - y_pred
    })

    metrics = {
        'MSE': mse,
        'R²': r2,
        'RMSE': np.sqrt(mse)
    }

    return results, metrics
'''

    # ERROR HANDLING PATTERNS
    ERROR_HANDLING = '''
@app.cell
def __(file_path, pd):
    """Load data with error handling"""
    try:
        df = pd.read_csv(file_path)
        return df, None
    except FileNotFoundError:
        return None, f"File not found: {file_path}"
    except pd.errors.EmptyDataError:
        return None, f"File is empty: {file_path}"
    except Exception as e:
        return None, f"Error loading file: {str(e)}"
'''

    VALIDATION = '''
@app.cell
def __(df, mo):
    """Validate data with error reporting"""
    errors = []

    # Check required columns
    required_columns = ['date', 'amount', 'category']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing columns: {missing_columns}")

    # Check data types
    if 'date' in df.columns:
        try:
            pd.to_datetime(df['date'])
        except:
            errors.append("Invalid date format")

    # Check for negative amounts
    if 'amount' in df.columns and (df['amount'] < 0).any():
        errors.append("Negative amounts found")

    # Return validation results
    if errors:
        return mo.md(f"❌ **Validation Errors:**\\n" + "\\n".join(f"- {error}" for error in errors))
    else:
        return mo.md("✅ **Data validation passed**")
'''

    # PERFORMANCE PATTERNS
    CACHING = '''
@app.cell
@marimo.cache
def __(file_path):
    """Cache expensive data loading operation"""
    import time
    start_time = time.time()

    df = pd.read_csv(file_path)

    load_time = time.time() - start_time
    print(f"Data loaded in {load_time:.2f} seconds")

    return df
'''

    LAZY_LOADING = '''
@app.cell
def __(file_path):
    """Implement lazy data loading"""
    def load_data():
        return pd.read_csv(file_path)

    # Only load when actually needed
    if not hasattr(load_data, '_loaded'):
        load_data._data = load_data()
        load_data._loaded = True

    return load_data._data
'''

    # EXPORT PATTERNS
    CSV_EXPORT = '''
@app.cell
def __(filtered_df, mo):
    """Export filtered data to CSV"""
    export_button = mo.ui.button(label="Export to CSV", kind="success")

    def export_data():
        if export_button.value:
            filename = f"exported_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filtered_df.to_csv(filename, index=False)
            return f"✅ Data exported to {filename}"
        return "Click export to save data"

    export_message = export_data()
    return export_button, export_message
'''

    @staticmethod
    def get_pattern(pattern_name: str) -> str:
        """Get a specific pattern by name"""
        return getattr(MarimoPatterns, pattern_name, "# Pattern not found")

    @staticmethod
    def list_patterns() -> list:
        """List all available patterns"""
        return [attr for attr in dir(MarimoPatterns)
                if not attr.startswith('_') and attr != 'get_pattern' and attr != 'list_patterns']