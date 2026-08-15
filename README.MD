# ros2_astra_camera

A ROS2 driver for Orbbec 3D cameras. Tested on ROS 2 Jazzy / Ubuntu 24.04.

> Architecture, data flow and depth/colour synchronisation are documented in
> [docs/astra_pro_ros2_notes_vi.md](docs/astra_pro_ros2_notes_vi.md) (Vietnamese).

## Install dependencies

### ROS2

● Please refer to the
official [ROS 2 installation guide](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)

### other dependencies

● Install dependencies (be careful with your ROS distribution)

```bash
# Assuming you have sourced the ros environment, same below
sudo apt install libgflags-dev ros-$ROS_DISTRO-image-geometry ros-$ROS_DISTRO-camera-info-manager \
ros-$ROS_DISTRO-image-transport ros-$ROS_DISTRO-message-filters ros-$ROS_DISTRO-cv-bridge \
libgoogle-glog-dev libusb-1.0-0-dev libeigen3-dev
```

● Install libuvc — on Ubuntu 24.04 the distribution package is enough:

```bash
sudo apt install libuvc-dev
```

or build it from source if your distribution does not ship it:

```bash
git clone https://github.com/libuvc/libuvc.git
cd libuvc
mkdir build && cd build
cmake .. && make -j4
sudo make install
sudo ldconfig # Refreshing the link library
```

## Getting Started

### Setup

● Create a new ROS2 workspace

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

● Clone this repository

```bash
git clone https://github.com/yourusername/ros2_astra_camera.git
```

● Install libusb rules

```bash
cd ros2_astra_camera/astra_camera/scripts
sudo bash install.sh
sudo udevadm control --reload-rules && sudo udevadm trigger
```

● Build the package

```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash 
colcon build --event-handlers console_direct+ --cmake-args -DCMAKE_BUILD_TYPE=Release
```

### Running the Camera

#### For Astra Pro (with UVC color)

```bash
source /opt/ros/jazzy/setup.bash 
source ./install/setup.bash 
ros2 launch astra_camera astra_pro.launch.py
```

#### For Astra (OpenNI only)

```bash
source /opt/ros/jazzy/setup.bash 
source ./install/setup.bash 
ros2 launch astra_camera astra.launch.py
```

#### Launch with custom parameters

```bash
# Example: Custom camera name
ros2 launch astra_camera astra_pro.launch.py camera_name:=my_camera

# Example: Custom color resolution (Astra Pro)
ros2 launch astra_camera astra_pro.launch.py color_width:=1280 color_height:=720 color_fps:=15

# Example: Enable depth registration (Astra)
ros2 launch astra_camera astra.launch.py depth_registration:=true

# Example: Multiple parameters
ros2 launch astra_camera astra_pro.launch.py \
  camera_name:=my_camera \
  enable_depth:=true \
  enable_color:=true \
  depth_registration:=true
```

### View in RViz2

Open another terminal and run:

```bash
source /opt/ros/jazzy/setup.bash 
source ./install/setup.bash 
rviz2
```

In RViz2:
1. Change **Fixed Frame** to `camera_link`
2. Add **Image** display → Select `/camera/color/image_raw` topic
3. Add **Image** display → Select `/camera/depth/image_raw` topic  
4. Add **PointCloud2** display → Select `/camera/depth/points` or `/camera/depth_registered/points`

### Check Topics and Services

List available topics:

```bash
source /opt/ros/jazzy/setup.bash 
ros2 topic list
```

List available services:

```bash
ros2 service list
```

List node parameters:

```bash
ros2 param list /camera
```

View topic information with QoS:

```bash
ros2 topic info -v /camera/depth/image_raw
```

● Get camera parameters

```bash
ros2 service call /camera/get_camera_info astra_camera_msgs/srv/GetCameraInfo '{}'
```

● Check camera parameters, please refer to the ROS documentation for the meaning of the specific fields of the camera
parameters  [camera info](http://docs.ros.org/en/melodic/api/sensor_msgs/html/msg/CameraInfo.html)

```bash
ros2 topic echo /camera/depth/camera_info
ros2 topic echo /camera/color/camera_info
```

● Check device information

```bash
ros2 service call /camera/get_device_info astra_camera_msgs/srv/GetDeviceInfo '{}'
```

● Get the SDK version

```bash
ros2 service call /camera/get_sdk_version  astra_camera_msgs/srv/GetString "{}"
```

● Set/get (auto) exposure

```bash
 # Auto exposure switch. For setting the exposure manually, please turn off the auto exposure first
 ros2 service call /camera/set_color_auto_exposure std_srvs/srv/SetBool '{data: false}' 
 ros2 service call /camera/set_uvc_auto_exposure std_srvs/srv/SetBool '{data: false}'
 ros2 service call /camera/set_ir_auto_exposure std_srvs/srv/SetBool "{data: false}"
    
# Setting exposure values
ros2 service call /camera/set_ir_exposure astra_camera_msgs/srv/SetInt32 "{data: 2000}"
ros2 service call /camera/set_color_exposure astra_camera_msgs/srv/SetInt32 "{data: 2000}"
ros2 service call /camera/set_uvc_exposure astra_camera_msgs/srv/SetInt32 "{data: 2000}"
 # Get exposure
 ros2 service call /camera/get_ir_exposure astra_camera_msgs/srv/GetInt32 "{}"
 ros2 service call /camera/get_color_exposure astra_camera_msgs/srv/GetInt32 "{}"
 ros2 service call /camera/get_uvc_exposure astra_camera_msgs/srv/GetInt32 "{}"
```

● Set/get gain

```bash
# Get Gain
ros2 service call /camera/get_color_gain astra_camera_msgs/srv/GetInt32 '{}' # OpenNI camera
ros2 service call /camera/get_ir_gain astra_camera_msgs/srv/GetInt32 '{}' # OpenNI camera
ros2 service call /camera/get_uvc_gain astra_camera_msgs/srv/GetInt32 "{}" # UVC camera
 # Setting the gain
ros2 service call /camera/set_color_gain astra_camera_msgs/srv/SetInt32 "{data: 200}"
ros2 service call /camera/set_ir_gain astra_camera_msgs/srv/SetInt32 "{data: 200}"
ros2 service call /camera/set_uvc_gain astra_camera_msgs/srv/SetInt32 "{data: 200}"
```

● Set mirror mode

```bash
ros2 service call /camera/set_color_mirror std_srvs/srv/SetBool '{data: true}'
ros2 service call /camera/set_ir_mirror std_srvs/srv/SetBool '{data: true}'
ros2 service call /camera/set_depth_mirror std_srvs/srv/SetBool '{data: true}'
ros2 service call /camera/set_uvc_color_mirror std_srvs/srv/SetBool '{data: true}'
```

● Set/get (auto) white balance

```bash
ros2 service call /camera/get_color_auto_white_balance astra_camera_msgs/srv/GetInt32 '{}' # Return 0 or 1
ros2 service call /camera/set_color_auto_white_balance std_srvs/srv/SetBool '{data: false}'
```

● Turn on/off laser

```bash
ros2 service call /camera/set_laser_enable std_srvs/srv/SetBool '{data: true}' # Turn on
ros2 service call /camera/set_laser_enable std_srvs/srv/SetBool '{data: false}' #Turn off
```

● Turn on/off fan

```bash
 ros2 service call /camera/set_fan_mode std_srvs/srv/SetBool '{data: true}' #Turn on
 ros2 service call /camera/set_fan_mode std_srvs/srv/SetBool '{data: false}' # Turn off
```

● Turn LDP on/off

```bash
ros2 service call /camera/set_ldp_enable std_srvs/srv/SetBool '{data: true}'
ros2 service call /camera/set_ldp_enable std_srvs/srv/SetBool '{data: false}'
```

● Turn sensors on/off

```bash
ros2 service call  /camera/toggle_ir std_srvs/srv/SetBool "{data: true}"
ros2 service call  /camera/toggle_color std_srvs/srv/SetBool "{data: true}"
ros2 service call  /camera/toggle_depth std_srvs/srv/SetBool "{data: true}"
ros2 service call /camera/toggle_uvc_camera std_srvs/srv/SetBool "{data : true}"
```

## Multi-Camera

### Get Serial Numbers

First, get the serial number of each camera:

```bash
source /opt/ros/jazzy/setup.bash 
source ./install/setup.bash
ros2 run astra_camera list_devices_node
```

Note the serial numbers for each camera.

### Launch Multiple Cameras

For multiple cameras of the same model, use the corresponding launch file with different serial numbers and namespaces:

```bash
# Terminal 1 - Camera 1 (Astra Pro with serial ABC123)
source /opt/ros/jazzy/setup.bash 
source ./install/setup.bash
ros2 launch astra_camera astra_pro.launch.py \
  camera_name:=camera_01 \
  serial_number:=ABC123 \
  device_num:=2

# Terminal 2 - Camera 2 (Astra Pro with serial DEF456)
source /opt/ros/jazzy/setup.bash 
source ./install/setup.bash
ros2 launch astra_camera astra_pro.launch.py \
  camera_name:=camera_02 \
  serial_number:=DEF456 \
  device_num:=2
```

### Shared Memory Cleanup

Astra camera uses semaphores for process synchronization. If the camera fails to start, the semaphore file may remain in `/dev/shm`, causing the next launch to hang.

Before launching, you can clean up the shared memory:

```bash
source /opt/ros/jazzy/setup.bash 
source ./install/setup.bash
ros2 run astra_camera cleanup_shm_node 
```

Or manually clean up:

```bash
sudo rm -f /dev/shm/astra_camera_*
```

### View All Camera Topics

In RViz2 or another application, you can now access topics from both cameras:

```bash
# Camera 1 topics
/camera_01/depth/image_raw
/camera_01/color/image_raw
/camera_01/depth/points

# Camera 2 topics
/camera_02/depth/image_raw
/camera_02/color/image_raw
/camera_02/depth/points
```

## Camera Calibration

You can use calibration files for more accurate camera parameters. To use custom calibration:

### Prepare Calibration Files

The calibration files should be in YAML format. Create two files: one for depth/IR camera and one for color camera.

**Depth/IR Camera Calibration** (`depth_camera.yaml`):

```yaml
image_width: 640
image_height: 480
camera_name: ir_camera
camera_matrix:
  rows: 3
  cols: 3
  data: [517.301, 0, 326.785, 0, 519.291, 244.563, 0, 0, 1]
distortion_model: plumb_bob
distortion_coefficients:
  rows: 1
  cols: 5
  data: [-0.41527, 0.31874, -0.00197, 0.00071, 0]
rectification_matrix:
  rows: 3
  cols: 3
  data: [0.999973, 0.00612598, -0.00406652, -0.00610201, 0.999964, 0.00588094, 0.0041024, -0.00585596, 0.999974]
projection_matrix:
  rows: 3
  cols: 4
  data: [517.301, 0, 326.785, 0, 0, 519.291, 244.563, 0, 0, 0, 1, 0]
```

**Color Camera Calibration** (`color_camera.yaml`):

```yaml
image_width: 640
image_height: 480
camera_name: rgb_camera
camera_matrix:
  rows: 3
  cols: 3
  data: [517.301, 0, 326.785, 0, 519.291, 244.563, 0, 0, 1]
distortion_model: plumb_bob
distortion_coefficients:
  rows: 1
  cols: 5
  data: [-0.41527, 0.31874, -0.00197, 0.00071, 0]
rectification_matrix:
  rows: 3
  cols: 3
  data: [0.999973, 0.00612598, -0.00406652, -0.00610201, 0.999964, 0.00588094, 0.0041024, -0.00585596, 0.999974]
projection_matrix:
  rows: 3
  cols: 4
  data: [517.301, 0, 326.785, -25.3167, 0, 519.291, 244.563, 0.282065, 0, 0, 1, 0.0777703]
```

> **Important:** Camera names must be exactly `ir_camera` (for depth/IR) and `rgb_camera` (for color).

### Launch with Calibration Files

Pass the calibration file paths to the launch file:

```bash
ros2 launch astra_camera astra_pro.launch.py \
  ir_info_url:=file:///path/to/depth_camera.yaml \
  color_info_url:=file:///path/to/color_camera.yaml
```

## Launch parameters

* `connection_delay`, The delay time for reopening the device in seconds. Some devices would take longer time to
  initialize, such as Astra mini, so reopening the device immediately would causes firmware crashes when hot plug.

* `enable_point_cloud`, Whether to enable point cloud.
* `enable_colored_point_cloud`, Whether to enable RGB point cloud.
* `point_cloud_qos`, `[color|depth|ir]_qos`,`[color|depth|ir]_camera_info_qos`, ROS2 Message QoS,
  can be set to `SYSTEM_DEFAULT`, `DEFAULT`,`PARAMETER_EVENTS` ,`SERVICES_DEFAULT`, `PARAMETERS`, `SENSOR_DATA`,
  corresponds to `rmw_qos_profile_system_default`, `rmw_qos_profile_default`, `rmw_qos_profile_parameter_events`
 `rmw_qos_profile_services_default`,`rmw_qos_profile_parameters`, `SENSOR_DATA`,Case-insensitive.
* `enable_d2c_viewer`, Publish D2C overlay image (For Test only).
* `device_num`,The number of devices, You need to fill in the number of devices when you need multiple cameras.
* `color_width`， `color_height`， `color_fps`， color stream resolution and frame rate.
* `ir_width`， `ir_height`， `ir_fps`，IR stream resolution and frame rate
* `depth_width`， `depth_height`， `depth_fps` depth stream resolution and frame rate
* `enable_color`， Whether to enable RGB camera, this parameter has no effect when the RGB camera is UVC protocol
* `enable_depth` , Whether to enable depth camera
* `enable_ir`, Whether to enable IR camera
* `depth_registration`, Enables hardware depth to color alignment, requires RGB point cloud to open
* `depth_scale`, Depth image zoom scale, e.g. set to 2 means aligning depth 320x240 to RGB 640x480
* `color_roi_x`， `color_roi_y`， `color_roi_width`， `color_roi_height`, Whether to crop RGB images, the default is -1,
  which is only used when the RGB resolution is greater than the depth resolution and needs to be aligned. For example,
  if you need to align the depth 640x400 to RGB 640x480, you need to set color_roi_x: 0, color_roi_y: 0,
  color_roi_width: 640, color_roi_height: 400. roi_height: 400, which will crop the top 400 pixels of the RGB with a
  corresponding depth ROI.
* `color_depth_synchronization`，Enable synchronization of RGB with depth
* `use_uvc_camera`，if the RGB camera is UVC protocol, setting as true, UVC is the protocol that currently includes
  dabai, dabai_dcw etc.
* `uvc_product_id`，pid of UVC camera
* `uvc_camera_format`，Image format for uvc camera
* `uvc_retry_count` sometimes the UVC protocol camera does not reconnect successfully when hot-plug, requiring many
  times to retry.
* `enable_publish_extrinsic` Enable publish camera extrinsic.
* `oni_log_level`, Log levels for OpenNI verbose/ info /warning/ error /none
* `oni_log_to_console`, Whether to output OpenNI logs to the console
* `oni_log_to_file`, Whether to output OpenNI logs to a file, by default it will save in Log folder under the path of
  the currently running program

## Advanced Configuration

### DDS Tuning (Optional - For High-Performance Applications)

**When to use:** Only if you experience:
- High latency (delayed image/data delivery)
- Dropped frames or messages
- Running multiple cameras on the same network
- Limited network bandwidth

**Default is usually fine for single camera applications.** Only proceed if you have performance issues.

#### What is DDS?

DDS (Data Distribution Service) is the middleware that ROS2 uses to communicate between nodes. It handles how image data, point clouds, and other messages are transmitted over the network/local IPC.

#### Quick Fix for Most Cases

If you just need better performance, this usually works:

```bash
# Add to ~/.bashrc or ~/.zshrc
export ROS_LOCALHOST_ONLY=1
```

This forces all ROS2 communication to use localhost (loopback), which is faster for single-machine setups.

Then restart your terminals:
```bash
source ~/.bashrc
```

#### Full DDS Tuning (CycloneDDS)

Only do this if the quick fix above doesn't work:

**Step 1: Create CycloneDDS config file**

```bash
sudo nano /etc/cyclonedds/config.xml
```

Add this content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CycloneDDS xmlns="https://cdds.io/config" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="https://cdds.io/config https://raw.githubusercontent.com/eclipse-cyclonedds/cyclonedds/master/etc/cyclonedds.xsd">
    <Domain id="any">
        <General>
            <!-- Use localhost only for local machine communication -->
            <NetworkInterfaceAddress>lo</NetworkInterfaceAddress>
            <!-- Disable multicast for cleaner network usage -->
            <AllowMulticast>false</AllowMulticast>
        </General>
        <Internal>
            <!-- Increase buffer size for high-throughput cameras (multiple streams) -->
            <MinimumSocketReceiveBufferSize>16MB</MinimumSocketReceiveBufferSize>
        </Internal>
        <Discovery>
            <!-- Automatic node discovery -->
            <ParticipantIndex>auto</ParticipantIndex>
            <MaxAutoParticipantIndex>30</MaxAutoParticipantIndex>
            <Peers>
                <Peer address="localhost"/>
            </Peers>
        </Discovery>
    </Domain>
</CycloneDDS>
```

**Step 2: Add environment variables**

Add to `~/.bashrc` or `~/.zshrc`:

```bash
export ROS_DOMAIN_ID=42                          # Domain ID (0-232)
export ROS_LOCALHOST_ONLY=1                       # Stay on localhost
export CYCLONEDDS_URI=file:///etc/cyclonedds/config.xml
```

Then reload:
```bash
source ~/.bashrc
```

**Step 3: Increase OS buffer sizes (optional but recommended)**

```bash
sudo nano /etc/sysctl.d/10-cyclone-max.conf
```

Add:
```bash
# Increase network buffer for high throughput
net.core.rmem_max=2147483647
net.core.rmem_default=2147483647
net.core.wmem_max=2147483647
net.core.wmem_default=2147483647
```

Apply changes:
```bash
sudo sysctl -p /etc/sysctl.d/10-cyclone-max.conf
```

#### What Each Setting Does

| Setting | Purpose | When Needed |
|---------|---------|------------|
| `NetworkInterfaceAddress=lo` | Use loopback (localhost) only | Always for single machine |
| `AllowMulticast=false` | Disable broadcast discovery | Reduces network noise |
| `MinimumSocketReceiveBufferSize=16MB` | Larger buffer for images | Multiple cameras or high FPS |
| `ROS_LOCALHOST_ONLY=1` | Force localhost communication | Best for single computer |
| `net.core.rmem_max` | OS receive buffer limit | Large camera data (multiple streams) |

#### Verify DDS Configuration

Check your DDS middleware:
```bash
ros2 doctor
```

Should show your configured DDS implementation (usually CycloneDDS).

#### Performance Testing

Compare performance before and after tuning:

```bash
# Measure latency of depth images
ros2 topic delay /camera/depth/image_raw

# Measure latency of color images
ros2 topic delay /camera/color/image_raw

# Check message rate
ros2 topic hz /camera/depth/image_raw
```

Record measurements before and after tuning to see if it helps.

#### Further Reading

- [ROS DDS Tuning Guide](https://docs.ros.org/en/humble/How-To-Guides/DDS-tuning.html)
- [ROS Domain IDs](https://docs.ros.org/en/humble/Concepts/About-Domain-ID.html)
- [CycloneDDS Documentation](https://github.com/eclipse-cyclonedds/cyclonedds)

## Frequently Asked Questions

● No point cloud or image displayed on Rviz2

* The default QoS for outgoing messages is sense_data, i.e. Relaiblity Policy = Best Effort, please check if the
  Relaiblity Policy is set to Best Effort on Rviz2, and also check if there is any problem with the QoS setting of the
  message via `ros2 topic info -v /xxx/topic`

● No picture from multiple cameras

* It is possible that the power supply is insufficient, do not connect all cameras to the same hub, and a powered hub is
  recommended

* It is also possible that the resolution is too high, try turning it lower
* If the color camera is an UVC camera, the serial number of the UVC may not be set

## License

Copyright 2023 Orbbec Ltd.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this project except in compliance with
the License. You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "
AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.

**Other names and brands may be claimed as the property of others**
