import json
import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict, Counter
from tictactoe import TicTacToe
from qlearning_agent import UltraAdvancedQLearningAgent


class SimplifiedUltraAdvancedAnalytics:
    """Simplified analytics for Q-learning AI."""
    
    def __init__(self, agent: UltraAdvancedQLearningAgent):
        """Initialize analytics with trained agent."""
        self.agent = agent
        self.analytics_data = {}
        
    def generate_q_value_analysis(self) -> Dict:
        """Generate Q-value analysis for all states."""
        all_states = set(self.agent.q_table_a.keys()) | set(self.agent.q_table_b.keys())
        
        # Aggregate Q-values by position
        position_q_values = defaultdict(list)
        
        for state_key in all_states:
            q_values = self.agent.get_combined_q_values(state_key)
            for pos in range(9):
                position_q_values[pos].append(float(q_values[pos]))
        
        # Calculate statistics for each position
        position_stats = {}
        for pos, values in position_q_values.items():
            if values:  # Only if we have values
                position_stats[f'position_{pos}'] = {
                    'mean_q': float(np.mean(values)),
                    'std_q': float(np.std(values)),
                    'max_q': float(np.max(values)),
                    'min_q': float(np.min(values)),
                    'frequency': len(values)
                }
        
        return {
            'total_states': len(all_states),
            'position_statistics': position_stats,
            'overall_preferences': self._calculate_overall_preferences(position_stats)
        }
    
    def _calculate_overall_preferences(self, position_stats: Dict) -> Dict:
        """Calculate overall strategic preferences."""
        preferences = {}
        
        # Center preference
        center_score = position_stats.get('position_4', {}).get('mean_q', 0)
        preferences['center_preference'] = center_score
        
        # Corner preference
        corners = [0, 2, 6, 8]
        corner_scores = [position_stats.get(f'position_{pos}', {}).get('mean_q', 0) for pos in corners]
        preferences['corner_preference'] = float(np.mean(corner_scores))
        
        # Edge preference
        edges = [1, 3, 5, 7]
        edge_scores = [position_stats.get(f'position_{pos}', {}).get('mean_q', 0) for pos in edges]
        preferences['edge_preference'] = float(np.mean(edge_scores))
        
        # Strategic ranking
        all_scores = [(pos, position_stats.get(f'position_{pos}', {}).get('mean_q', 0)) for pos in range(9)]
        all_scores.sort(key=lambda x: x[1], reverse=True)
        preferences['position_ranking'] = [pos for pos, score in all_scores]
        
        return preferences
    
    def analyze_move_patterns(self) -> Dict:
        """Analyze move patterns and winning sequences."""
        patterns = dict(self.agent.move_patterns)
        
        # Analyze pattern frequency
        pattern_analysis = {
            'total_patterns': len(patterns),
            'most_frequent_patterns': Counter(patterns).most_common(10),
            'pattern_diversity': len(set(patterns.values())),
            'average_frequency': float(np.mean(list(patterns.values()))) if patterns else 0
        }
        
        return pattern_analysis
    
    def generate_strategic_analysis(self) -> Dict:
        """Generate comprehensive strategic analysis."""
        strategic_analysis = {
            'opening_strategy': self._analyze_opening_strategy(),
            'mid_game_strategy': self._analyze_mid_game_strategy(),
            'end_game_strategy': self._analyze_end_game_strategy()
        }
        
        return strategic_analysis
    
    def _analyze_opening_strategy(self) -> Dict:
        """Analyze opening move preferences."""
        all_states = set(self.agent.q_table_a.keys()) | set(self.agent.q_table_b.keys())
        
        opening_states = [state for state in all_states if self._is_opening_state(state)]
        
        opening_preferences = defaultdict(list)
        for state in opening_states:
            q_values = self.agent.get_combined_q_values(state)
            for pos in range(9):
                opening_preferences[pos].append(float(q_values[pos]))
        
        opening_analysis = {}
        for pos, values in opening_preferences.items():
            if values:
                opening_analysis[f'position_{pos}'] = {
                    'mean_preference': float(np.mean(values)),
                    'frequency': len(values),
                    'consistency': float(np.std(values))
                }
        
        return opening_analysis
    
    def _is_opening_state(self, state_key: str) -> bool:
        """Check if state represents opening position."""
        try:
            empty_count = state_key.count('0')
            return empty_count >= 7  # Opening = 7+ empty positions
        except:
            return False
    
    def _analyze_mid_game_strategy(self) -> Dict:
        """Analyze mid-game strategic patterns."""
        all_states = set(self.agent.q_table_a.keys()) | set(self.agent.q_table_b.keys())
        
        mid_game_states = [state for state in all_states if self._is_mid_game_state(state)]
        
        # Analyze tactical patterns
        tactical_patterns = defaultdict(int)
        for state in mid_game_states:
            q_values = self.agent.get_combined_q_values(state)
            # Find high-value actions (tactical moves)
            mean_q = float(np.mean(q_values))
            std_q = float(np.std(q_values))
            high_value_actions = [i for i, q in enumerate(q_values) if float(q) > mean_q + std_q]
            for action in high_value_actions:
                tactical_patterns[f'position_{action}'] += 1
        
        return dict(tactical_patterns)
    
    def _is_mid_game_state(self, state_key: str) -> bool:
        """Check if state represents mid-game position."""
        try:
            empty_count = state_key.count('0')
            return 3 <= empty_count <= 6  # Mid-game = 3-6 empty positions
        except:
            return False
    
    def _analyze_end_game_strategy(self) -> Dict:
        """Analyze end-game tactical patterns."""
        all_states = set(self.agent.q_table_a.keys()) | set(self.agent.q_table_b.keys())
        
        end_game_states = [state for state in all_states if self._is_end_game_state(state)]
        
        # Analyze win/block patterns
        win_block_patterns = defaultdict(int)
        for state in end_game_states:
            q_values = self.agent.get_combined_q_values(state)
            max_q = float(np.max(q_values))
            # High Q-values in end-game likely represent wins/blocks
            critical_actions = [i for i, q in enumerate(q_values) if float(q) > max_q * 0.8]
            for action in critical_actions:
                win_block_patterns[f'position_{action}'] += 1
        
        return dict(win_block_patterns)
    
    def _is_end_game_state(self, state_key: str) -> bool:
        """Check if state represents end-game position."""
        try:
            empty_count = state_key.count('0')
            return empty_count <= 2  # End-game = 0-2 empty positions
        except:
            return False
    
    def generate_performance_report(self) -> Dict:
        """Generate comprehensive performance report."""
        report = {
            'agent_statistics': self.agent.get_statistics(),
            'q_value_analysis': self.generate_q_value_analysis(),
            'move_pattern_analysis': self.analyze_move_patterns(),
            'strategic_analysis': self.generate_strategic_analysis(),
            'performance_metrics': self._calculate_performance_metrics()
        }
        
        return report
    
    def _calculate_performance_metrics(self) -> Dict:
        """Calculate comprehensive performance metrics."""
        all_states = set(self.agent.q_table_a.keys()) | set(self.agent.q_table_b.keys())
        
        # Calculate Q-value statistics
        all_q_values = []
        for state in all_states:
            q_values = self.agent.get_combined_q_values(state)
            all_q_values.extend([float(q) for q in q_values])
        
        metrics = {
            'total_states': len(all_states),
            'total_q_values': len(all_q_values),
            'q_value_statistics': {
                'mean': float(np.mean(all_q_values)) if all_q_values else 0,
                'std': float(np.std(all_q_values)) if all_q_values else 0,
                'max': float(np.max(all_q_values)) if all_q_values else 0,
                'min': float(np.min(all_q_values)) if all_q_values else 0,
                'median': float(np.median(all_q_values)) if all_q_values else 0
            },
            'learning_efficiency': {
                'states_per_episode': len(all_states) / max(1, self.agent.episodes_trained),
                'q_value_stability': float(np.std(all_q_values)) if all_q_values else 0,
                'exploration_efficiency': float(self.agent.get_epsilon())
            }
        }
        
        return metrics
    
    def export_analytics(self, filename: str = "ultra_advanced_analytics.json"):
        """Export comprehensive analytics to JSON."""
        analytics = self.generate_performance_report()
        
        with open(filename, 'w') as f:
            json.dump(analytics, f, indent=2)
        
        print(f"Ultra-advanced analytics exported to {filename}")
        return analytics
    
    def create_visualization_summary(self) -> str:
        """Create text-based visualization summary."""
        report = self.generate_performance_report()
        
        summary = "Ultra-Advanced Q-Learning Analytics Summary\n"
        summary += "=" * 50 + "\n\n"
        
        # Agent statistics
        stats = report['agent_statistics']
        summary += f"Agent Statistics:\n"
        summary += f"  Total States: {stats['total_states']:,}\n"
        summary += f"  Episodes Trained: {stats['episodes_trained']:,}\n"
        summary += f"  Total Steps: {stats['total_steps']:,}\n"
        summary += f"  Current Alpha: {stats['current_alpha']:.6f}\n"
        summary += f"  Current Epsilon: {stats['current_epsilon']:.6f}\n"
        summary += f"  Experience Buffer: {stats['experience_buffer_size']:,}\n\n"
        
        # Strategic preferences
        q_analysis = report['q_value_analysis']
        if 'overall_preferences' in q_analysis:
            prefs = q_analysis['overall_preferences']
            summary += f"Strategic Preferences:\n"
            summary += f"  Center Preference: {prefs['center_preference']:.3f}\n"
            summary += f"  Corner Preference: {prefs['corner_preference']:.3f}\n"
            summary += f"  Edge Preference: {prefs['edge_preference']:.3f}\n"
            summary += f"  Position Ranking: {prefs['position_ranking']}\n\n"
        
        # Move patterns
        patterns = report['move_pattern_analysis']
        summary += f"Move Pattern Analysis:\n"
        summary += f"  Total Patterns: {patterns['total_patterns']:,}\n"
        summary += f"  Pattern Diversity: {patterns['pattern_diversity']}\n"
        summary += f"  Average Frequency: {patterns['average_frequency']:.1f}\n\n"
        
        # Performance metrics
        perf = report['performance_metrics']
        summary += f"Performance Metrics:\n"
        summary += f"  States per Episode: {perf['learning_efficiency']['states_per_episode']:.2f}\n"
        summary += f"  Q-value Stability: {perf['learning_efficiency']['q_value_stability']:.3f}\n"
        summary += f"  Exploration Efficiency: {perf['learning_efficiency']['exploration_efficiency']:.6f}\n"
        
        return summary


def main():
    """Main analytics function."""
    print("Ultra-Advanced Q-Learning Analytics")
    print("=" * 40)
    
    # Load trained agent
    agent = UltraAdvancedQLearningAgent()
    agent.load_q_table("q_table.json")
    
    # Create analytics
    analytics = SimplifiedUltraAdvancedAnalytics(agent)
    
    # Generate comprehensive report
    report = analytics.generate_performance_report()
    
    # Export analytics
    analytics.export_analytics()
    
    # Print summary
    summary = analytics.create_visualization_summary()
    print(summary)


if __name__ == "__main__":
    main()