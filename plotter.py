import streamlit as st


def main():
    st.set_page_config(page_title="Plotter", page_icon=":pencil:", layout="wide")
    st.title("Plotter")

    left, right = st.columns(2)

    with left:
        if "uploaded_image" not in st.session_state:
            dropper = st.file_uploader("Upload a picture", type=['png', 'jpg', 'jpeg'])
            if dropper:
                st.session_state.uploaded_image = dropper
                st.rerun()
        if "uploaded_image" in st.session_state:
            unload_image = st.button("Unload image")
            st.image(st.session_state.uploaded_image, use_column_width=True)
            if unload_image:
                st.session_state.pop("uploaded_image")
                st.rerun()

    with right:
        bed_x_size = st.number_input("Bed X size")
        bed_y_size = st.number_input("Bed Y size")
        x_offset = st.number_input("X offset")
        y_offset = st.number_input("Y offset")
        img_x_size = st.number_input("Image X size")
        img_y_size = st.number_input("Image Y size")
        head_lift = st.number_input("Head lift")
        reslice = st.button("Reslice")

if __name__ == '__main__':
    main()
