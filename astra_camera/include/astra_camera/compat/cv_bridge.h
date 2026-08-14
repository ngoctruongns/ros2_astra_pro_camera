/**************************************************************************/
/*                                                                        */
/* Compatibility shim: cv_bridge renamed its public header from            */
/* cv_bridge/cv_bridge.h to cv_bridge/cv_bridge.hpp in Iron. The old name  */
/* still exists in Jazzy but emits a deprecation warning, and is gone in   */
/* newer distributions. Include whichever the installed distribution has.  */
/*                                                                        */
/**************************************************************************/

#pragma once

#if __has_include(<cv_bridge/cv_bridge.hpp>)
#include <cv_bridge/cv_bridge.hpp>
#else
#include <cv_bridge/cv_bridge.h>
#endif
