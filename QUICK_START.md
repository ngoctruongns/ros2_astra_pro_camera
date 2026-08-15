# Quick Start Guide - Astra Pro Camera

## System Setup

### 1. Install ROS2 Jazzy

```bash
# Follow official ROS2 installation
# https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html
source /opt/ros/jazzy/setup.bash
```

### 2. Install Dependencies

```bash
sudo apt install libgflags-dev ros-jazzy-image-geometry \
  ros-jazzy-camera-info-manager ros-jazzy-image-transport \
  ros-jazzy-message-filters ros-jazzy-cv-bridge \
  libgoogle-glog-dev libusb-1.0-0-dev libeigen3-dev libuvc-dev
```

### 3. Build the Package

```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --event-handlers console_direct+ --cmake-args -DCMAKE_BUILD_TYPE=Release

# Wait for build to complete...
source ./install/setup.bash
```

### 4. Install USB Rules

```bash
cd src/ros2_astra_camera/astra_camera/scripts
sudo bash install.sh
sudo udevadm control --reload-rules && sudo udevadm trigger
```

## Running the Camera

### Start Astra Pro Camera

```bash
# Terminal 1 - Launch the camera driver
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch astra_camera astra_pro.launch.py
```

You should see logs like:
- "`setupDevices: Creating streams (use_uvc_camera=true)`"
- "`pollFrame: Waiting on N streams`"
- "`depth is started`"
- "`color is started`"

### View Data in RViz2

```bash
# Terminal 2 - Launch RViz2
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
rviz2
```

In RViz2:
1. Set **Fixed Frame** to `camera_link`
2. Add **Image** display → topic `/camera/color/image_raw`
3. Add **Image** display → topic `/camera/depth/image_raw`
4. Add **PointCloud2** display → topic `/camera/depth/points`

### Check Topics

```bash
# Terminal 3 - List available topics
source /opt/ros/jazzy/setup.bash
ros2 topic list

# Should show:
# /camera/color/camera_info
# /camera/color/image_raw
# /camera/depth/camera_info
# /camera/depth/image_raw
# /camera/ir/camera_info
# /camera/ir/image_raw
# /camera/depth/points
# ... and more
```

## Troubleshooting

### Color Stream Not Publishing

**Issue:** Depth works but color topic shows no data.

**Solution:**
- Verify you're using `astra_pro.launch.py` (NOT `astra.launch.py`)
- Check that `use_uvc_camera=true` is set (default for Astra Pro)
- Make sure UVC device is recognized: `lsusb | grep 2bc5`
- Verify color camera works in cheese: `cheese /dev/video0`

### Depth/Color Not Synchronized

**Note:** Astra Pro depth and color are captured on separate USB endpoints with separate clocks. Synchronization is approximate, not frame-accurate. Use `message_filters::ApproximateTime` in your application with a slop of 15-35 ms.

### Permission Denied on UVC Device

```bash
# Check USB device
lsusb | grep 2bc5

# If permission denied, reinstall USB rules
cd src/ros2_astra_camera/astra_camera/scripts
sudo bash install.sh
sudo udevadm control --reload-rules && sudo udevadm trigger

# Then disconnect and reconnect camera
```

### Shared Memory Lock

If the driver hangs at startup:

```bash
# Clean up semaphores
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run astra_camera cleanup_shm_node

# Then relaunch
ros2 launch astra_camera astra_pro.launch.py
```

## Common Parameters

### Camera Name
```bash
ros2 launch astra_camera astra_pro.launch.py camera_name:=my_camera
```

### Color Resolution and FPS
```bash
ros2 launch astra_camera astra_pro.launch.py \
  color_width:=1280 color_height:=720 color_fps:=15
```

### Depth Registration (Align Depth to Color)
```bash
ros2 launch astra_camera astra_pro.launch.py depth_registration:=true
```

### All Parameters with Values
```bash
ros2 launch astra_camera astra_pro.launch.py \
  camera_name:=camera \
  enable_depth:=true \
  enable_color:=true \
  enable_ir:=false \
  depth_width:=640 \
  depth_height:=480 \
  depth_fps:=30 \
  color_width:=640 \
  color_height:=480 \
  color_fps:=30 \
  depth_registration:=true \
  enable_point_cloud:=true \
  enable_colored_point_cloud:=true
```

## Key Topics and Services

### Topics (Published)
- `/camera/depth/image_raw` - Depth image (16UC1, mm units)
- `/camera/depth/camera_info` - Depth camera parameters
- `/camera/color/image_raw` - RGB color image (RGB8)
- `/camera/color/camera_info` - Color camera parameters
- `/camera/ir/image_raw` - IR image (MONO8)
- `/camera/ir/camera_info` - IR camera parameters
- `/camera/depth/points` - 3D point cloud
- `/camera/depth_registered/points` - Colored point cloud (if enabled)

### Key Services
```bash
# Get device info
ros2 service call /camera/get_device_info astra_camera_msgs/srv/GetDeviceInfo '{}'

# Get SDK version
ros2 service call /camera/get_sdk_version astra_camera_msgs/srv/GetString '{}'

# Set UVC color exposure (Astra Pro color only)
ros2 service call /camera/set_uvc_exposure astra_camera_msgs/srv/SetInt32 '{data: 2000}'

# Set UVC color gain
ros2 service call /camera/set_uvc_gain astra_camera_msgs/srv/SetInt32 '{data: 200}'

# Toggle sensors
ros2 service call /camera/toggle_depth std_srvs/srv/SetBool '{data: true}'
ros2 service call /camera/toggle_color std_srvs/srv/SetBool '{data: true}'
```

## For More Information

See [README.MD](README.MD) for:
- Complete parameter list
- Multi-camera setup
- Calibration file usage
- DDS tuning for high-throughput applications

See [docs/astra_pro_ros2_notes_vi.md](docs/astra_pro_ros2_notes_vi.md) for:
- Detailed architecture explanation
- Depth/color data flow
- Timestamp and synchronization details
