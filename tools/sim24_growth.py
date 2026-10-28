import random, statistics
random.seed(11)
BOSSL={8,16,24}; K=[2,2,3,3,3,3,3,1]
QC={'白':1.0,'蓝':1.25,'紫':1.6,'橙':2.1}; RANK={'白':0,'蓝':1,'紫':2,'橙':3}
def seg(n): return 0 if n<=8 else 1 if n<=16 else 2
def local(n): return (n-1)%8
def mk(q): c=QC[q]; return {'q':q,'atk':62*c,'hp':600*c,'max':600*c}
def grow(team,ap,hp):
    for p in team:
        p['atk']=round(p['atk']*(1+ap)); p['max']=round(p['max']*(1+hp)); p['hp']=min(p['max'],round(p['hp']*(1+hp)))
def heal(team,r):
    for p in team:
        if p['hp']>0: p['hp']=min(p['max'],p['hp']+p['max']*r)
def alivehp(t): return sum(p['hp'] for p in t if p['hp']>0)
def dmg(t,d):
    for p in t:
        if d<=0:break
        if p['hp']>0:
            x=min(p['hp'],d);p['hp']-=x;d-=x
# pity node gen
def gen(layer, since):
    if local(layer)==6: return ['heal','shop'],0
    chance=min(0.30,0.06+0.03*since)
    out=[]
    for _ in range(2):
        if random.random()<chance: out.append(random.choice(['heal','shop','event']))
        else: out.append(random.choice(['normal','elite']))
    # distinct-ish
    if out[0]==out[1] and out[0] in ('normal','elite'): out[1]='elite' if out[0]=='normal' else 'normal'
    has=any(x in ('heal','shop','event') for x in out)
    return out,(0 if has else since+1)
def play(HPB,ATB,bossG,affixP,eventGrow,healR):
    def S(n): return [1.0,1.4,1.9][seg(n)]*(1.09**local(n))
    team=[mk('白')]; active=0; sl=80; buff=0.0; since=0; tn=[]; tb={}
    for n in range(1,25):
        opts,since=gen(n,since); hp=alivehp(team); mx=sum(p['max'] for p in team)
        if local(n)==6: pickn=('heal' if hp<mx*0.6 else 'shop')
        else:
            if hp<mx*0.4 and 'heal' in opts: pickn='heal'
            elif hp<mx*0.4 and 'shop' in opts: pickn='shop'
            elif 'elite' in opts and hp>mx*0.6: pickn='elite'
            elif 'normal' in opts: pickn='normal'
            else: pickn=opts[0]
        if pickn=='heal': heal(team,0.4); continue
        if pickn=='shop':
            if sl>=120: sl-=120; buff=min(0.3,buff+0.1)
            continue
        if pickn=='event':
            if eventGrow and random.random()<0.5: grow(team,0.08,0.08)
            elif sl>=60: sl-=60; team[active]['atk']=round(team[active]['atk']*1.15)
            continue
        elite=(pickn=='elite'); boss=n in BOSSL
        thp=HPB*S(n)*(2.0 if boss else 1)*(1.4 if elite else 1)
        tatk=ATB*S(n)*(1.2 if boss else 1)*(1.4 if elite else 1)
        dps=team[active]['atk']*1.5*1.2*(1+buff); pool=alivehp(team); r=0
        while thp>0 and pool>0 and r<60: r+=1; thp-=dps; pool-=tatk
        if thp>0: return False,n,tn,tb
        dmg(team,tatk*r)
        if alivehp(team)<=0: return False,n,tn,tb
        if boss: tb[n]=r
        else: tn.append(r)
        sl+=(200 if boss else (85 if elite else 55))
        if boss:
            grow(team,bossG,bossG); grow(team,affixP,affixP); heal(team,healR)
        best=max(RANK[p['q']] for p in team if p['hp']>0)
        if sl>=220 and best<2:
            sl-=220; team[min(range(len(team)),key=lambda i:RANK[team[i]['q']])]=mk('紫')
        elif sl>=110 and best<1:
            sl-=110
            if len(team)<3: team.append(mk('蓝'))
            else: team[min(range(len(team)),key=lambda i:RANK[team[i]['q']])]=mk('蓝')
        alive=[i for i,p in enumerate(team) if p['hp']>0]
        if not alive: return False,n,tn,tb
        active=max(alive,key=lambda i:team[i]['hp'])
    return True,24,tn,tb
def run(name,*a,N=800):
    wins=0; allttk=[]; bt={8:[],16:[],24:[]}
    for _ in range(N):
        w,l,tn,tb=play(*a)
        if w:wins+=1
        allttk+=tn
        for b in (8,16,24):
            if b in tb: bt[b].append(tb[b])
    print('%s: 通关%.0f%% 普通TTK%.1f Boss8=%.1f Boss16=%.1f Boss24=%.1f'%(
      name,wins/N*100, statistics.mean(allttk) if allttk else 0,
      statistics.mean(bt[8]) if bt[8] else 0, statistics.mean(bt[16]) if bt[16] else 0, statistics.mean(bt[24]) if bt[24] else 0))
# 方案一：+10%全局 + 12%词条，无击杀成长
run('方案一(+10%/词条12%)',245,49.5,0.10,0.12,False,0.5)
# 方案二：+6%全局 + 12%词条 + 事件成长8%
run('方案二(+6%/词条12%/事件8%)',245,49.5,0.06,0.12,True,0.5)
# 结合：+8%全局 + 12%词条 + 事件8%
run('结合(+8%/词条12%/事件8%)',245,49.5,0.08,0.12,True,0.5)
