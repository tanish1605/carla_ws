import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String, Int32
import threading
import dearpygui.dearpygui as dpg
import time

# =============================================================
# SUBSCRIBER NODE
# =============================================================
class DashboardSubscriber(Node):
    def __init__(self):
        super().__init__("dashboard_subscriber")

        # Shared GUI values
        self.speed = 0.0
        self.throttle = 0.0
        self.v_actual = 0.0
        self.steer = 0.0
        self.led_color = "off"

        # Subscribers (dummy topic names)
        self.create_subscription(Float32, "/speed_topic", self.speed_callback, 10)
        self.create_subscription(Float32, "/throttle_topic", self.throttle_callback, 10)
        self.create_subscription(Float32, "/v_actual_topic", self.vactual_callback, 10)
        self.create_subscription(Float32, "/steer_topic", self.steer_callback, 10)
        self.create_subscription(String,  "/led_color_topic", self.led_callback, 10)

    def speed_callback(self, msg):
        self.speed = msg.data

    def throttle_callback(self, msg):
        self.throttle = msg.data

    def vactual_callback(self, msg):
        self.v_actual = msg.data

    def steer_callback(self, msg):
        self.steer = msg.data

    def led_callback(self, msg):
        self.led_color = msg.data.strip().lower()

# =============================================================
# RUN ROS IN BACKGROUND THREAD
# =============================================================
def ros_spin(node):
    rclpy.spin(node)

is_on = False

def toggle_callback():
    global is_on
    is_on = not is_on
    dpg.set_item_label("toggle_btn", f"ON" if is_on else "OFF")
    print("Current state:", is_on)

# =============================================================
# DEAR PY GUI (YOUR ORIGINAL GUI + ROS BINDING)
# =============================================================
def main():
    # -------------------------------- ROS2 --------------------------------
    rclpy.init()
    node = DashboardSubscriber()
    threading.Thread(target=ros_spin, args=(node,), daemon=True).start()

    # -------------------------------- DPG --------------------------------
    dpg.create_context()

    # ======================================================================
    # GLOBAL THEME (Glass, Modern)
    # ======================================================================
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (20, 22, 30, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (35, 40, 55, 180))
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

    # LED color setter
    def set_led(color):
        dpg.bind_item_theme("MAIN_LED", led_off)
        if color == "green": dpg.bind_item_theme("MAIN_LED", led_green)
        elif color == "red": dpg.bind_item_theme("MAIN_LED", led_red)
        elif color == "blue": dpg.bind_item_theme("MAIN_LED", led_blue)

    # ======================================================================
    # MAIN WINDOW (your original code)
    # ======================================================================
    with dpg.window(tag="root", label="Dashboard Layout", width=1200, height=-500, no_scrollbar=True):

        with dpg.child_window(height=-575):
            with dpg.table(header_row=False, policy=dpg.mvTable_SizingStretchProp):
                dpg.add_table_column(init_width_or_weight=2)
                dpg.add_table_column(init_width_or_weight=1)
                dpg.add_table_column(init_width_or_weight=1)
                dpg.add_table_column(init_width_or_weight=2)

                with dpg.table_row():

                    # Left - LED color buttons
                    with dpg.child_window(border=True):
                        dpg.add_text("Controls", color=(180, 200, 255))
                        dpg.add_separator()
                        with dpg.group(horizontal=True):
                                dpg.add_text("Go (Toggle):");     dpg.add_button(label="OFF", tag="toggle_btn", callback=toggle_callback)
                        dpg.add_button(label="Set Red", height=30, callback=lambda: set_led("red"))
                        dpg.add_button(label="Set Blue", height=30, callback=lambda: set_led("blue"))

                    # Middle - LED
                    with dpg.child_window(border=True):
                        dpg.add_text("Status LED", color=(180, 200, 255))
                        dpg.add_separator()
                        # dpg.add_spacer(height=5)
                        dpg.add_button(tag="MAIN_LED", label=" ", width=85, height=85)
                        dpg.bind_item_theme("MAIN_LED", led_off)
                    
                    with dpg.child_window(border=True):
                            dpg.add_button(tag="TS", label="TS", width=40, height=40)
                            dpg.add_button(tag="AS", label="AS", width=40, height=40)
                            dpg.add_button(tag="LV", label="LV", width=40, height=40)
                        
                    # Right - Data values
                    with dpg.child_window(border=True):
                        dpg.add_text("Real-Time Vehicle Data", color=(180, 200, 255))
                        dpg.add_separator()

                        with dpg.group(horizontal=True):
                            with dpg.group(horizontal=True):
                                dpg.add_text("Speed:");    dpg.add_text("0.0", tag="speed_val", color=(80, 180, 255))
                            dpg.add_spacer(width=30)
                            with dpg.group(horizontal=True):
                                dpg.add_text("Throttle:"); dpg.add_text("0.0", tag="throttle_val", color=(80, 180, 255))
                        with dpg.group(horizontal=True):
                            with dpg.group(horizontal=True):
                                dpg.add_text("V_actual:"); dpg.add_text("0.0", tag="vactual_val", color=(80, 180, 255))
                            dpg.add_spacer(width=10)
                            with dpg.group(horizontal=True):
                                dpg.add_text("Steer:");    dpg.add_text("0.0", tag="steer_val", color=(80, 180, 255))

        # Bottom logs (unchanged)
        with dpg.child_window(height=500):
            with dpg.table(header_row=False, policy=dpg.mvTable_SizingStretchProp):
                dpg.add_table_column(); dpg.add_table_column()
                with dpg.table_row():
                    with dpg.child_window(border=True):
                        dpg.add_text("ROS Monitor Logs", color=(200, 220, 255))
                        dpg.add_separator(); dpg.add_listbox(items=[], tag="ros_log_box", num_items=17)
                    with dpg.child_window(border=True):
                        dpg.add_text("CAN Monitor Logs", color=(200, 220, 255))
                        dpg.add_separator(); dpg.add_listbox(items=[], tag="can_log_box", num_items=17)

        with dpg.group(horizontal=True):
            dpg.add_spacer(width= -10)
            dpg.add_button(label="Fault Injection", width=200, height=40,
                           callback=lambda: dpg.fault_injection())
            dpg.add_spacer(width=540)
            dpg.add_button(label="Reset", width=200, height=40,
                           callback=lambda: dpg.reset())
            dpg.add_button(label="Close Window", width=200, height=40,
                           callback=lambda: dpg.stop_dearpygui())

    # =============================================================
    # VIEWPORT
    # =============================================================
    dpg.create_viewport(title="Dashboard Layout", width=1200, height=800)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("root", True)

    # =============================================================
    # MANUAL GUI LOOP (updates values from ROS)
    # =============================================================
    while dpg.is_dearpygui_running():

        # Update GUI fields
        dpg.set_value("speed_val",     f"{node.speed:.2f}")
        dpg.set_value("throttle_val",  f"{node.throttle:.2f}")
        dpg.set_value("vactual_val",   f"{node.v_actual:.2f}")
        dpg.set_value("steer_val",     f"{node.steer:.2f}")

        # Update LED
        set_led(node.led_color)

        dpg.render_dearpygui_frame()
        time.sleep(0.05)  # ~20 FPS

    dpg.destroy_context()


if __name__ == "__main__":
    main()
