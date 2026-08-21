-- Last Call — Cold Line / Warm Signal
-- Omarchy 4 native presentation. Layout and gaps remain user-owned.

local activeBorderColor = {
  colors = { "rgb(00C6C2)", "rgb(E0F5F2)" },
  angle = 45,
}
local inactiveBorderColor = "rgba(2C515888)"
local shadowColor = "rgba(010506CC)"
local shellSurfaces = "^(omarchy-bar|omarchy-menu|omarchy-image-selector|omarchy-emojis|omarchy-clipboard|omarchy-keyboard-panel|omarchy-notifications|omarchy-osd|omarchy-polkit|omarchy-reminders|omarchy-network-qr|omarchy-network-speedtest|omarchy-disk-speedtest|omarchy-speed-test)$"

hl.config({
  general = {
    col = {
      active_border = activeBorderColor,
      inactive_border = inactiveBorderColor,
    },
    border_size = 2,
  },
  group = {
    col = {
      border_active = activeBorderColor,
      border_inactive = inactiveBorderColor,
      border_locked_active = "rgb(B79A54)",
      border_locked_inactive = inactiveBorderColor,
    },
  },
  decoration = {
    rounding = 2,
    rounding_power = 2,
    blur = {
      enabled = true,
      size = 6,
      passes = 2,
      noise = 0.03,
      contrast = 0.92,
      brightness = 0.86,
      vibrancy = 0.08,
      vibrancy_darkness = 0.74,
      ignore_opacity = true,
    },
    shadow = {
      enabled = true,
      color = shadowColor,
      range = 12,
      render_power = 3,
    },
  },
})

-- Hyprland's blur settings only define the effect. Layer-shell clients must
-- opt in separately, so apply the theme's rain-glass treatment to Omarchy's
-- visible shell surfaces while leaving its wallpaper layer untouched.
hl.layer_rule({
  name = "last-call-shell-blur",
  match = { namespace = shellSurfaces },
  blur = true,
  blur_popups = true,
  ignore_alpha = 0.20,
})
