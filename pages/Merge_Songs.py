import streamlit as st
import time
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import  concatenate_audioclips
from io import BytesIO

import tempfile

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
#prepare-your-song-in-one-click
{
text-align:center;
}
#stBaseButton-secondary
{
visibility:"hidden";
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

.lines
{
width:100vw;
height:2px;
background: linear-gradient(45deg, #fc8000, #e4e245);
margin: 10px 0;
}
.emotion-cache-1weic72,.st-emotion-cache-1weic72
{
    margin: 10px; 
    width: 200px;
}
.st-emotion-cache-z8vbw2,.st-emotion-cache-1rwb540
{
    float: unset;
    width: 100%;
    margin-top: 35px;
}
</style>""", unsafe_allow_html=True)

if "y" not in st.session_state.keys():
    st.session_state["y"]=0
if "songs" not in st.session_state.keys():
    st.session_state["songs"]=0

def coubtn():
    if "song_count" not in st.session_state or len(str(st.session_state["song_count"])) == 0:
        st.toast("Enter Valid Song Count")
    else:
        try:
            cou = int(st.session_state["song_count"])
            if cou > 6:
                st.toast("Maximum 6 Songs Allowed")
            else:
                st.session_state["songs"] = cou
                st.session_state["y"] = 1
        except ValueError:
            st.toast("Enter Valid Song Count")


def trim_audio(uploaded_file, start_sec=None, end_sec=None):
    if uploaded_file:
        try:
            uploaded_file.seek(0)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            clip = AudioFileClip(tmp_path)
            if start_sec is not None and end_sec is not None and end_sec > start_sec:
                clip = clip[start_sec:end_sec]
            return clip
        except Exception as e:
            st.warning(f"Trim error: {e}")
    return None


def merge_song():
    trimsongs = []
    error_flag = False

    for i in range(1, st.session_state.get("songs", 0) + 1):
        try:
            start_val = st.session_state.get(f"st-{i}", "")
            end_val = st.session_state.get(f"et-{i}", "")
            start = float(start_val) if start_val != "" else None
            end = float(end_val) if end_val != "" else None
            uploaded = st.session_state.get(f"file-{i}", None)

            if not uploaded:
                st.warning(f"⚠️ No file uploaded for Song {i}.")
                error_flag = True
                continue

            if start is not None and end is not None and end <= start:
                st.warning(f"⚠️ Invalid time range for Song {i}.")
                error_flag = True
                continue

            trimmed = trim_audio(uploaded, start, end)
            if trimmed:
                trimsongs.append(trimmed)
            else:
                st.warning(f"⚠️ Could not process Song {i}.")
                error_flag = True

        except Exception as e:
            st.warning(f"⚠️ Error in processing Song {i}")
            error_flag = True

    if not error_flag and trimsongs:
        try:
            final_clip = concatenate_audioclips(trimsongs)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tmp_path = tmp.name
                final_clip.write_audiofile(tmp_path, codec="libmp3lame", fps=44100)

            with open(tmp_path, "rb") as f:
                buffer = BytesIO(f.read())
                buffer.seek(0)
                st.session_state["merge_audio"] = buffer
                st.session_state["y"] = 2
                st.toast("✅ Songs merged successfully!")

        except Exception as e:
            st.warning(f"🚫 Error merging songs try again ")
    else:
        st.warning("🚫 Merging skipped due to incorrect input.")

col1 = st.columns(4)
with col1[0]:
    st.header("Shivona Tunes")
st.title("Prepare Your Song In One Click")
st.info("Upload Your Songs To Merge And Edit Them!")

if st.session_state["y"]==0:
    col = st.columns(2)
    with col[0]:
        st.text_input(label="Enter The Number Of Songs", key="song_count")
    with col[1]:
        st.button("Proceed", on_click=coubtn)
elif st.session_state["y"]==1:
    for i in range(1,int(st.session_state["songs"])+1):
        colm=st.columns(3)
        with colm[0]:
            st.file_uploader(label=f"upload song file-> {i}",type=["mp3","mpeg"],key=f"file-{i}")
        with colm[1]:
            st.text_input(label=f"enter starting time in second",key=f"st-{i}")
        with colm[2]:
            st.text_input(label=f"enter ending time in second",key=f"et-{i}")
        st.markdown("""<div class='lines'/>""",unsafe_allow_html=True)
    st.button("Proceed",on_click=merge_song)
elif st.session_state["y"]==2:
    st.download_button("Download Merged Song", data=st.session_state["merge_audio"].getvalue(), file_name="Shivona_merged_song.mp3", mime="audio/mpeg")

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



