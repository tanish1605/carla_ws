import dearpygui.dearpygui as dpg

# -----------------------------------------
# GUI Setup
# -----------------------------------------
dpg.create_context()

screen_w, screen_h = 1920, 1080
win_w, win_h = 900, 550
x_pos = (screen_w - win_w) // 2
y_pos = (screen_h - win_h) // 2

dpg.create_viewport(
    title="Sensor Attributes",
    width=win_w,
    height=win_h,
    x_pos=x_pos,
    y_pos=y_pos,
    resizable=False
)

# -----------------------------------------
# Modern Theme
# -----------------------------------------
with dpg.theme() as sensor_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (15, 15, 23, 245))
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (38, 38, 55, 180))
        dpg.add_theme_color(dpg.mvThemeCol_Text, (240, 245, 255, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (70, 130, 200, 230))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (100, 160, 255, 255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (120, 175, 255, 255))
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 12)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 18, 18)

dpg.bind_theme(sensor_theme)

# -----------------------------------------
# GUI CONTENT
# -----------------------------------------
with dpg.window(
    tag="sensor_main",
    label="Sensor Attributes",
    width=win_w,
    height=win_h,
    no_resize=True
):

    dpg.add_text("Sensor Configuration Panel")
    dpg.add_separator()
    dpg.add_spacer(height=10)

    # 2-column layout
    with dpg.table(header_row=False,
                   resizable=False,
                   policy=dpg.mvTable_SizingStretchProp,
                   borders_innerV=True):

        dpg.add_table_column()
        dpg.add_table_column()

        with dpg.table_row():

            # -----------------------------------------
            # Left Column → LIDAR
            # -----------------------------------------
            with dpg.group():
                dpg.add_text("LIDAR", color=(180, 220, 255))
                dpg.add_separator()
                dpg.add_spacer(height=8)

                dpg.add_text("Range (m):")
                dpg.add_input_float(width=220, default_value=120.0)

                dpg.add_text("Vertical FOV (°):")
                dpg.add_input_float(width=220, default_value=45.0)

                dpg.add_text("Horizontal FOV (°):")
                dpg.add_input_float(width=220, default_value=360.0)

                dpg.add_text("Rotation Rate (Hz):")
                dpg.add_input_float(width=220, default_value=10.0)

                dpg.add_text("LIDAR Model:")
                dpg.add_combo(
                    items=["Ouster OS1-64", "Ouster OS2-128", "Velodyne VLP-16", "Velodyne HDL-32E"],
                    width=220,
                    default_value="Ouster OS1-64"
                )

                dpg.add_spacer(height=15)
                dpg.add_button(label="Save LIDAR Settings", width=220)

            # -----------------------------------------
            # Right Column → CAMERA
            # -----------------------------------------
            with dpg.group():
                dpg.add_text("CAMERA", color=(255, 210, 150))
                dpg.add_separator()
                dpg.add_spacer(height=8)

                dpg.add_text("Resolution:")
                dpg.add_input_text(width=220, hint="720p, 1080p, 4K...")

                dpg.add_text("FOV (°):")
                dpg.add_input_float(width=220, default_value=90.0)

                dpg.add_text("Exposure:")
                dpg.add_input_float(width=220, default_value=1.0)

                dpg.add_text("FPS:")
                dpg.add_input_int(width=220, default_value=30)

                # Camera Type removed as requested

                dpg.add_spacer(height=15)
                dpg.add_button(label="Save CAMERA Settings", width=220)

    dpg.add_spacer(height=20)
    dpg.add_separator()
    dpg.add_spacer(height=20)

    dpg.add_button(label="Close", width=150, callback=lambda: dpg.stop_dearpygui())


# -----------------------------------------
# Run GUI
# -----------------------------------------
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("sensor_main", True)
dpg.start_dearpygui()
dpg.destroy_context()
