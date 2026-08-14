# Ghi chú kỹ thuật: `ros2_astra_camera` với Astra Pro (ROS 2)

Tài liệu tóm tắt kiến trúc, luồng dữ liệu, tham số và các cạm bẫy thực tế của gói này,
tập trung vào cấu hình **Astra Pro** (depth/IR qua OpenNI2, color qua UVC).

Mọi tham chiếu mã nguồn ở dạng `file:line` theo trạng thái repo hiện tại (nhánh `master`, commit `f7e71d9`).

---

## 1. Kiến trúc gói

Gói `astra_camera` là driver **một-node** (`astra_camera_node`), không phải composable node thật sự.
Bên trong node có 4 khối chính:

| Khối | File | Vai trò |
|---|---|---|
| `OBCameraNodeFactory` | `src/ob_camera_node_factory.cpp` | Quản lý vòng đời USB: dò thiết bị (theo `serial_number` / `vendor_id` / `product_id`), xử lý hot-plug, tạo lại `OBCameraNode` sau `connection_delay`. Dùng semaphore trong `/dev/shm` để đồng bộ khi có nhiều camera. |
| `OBCameraNode` | `src/ob_camera_node.cpp` | Toàn bộ stream OpenNI2 (depth, IR, và color nếu **không** dùng UVC), camera_info, TF, dịch vụ điều khiển. |
| `UVCCameraDriver` | `src/uvc_camera_driver.cpp` | Stream color qua libuvc cho các camera có RGB dạng UVC (Astra Pro, Dabai, …). |
| `PointCloudXyzNode` / `PointCloudXyzrgbNode` | `src/point_cloud_proc/` | Sinh point cloud, chạy **trong cùng node** (không phải node riêng như `depth_image_proc`). |

Thư viện OpenNI2 được ship kèm trong `astra_camera/openni2_redist/{x64,arm64,arm}` (SDK 2.3.0.85),
không dùng OpenNI hệ thống. Driver `liborbbec.so` được cài cùng.

### Với Astra Pro cụ thể

- Camera lộ ra **hai thiết bị USB độc lập**:
  - Sensor depth/IR: giao tiếp OpenNI2 (`liborbbec.so`).
  - Camera RGB: giao tiếp **UVC chuẩn** (`uvc_vendor_id 0x2bc5`, `uvc_product_id 0x0501`, mặc định MJPEG) — xem `launch/astra_pro.launch.xml:49-53`.
- Vì vậy `use_uvc_camera=true` là bắt buộc, và stream COLOR của OpenNI bị bỏ qua
  (`src/ob_camera_node.cpp:339-341` trong `setupVideoMode`, `src/ob_camera_node.cpp:~262` trong `startStreams`).
- Hệ quả: **mọi service/tham số họ `color_*` của OpenNI không tác dụng lên RGB của Astra Pro**;
  phải dùng bản UVC tương ứng (`set_uvc_exposure`, `set_uvc_gain`, `set_uvc_auto_exposure`,
  `set_uvc_color_mirror`, `toggle_uvc_camera`).

---

## 2. Topic, service, TF

### Topic (dưới namespace `camera_name`, mặc định `/camera`)

| Topic | Nguồn |
|---|---|
| `depth/image_raw` + `depth/camera_info` | OpenNI, `16UC1`, đơn vị **mm** |
| `ir/image_raw` + `ir/camera_info` | OpenNI, `mono8` |
| `color/image_raw` + `color/camera_info` | **UVC** (`src/uvc_camera_driver.cpp:90-95`) với Astra Pro |
| `depth/points` | `PointCloudXyzNode` |
| `depth/color/points` | `PointCloudXyzrgbNode` (launch remap sang `depth_registered/points`) |
| `extrinsic/depth_to_color` | chỉ khi `enable_publish_extrinsic=true` |

> Lưu ý: khi `use_uvc_camera=true` và `enable_color=true`, `OBCameraNode::setupPublishers`
> **vẫn tạo một publisher `color/image_raw` thứ hai** (`src/ob_camera_node.cpp:381-397`) nhưng
> không bao giờ publish. Bạn sẽ thấy 2 publisher trên cùng topic khi chạy `ros2 topic info` — vô hại.

### TF

`publishStaticTransforms()` dựng cây:

```
camera_link
 ├── camera_depth_frame ── camera_depth_optical_frame
 └── camera_color_frame ── camera_color_optical_frame
```

Extrinsic depth→color lấy từ tham số hiệu chuẩn trong firmware (`camera_params_->r2l_r/r2l_t`).
Nếu `tf_publish_rate > 0`, TF được phát lặp lại trên `/tf` (dynamic) thay vì `/tf_static` —
mặc định 10 Hz (`launch/astra_pro.launch.xml:36`).

### Service đáng nhớ

`get_device_info`, `get_camera_params`, `get_sdk_version`, `get_supported_video_modes`,
`toggle_depth|ir|uvc_camera`, `set_laser_enable`, `set_ldp_enable`, `set_fan_mode`,
và nhóm exposure/gain/white-balance/mirror (bản `ir_`, `color_`, `uvc_`).

---

## 3. Tham số quan trọng (Astra Pro)

| Tham số | Ý nghĩa / lưu ý |
|---|---|
| `depth_registration` | Bật **hardware D2C** (căn chỉnh *không gian* depth về hệ tọa độ RGB). Khi bật, `frame_id` của ảnh depth đổi thành `camera_color_optical_frame` (`src/ob_camera_node.cpp:528-529`). |
| `enable_colored_point_cloud` | Ép `depth_registration=true` (`src/ob_camera_node.cpp:~363`). |
| `depth_scale` | Phóng ảnh depth bằng `cv::resize` INTER_NEAREST *sau khi* nhận frame (`src/ob_camera_node.cpp:518-521`). |
| `color_roi_*` / `depth_roi_*` | Crop, dùng khi độ phân giải RGB ≠ depth. |
| `color_depth_synchronization` | **Không có tác dụng với Astra Pro** — xem mục 4. |
| `use_uvc_camera`, `uvc_product_id`, `uvc_camera_format`, `uvc_retry_count`, `uvc_flip` | Cấu hình đường RGB. |
| `ir_info_url`, `color_info_url` | File hiệu chuẩn; **tên camera bắt buộc** là `ir_camera` và `rgb_camera`. |
| `*_qos` | Chuỗi: `SYSTEM_DEFAULT`, `DEFAULT`, `SENSOR_DATA`, … Mặc định của launch là `default` (RELIABLE) → RViz phải để Reliability = Reliable, hoặc đổi sang `SENSOR_DATA`. |
| `enable_ir` + `enable_color` | Với camera OpenNI thuần, bật cả hai sẽ **tự tắt IR** (`src/ob_camera_node.cpp:~152`). Astra Pro dùng UVC nên không dính luật này. |

**Bug nhỏ về QoS:** launch truyền `color_qos` nhưng `UVCCameraDriver` đọc tham số tên
`rgb_qos_profile` / `rgb_info_qos_profile` (`src/uvc_camera_driver.cpp:78-84`).
Muốn đổi QoS của ảnh màu Astra Pro phải set trực tiếp `rgb_qos_profile`.

---

## 4. Depth và Color có được lấy đồng bộ theo frameset không?

**Không.** Không có bất kỳ khái niệm frameset nào trong gói này. Chi tiết:

### 4.1 Hai đường dữ liệu hoàn toàn tách biệt

- **Depth/IR**: một thread `pollFrame()` (`src/ob_camera_node.cpp:68-109`) gọi
  `openni::OpenNI::waitForAnyStream(...)` → trả về **đúng một** stream sẵn sàng → `readFrame()`
  → `onNewFrameCallback()` publish **ngay lập tức**. Không có bộ đệm ghép cặp, không chờ stream còn lại.
  Ngay cả depth và IR (cùng đi qua OpenNI) cũng được publish rời rạc.
- **Color (Astra Pro)**: libuvc gọi `UVCCameraDriver::frameCallback()` (`src/uvc_camera_driver.cpp:332`)
  trên **thread riêng của libuvc**, qua **đường USB khác**, rồi publish ngay.

API OpenNI2 vốn không có `FrameSet` (khác với Orbbec SDK v2 với `pipeline.waitForFrames()` trả về
`ob::FrameSet` chứa depth+color đã ghép). Ở đây chỉ có `waitForAnyStream` — theo thiết kế là *any*, không phải *all*.

### 4.2 Timestamp là thời điểm phần mềm, không phải timestamp phần cứng

```cpp
auto timestamp = node_->now();          // ob_camera_node.cpp:526
image_msg->header.stamp = timestamp;
...
image.header.stamp = node_->now();      // uvc_camera_driver.cpp:341
```

- `openni::VideoFrameRef::getTimestamp()` (timestamp µs theo đồng hồ thiết bị) **không được dùng**.
- Do đó `header.stamp` mang toàn bộ jitter của: truyền USB, lịch trình thread, giải nén MJPEG.
- Với color, nếu bật `color_roi_*`, stamp còn bị **gán lại lần hai sau khi crop**
  (`src/uvc_camera_driver.cpp:389`), tức trễ thêm.
- Hai stream lấy `now()` ở hai thời điểm khác nhau ⇒ stamp **không bao giờ trùng khớp tuyệt đối**.

### 4.3 `color_depth_synchronization` không giúp gì cho Astra Pro

Tham số này gọi `device_->setDepthColorSyncEnabled()` (`src/ob_camera_node.cpp:556-562`) —
đây là đồng bộ *phơi sáng ở mức firmware* giữa depth và **color stream của OpenNI**.
Astra Pro lấy color qua UVC nên lệnh này không chạm được tới cảm biến RGB.
Ngoài ra `launch/astra_pro.launch.xml:48` để mặc định `false`.

### 4.4 Đồng bộ duy nhất là ở mức phần mềm, và chỉ cho point cloud màu

`PointCloudXyzrgbNode` (`src/point_cloud_proc/point_cloud_xyzrgb.cpp:73-83`) dùng `message_filters`:

- Mặc định: `ApproximateTime<Image(depth), Image(color), CameraInfo(color)>`, `queue_size=5`.
- Tham số `use_exact_sync=true` chuyển sang `ExactTime` — với kiến trúc stamp ở trên,
  **gần như không bao giờ khớp**, point cloud màu sẽ đứng im. Đừng bật.

`PointCloudXyzNode` chỉ dùng depth + depth camera_info, không liên quan color.

### 4.5 Cạm bẫy khiến point cloud màu không ra trên Astra Pro

`imageCb` bỏ qua cặp frame nếu `frame_id` không khớp (`src/point_cloud_proc/point_cloud_xyzrgb.cpp:139-146`):

- Ảnh depth khi `depth_registration=true` có `frame_id = camera_color_optical_frame`
  (= `camera_name` + `_color_optical_frame`).
- Ảnh color từ UVC mặc định `frame_id = color_optical_frame` — **không** có tiền tố `camera_name`
  (`src/uvc_camera_driver.cpp:76-77`).

⇒ Mismatch ⇒ callback return sớm, chỉ log WARN mỗi 5 giây. Cách sửa: truyền thêm tham số

```xml
<param name="color_optical_frame_id" value="camera_color_optical_frame"/>
<param name="color_frame_id"         value="camera_color_frame"/>
```

Việc này cũng cần thiết để RViz hiển thị ảnh màu đúng, vì `color_optical_frame` không nằm trong cây TF.

### 4.6 Kết luận và khuyến nghị thực tế

| Câu hỏi | Trả lời |
|---|---|
| Depth & color đến từ cùng một frameset phần cứng? | Không |
| Có hardware timestamp chung? | Không, dùng `node_->now()` phía host |
| Có ghép cặp trong driver trước khi publish? | Không, publish độc lập ngay khi nhận |
| Có đồng bộ *không gian* (D2C)? | Có, qua `depth_registration` (hardware, dùng calib trong firmware) |
| Có đồng bộ *thời gian*? | Chỉ ở downstream, bằng `message_filters` ApproximateTime |

Khuyến nghị khi dùng cho robot:

1. **Ở node tiêu thụ của bạn**, dùng `message_filters` `ApproximateTimeSynchronizer` với slop
   khoảng nửa đến một chu kỳ khung hình (~15–35 ms ở 30 fps). Đừng giả định stamp bằng nhau.
2. Nếu cần độ lệch nhỏ và ổn định hơn: sửa driver để dùng `frame.getTimestamp()` (OpenNI) và
   timestamp của `uvc_frame_t` rồi quy về đồng hồ ROS bằng một offset ước lượng — đây là thay đổi
   không nhỏ nhưng nằm gọn trong `onNewFrameCallback` và `frameCallback`.
3. Không dựa vào `color_depth_synchronization` cho Astra Pro.
4. Bật `depth_registration=true` nếu bạn cần depth và color cùng hệ pixel (ví dụ chiếu nhãn 2D
   xuống 3D) — nhưng nhớ đó là căn chỉnh *hình học*, không phải *thời gian*.
5. Nếu bài toán nhạy cảm với lệch thời gian (robot di chuyển nhanh, fusion với IMU/odom), hãy đo
   thực tế: `ros2 topic echo --field header.stamp` cho hai topic rồi so sánh, hoặc log trong node
   đồng bộ. Đừng dựa vào giả định.

---

## 5. Lưu ý khi build trên ROS 2 Jazzy

Gói này được viết cho **Galactic** (README, và mã dùng nhiều API cũ). Các điểm nhiều khả năng
phải chỉnh khi build trên Jazzy — hãy kiểm tra bằng chính lỗi biên dịch:

- Header kiểu cũ (Jazzy đã chuyển sang `.hpp`, các shim `.h` bị deprecate hoặc bỏ):
  - `cv_bridge/cv_bridge.h` — `include/astra_camera/ob_camera_node.h:19`,
    `src/ob_camera_node.cpp:15`, `src/uvc_camera_driver.cpp:15`,
    `include/astra_camera/point_cloud_proc/point_cloud_xyzrgb.h:46`, `src/point_cloud_proc/point_cloud_xyzrgb.cpp:43`
  - `tf2/LinearMath/Quaternion.h` — `include/astra_camera/ob_camera_node.h:24`, `include/astra_camera/utils.h:18`
  - `image_geometry/pinhole_camera_model.h` — `point_cloud_xyz.h:37`, `point_cloud_xyzrgb.h:44`, và 2 file `.cpp`
- `message_filters::Subscriber::subscribe(node, topic, rmw_qos_profile_t)` và
  `image_transport::SubscriberFilter` đã đổi chữ ký qua các bản mới — xem
  `src/point_cloud_proc/point_cloud_xyzrgb.cpp:127-132`.
- `rclcpp::QoSInitialization::from_rmw(...)` vẫn dùng được nhưng kiểu `rmw_qos_profile_t` đang bị
  dần loại bỏ khỏi API message_filters.
- Phụ thuộc ngoài ROS: `libgflags-dev`, `libgoogle-glog-dev` (macro `CHECK`, `CHECK_NOTNULL` dùng khắp nơi),
  `libusb-1.0-0-dev`, và **libuvc phải build từ nguồn** (README mục "Install libuvc").
- Thư viện OpenNI2 kèm theo là binary dựng sẵn (`openni2_redist/`); nếu chạy trên kiến trúc khác
  x64/arm64/arm thì không có sẵn.

---

## 6. Vận hành

```bash
# udev rules (một lần)
cd astra_camera/scripts && sudo bash install.sh
sudo udevadm control --reload-rules && sudo udevadm trigger

# chạy
ros2 launch astra_camera astra_pro.launch.xml

# nếu khởi động bị treo sau một lần crash (semaphore còn sót trong /dev/shm)
ros2 run astra_camera cleanup_shm_node
```

Nhiều camera: phân biệt **chỉ bằng serial number**, và với camera RGB dạng UVC thì serial của
phần UVC cũng phải đúng, nếu không sẽ không ra ảnh màu.
