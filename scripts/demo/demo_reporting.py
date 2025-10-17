#!/usr/bin/env python3
"""
Demo Script for Test Reporting System

Demonstrates the complete test reporting capabilities.
"""

import os
import time
import subprocess
import sys


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def run_command(cmd, description):
    """Run a command and show results."""
    print(f"\n{description}")
    print(f"   Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("   Success!")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()[:100]}...")
        else:
            print("   Failed!")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()[:100]}...")
    except subprocess.TimeoutExpired:
        print("   Timeout!")
    except Exception as e:
        print(f"   Error: {e}")


def main():
    """Main demo function."""
    print_header("Ultra-Advanced Q-Learning Tic-Tac-Toe AI - Test Reporting Demo")
    
    print("\nThis demo shows the complete test reporting system that generates")
    print("professional HTML reports similar to Robot Framework reports.")
    
    print("\nAvailable Reporting Features:")
    print("   - HTML Test Reports with Statistics")
    print("   - Visual Progress Bars and Status Indicators")
    print("   - Performance Metrics and Timing Information")
    print("   - Test Suite Organization")
    print("   - Browser Integration")
    
    print_header("Step 1: Generate Test Report")
    run_command("python test_report_generator.py", "Generate comprehensive test report")
    
    print_header("Step 2: Check Report File")
    if os.path.exists("test_report.html"):
        size = os.path.getsize("test_report.html")
        print(f"Report file created: test_report.html ({size:,} bytes)")
    else:
        print("Report file not found!")
        return
    
    print_header("Step 3: Open Report in Browser")
    run_command("python open_report.py", "Open report in default browser")
    
    print_header("Step 4: Run Complete Test Suite")
    run_command("python run_tests.py", "Run all tests and generate reports")
    
    print_header("Demo Complete!")
    print("\nYour test reporting system is now ready!")
    print("\nQuick Commands:")
    print("   - Generate report: python test_report_generator.py")
    print("   - Open report: python open_report.py")
    print("   - Run all tests: python run_tests.py")
    print("   - View report: file://" + os.path.abspath("test_report.html"))
    
    print("\nFeatures Available:")
    print("   - Professional HTML reports")
    print("   - Test statistics and progress bars")
    print("   - Performance metrics")
    print("   - Browser integration")
    print("   - Comprehensive test coverage")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
