/**************************************************************************/
/*                                                                        */
/* Compatibility shim: message_filters is migrating its headers from .h to */
/* .hpp. Jazzy still ships the .h names, later distributions do not.       */
/*                                                                        */
/**************************************************************************/

#pragma once

#if __has_include(<message_filters/subscriber.hpp>)
#include <message_filters/subscriber.hpp>
#include <message_filters/synchronizer.hpp>
#include <message_filters/sync_policies/exact_time.hpp>
#include <message_filters/sync_policies/approximate_time.hpp>
#else
#include <message_filters/subscriber.h>
#include <message_filters/synchronizer.h>
#include <message_filters/sync_policies/exact_time.h>
#include <message_filters/sync_policies/approximate_time.h>
#endif
