import bpy, os, json
from pathlib import Path
def project_root():
    p=Path(bpy.data.filepath).parent
    return p.parent if p.name.startswith('Episode ') else p
ROOT=str(project_root())
def render_tests(n,only=None):
    base=Path(ROOT)/('Episode %d - Clay'%n);(base/'test_frames').mkdir(parents=True,exist_ok=True)
    t=bpy.data.texts['anim_ep%d'%n]
    # Animation is already compiled by run_ep. Metadata is retained on the scene.
    fs=json.loads(bpy.context.scene['test_frames'])
    sc=bpy.context.scene;r=sc.render
    r.resolution_percentage=25;sc.cycles.samples=20
    try:
        for i,f in enumerate(fs):
            if only is not None and i not in only:continue
            sc.frame_set(f);r.filepath=str(base/'test_frames'/('a%02d.png'%i))
            bpy.ops.render.render(write_still=True)
    finally:
        r.resolution_percentage=100;sc.cycles.samples=64;r.filepath='//render/frames/ep%d_'%n;sc.frame_set(1)
    bpy.ops.wm.save_mainfile()
    print('TESTS',n,fs,'ONLY',only)
def run_ep(n,SRC,naskah=None,title='',only=None,render=True):
    base=Path(ROOT)/('Episode %d - Clay'%n);base.mkdir(parents=True,exist_ok=True)
    (base/'render'/'frames').mkdir(parents=True,exist_ok=True)
    fp=base/('Mitos_Nordik_Ep%d_clay.blend'%n)
    if str(fp)!=bpy.data.filepath:
        assert not fp.exists(),'Buka file episode yang sudah ada sebelum mengubahnya.'
        bpy.ops.wm.save_as_mainfile(filepath=str(fp))
        # Episode copies retain only actors and props named by their own script.
    for root in [o for o in bpy.data.objects if o.get('asset')]:
        if repr(root.name) not in SRC and ('"'+root.name+'"') not in SRC:
            for child in list(root.children_recursive):bpy.data.objects.remove(child,do_unlink=True)
            bpy.data.objects.remove(root,do_unlink=True)
    t=bpy.data.texts.get('anim_ep%d'%n) or bpy.data.texts.new('anim_ep%d'%n)
    t.clear();t.write(SRC);t.use_fake_user=True
    g={};exec(compile(SRC,t.name,'exec'),g)
    bpy.context.scene['test_frames']=json.dumps(g['TESTS'])
    bpy.context.scene['audio_status']='BELUM DIREKAM; DUR masih perkiraan'
    if naskah:
        words=sum(len(s.split()) for s in naskah)
        assert len(naskah)==6 and 190<=words<=200,(len(naskah),words)
        (base/'naskah.txt').write_text('MITOS NORDIK 101 — EPISODE %d: %s\n%d kata; narasi belum direkam; DUR masih perkiraan.\n\n'%(n,title,words)+'\n\n'.join('Babak %d: %s'%(i+1,s) for i,s in enumerate(naskah))+'\n',encoding='utf-8')
    bpy.context.scene.render.filepath='//render/frames/ep%d_'%n
    bpy.ops.wm.save_mainfile()
    if render:render_tests(n,only)
    print('EPISODE',n,'DURATION',bpy.context.scene.frame_end/12,'FILE',str(fp))
def patch_ep(n,reps,only=None):
    src=bpy.data.texts['anim_ep%d'%n].as_string()
    for a,b in reps:
        assert a in src,a[:60];src=src.replace(a,b)
    run_ep(n,src,only=only)
