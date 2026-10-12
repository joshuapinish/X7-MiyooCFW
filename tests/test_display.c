#include "x7/display_bus.h"
#include "x7/panel_hsd045f8w7.h"
#include <errno.h>
#include <stdio.h>
#include <string.h>
struct mock_bus { char log[64]; size_t used; int fail_command; };
static int append(struct mock_bus *bus, char event)
{
    if (bus == NULL || bus->used + 1U >= sizeof(bus->log)) return -1;
    bus->log[bus->used++] = event;
    bus->log[bus->used] = '\0';
    return 0;
}
static int mock_command(void *context, uint8_t value)
{
    struct mock_bus *bus = context;
    if (bus->fail_command != 0) return bus->fail_command;
    (void)value;
    return append(bus, 'C');
}
static int mock_data(void *context, uint8_t value)
{ (void)value; return append(context, 'D'); }
static int mock_delay(void *context, uint16_t value)
{ (void)value; return append(context, 'T'); }
static int mock_reset(void *context, bool asserted)
{ (void)asserted; return append(context, 'R'); }
static int mock_backlight(void *context, bool enabled)
{ (void)enabled; return append(context, 'B'); }
#define CHECK(condition) do { if (!(condition)) { \
    (void)fprintf(stderr, "FAIL %s:%d: %s\n", __FILE__, __LINE__, #condition); \
    return 1; } } while (0)
int main(void)
{
    struct mock_bus bus = { { 0 }, 0U, 0 };
    const struct x7_display_bus_ops ops = {
        mock_command, mock_data, mock_delay, mock_reset, mock_backlight
    };
    const struct x7_display_step steps[] = {
        { X7_DISPLAY_STEP_RESET, 1U },
        { X7_DISPLAY_STEP_COMMAND, 0x11U },
        { X7_DISPLAY_STEP_DELAY_MS, 120U },
        { X7_DISPLAY_STEP_DATA, 0x5AU },
        { X7_DISPLAY_STEP_END, 0U }
    };
    const struct x7_display_step missing_end[] = {
        { X7_DISPLAY_STEP_COMMAND, 0x11U }
    };
    const struct x7_panel_profile *profile;
    CHECK(x7_panel_hsd045f8w7_run_init(&ops, &bus, steps, 5U) == 0);
    CHECK(strcmp(bus.log, "RCTD") == 0);
    CHECK(x7_display_set_backlight(&ops, &bus, true) == 0);
    CHECK(bus.log[4] == 'B');
    CHECK(x7_display_run_sequence(&ops, &bus, missing_end, 1U) == -EINVAL);
    CHECK(x7_display_run_sequence(NULL, &bus, steps, 5U) == -EINVAL);
    bus.fail_command = -EIO;
    CHECK(x7_display_run_sequence(&ops, &bus, steps, 5U) == -EIO);
    profile = x7_panel_hsd045f8w7_get_profile();
    CHECK(profile != NULL);
    CHECK(strcmp(profile->firmware_identifier, "LCD_HSD045F8W7_9806E__4_5") == 0);
    CHECK(profile->expected_width == 480U && profile->expected_height == 854U);
    CHECK(!profile->timing_verified && !profile->init_sequence_verified);
    (void)puts("display core tests passed (mock bus only; no physical LCD accessed)");
    return 0;
}
