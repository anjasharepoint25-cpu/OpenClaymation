DUR=[14.5,14.5,14.5,14.5,14.5,14.5]  # Perkiraan; ganti dengan durasi audio asli per babak.
import bpy
exec(compile(bpy.data.texts['anim_lib'].as_string(),'anim_lib','exec'))
setup(1,2)
scene(0,'SEBELUM DUNIA: GINNUNGAGAP',[
    ('IceLand',-1.20,.20,.75),('FireLand',1.20,.20,.75)],'night')
pop('Mist',fr(0,.35),k=.70,loc=(0,.2,.15))
K('IceLand',fr(0,.80),loc=(-.8,.2,0));K('FireLand',fr(0,.80),loc=(.8,.2,0))
scene(1,'ES + PANAS = KEHIDUPAN',[
    ('IceLand',-1.25,.35,.7),('FireLand',1.25,.35,.7),('Mist',0,0,.65)],'fire')
K('IceLand',fr(1,.35),s=.35);hide('Mist',fr(1,.50));pop('Ymir',fr(1,.50),k=1.03,loc=(0,.1,0))
headto('Ymir',fr(1,.65),(0,0,-18));armsto('Ymir',fr(1,.72),(0,45,0),(0,-45,0))
scene(2,'YMIR DAN SAPI AUDHUMLA',[
    ('Ymir',-.95,.55,.86),('Audhumla',.75,-.25,.95),('IceBlock',-.20,-.42,.65)],'ice')
K('Audhumla',fr(2,.18),rot=(0,-8,0));K('Audhumla',fr(2,.35),rot=(0,4,0));K('Audhumla',fr(2,.52),rot=(0,-8,0));K('Audhumla',fr(2,.7),rot=(0,0,0))
headto('Ymir',fr(2,.30),(0,0,-22));armsto('Ymir',fr(2,.35),ar=(0,-65,0))
scene(3,'DARI ES: BURI DAN KETURUNANNYA',[
    ('IceBlock',-1.1,.2,.85),('Buri',-1.1,.23,.55)],'ice')
K('IceBlock',fr(3,.28),s=.60);K('IceBlock',fr(3,.45),s=.30);hide('IceBlock',fr(3,.6))
K('Buri',fr(3,.60),s=.84)
pop('OdinYoung',fr(3,.67),k=.61,loc=(-.15,0,0));pop('Vili',fr(3,.72),k=.61,loc=(.70,0,0));pop('Ve',fr(3,.77),k=.61,loc=(1.5,0,0))
scene(4,'TUBUH YMIR MENJADI DUNIA',[
    ('Ymir',0,.8,1),('OdinYoung',-1.4,-.25,.65),('Vili',-.45,-.55,.65),('Ve',.65,-.55,.65)],'night')
armsto('OdinYoung',fr(4,.18),ar=(0,-100,0));armsto('Vili',fr(4,.18),(0,85,0),(0,-85,0));armsto('Ve',fr(4,.18),al=(0,100,0))
K('Ymir',fr(4,.36),s=.80);hide('Ymir',fr(4,.48))
pop('WorldSea',fr(4,.49),k=1,loc=(0,.7,0));pop('WorldEarth',fr(4,.56),k=.95,loc=(0,.7,.13));pop('Mountains',fr(4,.68),k=.85,loc=(0,.65,.3))
scene(5,'LANGIT, CAHAYA, DAN MIDGARD',[
    ('WorldSea',0,.1,1),('WorldEarth',0,.1,.95),('Mountains',0,.30,.85),('SkyArc',0,.6,1)],'finale')
pop('Stars',fr(5,.18),k=1,loc=(0,.4,.25));pop('SunMoon',fr(5,.32),k=.65,loc=(0,.2,1.7))
for n in ['WorldSea','WorldEarth','Mountains','SkyArc','Stars','SunMoon']:hide(n,fr(5,.66))
pop('Yggdrasil',fr(5,.68),k=.65,loc=(0,.3,0))
ending();finish()
TESTS=tests((0,.65),(1,.3),(1,.75),(2,.45),(3,.35),(3,.86),(4,.28),(4,.80),(5,.45))
