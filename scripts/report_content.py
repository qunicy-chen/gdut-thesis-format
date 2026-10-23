# -*- coding: utf-8 -*-
"""报告正文内容与文档组装(调用 build_report.py 中的工具函数)——精简版v2"""
import sys, json, re
from build_report import *

TOC_JSON = WORK + r'\toc_data.json'

# ============================================================
# 摘要与正文文本
# ============================================================
ABSTRACT_CN = (
    '针对高渗透率分布式光伏接入引起的低压配电网电压越限问题，本报告设计智能配电网光储协同的电压治理系统方案：'
    '基于电压降落纵分量公式解析\u201c光伏大发—末端电压抬升\u201d机理，对比两类调压资源特性并论证协同必要性；'
    '构建\u201c就地快速控制＋区域协同优化\u201d双层架构；依据GB/T 12325—2008的±7%限值划分三级电压档位，设计'
    '\u201c光伏无功优先→储能无功补充→储能有功兜底\u201d分档位递进式协同调压策略，嵌入储能SOC硬约束，覆盖过电压、'
    '欠电压与夜间全工况。典型低压居民台区的Matlab准稳态仿真表明：**无调压时末端电压最高1.081 pu、重度越限'
    '4.0 h；光储协同后极值收敛至1.050/0.951 pu，全天越限为零，波动率降约27%，SOC保持[0.400, 0.508]健康区间**。'
)
KEYWORDS_CN = '智能配电网；分布式光伏；储能系统；电压越限；协同控制'
ABSTRACT_EN = (
    'Addressing voltage violation in low-voltage distribution networks with high-penetration '
    'distributed photovoltaic (PV), this report designs a coordinated PV-storage voltage '
    'regulation scheme. The feeder-end voltage rise mechanism is revealed by the longitudinal '
    'voltage-drop formula, and a two-level architecture of local fast control plus regional '
    'coordinated optimization is constructed. According to the plus/minus 7% limit of '
    'GB/T 12325-2008, a three-level stepped strategy of PV reactive power first, storage '
    'reactive supplement and storage active backup is designed with hard SOC constraints. '
    'Simulation shows that the maximum voltage of 1.081 pu and 4.0 h severe violation are '
    'eliminated: extremes converge to 1.050/0.951 pu with zero daily violation.'
)
KEYWORDS_EN = 'smart distribution network; distributed photovoltaic; energy storage; voltage violation; coordinated control'

CH1 = [
    ('h2', '1.1 研究背景与意义'),
    ('p', '在\u201c双碳\u201d战略驱动下，分布式光伏快速发展，截至2024年底全国累计装机已超3.7亿kW[[2]]，其中大量'
          '接入380 V低压台区。低压配电网按辐射状单向潮流设计、电阻与电抗之比（R/X）大：正午光伏大发、负荷轻载时'
          '功率倒送，末端电压大幅抬升，极易超出GB/T 12325—2008规定的三相供电电压偏差±7%限值[[3]]；傍晚光伏退出又现末端欠电压。OLTC动作慢且影响'
          '寿命，电容器组只能分级发无功，难以适应光伏出力的快时变波动。智能电网以\u201c感知—通信—控制\u201d闭环将调压模式升级为**主动、快速、'
          '协同**[[1]]；而光伏并网逆变器与储能变流器（PCS）均为毫秒级电力电子接口，是台区最易获取、响应最快的'
          '调压资源。本报告据此研究光储协同的电压治理方案，并作为后续毕业设计的前置研究。'),
    ('h2', '1.2 国内外研究现状'),
    ('p', '国外形成两类技术路线：无功调压方面，分布式无功电压控制、逆变器无功调节能力比较与Q(U)下垂等本地控制'
          '被系统研究[[5-7]]；有功调压方面，Tonkoski等提出光伏有功缩减协调控制[[8]]。储能方面，储能与OLTC协调'
          '[[9]]、光伏—储能联合改善电压[[10]]、本地控制策略比较[[11]]、主动—无功最优潮流[[12]]与促进光伏消纳'
          '[[13]]等被广泛研究，计及电压约束的容量评估方法亦趋成熟[[14]]。国内王成山等[[4]]、尤毅等[[15]]论述了'
          '智能配电网与主动配电网的发展；GB/T 33593—2017[[16]]与GB/T 36547—2018[[17]]规定了分布式电源与储能'
          '并网技术要求。现有研究多针对单一资源或目标，就地与全局割裂、全工况覆盖不足，本报告据此开展协同方案设计。'),
    ('h2', '1.3 报告主要内容与结构安排'),
    ('p', '第2章推导电压越限机理并对比调压资源特性；第3章设计双层系统架构；第4章设计分档位递进式协同调压控制'
          '策略；第5章完成台区参数配置、储能选型与仿真验证；第6章总结全文并展望。'),
]

CH2 = [
    ('h2', '2.1 高渗透率分布式光伏并网电压越限机理分析'),
    ('p', '以辐射状低压馈线为对象：台变出口电压U_{1}，线路阻抗Z=R+jX，末端功率S=P+jQ。低压网首末端电压相角差'
          '很小，横分量影响可忽略[[18,19]]，电压降落纵分量与末端电压近似为式(2.1)、式(2.2)：'),
    ('f', '2.1'), ('f', '2.2'),
    ('p', '对式(2.2)分别关于P、Q求偏导，得电压灵敏度式(2.3)：'),
    ('f', '2.3'),
    ('p', '式(2.3)表明：R越大有功对电压影响越强，X越大无功影响越强。本台区主干线路R=0.088 6 Ω、X=0.028 Ω，'
          'R/X≈3.2，即**单位有功的调压效果约为无功的3.2倍，低压配电网电压具有\u201c有功敏感\u201d特性**。光伏'
          '接入末端后，净负荷P_{net}=P_{L}−P_{PV}随出力增大越过零点即功率倒送，式(2.2)中PR项变号。**\u201c光伏'
          '大发→末端电压升高\u201d的本质是：反向有功潮流在线路电阻上产生负的电压降落纵分量，使末端电压被抬升**；'
          '且大发时段逆变器剩余无功能力最小，形成\u201c调压需求最大而无功资源最紧张\u201d的固有矛盾。'),
    ('fig', FIGS + r'\fig_2_1.png', '图2.1 高渗透率分布式光伏接入下的馈线电压分布与末端电压—出力关系', 15.2),
    ('p', '图2.1(a)显示：无光伏时末端约0.965 pu，光伏出力189 kW时电压分布倒挂、末端达1.081 pu；图2.1(b)表明：'
          '**出力约139 kW（渗透率66%）触及1.05 pu，约172 kW（82%）越1.07 pu重度越限**——本台区装机已越过两级'
          '临界点，不治理必然越限。'),
    ('h2', '2.2 光伏逆变器无功调压原理与特性'),
    ('p', '光伏逆变器具有四象限运行能力，接入点功率因数可在0.95（超前）～0.95（滞后）调节[[16]]；其中Q(U)下垂'
          '依据并网点电压就地调整无功、无需通信，是就地控制首选[[6,7]]。无功能力受逆变器视在功率的功率圆约束，'
          '如式(2.4)：'),
    ('f', '2.4'),
    ('p', '以本台区为例（逆变器210 kVA）：出力189 kW时剩余无功仅约90.7 kvar，出力100 kW时达184.9 kvar——'
          '**光伏出力越大，可用无功能力越小，恰与过电压最严重时刻重合**，是其固有局限。优势为毫秒级响应、边际'
          '成本近似为零；短板是仅光伏出力时段可用。'),
    ('h2', '2.3 储能系统有功/无功调压原理与特性'),
    ('p', '储能PCS同为四象限变换器，无功能力约束形式同式(2.4)；其通过充电（压低电压）与放电（抬升电压）直接'
          '改变R主导的电压降落分量，**是低压配电网中单位容量调压效果最强的手段**，但受\u201c功率—能量\u201d'
          '双重约束（PCS容量与电池SOC）[[17]]。有功充放伴随电量损耗与循环寿命损耗、成本较高，但全天候可用、'
          '响应数十毫秒，且可兼作需量管理与时移消纳以分摊投资。'),
    ('h2', '2.4 单一资源调压的局限性与光储协同的必要性'),
    ('p', '两类资源特性对比见表2.1。'),
    ('table2', None),
    ('p', '仅靠光伏无功：大发时能力萎缩、受电抗小制约幅度有限、夜间不可用（第5章仿真显示正午仍有6.25 h轻度'
          '越限）；仅靠储能：以有功为主需超大电池容量且深度循环损害寿命，仅用无功同样受电抗制约。**光储协同按'
          '\u201c零边际成本资源优先、高成本资源兜底\u201d组织调压：无功与有功机理互补（经X与R作用）、时段互补'
          '（白天/全天候）、约束互补（功率圆/电池能量），以最小电量与寿命损耗实现治理目标**，构成第4章策略的'
          '设计依据。'),
]

CH3 = [
    ('h2', '3.1 总体设计原则'),
    ('p', '①**主动调控**：由被动响应转为基于量测的主动电压管理；②**源网协同**：光储成为可观可控调压资源；'
          '③**分层控制**：快速性与全局性解耦；④**通信中断自治**：弱通信下维持基本调压；⑤**标准兼容**：遵循'
          'IEC 61850、IEC 60870-5-104、DL/T 645。'),
    ('h2', '3.2 \u201c就地快速控制＋区域协同优化\u201d双层控制架构'),
    ('p', '系统采用双层控制架构，如图3.1所示。'),
    ('fig', FIGS + r'\fig_3_1.png', '图3.1 光储协同电压治理系统双层控制架构', 14.5),
    ('p', '**就地快速控制层（毫秒～秒级）**：光伏与储能就地控制器执行Q(U)下垂与PQ跟踪、分档调压逻辑、指令限幅'
          '与斜率限制、SOC闭锁及通信中断本地自治，以最快速度将越限电压拉回合格区间。**区域协同优化层（分钟级）**：'
          '台区智能融合终端（边缘计算节点）及配电主站基于AMI量测进行全局态势感知与越限预警、调压容量全局优化'
          '分配、下垂参数在线整定及与OLTC协调。两层以\u201c量测上送—指令下发\u201d闭环衔接，就地层保速度下限、'
          '区域层提全局与经济性上限，实现**速度与最优性的解耦**。'),
    ('h2', '3.3 系统组成与信息交互设计'),
    ('p', '系统由电源侧、储能侧、感知层、通信层与控制层组成，见表3.1。'),
    ('table3', None),
    ('p', '感知层以15 min（AMI）至秒级量测经通信层上送；区域层优化后下发参考电压U_{c}、下垂系数k_{q}与功率'
          '限额；就地控制层毫秒级闭环执行并回传状态，形成完整闭环。'),
    ('h2', '3.4 与智能电网技术体系的融合'),
    ('p', '方案与智能电网体系一一对应：感知层—**高级量测体系（AMI）**；通信层—**配电自动化通信体系**（EPON'
          '为主，载波/无线专网补充）；区域层—**边缘计算**；整体—**主动配电网运行控制**框架，以\u201c感知—'
          '通信—控制\u201d闭环替代传统\u201c无感知、慢速、单点\u201d调压模式。'),
]

CH4 = [
    ('h2', '4.1 电压合格区间与分级阈值设定'),
    ('p', '依据GB/T 12325—2008，三相供电电压偏差限值为**−7%～+7%**[[3]]，台区合格区间[0.93, 1.07] pu。为避免'
          '限值边缘频繁投切，内设运行目标带**[0.95, 1.05] pu**（2%裕度）并分两级越限档位：**轻度**（过压'
          '(1.05, 1.07]、欠压[0.93, 0.95)）与**重度**（>1.07或<0.93）；配0.01 pu回差、差异化延时（轻度10 s、'
          '重度0.5 s）与60 s稳定退出。电压判定取主干末端节点为主判据、台变出口校核。各档位策略汇总见表4.1。'),
    ('table4', None),
    ('h2', '4.2 过电压场景分档位递进式协同调压逻辑'),
    ('p', '过电压治理遵循\u201c**光伏无功优先→储能无功补充→储能有功兜底**\u201d顺序，按边际成本升序逐级投入：'
          '前级动作3～5 s后仍越限方投后级；重度越限时各级并联满额投入。共同目标为将末端电压压回1.045 pu（留'
          '0.5%裕度）。整体逻辑如图4.1所示。'),
    ('fig', FIGS + r'\fig_4_1.png', '图4.1 分档位递进式光储协同调压控制流程', 14.0),
    ('p', '**级①光伏无功优先**：全部逆变器切换至无功吸收，按式(4.1)的Q(U)下垂特性分配无功指令：'),
    ('f', '4.1'),
    ('p', '式中：k_{q}为下垂系数；U_{c}为参考电压（取1.0 pu）；U_{m}为实测电压。总吸收容量受式(2.4)约束；退出'
          '条件为U<1.04 pu持续60 s。**级②储能无功补充**：级①后仍越限，PCS转入无功吸收，容量实时扣除有功占用。'
          '**级③储能有功兜底**：级②后仍越限或U>1.07 pu跳级投入，PCS恒功率充电压低电压——有功灵敏度约为无功'
          '的3.2倍，**是消除深度越限的最后手段**；**SOC≥0.90立即闭锁充电**。**级④资源耗尽上报**：全投后越限'
          '仍超30 s，上报区域层申请OLTC调档或光伏有功限额[[8]]。各级设斜率限制防过调振荡；电压恢复后按'
          '\u201c**逆序退出**\u201d先退高成本资源，回落至最低成本运行点。'),
    ('h2', '4.3 欠电压场景与夜间工况适配逻辑'),
    ('p', '欠电压治理与过电压呈镜像：①白天光伏发无功；②PCS发无功；③PCS放电抬压，**SOC≤0.20闭锁放电**；'
          '④仍越限上报转供/错峰，典型场景为傍晚光伏退出的负荷高峰，由储能独立支撑。夜间利用低谷时段'
          '（00:30—05:30）以不大于10 kW将SOC补至0.40基准，兼顾电价经济性与次日调压裕度，实现\u201c白天压顶、'
          '夜间补能、傍晚托底\u201d全时段治理。'),
    ('h2', '4.4 储能SOC保护硬约束设计'),
    ('p', 'SOC约束贯穿全部逻辑：**运行限[0.20, 0.90]**，越限即闭锁对应方向有功充放；告警带[0.20, 0.25]∪'
          '[0.85, 0.90]内有功限额自动收紧至50%；**约束仅作用于有功，PCS无功不受SOC限制**；基准0.40由夜间补电'
          '维持。典型日有功充电约29.3 kWh、日等效循环深度约0.12，**有利于延长电池寿命**。'),
]

CH5 = [
    ('h2', '5.1 典型低压居民台区场景与参数配置'),
    ('p', '选取南方城郊典型低压居民台区：1台400 kVA配变、主干线路0.35 km、居民80户（60户屋顶光伏合计'
          '210 kWp）、储能接于主干末端，主要参数见表5.1。'),
    ('table5', None),
    ('p', '该台区光伏容量渗透率**52.5%**；晴朗正午出力约190 kW、同期负荷64 kW，**净倒送约124 kW（负荷的'
          '1.9倍）**，属典型重过压台区；傍晚负荷峰值100 kW叠加光伏退出又构成欠压场景，具备全工况代表性。'),
    ('h2', '5.2 储能接入位置选型与容量配置'),
    ('p', '**接入位置**：由式(2.3)，电压灵敏度随节点至电源累计电阻增大而增大，储能接于主干末端调压效果最强，'
          '且与光伏出力就地平衡。**功率配置**：光伏无功满额吸收后末端仍约1.064 pu（见5.4节工况2），需有功再'
          '压降约0.019 pu，对应充电功率P=ΔU·U_{N}^{2}/R≈31 kW，叠加傍晚放电需求配置**PCS 50 kW/55 kVA**'
          '（视在容量为无功预留）。**能量配置**按式(5.1)估算：'),
    ('f', '5.1'),
    ('p', '取P_{av}≈25 kW、t_{max}=5 h、ΔSOC=0.5、η_{c}=0.92，得E_{N}≥272 kWh；考虑有功实际介入有限并为'
          '多功能复用预留，工程配置**50 kW/250 kWh磷酸铁锂储能**。'),
    ('h2', '5.3 Matlab/Simulink仿真验证方案'),
    ('p', '仿真基于Matlab/Simulink平台搭建[[20]]：三相电源＋Dyn11变压器＋多段Π等值线路；光伏含MPPT与PQ解耦'
          '控制逆变器（开放无功指令接口）；储能采用Thevenin等效电池＋PCS双闭环；控制器以Stateflow实现分档递进'
          '逻辑与SOC闭锁；暂态步长1×10⁻⁵ s。设置**三组工况**：工况1无调压基准、工况2仅光伏无功（全投Q(U)'
          '下垂）、工况3光储协同（递进逻辑全投入）；**指标**包括电压极值、越限时长、波动率、SOC轨迹与日充/'
          '放电量。'),
    ('h2', '5.4 准稳态预分析结果与预期结论'),
    ('p', '先以Matlab准稳态时序潮流程序（15 min步长，逐点求解式(2.2)并嵌入第4章控制逻辑）开展典型日预分析，'
          '结果如图5.1与表5.2所示。'),
    ('fig', FIGS + r'\fig_5_1.png', '图5.1 典型日三工况末端电压、储能SOC与调压资源出力预分析结果', 15.0),
    ('p', '工况1：正午末端最高**1.081 pu**、连续**4.0 h重度越限**；傍晚最低0.939 pu，全天目标带外8.5 h。'
          '工况2：峰值降至1.064 pu、重度越限消除，但仍有**6.25 h轻度越限**，欠压依旧。工况3：极值收敛至'
          '**1.050/0.951 pu**，**全天越限为零**，波动率由0.043 4 pu降至**0.031 7 pu**（约降27%）。资源层面：光伏最大吸无功132.9 kvar、PCS无功满额55.0 kvar、有功最大充电仅21.0 kW，日充/放'
          '电29.3/4.1 kWh，SOC范围**[0.400, 0.508]**未触任何边界。'),
    ('table5b', None),
    ('p', '**结论**：①光储协同可完全消除台区电压越限，单一光伏无功策略不能；②分档递进使储能有功介入强度与'
          '耗电量远低于无差别调压，兼具有效性与经济性；③SOC硬约束与夜间恢复保证多日可持续运行。'),
]

CH6 = [
    ('h2', '6.1 方案总结'),
    ('p', '本报告完成了光储协同电压治理系统方案设计：**机理上**，揭示\u201c光伏大发→末端电压抬升\u201d本质为'
          '反向有功潮流在线路电阻上的负电压降落，明确低压网\u201c有功敏感\u201d特性（R/X≈3.2）；**架构上**，'
          '设计\u201c就地快速控制＋区域协同优化\u201d双层架构，对应AMI、配电自动化、边缘计算与主动配电网运行'
          '控制；**策略上**，按±7%限值三级分档执行\u201c光伏无功→储能无功→储能有功\u201d递进调压，配合回差延时、跳级并联与SOC硬约束；**验证上**，典型台区预分析表明'
          '电压极值由1.081/0.939 pu收敛至1.050/0.951 pu，全天越限为零，波动率降约27%。方案适用于光伏渗透率超'
          '过50%、末端电压问题突出的辐射状低压台区。'),
    ('h2', '6.2 展望'),
    ('p', '面向毕业设计可沿四个方向深化：①区域协同层升级为二阶锥优化或深度强化学习；②扩展OLTC、SVG与电动汽车'
          '有序充电等多类型资源协同；③计及三相不平衡、多日电量迁移与通信延时检验鲁棒性；④由仿真走向硬件在环'
          '与现场样机验证。'),
]

REFS = [
    '刘振亚. 智能电网技术[M]. 北京：中国电力出版社, 2010.',
    '国家能源局. 2024年全国电力工业统计数据[EB/OL]. (2025-01-21)[2026-10-01]. http://www.nea.gov.cn.',
    'GB/T 12325—2008, 电能质量 供电电压偏差[S]. 北京：中国标准出版社, 2009.',
    '王成山, 李鹏. 分布式发电、微网与智能配电网的发展与挑战[J]. 电力系统自动化, 2010, 34(2): 10-14, 23.',
    'Carvalho P M S, Correia P F, Ferreira L A F M. Distributed reactive power generation control with voltage constraints in smart grids[J]. IEEE Transactions on Power Systems, 2008, 23(1): 405-413.',
    'Turitsyn K, Šulc P, Backhaus S, et al. Options for control of reactive power by distributed photovoltaic generators[J]. Proceedings of the IEEE, 2011, 99(6): 1063-1073.',
    'Demirok E, González P C, Sera D, et al. Local reactive power control methods for overvoltage prevention of distributed solar inverters in low-voltage grids[J]. IEEE Journal of Photovoltaics, 2011, 1(2): 174-182.',
    'Tonkoski R, Lopes L A C, El-Fouly T H M. Coordinated active power curtailment of grid connected PV inverters for overvoltage prevention[J]. IEEE Transactions on Sustainable Energy, 2010, 1(3): 139-147.',
    'Liu X, Aichhorn A, Liu L, et al. Coordinated control of distributed energy storage system with tap changer transformers for voltage rise mitigation under high photovoltaic penetration[J]. IEEE Transactions on Smart Grid, 2012, 3(2): 897-906.',
    'Kabir M N, Mishra Y, Ledwich G, et al. Improving voltage profile of residential distribution systems using rooftop PVs and battery storage units[J]. IEEE Transactions on Smart Grid, 2014, 5(2): 1359-1369.',
    'von Appen J V, Stetz T, Braun M, et al. Local voltage control strategies for PV storage systems in distribution grids[J]. IEEE Transactions on Smart Grid, 2014, 5(2): 1002-1009.',
    'Gabash A, Li P. Active-reactive optimal power flow in distribution networks with embedded generation and battery storage[J]. IEEE Transactions on Power Systems, 2012, 27(4): 2026-2035.',
    'Hill C A, Such M C, Chen D, et al. Battery energy storage for enabling integration of distributed solar power[J]. IEEE Transactions on Smart Grid, 2012, 3(2): 850-857.',
    'Ochoa L F, Dent C J, Harrison G P. Distribution network capacity assessment: variable DG and active networks[J]. IEEE Transactions on Power Systems, 2010, 25(1): 87-95.',
    '尤毅, 钟清, 许东荣, 等. 主动配电网技术及其进展[J]. 电力系统自动化, 2012, 36(18): 10-16.',
    'GB/T 33593—2017, 分布式电源并网技术要求[S]. 北京：中国标准出版社, 2017.',
    'GB/T 36547—2018, 电化学储能系统接入电网技术规定[S]. 北京：中国标准出版社, 2018.',
    '何仰赞, 温增银. 电力系统分析：上册[M]. 3版. 武汉：华中科技大学出版社, 2002.',
    'Baran M E, Wu F F. Optimal capacitor placement on radial distribution systems[J]. IEEE Transactions on Power Delivery, 1989, 4(1): 725-734.',
    'Kersting W H. Distribution system modeling and analysis[M]. 2nd ed. Boca Raton: CRC Press, 2007.',
]

# 表格数据
TABLE2_CAP = '表2.1 光伏逆变器与储能系统调压特性对比'
TABLE2_HEAD = ['对比维度', '光伏逆变器无功调压', '储能无功调压', '储能有功调压']
TABLE2_ROWS = [
    ['调压机理', '吸收/发出无功，改变无功潮流', 'PCS吞吐无功，改变无功潮流', '充/放电改变净有功潮流'],
    ['电压灵敏度', 'X/U_{N}（较小）', 'X/U_{N}（较小）', 'R/U_{N}（约为无功的3.2倍）'],
    ['响应速度', '毫秒级', '小于100 ms', '小于100 ms'],
    ['能力上限', '受功率圆√(S_{N}^{2}−P_{PV}^{2})约束，大发时段显著萎缩', '受PCS视在容量约束', '受PCS功率与电池能量双重约束'],
    ['可用时段', '仅光伏出力时段', '全天候', '全天候（SOC允许时）'],
    ['边际成本', '近似为零（不耗电量）', '低（仅变换损耗）', '较高（电量损耗＋循环寿命损耗）'],
    ['角色定位', '轻度越限第一道防线', '无功补充', '重度越限兜底与欠压支撑'],
]
TABLE3_CAP = '表3.1 系统组成模块功能与智能电网技术落点'
TABLE3_HEAD = ['组成模块', '核心设备', '主要功能', '信息交互', '智能电网技术落点']
TABLE3_ROWS = [
    ['电源侧', '分布式光伏＋并网逆变器', '有功发电与无功调压', '上送状态，接收无功指令', '分布式电源即插即用'],
    ['储能侧', '磷酸铁锂电池＋PCS＋BMS', '有功充放、无功吞吐与SOC管理', '上送SOC，接收P/Q指令', '源网荷储协同'],
    ['感知层', '智能电能表、传感器、辐照仪', '电压、功率、SOC量测', '15 min至秒级上送', '高级量测体系（AMI）'],
    ['通信层', 'EPON光纤、载波、4G/5G', '量测与指令双向传输', 'IEC 61850/104等', '配电自动化通信体系'],
    ['控制层', '就地控制器、智能融合终端', '就地快速调压＋区域优化', '下发整定参数，上报事件', '边缘计算、主动配电网'],
]
TABLE4_CAP = '表4.1 电压分级阈值与调压资源动作策略'
TABLE4_HEAD = ['电压档位', '区间（pu）', '相电压折算/V', '判定延时', '调压资源动作策略', '退出条件']
TABLE4_ROWS = [
    ['正常区', '[0.95, 1.05]', '[209.0, 231.0]', '—', '资源热备，维持监测', '回差0.01 pu，延时60 s'],
    ['轻度过压', '(1.05, 1.07]', '(231.0, 235.4]', '10 s', '光伏无功吸收→储能无功吸收→储能充电', 'U<1.04 pu持续60 s'],
    ['重度过压', '>1.07', '>235.4', '0.5 s', '各级并联满额投入，仍越限上报申请OLTC/光伏限额', '同上'],
    ['轻度欠压', '[0.93, 0.95)', '[204.6, 209.0)', '10 s', '光伏无功发出（白天）→储能无功发出→储能放电', 'U>0.96 pu持续60 s'],
    ['重度欠压', '<0.93', '<204.6', '0.5 s', '储能无功与放电满额投入，仍越限上报（转供/错峰）', '同上'],
]
TABLE5_CAP = '表5.1 典型低压居民台区主要参数'
TABLE5_HEAD = ['设备/系统', '参数项', '数值/型号']
TABLE5_ROWS = [
    ['配电变压器', '容量/电压/接线', '400 kVA，10/0.4 kV，Dyn11，出口电压1.01 pu'],
    ['主干线路', '型号/长度/阻抗', 'JKLYJ-120，0.35 km，R=0.088 6 Ω，X=0.028 Ω'],
    ['负荷', '户数/峰谷值/功率因数', '80户，峰值100 kW（20:00），正午64 kW，cosφ=0.90'],
    ['分布式光伏', '装机/逆变器/出力', '210 kWp（60户），逆变器210 kVA，晴天峰值190 kW'],
    ['储能系统', '功率/能量/PCS/效率', '50 kW/250 kWh磷酸铁锂，PCS 55 kVA，η=0.92'],
    ['储能SOC', '运行限/基准', '[0.20, 0.90]，基准0.40'],
]
TABLE5B_CAP = '表5.2 三工况准稳态预分析指标对比'
TABLE5B_HEAD = ['评价指标', '工况1：无调压', '工况2：仅光伏无功', '工况3：光储协同']
TABLE5B_ROWS = [
    ['电压最大值/pu', '1.081', '1.064', '**1.050**'],
    ['电压最小值/pu', '0.939', '0.939', '**0.951**'],
    ['重度越限时长/h', '4.00', '0', '**0**'],
    ['目标带外时长/h', '8.50', '6.25', '**0**'],
    ['电压波动率（标准差）/pu', '0.043 4', '0.037 3', '**0.031 7**'],
    ['光伏无功最大吸收/kvar', '—', '125.7', '132.9'],
    ['储能无功最大吸收/kvar', '—', '—', '55.0'],
    ['储能最大充电功率/kW', '—', '—', '21.0'],
    ['储能日充/放电量/kWh', '—', '—', '29.3/4.1'],
    ['储能SOC范围', '—', '—', '[0.400, 0.508]'],
]

# ============================================================
# 文档组装
# ============================================================
def build_cover(doc):
    plain_center(doc, '智能电网技术', ea='黑体', size=22, bold=True, space_after=6)
    plain_center(doc, '结课报告', ea='黑体', size=22, bold=True, space_after=30)
    # 信息表
    tb = doc.add_table(rows=4, cols=2)
    tb.alignment = WD_TABLE_ALIGNMENT.CENTER
    tb.autofit = False
    data = [('题　　目：', '智能配电网光储协同的电压治理系统方案设计'),
            ('专业班级：', '电气工程及其自动化'),
            ('姓　　名：', '　'),
            ('学　　号：', '　')]
    for i, (lab, val) in enumerate(data):
        c0, c1 = tb.rows[i].cells
        c0.width = Cm(3.8); c1.width = Cm(10.2)
        for c in (c0, c1):
            c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p0 = c0.paragraphs[0]
        p0.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.paragraph_format.line_spacing = 1.5
        r0 = p0.add_run(lab)
        set_run_fonts(r0, ea='黑体'); r0.font.size = Pt(16); r0.bold = True
        p1 = c1.paragraphs[0]
        p1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.line_spacing = 1.5
        r1 = p1.add_run(val)
        set_run_fonts(r1, ea='宋体'); r1.font.size = Pt(15)
        # 值单元格仅保留下边框(下划线效果)
        set_cell_border(c1, bottom=('single', 8))
        set_cell_border(c0, bottom=('none', 0), top=('none', 0), left=('none', 0), right=('none', 0))
        set_cell_border(c1, top=('none', 0), left=('none', 0), right=('none', 0))
    for _ in range(3):
        sp = doc.add_paragraph(); sp.paragraph_format.line_spacing = 1.5
    plain_center(doc, '2026 年 10 月', ea='黑体', size=16, bold=True, space_after=0)

def build_front_matter(doc, toc_entries):
    # ---- 摘要 ----
    page_break(doc)
    plain_center(doc, '摘　要', ea='黑体', size=16, bold=True)
    body_para(doc, ABSTRACT_CN)
    blank = doc.add_paragraph(); blank.paragraph_format.line_spacing = 1.5
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run('关键词：')
    set_run_fonts(r, ea='黑体'); r.bold = True; r.font.size = Pt(14)
    r2 = p.add_run(KEYWORDS_CN)
    set_run_fonts(r2); r2.font.size = Pt(12)
    # ---- Abstract ----
    page_break(doc)
    plain_center(doc, 'Abstract', ea='Times New Roman', size=16, bold=True)
    p = body_para(doc, ABSTRACT_EN, indent=False)
    for r in p.runs:
        set_run_fonts(r, ea='Times New Roman', ascii_f='Times New Roman')
    blank = doc.add_paragraph(); blank.paragraph_format.line_spacing = 1.5
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    r = p.add_run('Key words: ')
    set_run_fonts(r, ea='Times New Roman', ascii_f='Times New Roman'); r.bold = True; r.font.size = Pt(12)
    r2 = p.add_run(KEYWORDS_EN)
    set_run_fonts(r2, ea='Times New Roman', ascii_f='Times New Roman'); r2.font.size = Pt(12)
    # ---- 目录 ----
    page_break(doc)
    plain_center(doc, '目　录', ea='黑体', size=16, bold=True)
    # 静态目录(不用TOC域, 保证Word/WPS/LibreOffice渲染一致; 标题均用Heading样式, Word可随时重建)
    if toc_entries:
        for ent in toc_entries:
            pe = doc.add_paragraph()
            pf = pe.paragraph_format
            pf.line_spacing = 1.0
            pf.space_after = Pt(2)
            pf.tab_stops.add_tab_stop(Cm(15.9), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
            if ent['level'] == 1:
                pf.left_indent = Cm(0)
            elif ent['level'] == 2:
                pf.left_indent = Cm(0.74)
            else:
                pf.left_indent = Cm(1.48)
            r = pe.add_run(ent['text'])
            set_run_fonts(r, ea='黑体' if ent['level'] == 1 else '宋体')
            r.font.size = Pt(10.5)
            if ent['level'] == 1:
                r.bold = True
            r2 = pe.add_run('\t' + str(ent['page']))
            set_run_fonts(r2)
            r2.font.size = Pt(10.5)
    else:
        pe = doc.add_paragraph()
        pe.paragraph_format.line_spacing = 1.5
        r = pe.add_run('（目录页码待渲染回填）')
        set_run_fonts(r)
    note = doc.add_paragraph()
    note.paragraph_format.line_spacing = 1.0
    nr = note.add_run('（注：目录页码按当前排版生成；若正文有增删，可在Word中通过\u201c引用—目录\u201d功能重新生成。）')
    set_run_fonts(nr)
    nr.italic = True
    nr.font.size = Pt(9)
    nr.font.color.rgb = RGBColor(0x80, 0x80, 0x80)

def emit_chapter(doc, blocks):
    for b in blocks:
        kind = b[0]
        if kind == 'h2':
            heading(doc, b[1], 2)
        elif kind == 'p':
            body_para(doc, b[1])
        elif kind == 'f':
            add_formula(doc, b[1])
        elif kind == 'fig':
            add_figure(doc, b[1], b[2], b[3])
        elif kind == 'table2':
            three_line_table(doc, TABLE2_CAP, TABLE2_HEAD, TABLE2_ROWS, [2.3, 4.0, 3.8, 3.8], left_cols=(1, 2, 3))
        elif kind == 'table3':
            three_line_table(doc, TABLE3_CAP, TABLE3_HEAD, TABLE3_ROWS, [1.6, 3.2, 3.4, 3.2, 3.4], left_cols=(1, 2, 3, 4))
        elif kind == 'table4':
            three_line_table(doc, TABLE4_CAP, TABLE4_HEAD, TABLE4_ROWS, [1.7, 2.2, 2.6, 1.4, 4.6, 2.4], left_cols=(4,))
        elif kind == 'table5':
            three_line_table(doc, TABLE5_CAP, TABLE5_HEAD, TABLE5_ROWS, [2.6, 3.6, 9.6], left_cols=(2,))
        elif kind == 'table5b':
            three_line_table(doc, TABLE5B_CAP, TABLE5B_HEAD, TABLE5B_ROWS, [5.2, 3.4, 3.6, 3.6])

def build(toc_entries=None):
    doc = Document()
    setup_styles(doc)
    setup_sections(doc)
    # 打开文档时自动更新域
    settings = doc.settings.element
    if settings.find(qn('w:updateFields')) is None:
        uf = OxmlElement('w:updateFields'); uf.set(qn('w:val'), 'true')
        settings.append(uf)

    build_cover(doc)
    build_front_matter(doc, toc_entries)
    make_body_section(doc)

    heading(doc, '1　绪论', 1)
    emit_chapter(doc, CH1)
    heading(doc, '2　分布式光伏并网电压越限机理与调压资源特性分析', 1)
    emit_chapter(doc, CH2)
    heading(doc, '3　光储协同电压治理系统架构设计', 1)
    emit_chapter(doc, CH3)
    heading(doc, '4　分档位递进式协同调压控制策略设计', 1)
    emit_chapter(doc, CH4)
    heading(doc, '5　典型台区参数配置与仿真验证', 1)
    emit_chapter(doc, CH5)
    heading(doc, '6　总结与展望', 1)
    emit_chapter(doc, CH6)

    heading(doc, '参考文献', 1)
    for i, ref in enumerate(REFS, 1):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        r = p.add_run('[%d] ' % i + ref)
        set_run_fonts(r)
        for rr in p.runs:
            if not rr.font.size:
                rr.font.size = Pt(10.5)

    # 文档属性
    doc.core_properties.title = '智能配电网光储协同的电压治理系统方案设计'
    doc.core_properties.subject = '《智能电网》课程报告'

    os.makedirs(OUTDIR, exist_ok=True)
    doc.save(DOC_PATH)

    # 字数统计
    d2 = Document(DOC_PATH)
    cjk = 0
    for p in d2.paragraphs:
        cjk += len(re.findall(r'[\u4e00-\u9fff]', p.text))
    for tb in d2.tables:
        for row in tb.rows:
            for c in row.cells:
                cjk += len(re.findall(r'[\u4e00-\u9fff]', c.text))
    print('DOCX saved:', DOC_PATH)
    print('CJK char count (paragraphs+tables):', cjk)

if __name__ == '__main__':
    entries = None
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        with open(sys.argv[1], encoding='utf-8') as f:
            entries = json.load(f)
    build(entries)
