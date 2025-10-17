#!/usr/bin/env python3
"""
Test Runner and Report Generator

Runs comprehensive tests and generates HTML reports similar to Robot Framework.
"""

import subprocess
import sys
import os
import time
from datetime import datetime


def run_pytest_tests():
    """Run pytest tests and capture results."""
    print("Running pytest tests...")
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 'tests/', '-v', '--tb=short'
        ], capture_output=True, text=True, timeout=60)
        
        return {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            'returncode': -1,
            'stdout': '',
            'stderr': 'Tests timed out after 60 seconds'
        }


def run_baseline_tests():
    """Run baseline agent tests."""
    print("Running baseline agent tests...")
    try:
        result = subprocess.run([
            sys.executable, 'baseline_agents.py'
        ], capture_output=True, text=True, timeout=30)
        
        return {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            'returncode': -1,
            'stdout': '',
            'stderr': 'Baseline tests timed out after 30 seconds'
        }


def run_evaluation_tests():
    """Run evaluation tests."""
    print("Running evaluation tests...")
    try:
        result = subprocess.run([
            sys.executable, 'eval/comprehensive_evaluation.py', '--games', '10'
        ], capture_output=True, text=True, timeout=120)
        
        return {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            'returncode': -1,
            'stdout': '',
            'stderr': 'Evaluation tests timed out after 120 seconds'
        }


def main():
    """Main test runner."""
    print("=" * 60)
    print("Ultra-Advanced Q-Learning Tic-Tac-Toe AI - Test Suite")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run test report generator
    print("Generating comprehensive test report...")
    try:
        result = subprocess.run([
            sys.executable, 'test_report_generator.py'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("Test report generated successfully!")
            print(f"Report file: test_report.html")
        else:
            print("Test report generation failed!")
            print(f"Error: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("Test report generation timed out!")
    
    print()
    
    # Run pytest tests
    pytest_results = run_pytest_tests()
    if pytest_results['returncode'] == 0:
        print("Pytest tests passed!")
    else:
        print("Pytest tests failed!")
        print(f"Error: {pytest_results['stderr']}")
    
    print()
    
    # Run baseline tests
    baseline_results = run_baseline_tests()
    if baseline_results['returncode'] == 0:
        print("Baseline agent tests passed!")
    else:
        print("Baseline agent tests failed!")
        print(f"Error: {baseline_results['stderr']}")
    
    print()
    
    # Run evaluation tests
    eval_results = run_evaluation_tests()
    if eval_results['returncode'] == 0:
        print("Evaluation tests passed!")
    else:
        print("Evaluation tests failed!")
        print(f"Error: {eval_results['stderr']}")
    
    print()
    print("=" * 60)
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Show report location
    report_path = os.path.abspath("test_report.html")
    if os.path.exists(report_path):
        print(f"\nTest Report Available:")
        print(f"   File: {report_path}")
        print(f"   Open in browser: file://{report_path}")
        print(f"\nTo open the report:")
        print(f"   - Double-click the file in Finder")
        print(f"   - Or open in browser: file://{report_path}")


if __name__ == "__main__":
    main()
