#ifndef X7_PANEL_HSD045F8W7_H
#define X7_PANEL_HSD045F8W7_H
#include "x7/display_bus.h"
#ifdef __cplusplus
extern "C" {
#endif
struct x7_panel_profile {
    const char *firmware_identifier;
    const char *controller_candidate;
    uint16_t expected_width;
    uint16_t expected_height;
    bool timing_verified;
    bool init_sequence_verified;
};
const struct x7_panel_profile *x7_panel_hsd045f8w7_get_profile(void);
int x7_panel_hsd045f8w7_run_init(const struct x7_display_bus_ops *ops,
                                 void *context,
                                 const struct x7_display_step *steps,
                                 size_t step_count);
#ifdef __cplusplus
}
#endif
#endif
