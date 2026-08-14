/**************************************************************************/
/*                                                                        */
/* Compatibility shim: image_geometry renamed pinhole_camera_model.h to    */
/* pinhole_camera_model.hpp in Iron. The old name still exists in Jazzy    */
/* but emits a deprecation warning, and is gone in newer distributions.    */
/*                                                                        */
/**************************************************************************/

#pragma once

#if __has_include(<image_geometry/pinhole_camera_model.hpp>)
#include <image_geometry/pinhole_camera_model.hpp>
#else
#include <image_geometry/pinhole_camera_model.h>
#endif
