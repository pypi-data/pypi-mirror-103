import youtube_dl, requests
from bgeditor.common.utils import get_dir, download_file,normal_audio
from bgeditor.dao.FFmpeg import create_loop_audio_times
import uuid,json, shutil,os
def download_audio(url,ext='mp3'):
    file_name = str(uuid.uuid4()) + "." + ext
    rs = get_dir('download') + file_name
    ydl_opts = {
        'outtmpl': rs,
        'format': 'bestaudio/m4a',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return rs
def create_compilation_songs(data):
    #[{"type":3,"url":"","repeat":1}]
    #3: youtube_video
    #7: deezer
    #8: link direct
    arr_songs=json.loads(data)
    file_merg_path = get_dir('coolbg_ffmpeg') + str(uuid.uuid4())
    file_merg = open(file_merg_path, "a")
    final_clip_path = get_dir('coolbg_ffmpeg') + str(uuid.uuid4()) + '-final.mp3'
    try:
        for song in arr_songs:
            try:
                if song['type'] == 3:#youtube
                    song['local']=download_audio(song['url'])
                if song['type'] == 8:#direct
                    song['local']=download_file(song['url'])
                if song['type'] == 7:#deezer
                    song_info=requests.get("http://api.automusic.win/deezer/track/get/"+song['url']).json()
                    song['local']=download_file(song_info['url_128'])
                if len(arr_songs) > 1:
                    song['local']=normal_audio(song['local'])
                if song['repeat'] > 1:
                    song['local']= create_loop_audio_times(song['local'], song['repeat'])

                if not "coolbg_ffmpeg" in song['local']:
                    tmp_clip_path = get_dir('coolbg_ffmpeg') + str(uuid.uuid4()) + '-' + os.path.basename(song['local'])
                    shutil.copyfile(song['local'], tmp_clip_path)
                    os.remove(song['local'])
                    song['local']=tmp_clip_path

                file_merg.write("file '%s'\n" % os.path.basename(song['local']))
            except:
                pass
        file_merg.close()
        cmd = "ffmpeg -y -f concat -safe 0 -i \"%s\" -codec copy \"%s\"" % (file_merg_path, final_clip_path)
        os.system(cmd)
        os.remove(file_merg_path)
        for song in arr_songs:
            os.remove(song['local'])
    except:
        pass
    return final_clip_path




