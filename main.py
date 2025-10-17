#!/usr/bin/env python3
"""
Ultra-Advanced Q-Learning Tic-Tac-Toe AI - Main Entry Point

Professional entry point for all project functionality.
"""

import sys
import os
import argparse
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

def main():
    """Main entry point with professional CLI interface."""
    parser = argparse.ArgumentParser(
        description="Ultra-Advanced Q-Learning Tic-Tac-Toe AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s train --episodes 10000          # Train AI
  %(prog)s play                             # Play against AI
  %(prog)s demo                             # Watch AI vs AI
  %(prog)s test                             # Run tests
  %(prog)s report                           # Generate reports
  %(prog)s eval --games 100                 # Evaluate performance
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Training command
    train_parser = subparsers.add_parser('train', help='Train the AI')
    train_parser.add_argument('--episodes', type=int, default=50000,
                             help='Number of training episodes')
    train_parser.add_argument('--config', type=str, default='src/config.yaml',
                             help='Configuration file path')
    
    # Play command
    play_parser = subparsers.add_parser('play', help='Play against the AI')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Watch AI vs AI demo')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run tests')
    test_parser.add_argument('--report', action='store_true',
                            help='Generate HTML test report')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate reports')
    report_parser.add_argument('--type', choices=['html', 'analytics', 'all'],
                             default='html', help='Type of report to generate')
    
    # Evaluation command
    eval_parser = subparsers.add_parser('eval', help='Evaluate AI performance')
    eval_parser.add_argument('--games', type=int, default=100,
                           help='Number of games to play')
    eval_parser.add_argument('--agent', choices=['minimax', 'baseline', 'all'],
                           default='all', help='Agent to evaluate against')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute commands
    if args.command == 'train':
        run_training(args)
    elif args.command == 'play':
        run_play()
    elif args.command == 'demo':
        run_demo()
    elif args.command == 'test':
        run_tests(args)
    elif args.command == 'report':
        run_reports(args)
    elif args.command == 'eval':
        run_evaluation(args)


def run_training(args):
    """Run training with new structure."""
    print("Starting AI Training...")
    os.system(f"python src/training/train.py --episodes {args.episodes} --config {args.config}")


def run_play():
    """Run interactive play."""
    print("Starting Interactive Play...")
    os.system("python scripts/demo/play.py")


def run_demo():
    """Run AI vs AI demo."""
    print("Starting AI vs AI Demo...")
    os.system("python scripts/demo/demo.py")


def run_tests(args):
    """Run tests."""
    print("Running Tests...")
    if args.report:
        os.system("python reports/html/test_report_generator.py")
    else:
        os.system("python scripts/utils/run_tests.py")


def run_reports(args):
    """Generate reports."""
    print("Generating Reports...")
    if args.type == 'html':
        os.system("python reports/html/test_report_generator.py")
    elif args.type == 'analytics':
        os.system("python scripts/utils/analytics.py")
    elif args.type == 'all':
        os.system("python reports/html/test_report_generator.py")
        os.system("python scripts/utils/analytics.py")


def run_evaluation(args):
    """Run evaluation."""
    print("Running Evaluation...")
    if args.agent == 'minimax':
        os.system(f"python eval/checkpoint_vs_minimax.py --games {args.games}")
    elif args.agent == 'baseline':
        os.system(f"python eval/comprehensive_evaluation.py --games {args.games}")
    elif args.agent == 'all':
        os.system(f"python eval/comprehensive_evaluation.py --games {args.games}")


if __name__ == "__main__":
    main()
