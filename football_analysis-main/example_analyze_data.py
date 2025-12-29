"""
Example script demonstrating how to analyze the exported data.
This script loads the exported JSON/CSV data and performs basic analysis.
"""
import json
import pandas as pd
import os


def analyze_json_data(json_path):
    """Analyze data from JSON export."""
    print("=" * 60)
    print("ANALYZING JSON DATA")
    print("=" * 60)
    
    if not os.path.exists(json_path):
        print(f"❌ JSON file not found: {json_path}")
        return
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Print metadata
    print("\n📊 OVERALL STATISTICS")
    print(f"Total frames analyzed: {data['metadata']['total_frames']}")
    print(f"Team 1 ball control: {data['metadata']['team_1_ball_control_percent']:.2f}%")
    print(f"Team 2 ball control: {data['metadata']['team_2_ball_control_percent']:.2f}%")
    
    # Analyze first frame
    if data['frames']:
        first_frame = data['frames'][0]
        print(f"\n🎬 FRAME 0 ANALYSIS")
        print(f"Players detected: {len(first_frame['players'])}")
        print(f"Camera movement: X={first_frame['camera_movement']['x']:.2f}, Y={first_frame['camera_movement']['y']:.2f}")
        print(f"Ball control team: {first_frame['team_ball_control']}")
        
        # Show player details
        print("\n👥 PLAYERS IN FRAME 0:")
        for player in first_frame['players'][:5]:  # Show first 5 players
            print(f"  Player {player['id']} (Team {player['team']}): "
                  f"Speed={player['speed_kmh']:.1f} km/h, "
                  f"Distance={player['distance_m']:.1f}m, "
                  f"Ball={player['has_ball']}")
    
    # Find fastest players across all frames
    print("\n⚡ TOP 5 FASTEST SPEEDS RECORDED:")
    all_speeds = []
    for frame in data['frames']:
        for player in frame['players']:
            if player['speed_kmh'] > 0:
                all_speeds.append({
                    'frame': frame['frame_number'],
                    'player_id': player['id'],
                    'team': player['team'],
                    'speed': player['speed_kmh']
                })
    
    all_speeds.sort(key=lambda x: x['speed'], reverse=True)
    for i, speed_info in enumerate(all_speeds[:5], 1):
        print(f"  {i}. Player {speed_info['player_id']} (Team {speed_info['team']}): "
              f"{speed_info['speed']:.2f} km/h at frame {speed_info['frame']}")


def analyze_csv_data(csv_dir):
    """Analyze data from CSV exports."""
    print("\n" + "=" * 60)
    print("ANALYZING CSV DATA")
    print("=" * 60)
    
    # Check if directory exists
    if not os.path.exists(csv_dir):
        print(f"❌ CSV directory not found: {csv_dir}")
        return
    
    # Load players tracking data
    players_file = os.path.join(csv_dir, 'players_tracking.csv')
    if os.path.exists(players_file):
        df_players = pd.read_csv(players_file)
        
        print("\n📈 PLAYER STATISTICS")
        print(f"Total player-frame records: {len(df_players)}")
        print(f"Unique players tracked: {df_players['player_id'].nunique()}")
        
        # Average speed per player
        print("\n🏃 AVERAGE SPEED BY PLAYER:")
        avg_speeds = df_players.groupby('player_id')['speed_kmh'].mean().sort_values(ascending=False)
        for player_id, speed in avg_speeds.head(5).items():
            team = df_players[df_players['player_id'] == player_id]['team'].iloc[0]
            print(f"  Player {player_id} (Team {team}): {speed:.2f} km/h")
        
        # Total distance per player
        print("\n🏃 MAXIMUM DISTANCE COVERED BY PLAYER:")
        max_distances = df_players.groupby('player_id')['distance_m'].max().sort_values(ascending=False)
        for player_id, distance in max_distances.head(5).items():
            team = df_players[df_players['player_id'] == player_id]['team'].iloc[0]
            print(f"  Player {player_id} (Team {team}): {distance:.2f} meters")
        
        # Ball possession analysis
        print("\n⚽ BALL POSSESSION ANALYSIS:")
        ball_possessions = df_players[df_players['has_ball'] == 1]
        if not ball_possessions.empty:
            possession_by_team = ball_possessions.groupby('team').size()
            print(f"  Team 1 possessed ball: {possession_by_team.get(1, 0)} times")
            print(f"  Team 2 possessed ball: {possession_by_team.get(2, 0)} times")
    
    # Load frame summary data
    frames_file = os.path.join(csv_dir, 'frames_summary.csv')
    if os.path.exists(frames_file):
        df_frames = pd.read_csv(frames_file)
        
        print("\n📹 CAMERA MOVEMENT STATISTICS:")
        print(f"  Average X movement: {df_frames['camera_movement_x'].mean():.2f}")
        print(f"  Average Y movement: {df_frames['camera_movement_y'].mean():.2f}")
        print(f"  Max X movement: {df_frames['camera_movement_x'].abs().max():.2f}")
        print(f"  Max Y movement: {df_frames['camera_movement_y'].abs().max():.2f}")
    
    # Load ball control stats
    stats_file = os.path.join(csv_dir, 'ball_control_stats.csv')
    if os.path.exists(stats_file):
        df_stats = pd.read_csv(stats_file)
        
        print("\n📊 BALL CONTROL STATISTICS:")
        for _, row in df_stats.iterrows():
            print(f"  {row['metric']}: {row['value']}")


def main():
    """Main function to demonstrate data analysis."""
    print("\n" + "=" * 60)
    print("FOOTBALL ANALYSIS DATA - EXAMPLE ANALYSIS")
    print("=" * 60)
    
    # Default paths (adjust these if your data is elsewhere)
    json_path = 'output_data/analysis_data.json'
    csv_dir = 'output_data/csv'
    
    # Check if data exists
    if not os.path.exists(json_path) and not os.path.exists(csv_dir):
        print("\n❌ No exported data found!")
        print("Please run the main analysis first:")
        print("  python main.py")
        print("\nThis will generate:")
        print(f"  - {json_path}")
        print(f"  - {csv_dir}/")
        return
    
    # Analyze JSON data
    analyze_json_data(json_path)
    
    # Analyze CSV data
    analyze_csv_data(csv_dir)
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print("\n💡 You can use this exported data for:")
    print("  • Creating custom visualizations")
    print("  • Generating detailed reports")
    print("  • Training machine learning models")
    print("  • Integrating with other analysis tools")
    print("  • Exporting to Excel for further analysis")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
