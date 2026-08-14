cmake_minimum_required(VERSION 3.16)
project(astra_camera)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_C_STANDARD 11)

# Honour -DCMAKE_BUILD_TYPE from the command line; only pick a default when the
# caller did not choose one. (This used to be hard-coded to Debug, which
# silently discarded the Release build documented in the README.)
if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Build type" FORCE)
endif ()

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if (CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif ()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_index_cpp REQUIRED)
find_package(astra_camera_msgs REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(camera_info_manager REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(message_filters REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(image_geometry REQUIRED)
find_package(image_transport REQUIRED)
find_package(OpenCV REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(rcutils REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_eigen REQUIRED)
find_package(tf2_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_sensor_msgs REQUIRED)
find_package(PkgConfig REQUIRED)

pkg_search_module(LIBUVC REQUIRED libuvc)
if (NOT LIBUVC_FOUND)
  message(FATAL_ERROR "libuvc is not found")
endif ()
pkg_search_module(GLOG REQUIRED libglog)

if (NOT GLOG_FOUND)
  message(FATAL_ERROR "glog is not found")
endif ()


execute_process(COMMAND uname -m OUTPUT_VARIABLE MACHINES)
execute_process(COMMAND getconf LONG_BIT OUTPUT_VARIABLE MACHINES_BIT)
message(STATUS "ORRBEC Machine : ${MACHINES}")
message(STATUS "ORRBEC Machine Bits : ${MACHINES_BIT}")

if ((${MACHINES} MATCHES "x86_64") AND (${MACHINES_BIT} MATCHES "64"))
  set(HOST_PLATFORM "x64")
elseif (${MACHINES} MATCHES "arm")
  set(HOST_PLATFORM "arm")
elseif ((${MACHINES} MATCHES "aarch64") AND (${MACHINES_BIT} MATCHES "64"))
  set(HOST_PLATFORM "arm64")
elseif ((${MACHINES} MATCHES "aarch64") AND (${MACHINES_BIT} MATCHES "32"))
  set(HOST_PLATFORM "arm")
endif ()

if (NOT HOST_PLATFORM)
  message(FATAL_ERROR "Unsupported architecture ${MACHINES}: no prebuilt OpenNI2 redistributable")
endif ()

message(STATUS "ORRBEC : ${HOST_PLATFORM}")
set(ORBBEC_OPENNI2_REDIST
  "${CMAKE_CURRENT_SOURCE_DIR}/openni2_redist/${HOST_PLATFORM}")

# The shipped libOpenNI2.so carries no SONAME, so it must be linked through
# -L/-l (which records the plain "libOpenNI2.so" in DT_NEEDED). Linking it by
# absolute path would bake the source tree path into the binaries.
set(ORBBEC_OPENNI2_LINK_FLAGS -L${ORBBEC_OPENNI2_REDIST} -lOpenNI2)

set(dependencies
  ament_index_cpp
  astra_camera_msgs
  builtin_interfaces
  cv_bridge
  Eigen3
  image_geometry
  image_transport
  rclcpp
  rclcpp_components
  rcutils
  sensor_msgs
  std_msgs
  std_srvs
  tf2
  tf2_msgs
  tf2_ros
  tf2_sensor_msgs
  message_filters
  camera_info_manager
  )

# Applies the include directories and third-party libraries every target in this
# package needs.
function(astra_camera_configure_target target)
  target_include_directories(${target} PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/include>
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
    ${OpenCV_INCLUDE_DIRS}
    ${LIBUVC_INCLUDE_DIRS}
    ${GLOG_INCLUDE_DIRS}
    )
  ament_target_dependencies(${target} ${dependencies})
  target_link_libraries(${target}
    ${OpenCV_LIBS}
    Eigen3::Eigen
    ${GLOG_LIBRARIES}
    ${LIBUVC_LIBRARIES}
    ${ORBBEC_OPENNI2_LINK_FLAGS}
    )
endfunction()

add_library(${PROJECT_NAME} SHARED
  src/point_cloud_proc/point_cloud_xyz.cpp
  src/point_cloud_proc/point_cloud_xyzrgb.cpp
  src/ob_context.cpp
  src/dynamic_params.cpp
  src/ob_camera_info.cpp
  src/ob_timer_filter.cpp
  src/ob_camera_node_factory.cpp
  src/ob_camera_node.cpp
  src/ros_param_backend.cpp
  src/ros_service.cpp
  src/utils.cpp
  src/uvc_camera_driver.cpp
  )
astra_camera_configure_target(${PROJECT_NAME})

add_executable(${PROJECT_NAME}_node
  src/main.cpp
  )
astra_camera_configure_target(${PROJECT_NAME}_node)
target_link_libraries(${PROJECT_NAME}_node ${PROJECT_NAME})

add_executable(list_devices_node
  src/list_devices_node.cpp
  )
astra_camera_configure_target(list_devices_node)
target_link_libraries(list_devices_node ${PROJECT_NAME})

add_executable(clean_shm_node
  src/clean_up_shm_node.cpp
  )
astra_camera_configure_target(clean_shm_node)
target_link_libraries(clean_shm_node ${PROJECT_NAME})

install(TARGETS ${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
  )


install(FILES openni2_redist/${HOST_PLATFORM}/libOpenNI2.so
  DESTINATION lib/
  )

install(DIRECTORY openni2_redist/${HOST_PLATFORM}/OpenNI2
  DESTINATION lib/
  )

install(TARGETS list_devices_node
  clean_shm_node
  ${PROJECT_NAME}_node
  DESTINATION lib/${PROJECT_NAME}/
  )

install(
  DIRECTORY include/
  DESTINATION include
)

install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}/
  )


if (BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif ()
ament_export_include_directories(include)
ament_export_libraries(${PROJECT_NAME})
ament_export_dependencies(${dependencies})

ament_package()
