import streamlit as st

from linedraw import linedraw

def draw_lines(lines):
    points = [p for line in lines for p in line]
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    current_size = max(max_x - min_x, max_y - min_y)
    scale = st.session_state.img_size / current_size
    x_offset = st.session_state.x_offset
    y_offset = st.session_state.y_offset
    scaled_lines = [[((p[0] - min_x) * scale + x_offset, (p[1] - min_y) * scale + y_offset) for p in line] for line in lines]
    bed_x_size = st.session_state.bed_x_size
    bed_y_size = st.session_state.bed_y_size
    g_code_commands = []
    # Set up G-code
    # G28: Home all axes
    g_code_commands.append(f"G28")
    # G21: Set units to millimeters
    g_code_commands.append(f"G21")
    # G90: Set to absolute positioning
    g_code_commands.append(f"G90")
    # G92: Set current position to 0,0,0
    g_code_commands.append(f"G92 X0 Y0 Z0")
    # Move to starting position
    g_code_commands.append(f"G1 Z{st.session_state.head_lift}")
    svg_string = f"""<svg width="{bed_x_size}" height="{bed_y_size}" xmlns="http://www.w3.org/2000/svg">"""
    # Draw box from (0,0) to (bed_x_size, bed_y_size)
    svg_string += f"""<polyline points="0,0 0,{bed_y_size} {bed_x_size},{bed_y_size} {bed_x_size},0 0,0" fill="none" stroke="black" stroke-width="1"/>"""
    for line in scaled_lines:
        svg_string += f"""<polyline points='{" ".join([f"{p[0]},{p[1]}" for p in line])}' fill="none" stroke="black" stroke-width="{st.session_state.stroke_width}"/>"""
        # Move to starting position
        g_code_commands.append(f"G0 X{line[0][0]} Y{line[0][1]}")
        # Lower the pen
        g_code_commands.append(f"G1 Z{0}")
        for p in line[1:]:
            # Move to next point
            g_code_commands.append(f"G1 X{p[0]} Y{p[1]}")
        # Lift the pen
        g_code_commands.append(f"G1 Z{st.session_state.head_lift}")
    svg_string += "</svg>"
    st.image(svg_string, use_column_width=True)
    st.download_button("Download G-code", "\n".join(g_code_commands), "plotter.gcode")

def main():
    st.set_page_config(page_title="Plotter", page_icon=":pencil:", layout="wide")
    st.title("Plotter")

    left, middle, right = st.columns(3)

    with right:
        st.write("To apply changes, please click 'Unload image' and upload the image again.")
        st.write("All values are in millimeters.")
        bed_x_size = st.number_input("Bed X size", value=250, key="bed_x_size")
        bed_y_size = st.number_input("Bed Y size", value=250, key="bed_y_size")
        x_offset = st.number_input("X offset", value=25, key="x_offset")
        y_offset = st.number_input("Y offset", value=25, key="y_offset")
        img_size = st.number_input("Image size", value=200, key="img_size")
        head_lift = st.number_input("Head lift", value=1, key="head_lift")
        stroke_width = st.number_input("Stroke width", value=0.2, key="stroke_width")
        hatch = st.checkbox("Hatch")
        linedraw.draw_hatch = hatch
        contour_simplification = st.number_input("Contour simplification", step=1, value=2)
        linedraw.contour_simplify = contour_simplification

    with left:
        if "uploaded_image" not in st.session_state:
            dropper = st.file_uploader("Upload a picture", type=['png', 'jpg', 'jpeg'])
            if dropper:
                st.session_state.uploaded_image = dropper
                # Save image to temp file locally
                with open("temp.jpg", "wb") as f:
                    f.write(dropper.read())
                    st.session_state.lines = linedraw.sketch("temp.jpg")
                st.rerun()
        if "uploaded_image" in st.session_state:
            unload_image = st.button("Unload image", type="primary")
            st.image(st.session_state.uploaded_image, use_column_width=True)
            if unload_image:
                st.session_state.pop("uploaded_image")
                st.rerun()
            with middle:
                draw_lines(st.session_state.lines)

if __name__ == '__main__':
    main()
