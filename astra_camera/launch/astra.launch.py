from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    camera_name = LaunchConfiguration('camera_name')
    depth_registration = LaunchConfiguration('depth_registration')
    serial_number = LaunchConfiguration('serial_number')
    device_num = LaunchConfiguration('device_num')
    vendor_id = LaunchConfiguration('vendor_id')
    product_id = LaunchConfiguration('product_id')
    enable_point_cloud = LaunchConfiguration('enable_point_cloud')
    enable_colored_point_cloud = LaunchConfiguration('enable_colored_point_cloud')
    point_cloud_qos = LaunchConfiguration('point_cloud_qos')
    connection_delay = LaunchConfiguration('connection_delay')
    color_width = LaunchConfiguration('color_width')
    color_height = LaunchConfiguration('color_height')
    color_fps = LaunchConfiguration('color_fps')
    enable_color = LaunchConfiguration('enable_color')
    flip_color = LaunchConfiguration('flip_color')
    color_qos = LaunchConfiguration('color_qos')
    color_camera_info_qos = LaunchConfiguration('color_camera_info_qos')
    depth_width = LaunchConfiguration('depth_width')
    depth_height = LaunchConfiguration('depth_height')
    depth_fps = LaunchConfiguration('depth_fps')
    enable_depth = LaunchConfiguration('enable_depth')
    flip_depth = LaunchConfiguration('flip_depth')
    depth_qos = LaunchConfiguration('depth_qos')
    depth_camera_info_qos = LaunchConfiguration('depth_camera_info_qos')
    ir_width = LaunchConfiguration('ir_width')
    ir_height = LaunchConfiguration('ir_height')
    ir_fps = LaunchConfiguration('ir_fps')
    enable_ir = LaunchConfiguration('enable_ir')
    flip_ir = LaunchConfiguration('flip_ir')
    ir_qos = LaunchConfiguration('ir_qos')
    ir_camera_info_qos = LaunchConfiguration('ir_camera_info_qos')
    publish_tf = LaunchConfiguration('publish_tf')
    tf_publish_rate = LaunchConfiguration('tf_publish_rate')
    ir_info_url = LaunchConfiguration('ir_info_url')
    color_info_url = LaunchConfiguration('color_info_url')
    color_depth_synchronization = LaunchConfiguration('color_depth_synchronization')
    oni_log_level = LaunchConfiguration('oni_log_level')
    oni_log_to_console = LaunchConfiguration('oni_log_to_console')
    oni_log_to_file = LaunchConfiguration('oni_log_to_file')
    enable_d2c_viewer = LaunchConfiguration('enable_d2c_viewer')
    enable_publish_extrinsic = LaunchConfiguration('enable_publish_extrinsic')

    return LaunchDescription([
        DeclareLaunchArgument('camera_name', default_value='camera'),
        DeclareLaunchArgument('depth_registration', default_value='false'),
        DeclareLaunchArgument('serial_number', default_value=''),
        DeclareLaunchArgument('device_num', default_value='1'),
        DeclareLaunchArgument('vendor_id', default_value='0x2bc5'),
        DeclareLaunchArgument('product_id', default_value=''),
        DeclareLaunchArgument('enable_point_cloud', default_value='true'),
        DeclareLaunchArgument('enable_colored_point_cloud', default_value='false'),
        DeclareLaunchArgument('point_cloud_qos', default_value='default'),
        DeclareLaunchArgument('connection_delay', default_value='100'),
        DeclareLaunchArgument('color_width', default_value='640'),
        DeclareLaunchArgument('color_height', default_value='480'),
        DeclareLaunchArgument('color_fps', default_value='30'),
        DeclareLaunchArgument('enable_color', default_value='true'),
        DeclareLaunchArgument('flip_color', default_value='false'),
        DeclareLaunchArgument('color_qos', default_value='default'),
        DeclareLaunchArgument('color_camera_info_qos', default_value='default'),
        DeclareLaunchArgument('depth_width', default_value='640'),
        DeclareLaunchArgument('depth_height', default_value='480'),
        DeclareLaunchArgument('depth_fps', default_value='30'),
        DeclareLaunchArgument('enable_depth', default_value='true'),
        DeclareLaunchArgument('flip_depth', default_value='false'),
        DeclareLaunchArgument('depth_qos', default_value='default'),
        DeclareLaunchArgument('depth_camera_info_qos', default_value='default'),
        DeclareLaunchArgument('ir_width', default_value='640'),
        DeclareLaunchArgument('ir_height', default_value='480'),
        DeclareLaunchArgument('ir_fps', default_value='30'),
        DeclareLaunchArgument('enable_ir', default_value='true'),
        DeclareLaunchArgument('flip_ir', default_value='false'),
        DeclareLaunchArgument('ir_qos', default_value='default'),
        DeclareLaunchArgument('ir_camera_info_qos', default_value='default'),
        DeclareLaunchArgument('publish_tf', default_value='true'),
        DeclareLaunchArgument('tf_publish_rate', default_value='10.0'),
        DeclareLaunchArgument('ir_info_url', default_value=''),
        DeclareLaunchArgument('color_info_url', default_value=''),
        DeclareLaunchArgument('color_depth_synchronization', default_value='false'),
        DeclareLaunchArgument('oni_log_level', default_value='verbose'),
        DeclareLaunchArgument('oni_log_to_console', default_value='false'),
        DeclareLaunchArgument('oni_log_to_file', default_value='false'),
        DeclareLaunchArgument('enable_d2c_viewer', default_value='false'),
        DeclareLaunchArgument('enable_publish_extrinsic', default_value='false'),
        Node(
            package='astra_camera',
            executable='astra_camera_node',
            name='camera',
            namespace=camera_name,
            output='screen',
            parameters=[
                {'camera_name': camera_name},
                {'depth_registration': depth_registration},
                {'serial_number': serial_number},
                {'device_num': device_num},
                {'vendor_id': vendor_id},
                {'product_id': product_id},
                {'enable_point_cloud': enable_point_cloud},
                {'enable_colored_point_cloud': enable_colored_point_cloud},
                {'point_cloud_qos': point_cloud_qos},
                {'connection_delay': connection_delay},
                {'color_width': color_width},
                {'color_height': color_height},
                {'color_fps': color_fps},
                {'enable_color': enable_color},
                {'flip_color': flip_color},
                {'color_qos': color_qos},
                {'color_camera_info_qos': color_camera_info_qos},
                {'depth_width': depth_width},
                {'depth_height': depth_height},
                {'depth_fps': depth_fps},
                {'enable_depth': enable_depth},
                {'flip_depth': flip_depth},
                {'depth_qos': depth_qos},
                {'depth_camera_info_qos': depth_camera_info_qos},
                {'ir_width': ir_width},
                {'ir_height': ir_height},
                {'ir_fps': ir_fps},
                {'enable_ir': enable_ir},
                {'flip_ir': flip_ir},
                {'ir_qos': ir_qos},
                {'ir_camera_info_qos': ir_camera_info_qos},
                {'publish_tf': publish_tf},
                {'tf_publish_rate': tf_publish_rate},
                {'ir_info_url': ir_info_url},
                {'color_info_url': color_info_url},
                {'color_depth_synchronization': color_depth_synchronization},
                {'oni_log_level': oni_log_level},
                {'oni_log_to_console': oni_log_to_console},
                {'oni_log_to_file': oni_log_to_file},
                {'enable_d2c_viewer': enable_d2c_viewer},
                {'enable_publish_extrinsic': enable_publish_extrinsic},
            ],
            remappings=[
                ('depth/color/points', 'depth_registered/points'),
            ]
        ),
    ])
