import streamlit as st
import tempfile
import time
import requests
from io import BytesIO
from moviepy import VideoFileClip
import vd

st.set_page_config(page_title="Shivona Tunes", page_icon="logo.png", layout="wide")
st.markdown("""
<style>
.st-emotion-cache-ajtf3x 
{
display:block;
}
.elbt1zu4
{
padding:0px 5px;
}
#shivona-tunes
{
padding:0px;
margin-left:10px;
margin-top:10px;
color: rgb(239 106 7);
font-size:250%;
width:100vw;
}
#get-your-song-in-one-click
{
text-align:center;
}
#stBaseButton-secondary
{
visibility:"hidden";
}
.e16xj5sw0
{
height:500px;
margin:10px;
margin-bottom:10px;
display:flex;
align-items:center;
justify-content:center;
margin-top: 20px;
}
.e16xj5sw1
{
margin-right:0;
display:block;
}
.e16xj5sw2
{
    width: 100%;
    margin-right: 1rem;
    text-align: center;
    display: block;
    color:black;
}
.st-emotion-cache-bfgnao,.st-emotion-cache-1weic72
{
    color: rgb(239 106 7);
    margin:0 auto;
    font-family: serif;
    font-weight: 600;
    font-size: 150%;
    width:160px;
}
.e16xj5sw5
{
background-color: orange;
margin-bottom: 20px;
}
.stToastContainer
{
display:flex;
align-items:center;
justify-content:center;
}
.stAlertContainer
{
text-align:center;
}
.st-emotion-cache-1gulkj5 .st-emotion-cache-1rwb540,.st-emotion-cache-1erivf3 .st-emotion-cache-z8vbw2
{
position:absolute;
visibility:hidden;
}
.stDownloadButton .st-emotion-cache-1rwb540,.stDownloadButton .st-emotion-cache-z8vbw2 
{
width:100%;
margin-bottom:20px;
}
.st-emotion-cache-1an99fx,.st-emotion-cache-1o77jex
{
    margin: 2% 3%;
    background-color: gainsboro;
    padding: 15px;
    font-size: 120%;
    font-weight: 600;
    border-radius: 5px;

}
.st-emotion-cache-1o77jex
{
color:black;
}
.footer
{
    padding: 20px;
    font-family: serif;
    font-size: 120%;
    background: antiquewhite;
    margin-bottom: 10px;
    color:black;
}
.st-emotion-cache-1ort0lt
{
    width: 100%;
    text-align: center;
}
.st-emotion-cache-u8hs99
{
    width: 100%;
    text-align: center;
}
.st-emotion-cache-zy6yx3
{
padding: 60px 10px 0 10px;
}
.st-emotion-cache-1rwb540,.st-emotion-cache-z8vbw2
{
    float: unset;
    width: 100%;
}
</style>""", unsafe_allow_html=True)


if "y" not in st.session_state.keys():
    st.session_state["y"] = 0
video=None
def dwf():
    sdata=st.session_state
    link=sdata["link_box"]
    if len(link) != 0:
        if link.find("youtu") != -1 and link.find("=shared")!=-1:
            st.session_state["y"]=2
            url=None
            url= vd.getURL(st.session_state["link_box"])
            while url==None:
                pass
            if url=="not":
                st.session_state["y"]=0
                st.toast("Wrong URL Try Again!")

            else:
                if sdata["type"]==".mp3" :
                    cont = requests.get(url)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
                        tmp_video.write(cont.content)
                        tmp_video_path = tmp_video.name
                    video_clip = VideoFileClip(tmp_video_path)
                    audio_temp_path = tmp_video_path.replace(".mp4", ".mp3")
                    video_clip.audio.write_audiofile(audio_temp_path)
                    with open(audio_temp_path, "rb") as f:
                        audio_bytesio = BytesIO(f.read())
                    st.session_state["data"] = audio_bytesio
                    st.session_state["y"] = 3
                else:
                    cont = requests.get(url)
                    st.session_state["data"] = BytesIO(cont.content)
                    st.session_state["y"]=1

        else:
            st.toast("Wrong YouTube Video URL!")
    else:
        st.toast("Enter A Valid YouTube URL")
col1 = st.columns(4)
with col1[0]:
    st.header("Shivona Tunes")
st.title("Get Your Song In One Click")
st.info("Use Youtube Videos Link To Download And Convert It Into Audio")
col=st.columns(3)
with col[0]:
    st.text_input(label="Enter Youtube Link Here",key="link_box")
with col[1]:
    st.selectbox("Content Type",[".mp3",".mp4"],key="type",on_change=dwf)
with col[2]:
    st.write("")
    st.write("")
    if len(st.session_state['link_box'])==0:
        st.session_state["y"]=0

    if st.session_state["y"]==1 :
        st.download_button(
            label="Download 📽️",
            data=st.session_state["data"],
            file_name="Shivona_Tunes.mp4",
            mime="video/mp4"
        )
    elif st.session_state["y"]==3:
            st.download_button(
                label="Download 🎶",
                data=st.session_state["data"],
                file_name="Shivona_Tunes.mp3",
                mime="audio/mpeg"
            )
    elif st.session_state["y"]==0:
        coll=st.columns(2)
        with coll[0]:
            st.button("Download",on_click=dwf)
        with coll[1]:
            st.markdown("""
            <a href="/Merge_Songs">
                <button style="background-color:#FD504D;color:white;padding:8px;border:none;border-radius:10px;width:100%">
                 Merge Songs
                </button>
            </a>
            """, unsafe_allow_html=True)

    # elif st.session_state["y"]==2:
    #     with st.spinner("Processing your media..."):
    #         while True:
    #             if st.session_state["y"]!=2:
    #                 break
st.markdown("""
<style>
.st-emotion-cache-xhkv9f
{
  margin: 1% 4%;
  border: 1px solid gray;
  border-radius: 10px;
  # box-shadow: 10px 10px 10px gray;
  padding: 8px;
  background-color: rgb(255 127 21);
  box-shadow: rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px, rgba(10, 37, 64, 0.35) 0px -2px 6px 0px inset;
}
</style>""", unsafe_allow_html=True)
st.image("web.png", use_container_width=True)
content = """🎧 Shivona — Your Performance-Ready Music Assistant Turn YouTube moments into personalized audio experiences with Shivona, the all-in-one platform for performers, music lovers, and event organizers. Whether you're prepping for a show, curating a medley, or just want that one track in both audio and video format—Shivona gets it done with just a few clicks.

🔗 From URL to MP3, Shivona helps you:

🎶 Extract Audio from YouTube Videos to save and share your favorite sounds

📥 Download in Both Formats—whether you want crisp audio or full video

🧩 Merge Multiple Tracks Seamlessly to suit your vibe or stage routine

🕒 Prepare Songs on the Fly with tools designed for last-minute perfection

✨ Shivona isn’t just a downloader—it’s your backstage tech wizard. With intuitive design and reliable performance, your song prep becomes effortless and exciting. Because when the moment matters, Shivona makes sure your music is ready."""
st.text(content)

st.markdown(f"""<div class="footer">© {time.strftime('%Y')} Shivona Tunes. All rights reserved.</div>""",
            unsafe_allow_html=True)



