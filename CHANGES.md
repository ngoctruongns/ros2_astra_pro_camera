# Changes in This Update

## Major Changes

### 1. Python Launch Files (ROS2 Jazzy Standard)

**Old Way (XML):**
```bash
ros2 launch astra_camera astra.launch.xml
```

**New Way (Python):**
```bash
ros2 launch astra_camera astra.launch.py
```

**Benefits:**
- Python launch files are the ROS2 Jazzy standard
- Better IDE support and syntax highlighting
- More flexible configuration and composition
- Easier to maintain and version control

**New Launch Files:**
- `astra.launch.py` - For Astra camera (OpenNI color)
- `astra_pro.launch.py` - For Astra Pro camera (UVC color)

The XML launch files are still present but deprecated. We recommend migrating to Python launch files.

### 2. Enhanced Debug Logging

Added comprehensive logging in `ob_camera_node.cpp` to diagnose stream setup issues:

**setupDevices() logging:**
- Shows which streams are enabled and which have sensors
- Logs stream creation success/failure

**setupPublishers() logging:**
- Shows which publishers are created
- Indicates if UVC color is being used

**setupVideoMode() logging:**
- Shows video mode validation details
- Lists supported video modes if requested mode is not available
- Clearer format output (previously showed empty format field)

**startStreams() logging:**
- Shows stream status before starting
- Indicates if streams are skipped for UVC mode
- Better error messages for missing video modes or streams

**pollFrame() logging:**
- Shows which streams are being waited on (once at startup)
- Helps identify if color stream is included or not

**onNewFrameCallback() logging:**
- Shows if image buffer exists for received frames
- Catches missing buffers before processing

**Usage:** All logging is enabled by default at INFO level. Use:
```bash
ros2 launch astra_camera astra_pro.launch.py oni_log_level:=verbose
```

### 3. Documentation Updates

**README.MD:**
- Restructured "Getting Started" section with clear setup steps
- Updated all launch commands to use Python instead of XML
- Added examples of launching with custom parameters
- Improved RViz2 setup instructions
- Clarified multi-camera launching with `device_num` parameter
- Updated calibration file section with YAML examples

**QUICK_START.md (NEW):**
- Quick reference guide for Astra Pro users
- Step-by-step setup instructions
- Troubleshooting section with common issues
- Common parameter examples
- Topic and service reference

## For Users

### If you're using Astra Pro (with UVC color):

```bash
# Instead of:
ros2 launch astra_camera astra_pro.launch.xml

# Use:
ros2 launch astra_camera astra_pro.launch.py
```

### If you're using Astra (OpenNI only):

```bash
# Instead of:
ros2 launch astra_camera astra.launch.xml

# Use:
ros2 launch astra_camera astra.launch.py
```

### Parameter Passing

The parameter syntax has changed:

**XML (old):**
```bash
ros2 launch astra_camera astra_pro.launch.xml camera_name:=my_camera
```

**Python (new):**
```bash
ros2 launch astra_camera astra_pro.launch.py camera_name:=my_camera
```

The parameter format is the same, just with `.py` extension!

## For Debugging Color Stream Issues

If you're experiencing color stream not publishing data:

1. Check your launch command uses the correct launch file for your camera model
2. Run with verbose logging to see stream setup details:
   ```bash
   ros2 launch astra_camera astra_pro.launch.py oni_log_level:=verbose
   ```
3. Look for these key log lines:
   - "setupDevices: Creating streams" - should show color enabled
   - "setupPublishers: Creating publishers" - should show color publisher created
   - "startStreams: Starting streams" - should show color stream enabled and started
   - "pollFrame: Waiting on N streams" - color should be in the list
4. Check if the device actually has a color sensor for your camera model

## Backward Compatibility

- All XML launch files (`.launch.xml`) still work but are not actively maintained
- Existing ROS2 parameters remain unchanged
- All node executable names and topic names remain the same
- Services and message types are unchanged

## Next Steps

1. Update your launch scripts to use `.launch.py` files
2. Run the quick start guide to test your setup
3. Check the new enhanced logging if you have issues
4. Report any problems with detailed logs from the new debug output

## Build and Install

After pulling these changes, rebuild your workspace:

```bash
cd ~/ros2_ws
colcon build --event-handlers console_direct+ --cmake-args -DCMAKE_BUILD_TYPE=Release
source ./install/setup.bash
```

The new Python launch files will be automatically installed to:
```
~/ros2_ws/install/astra_camera/share/astra_camera/launch/
```
