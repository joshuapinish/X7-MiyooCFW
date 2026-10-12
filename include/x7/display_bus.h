#ifndef X7_DISPLAY_BUS_H
#define X7_DISPLAY_BUS_H
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
struct x7_display_bus_ops {
    int (*write_command)(void *context, uint8_t command);
    int (*write_data)(void *context, uint8_t data);
    int (*delay_ms)(void *context, uint16_t milliseconds);
    int (*set_reset)(void *context, bool asserted);
    int (*set_backlight)(void *context, bool enabled);
};
enum x7_display_step_kind {
    X7_DISPLAY_STEP_END = 0,
    X7_DISPLAY_STEP_COMMAND,
    X7_DISPLAY_STEP_DATA,
    X7_DISPLAY_STEP_DELAY_MS,
    X7_DISPLAY_STEP_RESET
};
struct x7_display_step {
    enum x7_display_step_kind kind;
    uint16_t value;
};
/* Board GPIO/SPI/parallel operations are injected by the platform layer. */
int x7_display_run_sequence(const struct x7_display_bus_ops *ops,
                            void *context,
                            const struct x7_display_step *steps,
                            size_t step_count);
int x7_display_set_backlight(const struct x7_display_bus_ops *ops,
                             void *context,
                             bool enabled);
#ifdef __cplusplus
}
#endif
#endif
