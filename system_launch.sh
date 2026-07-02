#!/bin/bash
echo "============================================"
echo "🤖 Museum Guide Robot - Full System Launch"
echo "============================================"
echo ""
echo "This will launch:"
echo "  ✅ LiDAR (RPLIDAR A1)"
echo "  ✅ SLAM (slam_toolbox)"
echo "  ✅ RViz (with all markers: people, crowds, barrier)"
echo "  ✅ Autonomous Viewer (merged guide + web interface)"
echo ""
echo "============================================"

cd ~/ws_lidar

# Kill any old processes
echo "🧹 Cleaning up old processes..."
pkill -f "sllidar_node" 2>/dev/null
pkill -f "slam_toolbox" 2>/dev/null
pkill -f "rviz2" 2>/dev/null
pkill -f "museum_guide_mqtt" 2>/dev/null
pkill -f "autonomous_view" 2>/dev/null
pkill -f "static_transform_publisher" 2>/dev/null
pkill -f "fake_odom" 2>/dev/null
sleep 2

# Source ROS2 and workspace
source /opt/ros/jazzy/setup.bash
source install/setup.bash

# Activate virtual environment (contains all Python dependencies)
source venv_mqtt/bin/activate

echo ""
echo "📡 Starting LiDAR + SLAM + RViz..."
echo ""

# Start LiDAR + SLAM + RViz in the background
./run_slam.sh &
SLAM_PID=$!

# Wait for LiDAR and SLAM to initialize
echo "⏳ Waiting for LiDAR and SLAM to initialize (15 sec)..."
sleep 15

# Start the autonomous viewer (merged guide + web UI)
echo ""
echo "🤖 Starting Autonomous Viewer (guide + web interface)..."
echo ""
python3 autonomous_view.py

# When the script stops (e.g., Ctrl+C), cleanup
echo ""
echo "🧹 Cleaning up..."
kill $SLAM_PID 2>/dev/null
pkill -f "sllidar_node" 2>/dev/null
pkill -f "slam_toolbox" 2>/dev/null
pkill -f "rviz2" 2>/dev/null
pkill -f "static_transform_publisher" 2>/dev/null
pkill -f "fake_odom" 2>/dev/null
echo "✅ Done!"
