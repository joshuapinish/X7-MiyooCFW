#include "x7/memory_profile.h"
#include <inttypes.h>
#include <stdio.h>
int main(void)
{
    const uint64_t expected = (uint64_t)X7_RAM_MIB * UINT64_C(1024) * UINT64_C(1024);
    if (x7_configured_ram_mib() != (uint32_t)X7_RAM_MIB ||
        x7_configured_ram_bytes() != expected) {
        (void)fprintf(stderr, "memory profile mismatch for %" PRIu32 " MiB\n",
                      x7_configured_ram_mib());
        return 1;
    }
    (void)printf("configured RAM profile: %" PRIu32 " MiB\n", x7_configured_ram_mib());
    return 0;
}
