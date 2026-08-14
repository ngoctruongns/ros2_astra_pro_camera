/**************************************************************************/
/*                                                                        */
/* Compatibility shim: tf2 and tf2_ros are migrating their headers from    */
/* .h to .hpp. Jazzy still ships the .h names, later distributions do not. */
/*                                                                        */
/**************************************************************************/

#pragma once

#if __has_include(<tf2/LinearMath/Quaternion.hpp>)
#include <tf2/LinearMath/Quaternion.hpp>
#else
#include <tf2/LinearMath/Quaternion.h>
#endif

#if __has_include(<tf2_ros/transform_broadcaster.hpp>)
#include <tf2_ros/transform_broadcaster.hpp>
#else
#include <tf2_ros/transform_broadcaster.h>
#endif

#if __has_include(<tf2_ros/static_transform_broadcaster.hpp>)
#include <tf2_ros/static_transform_broadcaster.hpp>
#else
#include <tf2_ros/static_transform_broadcaster.h>
#endif
