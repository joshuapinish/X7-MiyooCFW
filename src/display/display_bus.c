#include "x7/display_bus.h"
#include <errno.h>
int x7_display_run_sequence(const struct x7_display_bus_ops *ops,
                            void *context,
                            const struct x7_display_step *steps,
                            size_t step_count)
{
    size_t i;
    if (ops == NULL || steps == NULL || step_count == 0U) {
        return -EINVAL;
    }
    for (i = 0U; i < step_count; ++i) {
        int result = 0;
        switch (steps[i].kind) {
        case X7_DISPLAY_STEP_END:
            return 0;
        case X7_DISPLAY_STEP_COMMAND:
            if (ops->write_command == NULL) return -ENOSYS;
            result = ops->write_command(context, (uint8_t)steps[i].value);
            break;
        case X7_DISPLAY_STEP_DATA:
            if (ops->write_data == NULL) return -ENOSYS;
            result = ops->write_data(context, (uint8_t)steps[i].value);
            break;
        case X7_DISPLAY_STEP_DELAY_MS:
            if (ops->delay_ms == NULL) return -ENOSYS;
            result = ops->delay_ms(context, steps[i].value);
            break;
        case X7_DISPLAY_STEP_RESET:
            if (ops->set_reset == NULL) return -ENOSYS;
            result = ops->set_reset(context, steps[i].value != 0U);
            break;
        default:
            return -EINVAL;
        }
        if (result != 0) return result;
    }
    return -EINVAL; /* A sequence without an explicit END is malformed. */
}
int x7_display_set_backlight(const struct x7_display_bus_ops *ops,
                             void *context,
                             bool enabled)
{
    if (ops == NULL || ops->set_backlight == NULL) return -ENOSYS;
    return ops->set_backlight(context, enabled);
}
