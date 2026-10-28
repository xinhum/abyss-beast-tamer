import random, statistics
random.seed(2026)
HPB,ATB=245,49.5
K=[2,2,3,3,3,3,3,1]
BOSSL={8,16,24}
def seg(n): return 0 if n<=8 else 1 if n<=16 else 2
def local(n): return (n-1)%8
def S(n): return [1.0,1.4,1.9][seg(n)]*(1.09**local(n))
QC={'白':1.0,'蓝':1.25,'紫':1.6,'橙':2.1}; RANK={'白':0,'蓝':1,'紫':2,'橙':3}
PRICE={'白':50,'蓝':110,'紫':220,'橙':420}
def mk(q,el='火'): c=QC[q]; return {'q':q,'el':el,'atk':62*c,'hp':600*c,'max':600*c}
W=[('normal',54),('elite',32),('heal',5),('shop',4),('event',5)]
def draw():
    tot=sum(w for _,w in W); r=random.random()*tot
    for k,w in W:
        r-=w
        if r<=0: return k
    return 'normal'
def gen(layer):
    if local(layer)==6: return ['heal','shop']
    a=draw(); b=draw(); g=0
    while b==a and g<20: b=draw(); g+=1
    return [a,b]
def alivehp(team): return sum(p['hp'] for p in team if p['hp']>0)
def apply_dmg(team,d):
    for p in team:
        if d<=0: break
        if p['hp']>0:
            x=min(p['hp'],d); p['hp']-=x; d-=x
def play():
    team=[mk('白')]; active=0; sl=80; buff=0.0
    slat={}; ttk_norm=[]; ttk_boss={}
    for n in range(1,25):
        opts=gen(n)
        hp=alivehp(team); maxhp=sum(p['max'] for p in team)
        # bot choose
        pickn=None
        if local(n)==6:
            pickn = 'heal' if hp<maxhp*0.6 else 'shop'
        else:
            if hp<maxhp*0.4 and ('heal' in opts): pickn='heal'
            elif hp<maxhp*0.4 and ('shop' in opts): pickn='shop'
            elif 'elite' in opts and hp>maxhp*0.6: pickn='elite'
            elif 'normal' in opts: pickn='normal'
            else: pickn=opts[0]
        if pickn=='heal':
            for p in team:
                if p['hp']>0: p['hp']=min(p['max'],p['hp']+p['max']*0.4)
            continue
        if pickn=='shop':
            if sl>=120: sl-=120; buff=min(0.3,buff+0.1)
            continue
        if pickn=='event':
            if sl>=60: sl-=60; team[active]['atk']=round(team[active]['atk']*1.15)
            continue
        # battle
        elite = (pickn=='elite'); boss= n in BOSSL
        k=1 if boss else K[local(n)]
        thp=HPB*S(n)*(2.0 if boss else 1)*(1.4 if elite else 1)
        tatk=ATB*S(n)*(1.2 if boss else 1)*(1.4 if elite else 1)
        dps=team[active]['atk']*1.5*1.2*(1+buff)
        pool=alivehp(team); rounds=0
        while thp>0 and pool>0 and rounds<60:
            rounds+=1; thp-=dps; pool-=tatk
        if thp>0:
            return False,n,sl,slat,ttk_norm,ttk_boss   # died
        apply_dmg(team,tatk*rounds)
        if alivehp(team)<=0: return False,n,sl,slat,ttk_norm,ttk_boss
        if boss: ttk_boss[n]=rounds
        else: ttk_norm.append(rounds)
        sl += (200 if boss else (85 if elite else 55))
        if n in BOSSL: slat[n]=sl
        # capture upgrade
        best=max(RANK[p['q']] for p in team if p['hp']>0)
        if sl>=220 and best<2:
            sl-=220; idx=min(range(len(team)),key=lambda i:RANK[team[i]['q']])
            team[idx]=mk('紫'); active=0
        elif sl>=110 and best<1:
            sl-=110
            if len(team)<3: team.append(mk('蓝'))
            else:
                idx=min(range(len(team)),key=lambda i:RANK[team[i]['q']]); team[idx]=mk('蓝'); active=0
        # active = highest hp pet
        alive=[i for i,p in enumerate(team) if p['hp']>0]
        if not alive: return False,n,sl,slat,ttk_norm,ttk_boss
        active=max(alive,key=lambda i:team[i]['hp'])
    return True,24,sl,slat,ttk_norm,ttk_boss
N=1000; wins=0; deaths={}; allttk=[]; bossttk={8:[],16:[],24:[]}; slat={8:[],16:[],24:[]}
for _ in range(N):
    w,layer,sl,slat_,tn,tb=play()
    if w: wins+=1
    else: deaths[seg(layer)+1]=deaths.get(seg(layer)+1,0)+1
    allttk+=tn
    for b in (8,16,24):
        if b in tb: bossttk[b].append(tb[b])
    for b in (8,16,24):
        if b in slat_: slat[b].append(slat_[b])
print('1000局 通关率: %.1f%%'%(wins/N*100))
print('死亡分布(按段):',deaths)
print('普通战TTK: 均%.1f  P10=%d P90=%d'%(statistics.mean(allttk),sorted(allttk)[int(.1*len(allttk))],sorted(allttk)[int(.9*len(allttk))]))
for b in (8,16,24):
    if bossttk[b]:
        print('Boss%d TTK: 均%.1f  到达%d次'%(b,statistics.mean(bossttk[b]),len(bossttk[b])))
    if slat[b]:
        print('  到Boss%d时SL: 均%.0f'%(b,statistics.mean(slat[b])))
