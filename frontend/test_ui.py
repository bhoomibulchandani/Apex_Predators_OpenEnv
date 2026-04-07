"""
Test script for Apex Data Cleaner UI
Run this to test if the UI is working correctly
"""

import pandas as pd
import numpy as np
import tempfile
import os

def create_test_csv():
    """Create a test CSV file with missing values for testing"""
    
    # Create sample data with missing values i had make this so u can use this for testing
    test_data = {
        'name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson',
                 'Diana Miller', 'Eve Davis', 'Frank Thomas', 'Grace Lee', 'Henry Clark'],
        'age': [25, None, 30, 28, 35, None, 42, 31, 29, 36],
        'salary': [50000, 60000, None, 55000, 70000, 65000, 80000, None, 58000, 72000],
        'department': ['Sales', 'Marketing', 'Engineering', 'Sales', 'Marketing',
                      'Engineering', 'Sales', 'Marketing', 'Engineering', 'Sales'],
        'experience': [2, None, 5, 3, 8, None, 15, 4, 2, 7],
        'performance_score': [85, 92, 78, 88, 91, 86, 94, 89, 82, 87]
    }
    
    df = pd.DataFrame(test_data)
    
    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='')
    df.to_csv(temp_file.name, index=False)
    temp_file.close()
    
    return temp_file.name

def test_ui_components():
    """Test all UI components individually"""
    
    print("=" * 60)
    print(" TESTING APEX DATA CLEANER UI")
    print("=" * 60)
    
    # Import UI class
    try:
        from ui import ApexDataCleanerUI
        print("✅ Successfully imported ApexDataCleanerUI class")
    except ImportError as e:
        print(f"❌ Failed to import UI: {e}")
        return False
    
    # Create UI instance
    ui = ApexDataCleanerUI()
    print("✅ Created UI instance")
    
    # Test 1: CSV Validation
    print("\n TEST 1: CSV Validation")
    test_file = create_test_csv()
    print(f"   Created test CSV: {test_file}")
    
    df = ui._validate_csv(test_file)
    if df is not None:
        print(f"   ✅ CSV validation passed - Loaded {len(df)} rows")
    else:
        print("   ❌ CSV validation failed")
        return False
    
    # Test 2: Data Quality Analysis
    print("\n TEST 2: Data Quality Analysis")
    analysis = ui._analyze_data_quality(df)
    
    required_keys = ['total_rows', 'total_columns', 'missing_values', 'duplicate_rows']
    all_present = all(key in analysis for key in required_keys)
    
    if all_present:
        print(f"   ✅ Analysis complete - Found {analysis['missing_values']} missing values")
        print(f"   - Rows: {analysis['total_rows']}")
        print(f"   - Columns: {analysis['total_columns']}")
        print(f"   - Missing: {analysis['missing_values']}")
    else:
        print("   ❌ Analysis missing required fields")
        return False
    
    # Test 3: Format Quality Report
    print("\n TEST 3: Quality Report Formatting")
    report = ui._format_quality_report(analysis)
    if report and len(report) > 0:
        print("   ✅ Report generated successfully")
        print(f"   Report length: {len(report)} characters")
    else:
        print("   ❌ Failed to generate report")
        return False
    
    # Test 4: Upload and Analyze
    print("\n TEST 4: Upload and Analyze Function")
    preview, quality, score = ui.upload_and_analyze(test_file)
    
    if preview and quality and score:
        print(f"   ✅ Upload analyze successful")
        print(f"   Initial Score: {score}")
    else:
        print("   ❌ Upload analyze failed")
        return False
    
    # Test 5: Autonomous Cleaning
    print("\n TEST 5: Autonomous Cleaning")
    cleaned_preview, clean_report, final_score, download_path = ui.autonomous_clean(preview, "balanced")
    
    if cleaned_preview and clean_report and final_score:
        print(f"   ✅ Cleaning successful")
        print(f"   Final Score: {final_score}")
        print(f"   Download path: {download_path}")
    else:
        print("   ❌ Cleaning failed")
        return False
    
    # Test 6: Reset Environment
    print("\n TEST 6: Reset Environment")
    reset_preview, reset_status, reset_score, reset_download = ui.reset_environment()
    
    if ui.current_dataset is None:
        print("   ✅ Reset successful - Dataset cleared")
    else:
        print("   ❌ Reset failed - Dataset still present")
        return False
    
    # Test 7: Cleaning History
    print("\n TEST 7: Cleaning History")
    if len(ui.cleaning_history) > 0:
        print(f"   ✅ History tracked - {len(ui.cleaning_history)} cleaning operation(s)")
        print(f"   Last cleaning score: {ui.cleaning_history[-1]['score']:.4f}")
    else:
        print("   No cleaning history recorded")
    
    # Clean up temp file
    os.unlink(test_file)
    if 'download_path' in locals() and download_path and os.path.exists(download_path):
        os.unlink(download_path)
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED! UI is working correctly.")
    print("=" * 60)
    print("\n You can now run: python ui.py")
    print("   Then open http://127.0.0.1:7860 in your browser")
    
    return True

def test_gradio_import():
    """Test if gradio is properly installed"""
    print("\n Checking Dependencies...")
    
    try:
        import gradio as gr
        print(f"✅ Gradio version: {gr.__version__}")
    except ImportError:
        print("❌ Gradio not installed. Run: pip install gradio")
        return False
    
    try:
        import pandas as pd
        print(f"✅ Pandas version: {pd.__version__}")
    except ImportError:
        print("❌ Pandas not installed")
        return False
    
    try:
        import numpy as np
        print(f"✅ NumPy version: {np.__version__}")
    except ImportError:
        print("❌ NumPy not installed")
        return False
    
    return True

def quick_manual_test():
    """Quick manual test instructions"""
    print("\n" + "=" * 60)
    print(" MANUAL TESTING INSTRUCTIONS")
    print("=" * 60)
    print("""
1. Run the UI:
   python ui.py

2. Open browser and go to:
   http://127.0.0.1:7860

3. Verify the following:
   ✓ Dark theme with purple gradients
   ✓ Title: "APEX DATA CLEANER"
   ✓ Left panel has file upload button
   ✓ Right panel has score display

4. Upload a CSV file and verify:
   ✓ Data preview shows correctly
   ✓ Quality report updates
   ✓ Score appears (0.00 to 1.00)

5. Click "INITIALIZE AUTONOMOUS CLEANING AGENT" and verify:
   ✓ Loading popups appear
   ✓ Cleaning operations complete
   ✓ Score updates (should be higher)
   ✓ Download button appears
   ✓ Can download cleaned CSV

If all these work, UI is ready!
""")

if __name__ == "__main__":
    print("\n Starting Apex Data Cleaner UI Tests\n")
    
    # Check dependencies
    if test_gradio_import():
        print("\n✅ All dependencies installed!\n")
        
        # Run automated tests
        if test_ui_components():
            quick_manual_test()
        else:
            print("\n❌ Automated tests failed. Please check the errors above.")
    else:
        print("\n❌ Missing dependencies. Please install required packages:")
        print("   pip install gradio pandas numpy")