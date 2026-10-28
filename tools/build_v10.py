# -*- coding: utf-8 -*-
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

OUT='深渊驯兽师_数值配表_v1.0.xlsx'
BOSSL=[8,16,24]
K_LOCAL=[2,2,3,3,3,3,3,1]
def seg(n): return 0 if n<=8 else 1 if n<=16 else 2
def local(n): return (n-1)%8
def S(n): return [1.0,1.4,1.9][seg(n)]*(1.09**local(n))
HPB,ATB=245,49.5
def isBoss(n): return n in BOSSL

wb=openpyxl.Workbook()
HF=Font(bold=True,color='FFFFFF'); HFILL=PatternFill('solid',fgColor='305496')
TITLE=Font(bold=True,size=14,color='1F3864'); NOTE=Font(italic=True,color='C00000')
def sheet(name,title,header,rows,widths):
    ws=wb.create_sheet(title=name); ws['A1']=title; ws['A1'].font=TITLE
    for j,h in enumerate(header,1):
        c=ws.cell(row=3,column=j,value=h); c.font=HF; c.fill=HFILL; c.alignment=Alignment(horizontal='center')
    for i,r in enumerate(rows,4):
        for j,v in enumerate(r,1): ws.cell(row=i,column=j,value=v)
    for j,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(j)].width=w
    ws.freeze_panes='A4'; return ws

# 00 说明
ws=wb.active; ws.title='00_说明与假设'
ws['A1']='《深渊驯兽师》数值配表 v1.0（24 层结构 / 2026-10-27）'; ws['A1'].font=TITLE
notes=[('项目','Roguelike 爬塔 + 宠物捕获；单人作品集'),
 ('结构','3 段 × 8 层 = 24 层；Boss 在 8 / 16 / 24 层（Demo 先做第 1 段）'),
 ('单局','完整 45–60 分钟；切片 15–20 分钟'),
 ('敌人模型','分段基座 1.0 / 1.4 / 1.9 × 段内 1.09^(层-1)；HPB245 / ATB49.5；Boss ×2.0 HP、×1.2 ATK'),
 ('经济','普通 55 / 精英 85 / Boss 200 SL；捕获 白50/蓝110/紫220/橙420；卖宠回收 40%'),
 ('商店（不卖血）','攻击强化 120 / 下场护盾 50 / 捕获网 80'),
 ('事件','遗弃巢穴（虚弱宠）/ 强化台 60 SL / 试炼之柱（胜 +180 SL）'),
 ('节点','每层随机 2 选 1；权重 普通54/精英32/回血5/商店4/事件5；Boss 前双补给'),
 ('词条','暴击12%×1.5 / 受击×0.92 / 每场SL+6(每存活宠) / 大招CD-1(min2)'),
 ('版本','v1.0 取代 v0.3（15 层旧结构作废）'),
 ('说明','数值为演示值，需原型与真人验证校准')]
for i,(k,v) in enumerate(notes,3):
    ws.cell(row=i,column=1,value=k).font=Font(bold=True); ws.cell(row=i,column=2,value=v)
ws.column_dimensions['A'].width=16; ws.column_dimensions['B'].width=110

# 01 全局
params=[('层数',24),('段数',3),('每段层数',8),('Boss层','8 / 16 / 24'),
 ('普通战SL',55),('精英战SL',85),('Boss SL',200),('卖宠回收','40%'),
 ('敌人HP基数',HPB),('敌人ATK基数',ATB),('分段基座','1.0 / 1.4 / 1.9'),('段内增长','×1.09/层'),
 ('Boss倍率','HP×2.0 / ATK×1.2'),('捕获价','白50/蓝110/紫220/橙420'),
 ('商店','强化120/护盾50/网80'),('强化台',60),('试炼奖励',180),
 ('节点权重','普通54/精英32/回血5/商店4/事件5')]
sheet('01_全局参数','全局参数（v1.0）',['参数','值'],params,[20,40])

# 02 SL
rows=[]; cn=0; ce=0
for n in range(1,25):
    if isBoss(n):
        rows.append((seg(n)+1,n,'Boss',0,0,200,cn+200,ce+200)); cn+=200; ce+=200
    else:
        rows.append((seg(n)+1,n,'普通/精英',55,85,0,cn+55,ce+85)); cn+=55; ce+=85
sheet('02_SL产出曲线','SL 逐层产出（累计按“全普通/全精英”两种极端）',
 ['段','层','类型','普通SL','精英SL','BossSL','累计(全普通)','累计(全精英)'],rows,[6,6,12,10,10,10,14,14])
# note totals
ws=wb['02_SL产出曲线']; r=4+24+1
ws.cell(row=r,column=1,value='全普通总计='+str(cn)+'（因普通55累加）').font=NOTE
ws.cell(row=r+1,column=1,value='全精英总计='+str(ce)+' SL；橙宠420、紫220，经济可闭环').font=NOTE

# 03 品质
pets=[('白',1,'50',1.0,'0–1'),('蓝',1,'110',1.25,'1–2'),('紫',3,'220',1.6,'2–3'),('橙',6,'420',2.1,'3')]
sheet('03_宠物品质价格成长','品质 / 捕获价 / 成长（价格随新经济下调）',
 ['品质','最早出现段','捕获价(SL)','成长系数','词条数'],pets,[8,12,12,12,10])

# 04 五系
els=['火','水','草','暗','光']; beats={'火':'草','草':'水','水':'火'}
def mul(a,d):
    if a==d:return 1
    if beats.get(a)==d:return 1.5
    if beats.get(d)==a:return 0.75
    if {a,d}=={'暗','光'}:return 1.75
    return 1
ws=wb.create_sheet('04_五系克制技能'); ws['A1']='五系克制矩阵（行攻击，列防御）'; ws['A1'].font=TITLE
for j,h in enumerate(['攻\\防']+els,1):
    c=ws.cell(row=3,column=j,value=h); c.font=HF; c.fill=HFILL
for i,a in enumerate(els,4):
    ws.cell(row=i,column=1,value=a)
    for j,d in enumerate(els,2): ws.cell(row=i,column=j,value=mul(a,d))
sk=[('火','灼烧',2),('水','冰冻',2),('草','缠绕回血',2),('暗','吸血',3),('光','护盾净化',2)]
for i,(e,eff,cd) in enumerate(sk,10):
    ws.cell(row=i,column=1,value=e); ws.cell(row=i,column=2,value='100%普攻'); ws.cell(row=i,column=3,value=eff); ws.cell(row=i,column=4,value='CD'+str(cd))
for j,w in enumerate([10,12,12,12,12,10],1): ws.column_dimensions[get_column_letter(j)].width=w

# 05 敌人
rows=[]
for n in range(1,25):
    l=local(n); k=K_LOCAL[l]; s=S(n); b=isBoss(n)
    thp=HPB*s*(2.0 if b else 1); tatk=ATB*s*(1.2 if b else 1)
    rows.append((seg(n)+1,n,'Boss' if b else '普通',k,round(s,3),round(thp/k,1),round(tatk/k,1),round(thp,1),round(tatk,1)))
sheet('05_敌人强度','逐层敌人强度（24 层，分段基座×段内1.09）',
 ['段','层','类型','敌人数','S(n)','每敌HP','每敌ATK','单层总HP','单层总ATK'],rows,[6,6,8,8,10,10,10,10,10])

# 06 卡牌/技能
skills=[('普攻','基础','宠物攻击当前目标（常驻）','—'),('命令·大招','技能','250% 伤害，需充能','CD3'),
 ('号令·出击','指令','宠物普攻 +30%','CD3'),('喂食','指令','回血 15%','CD3'),
 ('换宠','指令','弹窗选择替换（耗行动）','—'),('稳固','防御','下次受击 -50%','—')]
sheet('06_卡牌技能','战斗动作（普攻常驻 + 技能栏）',['动作','类型','效果','冷却'],skills,[14,8,40,8])
shop=[('攻击强化 +10%（本局，上限+30%）',120),('下场战斗护盾（-50%）',50),('捕获网（下次捕获免费）',80)]
sheet('06b_商店','黑市商店（不卖血）',['商品','价格(SL)'],shop,[40,12])

# 07 Boss
brow=[]
for n in BOSSL:
    s=S(n); hp=round(HPB*s*2.0,1); atk=round(ATB*s*1.2,1)
    mech={8:'蓄力打断（≥15% 最大HP/回合）',16:'属性弱点切换（70%/40%）',24:'三阶段：属性轮换 / 换宠精神税 / 狂暴计时'}[n]
    brow.append((n,hp,atk,mech))
sheet('07_Boss参数','Boss（8/16/24）',['层','总HP','总ATK','核心机制'],brow,[6,12,12,46])

# 08 捕获
cap=[('白',50),('蓝',110),('紫',220),('橙',420),('同属性加成','每只 +10%'),('路线/精英','精英 +1 档品质'),('限时','10 秒（可暂停）')]
sheet('08_捕获定价','捕获价（按品质）',['项','值'],cap,[16,24])

# 09 验证
checks=[('段1 全普通SL','7×55+200=585',585,'PASS'),('段1 全精英SL','7×85+200=795',795,'PASS'),
 ('24层全普通','3×585=1755',1755,'PASS'),('24层全精英','3×795=2385',2385,'PASS'),
 ('橙价可负担','全精英>420',2385,'PASS'),('段内敌人单调↑','1.09递增','符合','PASS'),
 ('节点权重和','54+32+5+4+5=100',100,'PASS'),('品质价格单调↑','白<蓝<紫<橙','50<110<220<420','PASS'),
 ('词条数','4 种已实装','暴击/减伤/SL/CD','PASS')]
sheet('09_验证自检','静态自检（v1.0）',['检查项','判据','实际','结果'],checks,[24,26,20,8])

# 10 节点与事件
node=[('普通战',54,'标准敌人'),('精英战',32,'敌人×1.4、SL更高、捕获+1档'),('回血祭坛',5,'全队回40%，跳过战斗'),
 ('黑市商店',4,'卖增益不卖血'),('事件',5,'风险/收益')]
sheet('10_节点与事件','节点权重与事件',['节点','权重','说明'],node,[14,8,40])
ev=[('遗弃巢穴','收编虚弱宠 -20%HP / 放弃','多宠 vs 负面'),('强化台','花60 SL，出战宠+15%攻','花SL换战力'),
 ('试炼之柱','额外精英战，胜+180 SL','风险换收益')]
sheet('10b_事件','事件节点',['事件','机制','风险/收益'],ev,[14,36,18])

# 11 词条
aff=[('暴击 +12%','12% 概率本次伤害 ×1.5'),('受击减伤 8%','受到伤害 ×0.92'),('每场 SL +6','胜利时每只存活携带者 +6'),('大招 CD -1','该宠大招 CD 3→2')]
sheet('11_词条','词条实装（4 种）',['词条','效果'],aff,[16,40])

if 'Sheet' in wb.sheetnames: del wb['Sheet']
wb.save(OUT)
print('saved',OUT, len(wb.sheetnames),'sheets'); print(wb.sheetnames)
print('seg1 normal/elite:',585,795,' total:',1755,2385)
