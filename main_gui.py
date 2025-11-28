import dearpygui.dearpygui as dpg

dpg.create_context()

# ======================================================================
# GLOBAL THEME (Glass, Modern)
# ======================================================================
with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (20, 22, 30, 255))         # dark background
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (35, 40, 55, 180))           # frosted glass
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (45, 50, 70, 200))
        dpg.add_theme_color(dpg.mvThemeCol_Text, (230, 235, 245, 255))
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 12)
        dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 18)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 16)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 12, 12)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 10, 10)

dpg.bind_theme(global_theme)

# ======================================================================
# LED THEMES
# ======================================================================
def make_led(color):
    """LED with glow effect"""
    with dpg.theme() as t:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, color)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, color)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, color)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 200)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 20, 20)
    return t

led_off  = make_led((60, 60, 80, 180))
led_green = make_led((0, 255, 140, 255))
led_red   = make_led((255, 80, 80, 255))
led_blue  = make_led((80, 150, 255, 255))

# ======================================================================
# LED CONTROL CALLBACK
# ======================================================================
def set_led(color):
    dpg.bind_item_theme("MAIN_LED", led_off)

    if color == "green":
        dpg.bind_item_theme("MAIN_LED", led_green)
    elif color == "red":
        dpg.bind_item_theme("MAIN_LED", led_red)
    elif color == "blue":
        dpg.bind_item_theme("MAIN_LED", led_blue)

# ======================================================================
# MAIN WINDOW
# ======================================================================
with dpg.window(tag="root", label="Dashboard Layout", width=1200, height=800, no_scrollbar=True):

    # ------------------------------------------------------------
    # TOP REGION — (75%)
    # ------------------------------------------------------------
    with dpg.child_window(height=-600):

        with dpg.table(header_row=False, policy=dpg.mvTable_SizingStretchProp):
            dpg.add_table_column(init_width_or_weight=1)
            dpg.add_table_column(init_width_or_weight=1)
            dpg.add_table_column(init_width_or_weight=1)

            with dpg.table_row():

                # ------------------------------------------------------------
                # LEFT SECTION (Buttons)
                # ------------------------------------------------------------
                with dpg.child_window(border=True):
                    dpg.add_text("⚙️ Controls", color=(180, 200, 255))
                    dpg.add_separator()

                    dpg.add_button(label="🌿 Set Green", height=30, callback=lambda: set_led("green"))
                    dpg.add_button(label="🔥 Set Red", height=30, callback=lambda: set_led("red"))
                    dpg.add_button(label="💧 Set Blue", height=30, callback=lambda: set_led("blue"))

                # ------------------------------------------------------------
                # MIDDLE SECTION (LED)
                # ------------------------------------------------------------
                with dpg.child_window(border=True):
                    dpg.add_text("🔵 Status LED", color=(180, 200, 255))
                    dpg.add_separator()
                    dpg.add_spacer(height=5)

                    dpg.add_button(tag="MAIN_LED", label=" ", width=100, height=100)
                    dpg.bind_item_theme("MAIN_LED", led_off)

                # ------------------------------------------------------------
                # RIGHT SECTION (Data Values)
                # ------------------------------------------------------------
                with dpg.child_window(border=True):
                    dpg.add_text("📈 Real-Time Vehicle Data", color=(180, 200, 255))
                    dpg.add_separator()

                    dpg.add_text("Speed:");    dpg.add_text("0.0", tag="speed_val", color=(80, 180, 255))
                    dpg.add_text("Throttle:"); dpg.add_text("0.0", tag="throttle_val", color=(80, 180, 255))
                    dpg.add_text("V_actual:"); dpg.add_text("0.0", tag="vactual_val", color=(80, 180, 255))
                    dpg.add_text("Steer:");    dpg.add_text("0.0", tag="steer_val", color=(80, 180, 255))

    # ------------------------------------------------------------
    # BOTTOM REGION — Logs (25%)
    # ------------------------------------------------------------
    with dpg.child_window(height=600):
        with dpg.table(header_row=False, policy=dpg.mvTable_SizingStretchProp):
            dpg.add_table_column()
            dpg.add_table_column()

            with dpg.table_row():

                # ------------------------------------------------------------
                # ROS MONITOR LOGS
                # ------------------------------------------------------------
                with dpg.child_window(border=True):
                    dpg.add_text("🟢 ROS Monitor Logs", color=(200, 220, 255))
                    dpg.add_separator()
                    dpg.add_listbox(items=[], tag="ros_log_box", num_items=10)

                # ------------------------------------------------------------
                # CAN MONITOR LOGS
                # ------------------------------------------------------------
                with dpg.child_window(border=True):
                    dpg.add_text("🟡 CAN Monitor Logs", color=(200, 220, 255))
                    dpg.add_separator()
                    dpg.add_listbox(items=[], tag="can_log_box", num_items=10)

    # --------------------------------------------------------
    # CLOSE BUTTON (BOTTOM RIGHT)
    # --------------------------------------------------------
    dpg.add_spacer(height=5)
    with dpg.group(horizontal=True):
        dpg.add_spacer(width=950)   # pushes button to the right
        dpg.add_button(
            label="❌ Close Window",
            width=200,
            height=40,
            callback=lambda: dpg.stop_dearpygui()
        )

# ======================================================================
# VIEWPORT
# ======================================================================
dpg.create_viewport(title="Dashboard Layout", width=1200, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("root", True)
dpg.start_dearpygui()
dpg.destroy_context()
