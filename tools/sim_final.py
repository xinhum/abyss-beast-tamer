import random, statistics
BOSS=[5,10,15]
STEP={1:1.10,2:1.38,3:1.99}   # 配对后的敌人阶段基准
KMAP={1:2,2:2,3:3,4:3,5:1,6:3,7:3,8:4,9:4,10:1,11:3,12:3,13:4,14:4,15:1}
def ph(n): return 1 if n<=5 else 2 if n<=10 else 3
Q={1:1.4,2:1.6,3:2.1}; MULT=2.925
def bp(n): return 1 if 6<=n<=10 else 2 if n>=11 else 0
HPB,ATB=223,45; AFFIX=0.10; BOSS_MULT=2.0; BOSS_ATK=1.2
random.seed(11); rows=[]
for n in range(1,16):
    s=STEP[ph(n)]; k=KMAP[n]; q=Q[ph(n)]
    dps=12*q*MULT*(1+AFFIX*bp(n)); pool=3*120*q+1200
    hpE0=HPB*s*(BOSS_MULT if n in BOSS else 1.0); atkE=ATB*s*(BOSS_ATK if n in BOSS else 1.0)
    ttks=[];wins=0
    for _ in range(3000):
        hpE=hpE0;hpP=pool;r=0
        while hpE>0 and hpP>0 and r<80:
            r+=1; hpE-=dps*random.uniform(.95,1.05); hpP-=atkE*random.uniform(.95,1.05)
        ttks.append(r)
        if hpE<=0 and hpP>0: wins+=1
    ttks.sort(); rows.append((n,round(s,2),k,round(hpE0),round(atkE),round(dps),round(statistics.mean(ttks),1),ttks[int(.1*3000)],ttks[int(.9*3000)],round(100*wins/3000,1)))
print('层| S |敌数|敌总HP|敌ATK|玩家DPS|均TTK|P10|P90|胜%')
for r in rows: print('%2d|%.2f|%d|%5d|%4d|%4.0f|%4.1f|%2d|%2d|%4.1f'%r)
print('\n普通战TTK区间:', min(r[6] for r in rows if r[0] not in BOSS), '-', max(r[6] for r in rows if r[0] not in BOSS))
print('Boss TTK:', [ (r[0],r[6]) for r in rows if r[0] in BOSS])
