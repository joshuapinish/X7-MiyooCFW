#include "x7/memory_profile.h"
uint32_t x7_configured_ram_mib(void)
{
    return (uint32_t)X7_RAM_MIB;
}
uint64_t x7_configured_ram_bytes(void)
{
    return (uint64_t)X7_RAM_MIB * UINT64_C(1024) * UINT64_C(1024);
}
