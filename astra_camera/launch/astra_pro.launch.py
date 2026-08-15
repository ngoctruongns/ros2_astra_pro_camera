from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, PushRosNamespace


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
    color_roi_x = LaunchConfiguration('color_roi_x')
    color_roi_y = LaunchConfiguration('color_roi_y')
    color_roi_width = LaunchConfiguration('color_roi_width')
    color_roi_height = LaunchConfiguration('color_roi_height')
    depth_roi_x = LaunchConfiguration('depth_roi_x')
    depth_roi_y = LaunchConfiguration('depth_roi_y')
    depth_roi_width = LaunchConfiguration('depth_roi_width')
    depth_roi_height = LaunchConfiguration('depth_roi_height')
    depth_scale = LaunchConfiguration('depth_scale')
    color_depth_synchronization = LaunchConfiguration('color_depth_synchronization')
    use_uvc_camera = LaunchConfiguration('use_uvc_camera')
    uvc_vendor_id = LaunchConfiguration('uvc_vendor_id')
    uvc_product_id = LaunchConfiguration('uvc_product_id')
    uvc_retry_count = LaunchConfiguration('uvc_retry_count')
    uvc_camera_format = LaunchConfiguration('uvc_camera_format')
    uvc_flip = LaunchConfiguration('uvc_flip')
    oni_log_level = LaunchConfiguration('oni_log_level')
    oni_log_to_console = LaunchConfiguration('oni_log_to_console')
    oni_log_to_file = LaunchConfiguration('oni_log_to_file')
    enable_d2c_viewer = LaunchConfiguration('enable_d2c_viewer')
    enable_publish_extrinsic = LaunchConfiguration('enable_publish_extrinsic')

    declare_camera_name_cmd = DeclareLaunchArgument(
        'camera_name',
        default_value='camera',
        description='Camera name'
    )

    declare_depth_registration_cmd = DeclareLaunchArgument(
        'depth_registration',
        default_value='false',
        description='Enable hardware depth registration'
    )

    declare_serial_number_cmd = DeclareLaunchArgument(
        'serial_number',
        default_value='',
        description='Camera serial number'
    )

    declare_device_num_cmd = DeclareLaunchArgument(
        'device_num',
        default_value='1',
        description='Number of devices'
    )

    declare_vendor_id_cmd = DeclareLaunchArgument(
        'vendor_id',
        default_value='0',
        description='Vendor ID'
    )

    declare_product_id_cmd = DeclareLaunchArgument(
        'product_id',
        default_value='0',
        description='Product ID'
    )

    declare_enable_point_cloud_cmd = DeclareLaunchArgument(
        'enable_point_cloud',
        default_value='true',
        description='Enable point cloud'
    )

    declare_enable_colored_point_cloud_cmd = DeclareLaunchArgument(
        'enable_colored_point_cloud',
        default_value='false',
        description='Enable colored point cloud'
    )

    declare_point_cloud_qos_cmd = DeclareLaunchArgument(
        'point_cloud_qos',
        default_value='default',
        description='Point cloud QoS'
    )

    declare_connection_delay_cmd = DeclareLaunchArgument(
        'connection_delay',
        default_value='100',
        description='Connection delay in ms'
    )

    declare_color_width_cmd = DeclareLaunchArgument(
        'color_width',
        default_value='640',
        description='Color image width'
    )

    declare_color_height_cmd = DeclareLaunchArgument(
        'color_height',
        default_value='480',
        description='Color image height'
    )

    declare_color_fps_cmd = DeclareLaunchArgument(
        'color_fps',
        default_value='30',
        description='Color image FPS'
    )

    declare_enable_color_cmd = DeclareLaunchArgument(
        'enable_color',
        default_value='true',
        description='Enable color camera'
    )

    declare_flip_color_cmd = DeclareLaunchArgument(
        'flip_color',
        default_value='false',
        description='Flip color image'
    )

    declare_color_qos_cmd = DeclareLaunchArgument(
        'color_qos',
        default_value='default',
        description='Color QoS'
    )

    declare_color_camera_info_qos_cmd = DeclareLaunchArgument(
        'color_camera_info_qos',
        default_value='default',
        description='Color camera info QoS'
    )

    declare_depth_width_cmd = DeclareLaunchArgument(
        'depth_width',
        default_value='640',
        description='Depth image width'
    )

    declare_depth_height_cmd = DeclareLaunchArgument(
        'depth_height',
        default_value='480',
        description='Depth image height'
    )

    declare_depth_fps_cmd = DeclareLaunchArgument(
        'depth_fps',
        default_value='30',
        description='Depth image FPS'
    )

    declare_enable_depth_cmd = DeclareLaunchArgument(
        'enable_depth',
        default_value='true',
        description='Enable depth camera'
    )

    declare_flip_depth_cmd = DeclareLaunchArgument(
        'flip_depth',
        default_value='false',
        description='Flip depth image'
    )

    declare_depth_qos_cmd = DeclareLaunchArgument(
        'depth_qos',
        default_value='default',
        description='Depth QoS'
    )

    declare_depth_camera_info_qos_cmd = DeclareLaunchArgument(
        'depth_camera_info_qos',
        default_value='default',
        description='Depth camera info QoS'
    )

    declare_ir_width_cmd = DeclareLaunchArgument(
        'ir_width',
        default_value='640',
        description='IR image width'
    )

    declare_ir_height_cmd = DeclareLaunchArgument(
        'ir_height',
        default_value='480',
        description='IR image height'
    )

    declare_ir_fps_cmd = DeclareLaunchArgument(
        'ir_fps',
        default_value='30',
        description='IR image FPS'
    )

    declare_enable_ir_cmd = DeclareLaunchArgument(
        'enable_ir',
        default_value='true',
        description='Enable IR camera'
    )

    declare_flip_ir_cmd = DeclareLaunchArgument(
        'flip_ir',
        default_value='false',
        description='Flip IR image'
    )

    declare_ir_qos_cmd = DeclareLaunchArgument(
        'ir_qos',
        default_value='default',
        description='IR QoS'
    )

    declare_ir_camera_info_qos_cmd = DeclareLaunchArgument(
        'ir_camera_info_qos',
        default_value='default',
        description='IR camera info QoS'
    )

    declare_publish_tf_cmd = DeclareLaunchArgument(
        'publish_tf',
        default_value='true',
        description='Publish TF'
    )

    declare_tf_publish_rate_cmd = DeclareLaunchArgument(
        'tf_publish_rate',
        default_value='10.0',
        description='TF publish rate'
    )

    declare_ir_info_url_cmd = DeclareLaunchArgument(
        'ir_info_url',
        default_value='',
        description='IR camera info URL'
    )

    declare_color_info_url_cmd = DeclareLaunchArgument(
        'color_info_url',
        default_value='',
        description='Color camera info URL'
    )

    declare_color_roi_x_cmd = DeclareLaunchArgument(
        'color_roi_x',
        default_value='-1',
        description='Color ROI X'
    )

    declare_color_roi_y_cmd = DeclareLaunchArgument(
        'color_roi_y',
        default_value='-1',
        description='Color ROI Y'
    )

    declare_color_roi_width_cmd = DeclareLaunchArgument(
        'color_roi_width',
        default_value='-1',
        description='Color ROI width'
    )

    declare_color_roi_height_cmd = DeclareLaunchArgument(
        'color_roi_height',
        default_value='-1',
        description='Color ROI height'
    )

    declare_depth_roi_x_cmd = DeclareLaunchArgument(
        'depth_roi_x',
        default_value='-1',
        description='Depth ROI X'
    )

    declare_depth_roi_y_cmd = DeclareLaunchArgument(
        'depth_roi_y',
        default_value='-1',
        description='Depth ROI Y'
    )

    declare_depth_roi_width_cmd = DeclareLaunchArgument(
        'depth_roi_width',
        default_value='-1',
        description='Depth ROI width'
    )

    declare_depth_roi_height_cmd = DeclareLaunchArgument(
        'depth_roi_height',
        default_value='-1',
        description='Depth ROI height'
    )

    declare_depth_scale_cmd = DeclareLaunchArgument(
        'depth_scale',
        default_value='1',
        description='Depth scale'
    )

    declare_color_depth_synchronization_cmd = DeclareLaunchArgument(
        'color_depth_synchronization',
        default_value='false',
        description='Enable color-depth synchronization'
    )

    declare_use_uvc_camera_cmd = DeclareLaunchArgument(
        'use_uvc_camera',
        default_value='true',
        description='Use UVC camera for color'
    )

    declare_uvc_vendor_id_cmd = DeclareLaunchArgument(
        'uvc_vendor_id',
        default_value='0x2bc5',
        description='UVC vendor ID'
    )

    declare_uvc_product_id_cmd = DeclareLaunchArgument(
        'uvc_product_id',
        default_value='0x0501',
        description='UVC product ID'
    )

    declare_uvc_retry_count_cmd = DeclareLaunchArgument(
        'uvc_retry_count',
        default_value='100',
        description='UVC retry count'
    )

    declare_uvc_camera_format_cmd = DeclareLaunchArgument(
        'uvc_camera_format',
        default_value='mjpeg',
        description='UVC camera format'
    )

    declare_uvc_flip_cmd = DeclareLaunchArgument(
        'uvc_flip',
        default_value='false',
        description='Flip UVC camera'
    )

    declare_oni_log_level_cmd = DeclareLaunchArgument(
        'oni_log_level',
        default_value='verbose',
        description='OpenNI log level'
    )

    declare_oni_log_to_console_cmd = DeclareLaunchArgument(
        'oni_log_to_console',
        default_value='false',
        description='OpenNI log to console'
    )

    declare_oni_log_to_file_cmd = DeclareLaunchArgument(
        'oni_log_to_file',
        default_value='false',
        description='OpenNI log to file'
    )

    declare_enable_d2c_viewer_cmd = DeclareLaunchArgument(
        'enable_d2c_viewer',
        default_value='false',
        description='Enable D2C viewer'
    )

    declare_enable_publish_extrinsic_cmd = DeclareLaunchArgument(
        'enable_publish_extrinsic',
        default_value='false',
        description='Enable publish extrinsic'
    )

    camera_node = Node(
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
            {'color_roi_x': color_roi_x},
            {'color_roi_y': color_roi_y},
            {'color_roi_width': color_roi_width},
            {'color_roi_height': color_roi_height},
            {'depth_roi_x': depth_roi_x},
            {'depth_roi_y': depth_roi_y},
            {'depth_roi_width': depth_roi_width},
            {'depth_roi_height': depth_roi_height},
            {'depth_scale': depth_scale},
            {'color_depth_synchronization': color_depth_synchronization},
            {'use_uvc_camera': use_uvc_camera},
            {'uvc_vendor_id': uvc_vendor_id},
            {'uvc_product_id': uvc_product_id},
            {'uvc_retry_count': uvc_retry_count},
            {'uvc_camera_format': uvc_camera_format},
            {'uvc_flip': uvc_flip},
            {'oni_log_level': oni_log_level},
            {'oni_log_to_console': oni_log_to_console},
            {'oni_log_to_file': oni_log_to_file},
            {'enable_d2c_viewer': enable_d2c_viewer},
            {'enable_publish_extrinsic': enable_publish_extrinsic},
        ],
        remappings=[
            ('depth/color/points', 'depth_registered/points'),
        ]
    )

    return LaunchDescription([
        declare_camera_name_cmd,
        declare_depth_registration_cmd,
        declare_serial_number_cmd,
        declare_device_num_cmd,
        declare_vendor_id_cmd,
        declare_product_id_cmd,
        declare_enable_point_cloud_cmd,
        declare_enable_colored_point_cloud_cmd,
        declare_point_cloud_qos_cmd,
        declare_connection_delay_cmd,
        declare_color_width_cmd,
        declare_color_height_cmd,
        declare_color_fps_cmd,
        declare_enable_color_cmd,
        declare_flip_color_cmd,
        declare_color_qos_cmd,
        declare_color_camera_info_qos_cmd,
        declare_depth_width_cmd,
        declare_depth_height_cmd,
        declare_depth_fps_cmd,
        declare_enable_depth_cmd,
        declare_flip_depth_cmd,
        declare_depth_qos_cmd,
        declare_depth_camera_info_qos_cmd,
        declare_ir_width_cmd,
        declare_ir_height_cmd,
        declare_ir_fps_cmd,
        declare_enable_ir_cmd,
        declare_flip_ir_cmd,
        declare_ir_qos_cmd,
        declare_ir_camera_info_qos_cmd,
        declare_publish_tf_cmd,
        declare_tf_publish_rate_cmd,
        declare_ir_info_url_cmd,
        declare_color_info_url_cmd,
        declare_color_roi_x_cmd,
        declare_color_roi_y_cmd,
        declare_color_roi_width_cmd,
        declare_color_roi_height_cmd,
        declare_depth_roi_x_cmd,
        declare_depth_roi_y_cmd,
        declare_depth_roi_width_cmd,
        declare_depth_roi_height_cmd,
        declare_depth_scale_cmd,
        declare_color_depth_synchronization_cmd,
        declare_use_uvc_camera_cmd,
        declare_uvc_vendor_id_cmd,
        declare_uvc_product_id_cmd,
        declare_uvc_retry_count_cmd,
        declare_uvc_camera_format_cmd,
        declare_uvc_flip_cmd,
        declare_oni_log_level_cmd,
        declare_oni_log_to_console_cmd,
        declare_oni_log_to_file_cmd,
        declare_enable_d2c_viewer_cmd,
        declare_enable_publish_extrinsic_cmd,
        camera_node,
    ])
