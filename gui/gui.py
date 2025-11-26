import dearpygui.dearpygui as dpg
import platform
import os
import subprocess
import sys

processes = {}  # to track running background processes
# Path to your CARLA project directory
PROJECT_DIR = os.path.expanduser("~/carla-project/carla")


def launch_simulation():
    print("Launching simulation in:", PROJECT_DIR)

    processes["simulation"] = subprocess.Popen(
        ["make", "launch"],
        cwd=PROJECT_DIR
    )

    selected = weather["selected"]

    if selected == "sunny_tex":
        subprocess.Popen(["python3", "sunny.py"], cwd=PROJECT_DIR)

    elif selected == "rainy_tex":
        subprocess.Popen(["python3", "rainy.py"], cwd=PROJECT_DIR)

    elif selected == "cloudy_tex":
        subprocess.Popen(["python3", "cloudy.py"], cwd=PROJECT_DIR)

    elif selected == "night_tex":
        subprocess.Popen(["python3", "night.py"], cwd=PROJECT_DIR)


    dpg.set_value("status_text", "Status: Running Simulation")

def stop_simulation():
    # Kill CARLA process
    subprocess.Popen(["pkill", "-f", "CarlaUE4"])

    # Kill make launch if stored
    if "simulation" in processes:
        processes["simulation"].terminate()
        del processes["simulation"]

    dpg.set_value("status_text", "Status: Simulation Stopped")


def run_track_generator():
    subprocess.Popen(["python3", "trackgenerator.py"], cwd=PROJECT_DIR)


# -------------------------------------------------
# Utility: Absolute path loader for images
# -------------------------------------------------
def load_texture(filename, tag):
    """Safely load an image and register as texture."""
    base = os.path.dirname(os.path.abspath(__file__))
    pics_dir = os.path.join(base, "pics")       # <-- NEW: use pics folder
    path = os.path.join(pics_dir, filename)

    if not os.path.exists(path):
        print(f"[WARN] Image not found: {path}")
        return

    try:
        w, h, c, d = dpg.load_image(path)
        dpg.add_static_texture(w, h, d, tag=tag)
    except Exception as e:
        print(f"[ERROR] Failed loading {filename}: {e}")


screen_width, screen_height = 1920, 1080
window_width = int(screen_width * 0.75)
window_height = int(screen_height * 0.75)
x_pos = (screen_width - window_width) // 2
y_pos = (screen_height - window_height) // 2

# -------------------------------------------------
# Setup Dear PyGui
# -------------------------------------------------
dpg.create_context()
dpg.create_viewport(
    title="Simulation Control Panel",
    width=window_width,
    height=window_height,
    x_pos=x_pos,
    y_pos=y_pos,
    resizable=False
)

dpg.setup_dearpygui()
dpg.show_viewport()

def draw_background():
    with dpg.viewport_drawlist(front=False, tag="background_layer"):
        dpg.draw_image("bg_texture", (0, 0), (window_width, window_height))


# -------------------------------------------------
# Load All Textures (including background)
# -------------------------------------------------
with dpg.texture_registry(show=False):

    # Background image MUST be inside registry
    load_texture("background.png", "bg_texture")

    # Main buttons
    load_texture("launch.png", "launch_texture")
    load_texture("stop.png", "stop_texture")

    # Dropdown icons
    image_list = [
        ("sunny.png", "sunny_tex"),
        ("rainy.png", "rainy_tex"),
        ("cloudy.png", "cloudy_tex"),
        ("night.png", "night_tex"),
        ("track_a.png", "trackA_tex"),
        ("track_b.png", "trackB_tex"),
        ("track_c.png", "trackC_tex"),
        ("dry.png", "dry_tex"),
        ("wet.png", "wet_tex"),
        ("front_cam.png", "front_tex"),
        ("rear_cam.png", "rear_tex"),
        ("top_cam.png", "top_tex"),
        ("veh1.png", "veh1_tex"),
        ("veh2.png", "veh2_tex"),
        ("veh3.png", "veh3_tex"),
    ]

    for file, tag in image_list:
        load_texture(file, tag)

# -------------------------------------------------
# Background Image (viewport)
# -------------------------------------------------

# print("Loaded bg_texture:", dpg.does_item_exist("bg_texture"))

def open_sensor_gui():
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sensor_gui.py")
    subprocess.Popen([sys.executable, script_path])

# -------------------------------------------------
# Helper: Create image dropdown
# -------------------------------------------------
def create_image_dropdown(label, texture_tags, default_tag):
    current = {"selected": default_tag}

    def select_option(sender, app_data, user_data):
        current["selected"] = user_data
        dpg.configure_item(f"{label}_image", texture_tag=user_data)
        dpg.hide_item(f"{label}_popup")

    with dpg.group(horizontal=True):
        dpg.add_text(label + ":")
        dpg.add_image_button(
            texture_tag=current["selected"],
            width=190, height=100,
            tag=f"{label}_image"
        )
        with dpg.popup(parent=f"{label}_image", tag=f"{label}_popup"):
            for tex in texture_tags:
                dpg.add_image_button(
                    texture_tag=tex,
                    width=190, height=100,
                    callback=select_option,
                    user_data=tex
                )

    return current

# -------------------------------------------------
# Modern Theme
# -------------------------------------------------
with dpg.theme() as modern_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0, 0))
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (40, 40, 60, 20))
        dpg.add_theme_color(dpg.mvThemeCol_Text, (240, 245, 255, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 110, 190, 240))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (80, 140, 250, 255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (100, 160, 255, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Border, (90, 90, 120, 150))
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 15)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 10, 8)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 20, 20)
        dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 12)
        dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0)

dpg.bind_theme(modern_theme)

# -------------------------------------------------
# GUI Content
# -------------------------------------------------
def close_launcher():
    dpg.stop_dearpygui()

with dpg.window(tag="main_window",
                label="Simulation Control Panel",
                pos=(30, 30),
                width=window_width - 60,
                height=window_height - 80,
                no_resize=True,
                no_background=True):

    dpg.add_text("Simulation Dashboard")
    dpg.add_separator()
    dpg.add_spacer(height=10)

    with dpg.group(horizontal=True):
        weather = create_image_dropdown("Weather", ["sunny_tex", "rainy_tex", "cloudy_tex", "night_tex"], "sunny_tex")
        create_image_dropdown("Track", ["trackA_tex", "trackB_tex", "trackC_tex"], "trackA_tex")
        create_image_dropdown("Condition", ["dry_tex", "wet_tex"], "dry_tex")
        create_image_dropdown("Camera", ["front_tex", "rear_tex", "top_tex"], "front_tex")
        create_image_dropdown("Vehicle", ["veh1_tex", "veh2_tex", "veh3_tex"], "veh1_tex")

    dpg.add_spacer(height=15)

    with dpg.group(horizontal=True):
        dpg.add_spacer(width=50) 
        dpg.add_button(label="Track Generator", width=200, height=40, callback=run_track_generator)
        dpg.add_spacer(width=45) 
        dpg.add_button(
        label="Sensor Attributes",
        width=200,
        height=40,
        callback=open_sensor_gui
)
    dpg.add_spacer(height=15)

    with dpg.group(horizontal=True):
        dpg.add_text("Visualizer:")
        dpg.add_combo(
            items=["Rviz","None"],
            default_value="None",
            width=150
        )
    


    dpg.add_spacer(height=30)
    with dpg.group(horizontal=True):
        dpg.add_image_button(texture_tag="launch_texture", width=655, height=250, callback=launch_simulation)
        dpg.add_spacer(width=50)
        dpg.add_image_button(texture_tag="stop_texture", width=655, height=250, callback=stop_simulation)

    dpg.add_spacer(height=40)
    dpg.add_separator()
    dpg.add_spacer(height=20)

    dpg.add_button(label="Close Launcher",
                   callback=close_launcher,
                   width=200, height=40)

dpg.set_frame_callback(1, draw_background)
# -------------------------------------------------
# Run
# -------------------------------------------------
dpg.set_primary_window("main_window", True)
dpg.set_viewport_resizable(False)
dpg.start_dearpygui()
dpg.destroy_context()
