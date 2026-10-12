#ifndef X7_MEMORY_PROFILE_H
#define X7_MEMORY_PROFILE_H
#include <stdint.h>
#ifndef X7_RAM_MIB
#define X7_RAM_MIB 32
#endif
#if X7_RAM_MIB < 32 || X7_RAM_MIB > 256
#error "X7_RAM_MIB must be configured between 32 and 256 MiB"
#endif
#ifdef __cplusplus
extern "C" {
#endif
/* Build-time target setting; this is not hardware RAM discovery. */
uint32_t x7_configured_ram_mib(void);
uint64_t x7_configured_ram_bytes(void);
#ifdef __cplusplus
}
#endif
#endif
