import bpy, math, random
from mathutils import Vector
D=bpy.data.objects; sc=bpy.context.scene; FPS=12; GAP=.45
ST=[.5]
for dur in DUR[:-1]: ST.append(ST[-1]+dur+GAP)
END=ST[-1]+DUR[-1]+1.5; LAST=round(END*FPS)
sc.frame_start=1; sc.frame_end=LAST; sc.render.fps=FPS
sc['narration_starts_seconds']=ST;sc['narration_duration_estimates']=DUR
def fr(i,u): return round((ST[i]+DUR[i]*u)*FPS)+1
CUT=[1]+[round((ST[i]-.20)*FPS)+1 for i in range(1,6)]
for idb in list(D)+list(bpy.data.lights)+list(bpy.data.cameras):
    if idb.animation_data: idb.animation_data_clear()
bd=bpy.data.materials['backdrop'].node_tree
if bd.animation_data: bd.animation_data_clear()
prefs=bpy.context.preferences.edit
prefs.keyframe_new_interpolation_type='BEZIER'
HID=(.001,)*3; ONE=(1,1,1); last={}; C={}
ASSETS=[o for o in D if o.get('asset')]
CURRENT_MOOD='ice'
def K(o,f,loc=None,rot=None,s=None):
    if isinstance(o,str): o=D[o]
    st=last.setdefault(o.name,[tuple(o.location),tuple(math.degrees(a) for a in o.rotation_euler),tuple(o.scale)])
    if loc is not None: st[0]=tuple(loc)
    if rot is not None: st[1]=tuple(rot)
    if s is not None: st[2]=(s,s,s) if isinstance(s,(int,float)) else tuple(s)
    o.location=st[0];o.rotation_euler=[math.radians(a) for a in st[1]];o.scale=st[2]
    for p in ['location','rotation_euler','scale']:o.keyframe_insert(p,frame=max(1,f))
def cut(o,f,**kw): K(o,f-1);K(o,f,**kw)
def show(o,f,**kw):
    s=kw.pop('s',1);cut(o,f,s=s,**kw)
def hide(o,f):cut(o,f,s=HID)
def pop(o,f,k=1,**kw):
    K(o,f-1,s=HID,**kw);K(o,f,s=.25*k);K(o,f+3,s=(1.08*k,1.08*k,1.13*k));K(o,f+6,s=k)
def place(o,f,x,y=0,rot=0,s=1):cut(o,f,loc=(x,y,0),rot=(0,0,rot),s=s)
def hop(o,f,x,y=0,n=4,h=.30):
    if isinstance(o,str):o=D[o]
    a=last[o.name][0];K(o,f);K(o,f+n,loc=((a[0]+x)/2,(a[1]+y)/2,a[2]+h));K(o,f+2*n,loc=(x,y,a[2]))
def jump(o,f,h=.28,n=3):
    if isinstance(o,str):o=D[o]
    a=last[o.name][0];K(o,f);K(o,f+n,loc=(a[0],a[1],a[2]+h));K(o,f+2*n,loc=a)
def walk(o,f0,f1,x1,y1=0,h=.15):
    if isinstance(o,str):o=D[o]
    x0,y0,_=last[o.name][0];n=max(1,(f1-f0)//8)
    for j in range(n):hop(o,f0+j*8,x0+(x1-x0)*(j+1)/n,y0+(y1-y0)*(j+1)/n,n=4,h=h)
def armsto(n,f,al=None,ar=None,d=5):
    for k,r in [('AL',al),('AR',ar)]:
        if r is not None:K(C[n+k],f);K(C[n+k],f+d,rot=r)
def headto(n,f,rot,d=4):K(C[n+'H'],f);K(C[n+'H'],f+d,rot=rot)
def reset(n,f):
    for k in ['AL','AR','H']:cut(C[n+k],f,rot=(0,0,0))
def parts(n,token,f,s=1):
    for ch in D[n].children_recursive:
        if token in ch.name:
            if ch.name not in last:K(ch,1,s=1)
            cut(ch,f,s=s)
def wave(n,f,reps=3):
    for j in range(reps):K(C[n+'AR'],f+j*8,rot=(0,-145,0));K(C[n+'AR'],f+j*8+4,rot=(0,-110,0))
def cheer(n,f):armsto(n,f,(0,140,0),(0,-140,0))
def shakehead(n,f,reps=2):
    for j in range(reps):K(C[n+'H'],f+j*8,rot=(0,0,20));K(C[n+'H'],f+j*8+4,rot=(0,0,-20))
    K(C[n+'H'],f+reps*8,rot=(0,0,0))
cam=D['Cam'];foc=D['Focus']
def CK(f,loc,tgt,lens):
    cam.location=loc;cam.rotation_euler=(Vector(tgt)-Vector(loc)).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens
    for p in ['location','rotation_euler']:cam.keyframe_insert(p,frame=f)
    cam.data.keyframe_insert('lens',frame=f);foc.location=tgt;foc.keyframe_insert('location',frame=f)
def shake(f,loc=(0,-9.8,3.2),tgt=(0,0,1.45),lens=35):
    for j,x in enumerate([0,.07,-.07,.04,0]):CK(f+j,(loc[0]+x,loc[1],loc[2]),tgt,lens)
MOOD={'ice':(800,220,950,450,(.012,.04,.10,1),(.045,.18,.28,1),(.20,.40,.46,1)),
      'fire':(800,160,1100,250,(.025,.012,.04,1),(.23,.055,.03,1),(.45,.16,.04,1)),
      'night':(500,170,1000,220,(.004,.012,.04,1),(.02,.07,.15,1),(.05,.16,.25,1)),
      'forest':(900,220,950,450,(.008,.035,.05,1),(.03,.14,.15,1),(.16,.32,.26,1)),
      'finale':(1000,260,900,500,(.015,.065,.10,1),(.055,.22,.30,1),(.28,.48,.43,1))}
def mood(f,name):
    v=MOOD[name]
    for n,e in zip(['Key','Fill','Rim','Back'],v[:4]):
        d=bpy.data.lights.get(n)
        if d:d.energy=e;d.keyframe_insert('energy',frame=f)
    ramp=next(n for n in bd.nodes if n.type=='VALTORGB')
    for i,e in enumerate(ramp.color_ramp.elements):e.color=v[4+min(i,2)];e.keyframe_insert('color',frame=f)
def moods(seq):
    prev=None
    for f,n in seq:
        if prev:mood(f-1,prev)
        mood(f,n);prev=n
def text_obj(name,body,y,size):
    o=D.get(name)
    if o is None:
        c=bpy.data.curves.new(name,'FONT');o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o)
    o.parent=cam;o.location=(0,y,-6.8);o.rotation_euler=(0,0,0);o.scale=ONE;o.hide_render=False
    o.data.body=body;o.data.size=size;o.data.align_x='CENTER';o.data.extrude=.001
    mat=bpy.data.materials['NordicLettering']
    if name in ['T_end','T_next']:
        mat=bpy.data.materials.get('NordicEndInk') or mat.copy();mat.name='NordicEndInk'
        bs=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
        bs.inputs['Base Color'].default_value=(.008,.025,.06,1)
        bs.inputs['Emission Color'].default_value=(.008,.025,.06,1);bs.inputs['Emission Strength'].default_value=.25
    o.data.materials.clear();o.data.materials.append(mat)
    return o
def setup(ep,nxt=None):
    sc.render.resolution_x=1080;sc.render.resolution_y=1920;sc.render.resolution_percentage=100
    sc.cycles.samples=64;sc.cycles.use_denoising=True;sc.render.image_settings.file_format='PNG'
    sc.camera=cam;cam.data.dof.use_dof=False
    CK(1,(0,-8.8,3.1),(0,0,1.45),43);CK(LAST,(0,-8.8,3.1),(0,0,1.45),43)
    for o in ASSETS:
        K(o,1,loc=(0,0,0),rot=(0,0,0),s=HID)
        if o.get('kind')=='person':
            for k in ['H','AL','AR']:
                p=D.get(o.name+'_'+k+'piv')
                if p:C[o.name+k]=p;K(p,1,rot=(0,0,0),s=1)
    for o in list(D):
        if o.type=='FONT' and o.parent==cam:K(o,1,s=HID)
    for n,b,y,s in [('T_title','MITOS NORDIK',2.30,.20),('T_101','101',1.98,.26),('T_ep','EPISODE '+str(ep),1.72,.12),('T_end','BERSAMBUNG...' if nxt else 'TAMAT',-1.65,.20),('T_next','EPISODE '+str(nxt) if nxt else 'MITOS NORDIK 101',-1.94,.12)]:
        o=text_obj(n,b,y,s);K(o,1,s=HID)
    for n,f in [('T_title',4),('T_101',9),('T_ep',15)]:pop(D[n],f);hide(D[n],fr(0,.30))
    D['Benben_mound'].scale=(2.2,2.2,1);D['Benben_mound'].location=(0,0,-.42)
    for n in ['IceStone0','IceStone1','IceStone2']:D[n].hide_render=True
def scene(i,caption,items,look='ice'):
    global CURRENT_MOOD
    f=CUT[i]
    present={item[0] for item in items}
    for o in ASSETS:
        if o.name not in present:hide(o,f)
        if o.get('kind')=='person':reset(o.name,f)
    for j in range(6):
        o=D.get('SceneCaption'+str(j))
        if o:hide(o,f)
    for item in items:
        n,x,y,s,*angle=item;place(n,f,x,y,rot=angle[0] if angle else 0,s=s)
    o=text_obj('SceneCaption'+str(i),caption,1.35,.135);K(o,1,s=HID);show(o,f)
    mood(max(1,f-1),CURRENT_MOOD);mood(f,look);CURRENT_MOOD=look
    return f
def ending(u1=.82,u2=.91):
    mood(fr(5,u1),'finale');pop(D['T_end'],fr(5,u1));pop(D['T_next'],fr(5,u2))
def set_interpolation(o,mode):
    a=o.animation_data.action
    if hasattr(a,'fcurves'):curves=list(a.fcurves)
    else:
        curves=[c for layer in a.layers for strip in layer.strips for bag in strip.channelbags for c in bag.fcurves]
    for c in curves:
        for p in c.keyframe_points:p.interpolation=mode
def finish():
    prefs.keyframe_new_interpolation_type='CONSTANT';random.seed(4)
    for f in range(1,LAST+1,3):
        D['BoilCtl'].location=tuple(random.uniform(-.03,.03) for _ in range(3));D['BoilCtl'].keyframe_insert('location',frame=f)
    prefs.keyframe_new_interpolation_type='LINEAR'
    D['WaveCtl'].location=(0,0,0);D['WaveCtl'].keyframe_insert('location',frame=1)
    D['WaveCtl'].location=(1.5,.8,3.2);D['WaveCtl'].keyframe_insert('location',frame=LAST)
    # Scripted insertion in Blender 5 can ignore the UI interpolation preference.
    set_interpolation(D['BoilCtl'],'CONSTANT');set_interpolation(D['WaveCtl'],'LINEAR')
    prefs.keyframe_new_interpolation_type='BEZIER';sc.frame_set(1)
def tests(*us):return [30]+[fr(i,u) for i,u in us]+[LAST-5]
