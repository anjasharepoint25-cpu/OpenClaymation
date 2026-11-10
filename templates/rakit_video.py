# Adapted from Egypt Myth 101/Episode 1 - Clay/rakit_video.py.
# Run AFTER rendering the full PNG sequence. Never overwrites a previous MP4.
import bpy, os, re
from pathlib import Path
sc=bpy.context.scene
base=Path(bpy.path.abspath('//'))
m=re.search(r'Ep(\d+)_clay',Path(bpy.data.filepath).stem)
if not m:raise RuntimeError('Buka file Mitos_Nordik_EpN_clay.blend terlebih dahulu.')
ep=int(m.group(1));frames=base/'render'/'frames';frames.mkdir(parents=True,exist_ok=True)
expected=list(range(sc.frame_start,sc.frame_end+1))
files=[frames/('ep%d_%04d.png'%(ep,f)) for f in expected]
missing=[p.name for p in files if not p.is_file()]
if missing:raise RuntimeError('Render PNG belum lengkap: %d frame hilang; contoh %s. Lihat CARA_RENDER.txt.'%(len(missing),missing[:3]))
se=sc.sequence_editor_create()
coll=se.strips if hasattr(se,'strips') else se.sequences
for st in list(coll):
    if st.name.startswith('NORDIC_'):coll.remove(st)
st=coll.new_image('NORDIC_frames',str(files[0]),5,sc.frame_start)
for f in files[1:]:st.elements.append(f.name)
audio=[base/'audio'/('babak%d.mp3'%i) for i in range(1,7)]
have_audio=all(p.is_file() for p in audio)
if any(p.is_file() for p in audio) and not have_audio:raise RuntimeError('Audio hanya sebagian. Lengkapi babak1–6 sebelum perakitan.')
if have_audio:
    if sc.get('audio_status','').startswith('BELUM'):raise RuntimeError('Audio belum disinkronkan. Ukur durasi asli, perbarui DUR, jalankan anim_epN, lalu render ulang.')
    for i,p in enumerate(audio):
        coll.new_sound('NORDIC_babak%d'%(i+1),str(p),1,round(sc['narration_starts_seconds'][i]*sc.render.fps)+1)
suffix='' if have_audio else '_preview_silent'
out=base/'render'/('Mitos_Nordik_Ep%d%s.mp4'%(ep,suffix))
k=2
while out.exists():
    out=base/'render'/('Mitos_Nordik_Ep%d%s_v%d.mp4'%(ep,suffix,k));k+=1
r=sc.render
try:r.image_settings.media_type='VIDEO'
except (AttributeError,TypeError):pass
r.image_settings.file_format='FFMPEG';r.ffmpeg.format='MPEG4';r.ffmpeg.codec='H264';r.ffmpeg.constant_rate_factor='HIGH'
r.ffmpeg.audio_codec='AAC';r.ffmpeg.audio_bitrate=192;r.resolution_percentage=100;r.use_sequencer=True;r.filepath=str(out)
print('OUTPUT',str(out),'AUDIO',have_audio)
bpy.ops.render.render(animation=True)
print('SELESAI',str(out))
