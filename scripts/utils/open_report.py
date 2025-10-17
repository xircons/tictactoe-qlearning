#!/usr/bin/env python3
"""
Open Test Report in Browser

Opens the generated test report in the default web browser.
"""

import webbrowser
import os
import sys


def open_report():
    """Open the test report in browser."""
    report_file = "test_report.html"
    
    if not os.path.exists(report_file):
        print(f"Report file not found: {report_file}")
        print("Run 'python test_report_generator.py' first to generate the report.")
        return False
    
    report_path = os.path.abspath(report_file)
    report_url = f"file://{report_path}"
    
    print(f"Opening test report...")
    print(f"   File: {report_path}")
    print(f"   URL: {report_url}")
    
    try:
        webbrowser.open(report_url)
        print("Report opened in browser!")
        return True
    except Exception as e:
        print(f"Failed to open report: {e}")
        print(f"   You can manually open: {report_url}")
        return False


def main():
    """Main function."""
    print("Ultra-Advanced Q-Learning Tic-Tac-Toe AI - Test Report Viewer")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        report_file = sys.argv[1]
    else:
        report_file = "test_report.html"
    
    if not os.path.exists(report_file):
        print(f"Report file not found: {report_file}")
        print("\nAvailable options:")
        print("1. Generate new report: python test_report_generator.py")
        print("2. Run all tests: python run_tests.py")
        print("3. Specify custom report: python open_report.py <filename>")
        return
    
    report_path = os.path.abspath(report_file)
    report_url = f"file://{report_path}"
    
    print(f"Opening test report...")
    print(f"   File: {report_path}")
    
    try:
        webbrowser.open(report_url)
        print("Report opened in browser!")
    except Exception as e:
        print(f"Failed to open report: {e}")
        print(f"   You can manually open: {report_url}")


if __name__ == "__main__":
    main()
