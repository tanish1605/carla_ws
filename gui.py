import dearpygui.dearpygui as dpg
import platform
import os
import subprocess
import sys

scale = 1.0

processes = {}  # to track running background processes
# Path to your CARLA project directory
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CARLA_DIR = os.path.dirname(PROJECT_DIR)
SENSOR_DIR = os.path.join(CARLA_DIR, "IITBDV-Simulator", "src", "car_sensor", "car_sensor")
# SH_DIR = os.path.join(CARLA_DIR,"Unreal", "CarlaUE4","Binaries","LinuxNoEditor")
SH_DIR = "/mnt/IITB-DV/IITB-DV-Simulator/mnt/carla/Unreal/CarlaUE4/Binaries/LinuxNoEditor"
print("Project Directory:", SENSOR_DIR)

def build_sensor_nodes():
    subprocess.Popen(["colcon","build"], cwd=os.path.dirname(SENSOR_DIR))
    # subprocess.Popen(["bash", "-c", "source install/setup.bash && ros2 run car_sensor car_spawner"], cwd=os.path.dirname(SENSOR_DIR))



# uncomment launch_sensor_nodes only after fixing the nodes killing issue

def launch_sensor_nodes():
    sensor_scripts = {
        "car_spawner": "car_spawner",
        "pygame_control": "pygame_control",
        "lidar_out": "lidar_out",
        "camera_manager": "camera_manager",
        "imu_node": "imu_node"
    }

    # for name, script in sensor_scripts.items():
    #     proc = subprocess.Popen(
    #         ["bash", "-c", f"source install/setup.bash && ros2 run car_sensor {script}"],
    #         cwd=os.path.dirname(SENSOR_DIR)
    #     )
    #     processes[name] = proc

def launch_simulation():
    print("Launching simulation in:", PROJECT_DIR)

    processes["simulation"] = subprocess.Popen(
        ["bash", "-c","./CarlaUE4.sh -carla-map=CustomTrack1 -windowed -ResX=1280 -ResY=720"],
        cwd=SH_DIR
    )
    main_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main_gui.py")
    subprocess.Popen([sys.executable, main_path])
    # /mnt/IITB-DV/IITB-DV-Simulator/mnt/IITB-DV/carla/Unreal/CarlaUE4/Binaries/Linux/ 


    # selected = weather["selected"]

    # if selected == "sunny_tex":
    #     subprocess.Popen(["python3", "sunny.py"], cwd=PROJECT_DIR)

    # elif selected == "rainy_tex":
    #     subprocess.Popen(["python3", "rainy.py"], cwd=PROJECT_DIR)

    # elif selected == "cloudy_tex":
    #     subprocess.Popen(["python3", "cloudy.py"], cwd=PROJECT_DIR)

    # elif selected == "night_tex":
    #     subprocess.Popen(["python3", "night.py"], cwd=PROJECT_DIR)
    # launch_sensor_nodes()
    # dpg.set_value("status_text", "Status: Running Simulation")

def stop_simulation():
    # Kill CARLA process
    subprocess.Popen(["pkill", "-f", "CarlaUE4"])

    # Kill all ROS2 sensor nodes
    ros_nodes = [
        "camera_leftleft_node",
        "camera_leftright_node",
        "camera_manager_node",
        "camera_rightleft_node",
        "camera_rightright_node",
        "car_spawner_node",
        "carla_manual_control_node",
        "lidar_spawner_node",
        "pygame_control",
        "imu_node"
    ]
    for node in ros_nodes:
        subprocess.Popen(["pkill", "-f", node])

    # Clear stored processes
    processes.clear()

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
window_width = int(screen_width * (scale*0.75))
window_height = int(screen_height * (scale*0.75))
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
        ("ads_dv.png", "veh1_tex"),
        ("e11.png", "veh2_tex"),
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
            width=scale*190, height=scale*100,
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
                pos=(scale*30, scale*30),
                width=(window_width - 60)*scale,
                height=(window_height - 80)*scale,
                no_resize=True,
                no_background=True):

    dpg.add_text("Simulation Dashboard")
    dpg.add_separator()
    dpg.add_spacer(height=scale*10)

    with dpg.group(horizontal=True):
        weather = create_image_dropdown("Weather", ["sunny_tex", "rainy_tex", "cloudy_tex", "night_tex"], "sunny_tex")
        create_image_dropdown("Track", ["trackA_tex", "trackB_tex", "trackC_tex"], "trackA_tex")
        create_image_dropdown("Condition", ["dry_tex", "wet_tex"], "dry_tex")
        create_image_dropdown("Camera", ["front_tex", "rear_tex", "top_tex"], "front_tex")
        create_image_dropdown("Vehicle", ["veh1_tex", "veh2_tex", "veh3_tex"], "veh1_tex")

    dpg.add_spacer(height=scale*15)

    with dpg.group(horizontal=True):
        dpg.add_spacer(width=50*scale) 
        dpg.add_button(label="Track Generator", width=200*scale, height=40*scale, callback=run_track_generator)
        dpg.add_spacer(width=45*scale) 
        dpg.add_button(
        label="Sensor Attributes",
        width=200*scale,
        height=40*scale,
        callback=open_sensor_gui)
        dpg.add_spacer(width=65*scale) 
        dpg.add_button(label="Build Sensor Nodes", width=200*scale, height=40*scale, callback=build_sensor_nodes)
        dpg.add_spacer(width=50*scale)
        dpg.add_button(label="Launch Sensor Nodes", width=200*scale, height=40*scale, callback=launch_sensor_nodes)
        dpg.add_spacer(width=50*scale)
        dpg.add_button(label="Advanced Settings", width=200*scale, height=40*scale
                    #    , callback=advanced_settings
                       )



    dpg.add_spacer(height=scale*15)

    with dpg.group(horizontal=True):
        dpg.add_text("Visualizer:")
        dpg.add_combo(
            items=["Rviz","None"],
            default_value="None",
            width=150*scale
        )
    


    dpg.add_spacer(height=30*scale)
    with dpg.group(horizontal=True):
        dpg.add_image_button(texture_tag="launch_texture", width=655*scale, height=250*scale, callback=launch_simulation)
        dpg.add_spacer(width=50*scale)
        dpg.add_image_button(texture_tag="stop_texture", width=655*scale, height=250*scale, callback=stop_simulation)

    dpg.add_spacer(height=40*scale)
    dpg.add_separator()
    dpg.add_spacer(height=20*scale)

    dpg.add_button(label="Close Launcher",
                   callback=close_launcher,
                   width=scale*200, height=scale*40)

dpg.set_frame_callback(1, draw_background)
# -------------------------------------------------
# Run
# -------------------------------------------------
dpg.set_primary_window("main_window", True)
dpg.set_viewport_resizable(False)
dpg.start_dearpygui()
dpg.destroy_context()
