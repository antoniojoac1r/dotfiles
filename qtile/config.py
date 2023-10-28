# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os, subprocess
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration

@hook.subscribe.setgroup
def setgroup():
    for i in range(0, 9):
        if len(qtile.groups[i].windows) > 0:
            qtile.groups[i].label = "󰊠"
        else:
            qtile.groups[i].label = "󱙝"
    qtile.current_group.label = "󰮯"
    
mod = "mod4"
terminal = "alacritty"
browser = "firefox"

colors = [
    ["#00FF7F", "#00FF7F"], # 0 SpringGreen
    ["#FF7F50", "#FF7F50"], # 1 Coral
    ["#FFFF00", "#FFFF00"], # 2 Yellow
    ["#DC143C", "#DC143C"], # 3 Crimson
    ["#40E0D0", "#40E0D0"], # 4 Turquoise
    ["#E0FFFF", "#E0FFFF"], # 5 LightCyan
    ["#00FF00", "#00FF00"], # 6 Lime
    ["#FFFAFA", "#FFFAFA"], # 7 Snow
    ["#EEE8AA", "#EEE8AA"], # 8 PaleGoldenrod
    ["#A52A2A", "#A52A2A"], # 9 Brown
    ["#D8BFD8", "#D8BFD8"], # 10 Thistle
    ["#B0E0E6", "#B0E0E6"], # 11 PowderBlue
    ["#000000", "#000000"], # 12 Black
    ["#1919A6", "#1919A6"], # 13
    ["#FD0000", "#FD0000"], # 14
]

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Launcher rofi"),
    Key([mod], "w", lazy.spawn(browser), desc="web browser"),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    Key([mod], "e", lazy.spawn('nemo'), desc="launch my file manager")
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            Key(
                [mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=False), 
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

layouts = [
    layout.Bsp(
        margin_on_single = 10,
        margin = 3,
        border_width = 3,
        border_on_single = True,
        border_focus = colors[4],
        border_normal = colors[12]
    ),
]

widget_defaults = dict(
    font="JetBrains Mono Nerd Bold",
    fontsize=13,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        wallpaper = "~/Pictures/Wallpapers/748856.jpg",
        wallpaper_mode = "fill",
        top=bar.Bar(
            [
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    size_percent=40,
                    decorations = [
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True,
                        )
                    ],
                ),
                widget.GroupBox(
                    # margin_y = 3,
                    # margin_x = 4,
                    # padding_y = 2,
                    # padding_x = 3,
                    # borderwidth = 3,
                    # rounded = False,
                    highlight_method = "text",
                    urgent_alert_method = "text",
                    urgent_border = colors[14],
                    inactive = colors[7],
                    active = colors[13],
                    this_current_screen_border = colors[2],
                    hide_unused = False,
                    fontsize = 17,
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    size_percent=40,
                    decorations = [
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True,
                        )
                    ]
                ),
                widget.Spacer(),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    size_percent=40,
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),
                widget.TextBox(
                    text = " ",
                    fontsize = 16,
                    foreground = colors[7],
                    decorations = [
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ]
                ),
                widget.Clock(
                    foreground = colors[7],
                    format = '%b %a %H:%M %p',
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    size_percent=40,
                    decorations = [
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ]
                ),
                widget.Spacer(),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    size_percent=40,
                    decorations = [
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ]
                ),
                widget.StatusNotifier(
                    padding = 6,
                    decorations = [
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True,
                        )
                    ]
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    size_percent=40,
                    decorations = [
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ]
                ),
                widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    size_percent = 40
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    size_percent=40,
                    decorations = [
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True,
                        )
                    ]
                ),
                widget.Net(
                    interface= 'wlan0',
                    format = "{down:.1f}{down_suffix}",
                    foreground= colors[0],
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),
                widget.TextBox(
                    text = "󰇚",
                    fontsize = 20,
                    foreground = colors[0],
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    size_percent=40,
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),
                widget.Net(
                    interface='wlan0',
                    format ="{up:.1f}{up_suffix}",
                    foreground = colors[1],
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),
                widget.TextBox(
                    text = "󰕒",
                    fontsize = 20,
                    foreground = colors[1],
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    size_percent=40,
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    size_percent=40,
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    size_percent=40,
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),

                widget.TextBox(
                    text = "󱍖 ",
                    fontsize = 20,
                    foreground = colors[2],
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),
                widget.Backlight(
                    foreground = colors[2],
                    backlight_name = 'intel_backlight',
                    brightness_file = 'brightness',
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    size_percent=40,
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),
                widget.Volume(
                    volume_app = "pavucontrol",
                    get_volume_command = "pactl list sinks | grep 'Volume: front-left' | awk '{print $5}'",
                    emoji = True,
                    emoji_list = ["󰖁", "", "󰖀", "󰕾"],
                    fontsize = 16,
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),
                widget.Volume(
                    get_volume_command = "pactl list sinks | grep 'Volume: front-left' | awk '{print $5}'", 
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    size_percent=40,
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),
                widget.UPowerWidget(
                    text_charging = None,
                    text_discharging = None,
                    text_displaytime = None,
                    border_critical_colour = colors[14],
                    border_charge_colour = colors[6],
                    border_colour = colors[6],
                    fill_normal = colors[6],
                    fill_low = colors[2],
                    fill_critical = colors[14],
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),
                widget.Battery(
                    foreground = colors[6],
                    charge_char = "󱐋",
                    discharge_char = "",
                    unknown_char = "",
                    format = '{char} {percent:2.0%}',
                    full_char = "100%",
                    update_interval = 1,
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),
                widget.Sep(
                    linewidth=0,
                    padding=6,
                    size_percent=40,
                    decorations=[
                        RectDecoration(
                            colour = colors[12],
                            radius = 5,
                            filled = True,
                            group = True
                        )
                    ],
                ),
            ],
            34,
            background = "#00000000",
            margin = [8, 3, 0, 3],
            border_width=[0, 0, 0, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
