---
name: data-analysis
description: Process, analyze, and visualize data from Excel spreadsheets, CSV files, and various data sources. Use when working with spreadsheets, performing statistical analysis, or creating data visualizations.
allowed-tools: Read, Write, Edit, Bash
---

# Data Analysis

## Instructions
1. **Identify Data Source**: Determine the file format (Excel, CSV, JSON) and location of the data to be analyzed
2. **Assess File Size**: Check if the file is reasonable for analysis (>100MB may require sampling)
3. **Load Data**: Read the data using appropriate methods based on file format:
   - Excel files: Use pandas `read_excel()` with proper engine
   - CSV files: Use pandas `read_csv()` with encoding detection if needed
   - JSON files: Use pandas `read_json()` or custom parsing
4. **Initial Data Exploration**:
   - Check data dimensions and structure
   - Identify data types and potential issues
   - Look for missing values and duplicates
   - Examine basic statistics (describe(), info())
5. **Data Cleaning**: Address data quality issues:
   - Handle missing values (imputation, removal)
   - Correct data types and formats
   - Remove duplicates and outliers if appropriate
   - Standardize text data and categories
6. **Statistical Analysis**:
   - Calculate descriptive statistics
   - Perform correlation analysis
   - Identify trends and patterns
   - Apply relevant statistical tests
7. **Generate Visualizations**: Create appropriate charts for data insights:
   - Use histograms for distributions
   - Scatter plots for relationships
   - Line charts for time series
   - Bar charts for comparisons
8. **Provide Insights**: Summarize key findings and actionable recommendations

## Capabilities
- Data loading from multiple formats (Excel, CSV, JSON, etc.)
- Data cleaning and preprocessing
- Statistical analysis and hypothesis testing
- Data visualization and chart creation
- Pattern recognition and trend analysis
- Anomaly detection and outlier identification

## Data Formats Supported

### Excel Files (.xlsx, .xls)
- Multiple worksheets handling
- Formatted cell preservation
- Large file optimization with chunking
- Error handling for corrupted files

### CSV Files
- Automatic delimiter detection
- Encoding handling (UTF-8, ASCII, Latin-1)
- Header identification and validation
- Quoted text and escaped characters

### JSON Files
- Nested JSON flattening
- Schema validation
- Array handling and normalization
- Missing data handling

## Statistical Methods Available

### Descriptive Statistics
- Measures of central tendency (mean, median, mode)
- Measures of dispersion (std dev, variance, range)
- Distribution analysis (skewness, kurtosis)
- Percentiles and quartiles

### Inferential Statistics
- t-tests and ANOVA for group comparisons
- Chi-square tests for categorical data
- Correlation analysis (Pearson, Spearman)
- Linear and logistic regression
- Time series analysis

### Advanced Analytics
- Clustering (K-means, hierarchical)
- Principal component analysis (PCA)
- Decision trees and random forests
- Time series forecasting

## Visualization Types

### Basic Charts
- **Histograms**: Distribution analysis
- **Scatter plots**: Relationship visualization
- **Line charts**: Trends over time
- **Bar charts**: Category comparisons
- **Pie charts**: Proportion visualization

### Advanced Visualizations
- **Heatmaps**: Correlation and intensity
- **Box plots**: Distribution comparison
- **Violin plots**: Distribution density
- **Treemaps**: Hierarchical data
- **Geographic maps**: Location-based data

## Requirements
- Python 3.8+ with required packages:
  ```bash
  pip install pandas numpy matplotlib seaborn scipy scikit-learn openpyxl xlrd
  ```
- Sufficient memory for data processing (recommend 8GB+ for large datasets)
- File permissions for reading/writing data files

## Performance Considerations

### Large File Handling
- Files >100MB: Recommend sampling techniques
- Files >500MB: Use chunked processing
- Files >1GB: Consider database solutions
- Memory usage: ~10x file size during processing

### Optimization Strategies
- Use appropriate data types (category for strings)
- Drop unnecessary columns early
- Apply filters before complex operations
- Use vectorized operations over loops
- Cache intermediate results when possible

## Examples

**Basic Data Analysis**:
"Can you analyze this sales data spreadsheet and tell me which products performed best last quarter?"

**Statistical Analysis**:
"I have customer survey results in a CSV file. Can you analyze the responses and identify key trends?"

**Data Quality Assessment**:
"Please check this dataset for any data quality issues, missing values, or anomalies."

**Comparative Analysis**:
"Compare the performance metrics between Q1 and Q2 and highlight any significant differences."

**Predictive Analysis**:
"Based on historical sales data, can you identify patterns that might predict future sales?"

**Data Visualization**:
"Create visualizations from this financial data that would be suitable for a board presentation."

**Data Cleaning**:
"This dataset has formatting issues and missing values. Can you clean it up for analysis?"

**Market Analysis**:
"Analyze competitor pricing data and identify pricing strategies and market positioning."

## Common Data Issues and Solutions

### Missing Data
- **Less than 5%**: Remove rows or impute with mean/median
- **5-20%**: Use advanced imputation (KNN, regression)
- **More than 20%**: Consider removing variable or collection method review

### Outliers
- **Statistical outliers**: Use IQR method (1.5 * IQR)
- **Domain-specific outliers**: Consult subject matter experts
- **Data entry errors**: Correct or remove if clearly erroneous

### Inconsistent Formats
- **Dates**: Standardize to ISO format (YYYY-MM-DD)
- **Text**: Normalize case, remove extra whitespace
- **Numbers**: Ensure consistent decimal places and units

## Best Practices

### Data Validation
- Always validate data integrity before analysis
- Check for reasonable value ranges
- Verify relationships between variables
- Document any assumptions made

### Statistical Validity
- Check normality assumptions for parametric tests
- Use appropriate sample sizes for statistical power
- Consider multiple comparison corrections
- Report confidence intervals and p-values

### Visualization Guidelines
- Choose appropriate chart types for your data
- Use clear labels and descriptive titles
- Include legends and scales
- Maintain consistent color schemes
- Consider accessibility (colorblind-friendly palettes)

## Error Handling

### Common Issues
- **File not found**: Verify file path and permissions
- **Encoding errors**: Try different encodings (UTF-8, Latin-1)
- **Memory errors**: Use sampling or chunked processing
- **Format errors**: Validate file format and structure

### Debugging Steps
1. Check file exists and is readable
2. Verify file format matches expected type
3. Test with smaller sample of data
4. Review error messages for specific issues
5. Check available system resources

## Notes
- Always make a backup of original data before processing
- Document all transformations and assumptions
- Consider ethical implications of data analysis
- Validate results with domain experts when possible
- Use appropriate statistical significance levels (typically p < 0.05)