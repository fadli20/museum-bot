#!/bin/bash
echo "============================================"
echo "🤖 Museum Guide Robot - Full System Launch"
echo "============================================"
echo ""
echo "This will launch:"
echo "  ✅ LiDAR (RPLIDAR A1)"
echo "  ✅ SLAM (slam_toolbox)"
echo "  ✅ RViz (with all markers: people, crowds, barrier)"
echo "  ✅ Motor Driver (xy160d_driver.py)"
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
pkill -f "xy160d_driver" 2>/dev/null
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

echo ""
echo "🛞 Starting Motor Driver (xy160d_driver.py)..."
echo ""

# Start the motor driver in the background
ros2 run mecanum_robot xy160d_driver.py &
DRIVER_PID=$!

# Give the driver time to initialise
sleep 3

echo ""
echo "🤖 Starting Autonomous Viewer (guide + web interface)..."
echo ""

# Start the autonomous viewer (this will block until Ctrl+C)
python3 autonomous_view.py

# When the script stops (e.g., Ctrl+C), cleanup
echo ""
echo "🧹 Cleaning up..."
kill $DRIVER_PID 2>/dev/null
kill $SLAM_PID 2>/dev/null
pkill -f "sllidar_node" 2>/dev/null
pkill -f "slam_toolbox" 2>/dev/null
pkill -f "rviz2" 2>/dev/null
pkill -f "static_transform_publisher" 2>/dev/null
pkill -f "fake_odom" 2>/dev/null
echo "✅ Done!"
