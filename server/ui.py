import gradio as gr
import pandas as pd
import numpy as np
import tempfile
import os
from datetime import datetime

class ApexDataCleanerUI:
    """
    Premium Gradio interface for Apex Data Cleaner OpenEnv environment.
    Provides enterprise-grade data cleaning interface with real-time feedback.
    """
    
    def __init__(self):
        self.current_dataset = None
        self.cleaning_history = []
    
    def _validate_csv(self, file_path):
        """Validate and load CSV file with error handling."""
        try:
            if file_path is None:
                return None
            df = pd.read_csv(file_path)
            
            # Basic validation
            if df.empty:
                gr.Warning("Dataset is empty. Please upload a valid CSV file.")
                return None
            
            # Check for excessive missing values
            missing_pct = (df.isnull().sum().sum() / df.size) * 100
            if missing_pct > 90:
                gr.Warning(f"Dataset has {missing_pct:.1f}% missing values. Cleaning may be challenging.")
            
            return df
        except Exception as e:
            gr.Error(f"Failed to load CSV: {str(e)}")
            return None
    
    def _analyze_data_quality(self, df):
        """Generate comprehensive data quality metrics."""
        analysis = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "missing_values": df.isnull().sum().sum(),
            "missing_by_column": df.isnull().sum().to_dict(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "duplicate_rows": df.duplicated().sum()
        }
        
        # Column type distribution
        analysis["column_types"] = {
            "numeric": len(df.select_dtypes(include=[np.number]).columns),
            "categorical": len(df.select_dtypes(include=['object']).columns),
            "other": len(df.columns) - len(df.select_dtypes(include=[np.number, 'object']).columns)
        }
        
        return analysis
    
    def _format_quality_report(self, analysis):
        """Format quality metrics as readable report."""
        report = f"""
### Dataset Quality Report

**Dataset Overview:**
- Rows: {analysis['total_rows']:,}
- Columns: {analysis['total_columns']}
- Missing Values: {analysis['missing_values']:,}
- Duplicate Rows: {analysis['duplicate_rows']:,}

**Column Type Distribution:**
- Numeric: {analysis['column_types']['numeric']}
- Categorical: {analysis['column_types']['categorical']}
- Other: {analysis['column_types']['other']}

**Top Columns with Missing Values:**
"""
        # Show top 5 columns with most missing values
        missing_sorted = sorted(analysis['missing_by_column'].items(), 
                                key=lambda x: x[1], reverse=True)[:5]
        for col, missing in missing_sorted:
            if missing > 0:
                report += f"- {col}: {missing} missing ({missing/analysis['total_rows']*100:.1f}%)\n"
        
        return report
    
    def upload_and_analyze(self, file):
        """
        Handle CSV upload, analyze data quality, and display initial stats.
        """
        if file is None:
            return None, "⚠️ Please upload a CSV file to begin", "0.00"
        
        # Load and validate CSV
        df = self._validate_csv(file)
        if df is None:
            return None, "❌ Failed to load dataset. Please check file format.", "0.00"
        
        self.current_dataset = df.copy()
        
        # Generate analysis
        analysis = self._analyze_data_quality(df)
        quality_report = self._format_quality_report(analysis)
        
        # Calculate initial ML readiness score (inverse of missing data percentage)
        missing_pct = (analysis['missing_values'] / (analysis['total_rows'] * analysis['total_columns'])) * 100
        initial_score = max(0.0, 1.0 - (missing_pct / 100))
        
        # Display preview (first 10 rows as HTML for better display)
        preview_html = df.head(10).to_html(classes='dataframe', border=0, index=False)
        
        return preview_html, quality_report, f"{initial_score:.2f}"
    
    def autonomous_clean(self, dataset_html, cleaning_strategy="balanced"):
        """
        Execute autonomous cleaning with real-time feedback.
        This simulates connecting to your actual cleaning logic.
        """
        if self.current_dataset is None:
            gr.Error("No dataset loaded. Please upload a CSV first.")
            return None, "❌ No dataset to clean", "0.00", ""
        
        gr.Info(" Initializing Autonomous Cleaning Agent...")
        
        try:
            # Make a copy of the current dataset
            df_cleaned = self.current_dataset.copy()
            
            # Step 1: Analyze data types
            gr.Info(" Agent is analyzing data types and column distributions...")
            import time
            time.sleep(0.8)  # Simulate processing
            
            # Step 2: Handle missing values in numeric columns
            gr.Info(" Scanning for missing values and outliers...")
            numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if df_cleaned[col].isnull().any():
                    # Fill with median for numeric columns
                    df_cleaned[col].fillna(df_cleaned[col].median(), inplace=True)
            time.sleep(0.8)
            
            # Step 3: Handle categorical missing values
            gr.Info(" Processing categorical columns...")
            categorical_cols = df_cleaned.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                if df_cleaned[col].isnull().any():
                    df_cleaned[col].fillna("unknown", inplace=True)
            time.sleep(0.8)
            
            # Step 4: Remove duplicates
            gr.Info(" Removing duplicate records...")
            initial_rows = len(df_cleaned)
            df_cleaned.drop_duplicates(inplace=True)
            duplicates_removed = initial_rows - len(df_cleaned)
            time.sleep(0.5)
            
            # Step 5: Optimize data types
            gr.Info(" Optimizing data types for ML readiness...")
            for col in df_cleaned.columns:
                if df_cleaned[col].dtype == 'object':
                    # Try to convert to numeric if possible
                    try:
                        df_cleaned[col] = pd.to_numeric(df_cleaned[col])
                    except (ValueError, TypeError):
                        pass
            time.sleep(0.8)
            
            # Step 6: Final validation and scoring
            gr.Info(" Calculating ML Readiness Score...")
            
            # Calculate final score based on data quality
            analysis_cleaned = self._analyze_data_quality(df_cleaned)
            missing_pct_cleaned = (analysis_cleaned['missing_values'] / 
                                   (analysis_cleaned['total_rows'] * analysis_cleaned['total_columns'])) * 100
            
            # Deterministic grader score based on:
            # - 70%: Missing data reduction
            # - 20%: Data type appropriateness
            # - 10%: Duplicate removal
            missing_score = max(0.0, 1.0 - (missing_pct_cleaned / 20))
            type_score = min(1.0, analysis_cleaned['column_types']['numeric'] / len(df_cleaned.columns) if len(df_cleaned.columns) > 0 else 0.5)
            duplicate_score = 1.0 if duplicates_removed > 0 else 0.5
            
            final_score = (missing_score * 0.7 + type_score * 0.2 + duplicate_score * 0.1)
            final_score = min(1.0, max(0.0, final_score))
            
            # Generate detailed cleaning report
            report = f"""
### ✅ Cleaning Complete

**Operations Performed:**
- ✓ Imputed median values for numeric columns with missing data
- ✓ Filled categorical missing values with 'unknown'
- ✓ Removed {duplicates_removed:,} duplicate rows
- ✓ Optimized data types for ML compatibility

**Quality Metrics After Cleaning:**
- Remaining Missing Values: {analysis_cleaned['missing_values']:,}
- Data Quality Score: {final_score:.2%}
- ML Readiness: {'✅ High' if final_score > 0.8 else '⚠️ Medium' if final_score > 0.6 else '❌ Low'}

**Deterministic Grader Validation:**
- Missing Data Reduction: {missing_score:.2%}
- Data Type Optimization: {type_score:.2%}
- Duplicate Resolution: {duplicate_score:.2%}
- **Final Score: {final_score:.4f}**
"""
            
            # Record cleaning history
            self.cleaning_history.append({
                'timestamp': datetime.now().isoformat(),
                'score': final_score,
                'operations': {
                    'duplicates_removed': duplicates_removed,
                    'missing_remaining': analysis_cleaned['missing_values']
                }
            })
            
            # Save cleaned dataset to a temporary CSV file for download
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
            df_cleaned.to_csv(temp_file.name, index=False)
            temp_file.close()
            
            # Update current dataset
            self.current_dataset = df_cleaned
            
            # Convert preview to HTML
            preview_html = df_cleaned.head(10).to_html(classes='dataframe', border=0, index=False)
            
            gr.Info(f" Cleaning completed! Final Score: {final_score:.2%}")
            
            return preview_html, report, f"{final_score:.4f}", temp_file.name
            
        except Exception as e:
            gr.Error(f"Cleaning failed: {str(e)}")
            return None, f"❌ Cleaning process failed: {str(e)}", "0.00", ""
    
    def reset_environment(self):
        """Reset the cleaning environment."""
        self.current_dataset = None
        self.cleaning_history = []
        gr.Info(" Environment reset. Ready for new dataset.")
        return None, "Ready for new cleaning session", "0.00", ""

# Create the Gradio interface
def create_interface():
    """Create the main Gradio interface with premium design."""
    
    ui_handler = ApexDataCleanerUI()
    
    # Premium theme with dark mode
    with gr.Blocks(theme=gr.themes.Soft(), title="Apex Data Cleaner") as app:
        
        # Header with branding
        gr.Markdown("""
        <div style="text-align: center;">

        # APEX DATA CLEANER

        ### Autonomous Data Cleaning Environment for ML Readiness

        *Powered by OpenEnv — Deterministic RL Training for Real-World Data Engineering*

        </div>
        """)
        
        gr.HTML("<br>")
        gr.HTML("<br>")
        
        # Main dashboard with Rule of Thirds layout
        with gr.Row(equal_height=False):
            # Left Column (Inputs - 1/3)
            with gr.Column(scale=1, min_width=300):
                gr.Markdown("### Data Ingestion")
                
                # File upload with professional microcopy
                file_input = gr.File(
                    label="INGEST CORRUPTED DATASET (.csv)",
                    file_types=[".csv"],
                    type="filepath"
                )
                
                gr.HTML("<br>")
                
                # Cleaning configuration
                cleaning_strategy = gr.Radio(
                    choices=["conservative", "balanced", "aggressive"],
                    value="balanced",
                    label="Cleaning Strategy",
                    info="Balanced: Standard cleaning with median imputation"
                )
                
                gr.HTML("<br>")
                gr.HTML("<br>")
                
                # Main action button with professional copy
                clean_button = gr.Button(
                    "INITIALIZE AUTONOMOUS CLEANING AGENT",
                    variant="primary",
                    size="lg"
                )
                
                gr.HTML("<br>")
                
                # Reset button
                reset_button = gr.Button(
                    "RESET ENVIRONMENT",
                    variant="secondary",
                    size="sm"
                )
                
                gr.HTML("<br>")
                gr.HTML("<br>")
                
                # Status information
                status_display = gr.Textbox(
                    label="System Status",
                    value="Awaiting dataset upload...",
                    interactive=False,
                    lines=2
                )
            
            # Right Column (Outputs - 2/3)
            with gr.Column(scale=2):
                gr.Markdown("### ML Readiness Dashboard")
                
                # Deterministic Grader Score with premium styling
                gr.Markdown("#### Deterministic Grader Score (ML Readiness)")
                score_output = gr.Textbox(
                    label="ML-Score",
                    value="None",
                    interactive=False,
                    elem_classes="score-display"
                )
                
                gr.HTML("<br>")
                
                # Data quality report
                with gr.Group():
                    gr.Markdown("#### Data Quality Analysis")
                    quality_report = gr.Markdown(
                        "Upload a CSV to see quality metrics",
                        elem_classes="quality-report"
                    )
                
                gr.HTML("<br>")
                
                # Dataset preview
                with gr.Group():
                    gr.Markdown("#### Dataset Preview (First 10 Rows)")
                    dataset_preview = gr.HTML(
                        "<p>No dataset loaded</p>"
                    )
                
                gr.HTML("<br>")
                
                # Download cleaned dataset
                with gr.Group():
                    gr.Markdown("#### Export Cleaned Dataset")
                    download_button = gr.File(
                        label="Download ML-Ready Dataset",
                        interactive=False
                    )
        
          # Custom CSS for premium styling (Dark & Light theme support)
        gr.HTML("""
        <style>
            /* Score display - clean gradient text with no background */
            .score-display {
                text-align: center !important;
            }

            .score-display textarea,
            .score-display input {
                font-size: 38px !important;
                font-weight: bold !important;
                text-align: center !important;
                color: white !important;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                border-radius: 12px !important;
                padding: 20px !important;
                border: none !important;
            }
            
            /* ========== DARK THEME STYLES ========== */
            .dark .quality-report {
                background: #1e1e1e !important;
                padding: 20px;
                border-radius: 12px;
                font-family: monospace;
                color: #e0e0e0 !important;
                border: 1px solid #2d2d2d;
            }
            
            .dark .quality-report h1, 
            .dark .quality-report h2, 
            .dark .quality-report h3 {
                color: #667eea !important;
            }
            
            .dark .quality-report p, 
            .dark .quality-report li, 
            .dark .quality-report span {
                color: #e0e0e0 !important;
            }
            
            .dark .quality-report strong {
                color: #ffffff !important;
            }
            
            .dark table.dataframe {
                width: 100%;
                border-collapse: collapse;
                font-size: 14px;
                background: #1e1e1e !important;
                color: #e0e0e0 !important;
                border-radius: 8px;
                overflow: hidden;
            }
            
            .dark table.dataframe th {
                background: #2d3748 !important;
                color: #ffffff !important;
                padding: 12px;
                text-align: left;
                font-weight: 600;
            }
            
            .dark table.dataframe td {
                padding: 10px 12px;
                border-bottom: 1px solid #4a5568 !important;
                color: #e0e0e0 !important;
            }
            
            .dark table.dataframe tr:hover {
                background: #2d3748 !important;
            }
            
            .dark .gr-box, 
            .dark .gr-group {
                background: #1a1a1a !important;
                border: 1px solid #2d2d2d;
                border-radius: 12px;
                padding: 20px;
            }
            
            .dark .gr-file {
                background: #1e1e1e !important;
                border: 1px solid #4a5568 !important;
                border-radius: 8px !important;
            }
            
            .dark .gr-file-label {
                background: #2d3748 !important;
                color: #e0e0e0 !important;
            }
            
            /* ========== LIGHT THEME STYLES ========== */
            .light .quality-report {
                background: #f5f5f5 !important;
                padding: 20px;
                border-radius: 12px;
                font-family: monospace;
                color: #2c3e50 !important;
                border: 1px solid #e0e0e0;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }
            
            .light .quality-report h1, 
            .light .quality-report h2, 
            .light .quality-report h3 {
                color: #5a3e8a !important;
            }
            
            .light .quality-report p, 
            .light .quality-report li, 
            .light .quality-report span {
                color: #2c3e50 !important;
            }
            
            .light .quality-report strong {
                color: #1a1a1a !important;
            }
            
            .light table.dataframe {
                width: 100%;
                border-collapse: collapse;
                font-size: 14px;
                background: #f5f5f5 !important;
                color: #2c3e50 !important;
                border-radius: 8px;
                overflow: hidden;
                border: 1px solid #e0e0e0;
            }
            
            .light table.dataframe th {
                background: #e8e8e8 !important;
                color: #1a1a1a !important;
                padding: 12px;
                text-align: left;
                font-weight: 600;
                border-bottom: 2px solid #d0d0d0;
            }
            
            .light table.dataframe td {
                padding: 10px 12px;
                border-bottom: 1px solid #e0e0e0 !important;
                color: #2c3e50 !important;
            }
            
            .light table.dataframe tr:hover {
                background: #e8e8e8 !important;
            }
            
            .light .gr-box, 
            .light .gr-group {
                background: #fafafa !important;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 1px 2px rgba(0,0,0,0.03);
            }
            
            .light .gr-file {
                background: #f5f5f5 !important;
                border: 2px dashed #c0c0c0 !important;
                border-radius: 12px !important;
                padding: 20px !important;
                transition: all 0.3s ease;
            }
            
            .light .gr-file:hover {
                border-color: #667eea !important;
                background: #fafafa !important;
            }
            
            .light .gr-file-label {
                background: #e8e8e8 !important;
                color: #2c3e50 !important;
                border-radius: 6px !important;
                padding: 8px 16px !important;
                font-weight: 500 !important;
            }
            
            .light .gr-file-label:hover {
                background: #667eea !important;
                color: white !important;
            }
            
            .light .gr-radio {
                background: #f5f5f5 !important;
                border: 1px solid #e0e0e0 !important;
                border-radius: 8px !important;
                padding: 8px !important;
            }
            
            .light .gr-textbox {
                background: #f5f5f5 !important;
                border: 1px solid #e0e0e0 !important;
                border-radius: 8px !important;
                color: #2c3e50 !important;
            }
            
            /* ========== COMMON STYLES ========== */
            .gradio-button-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                border: none !important;
                font-weight: bold !important;
                transition: all 0.3s ease !important;
            }
            
            .gradio-button-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
            }
            
            .gradio-button-secondary {
                background: #4a5568 !important;
                border: none !important;
                transition: all 0.3s ease !important;
            }
            
            .gradio-button-secondary:hover {
                background: #2d3748 !important;
                transform: translateY(-1px);
            }
            
            .light .gradio-button-secondary {
                background: #6c757d !important;
                color: white !important;
            }
            
            .light .gradio-button-secondary:hover {
                background: #5a6268 !important;
            }
            
            .dark h1, .dark h2, .dark h3, .dark h4 {
                color: #e0e0e0 !important;
            }
            
            .light h1, .light h2, .light h3, .light h4 {
                color: #2c3e50 !important;
            }
            
            .dark .gr-markdown p,
            .dark .gr-markdown li,
            .dark .gr-markdown span {
                color: #e0e0e0 !important;
            }
            
            .light .gr-markdown p,
            .light .gr-markdown li,
            .light .gr-markdown span {
                color: #2c3e50 !important;
            }
            
            .dark label, .dark .gr-form-label {
                color: #e0e0e0 !important;
            }
            
            .light label, .light .gr-form-label {
                color: #2c3e50 !important;
            }
            
            .dark .gr-info {
                background: #2d3748 !important;
                color: #e0e0e0 !important;
                border-left: 4px solid #667eea !important;
            }
            
            .light .gr-info {
                background: #e3f2fd !important;
                color: #1a202c !important;
                border-left: 4px solid #667eea !important;
            }
            
            .dark .gr-error {
                background: #742a2a !important;
                color: #ffcccc !important;
            }
            
            .light .gr-error {
                background: #fed7d7 !important;
                color: #742a2a !important;
            }
            
            .dark .gr-warning {
                background: #744d2a !important;
                color: #ffddcc !important;
            }
            
            .light .gr-warning {
                background: #feebc8 !important;
                color: #744d2a !important;
            }
            
            .gr-box, .gr-group {
                transition: all 0.3s ease;
            }
            
            .gr-column {
                gap: 16px !important;
            }
            
            @media (max-width: 768px) {
                .score-display {
                    font-size: 32px !important;
                }
                .gr-box, .gr-group {
                    padding: 12px !important;
                }
            }
        </style>
        """)
        
        # Wire up event handlers
        file_input.change(
            fn=ui_handler.upload_and_analyze,
            inputs=file_input,
            outputs=[dataset_preview, quality_report, score_output]
        ).then(
            fn=lambda: "Dataset loaded. Ready for cleaning.",
            inputs=None,
            outputs=status_display
        )
        
        clean_button.click(
            fn=ui_handler.autonomous_clean,
            inputs=[dataset_preview, cleaning_strategy],
            outputs=[dataset_preview, quality_report, score_output, download_button]
        ).then(
            fn=lambda: "Cleaning complete. Score updated.",
            inputs=None,
            outputs=status_display
        )
        
        reset_button.click(
            fn=ui_handler.reset_environment,
            inputs=None,
            outputs=[dataset_preview, quality_report, score_output, download_button]
        ).then(
            fn=lambda: "Environment reset. Ready for new dataset.",
            inputs=None,
            outputs=status_display
        )
    
    return app

# Launch the application
if __name__ == "__main__":
    app = create_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )