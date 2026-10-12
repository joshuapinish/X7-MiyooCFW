#include "x7/panel_hsd045f8w7.h"
static const struct x7_panel_profile panel_profile = {
    .firmware_identifier = "LCD_HSD045F8W7_9806E__4_5",
    .controller_candidate = "ILI9806E (candidate; verify bus and revision)",
    .expected_width = 480U,
    .expected_height = 854U,
    .timing_verified = false,
    .init_sequence_verified = false
};
const struct x7_panel_profile *x7_panel_hsd045f8w7_get_profile(void)
{
    return &panel_profile;
}
int x7_panel_hsd045f8w7_run_init(const struct x7_display_bus_ops *ops,
                                 void *context,
                                 const struct x7_display_step *steps,
                                 size_t step_count)
{
    /* Use the sequence recovered from the original ARM driver, not guessed commands. */
    return x7_display_run_sequence(ops, context, steps, step_count);
}
