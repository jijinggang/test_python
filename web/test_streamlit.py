import streamlit as st;
import random

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
if "islogin" not in st.session_state:
    st.session_state.userid= random.randint(0,99999999);
    st.session_state.islogin = False

def login():
    if( st.session_state.islogin):
        st.title("hello world")
    else:
        st.text(st.session_state.userid)
        st.text_area('')
        #st.checkbox('islogin',key="islogin")
        pswd = st.text_input('pswd');
        if pswd == '123456':
            st.session_state.islogin = True
            st.experimental_rerun()

def df():
    import streamlit as st
    import pandas as pd
    import numpy as np

    df = pd.DataFrame(
    np.random.randn(50, 20),
    columns=('col %d' % i for i in range(20)))

    st.dataframe(df)  # Same as st.write(df)

def de():
    import streamlit as st
    import pandas as pd

    df = pd.DataFrame(
        [
        {"command": "st.selectbox", "rating": 4, "is_widget": True},
        {"command": "st.balloons", "rating": 5, "is_widget": False},
        {"command": "st.time_input", "rating": 3, "is_widget": True},
    ]
    )
    edited_df = st.data_editor(df)

    favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
    print(favorite_command)
    st.markdown(f"Your favorite command is **{favorite_command}** 🎈")

def button():
    st.download_button("Download",data="hello world",file_name="1.txt")
    st.checkbox('islogin',st.session_state.islogin)


def column():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg")

    with col2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg")

    with col3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg")


def tabs():
    tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

    with tab1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg", width=400)

    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=400)

    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=400)

def empty():

    placeholder = st.empty()

    # Replace the placeholder with some text:
    placeholder.text("Hello")
    # Replace the text with a chart:
    placeholder.line_chart({"data": [1, 5, 2, 6]})

    # Replace the chart with several elements:
    with placeholder.container():
        st.write("This is one element")
        st.write("This is another")

    pswd = placeholder.text_input('check_pswd')


    # Clear all those elements:
    if(pswd =="123456"):
       placeholder.empty()


def chat():
    prompt = st.chat_input("Say something")
    if prompt:
        st.chat_message('user').text(f"user:{prompt}")
def echo():
    with st.echo():
        def get_name():
            return 'John'
        def get_punctuation():
            return '!!!'

        st.write("Hi there, ", get_name(), get_punctuation())

def component():
    import streamlit.components.v1 as components
    # embed streamlit docs in a streamlit app
    st.markdown("# Header")
    components.iframe("https://docs.streamlit.io/en/latest",height=600)
    st.markdown("# Footer")



def main():
    cmds = {"login":login,"df":df,"de":de,"button":button,"column":column,"tabs":tabs,"empty":empty,"chat":chat,"echo":echo,"component":component}
    sel =st.sidebar.selectbox("选择命令：",cmds.keys())
    cmds[sel]()


if __name__ == '__main__':
    main()