from autoagents_graph.agentify import FlowGraph, START
from autoagents_graph.agentify.models import QuestionInputState, AiChatState, ConfirmReplyState, KnowledgeSearchState, Pdf2MdState, AddMemoryVariableState,CodeFragmentState,InfoClassState,ForEachState
import uuid

def main():
    graph = FlowGraph(
        personal_auth_key="7217394b7d3e4becab017447adeac239",
        personal_auth_secret="f4Ziua6B0NexIMBGj1tQEVpe62EhkCWB",
        base_url="https://uat.agentspro.cn"
    )

    # 添加节点
    # 用户提问节点
    graph.add_node(
        id=START,
        position={'x': -2050.0187299418194, 'y': 168.1277274588137},
        state=QuestionInputState(
            inputText=True,
            uploadFile=False,
            uploadPicture=False,
            fileUpload=False,
            fileContrast=False,
        )
    )

    # 确定回复节点
    graph.add_node(
        id="confirm_reply",
        position={'x': -465.81689900126946, 'y': -1668.2275989292857},
        state=ConfirmReplyState(
            isvisible=False,
            text="""# 值班日志数据库表详细描述

## 表基本信息

- **表名**: `duty_log`
- **中文名称**: 生产指挥中心值班日志记录表
- **用途**: 记录电力系统的缺陷、跳闸、问题、隐患等事件信息，用于运维管理和数据分析
- **总记录数**: 1,245条
- **字段数量**: 24个
- **数据质量**: 完整性99.5%，准确性高，一致性良好，实时更新

## 字段详细说明

### 1. 主键字段

#### `id`
- **类型**: INT
- **约束**: PRIMARY KEY, AUTO_INCREMENT
- **描述**: 主键ID，自增
- **用途**: 用于唯一标识每条记录，查询时常用作条件
- **示例值**: 1, 2, 3, 4, 5

### 2. 核心分类字段

#### `事件类型`
- **类型**: TEXT
- **描述**: 事件的主要分类
- **枚举值**:
  - `缺陷`: 设备或系统存在的缺陷问题 (874条, 70.2%)
  - `跳闸`: 设备跳闸事件 (144条, 11.6%)
  - `问题`: 一般性问题 (129条, 10.4%)
  - `隐患`: 潜在的安全隐患 (97条, 7.8%)
- **用途**: 用于按事件类型分类查询和统计
- **示例查询**:
  - 查询所有缺陷类型的记录
  - 统计各事件类型的数量
  - 查找跳闸事件

#### `缺陷等级`
- **类型**: TEXT
- **描述**: 缺陷的严重程度等级
- **枚举值**:
  - `紧急`: 需要立即处理的严重缺陷
  - `严重`: 需要尽快处理的重要缺陷
  - `一般`: 可以稍后处理的普通缺陷
- **用途**: 用于按严重程度分类查询和统计
- **示例查询**:
  - 查询所有紧急缺陷
  - 统计各缺陷等级的数量
  - 优先处理严重缺陷

### 3. 时间相关字段

#### `日期`
- **类型**: TEXT
- **格式**: YYYY年MM月DD日
- **用途**: 用于时间范围查询、按日期统计
- **示例查询**:
  - 查询2024年的所有记录
  - 统计各月份的事件数量
  - 查找最近一周的记录

#### `时间`
- **类型**: TEXT
- **格式**: HH:MM
- **时间段分布**:
  - 0-11点: 上午时段
  - 12-15点: 下午时段
  - 16-19点: 傍晚时段
  - 20-23点: 夜间时段
- **用途**: 用于精确时间查询、时间段分析
- **示例查询**:
  - 查询上午发生的事件
  - 统计各时间段的事件分布
  - 查找夜间发生的问题

### 4. 地理位置字段

#### `变电站`
- **类型**: TEXT
- **描述**: 变电站名称
- **主要变电站** (前15名):
  - 天一变: 40条
  - 春晓变: 32条
  - 明州变: 31条
  - 宁海变: 30条
  - 河姆变: 25条
  - 长石变: 21条
  - 洛迦变: 19条
  - 武胜变: 19条
  - 沙湾变: 18条
  - 殿跟变: 18条
  - 沿海变: 17条
  - 淞浦变: 17条
  - 衣亭变: 16条
  - 句章变: 16条
  - 洪塘变: 15条
- **用途**: 用于按变电站查询、地理位置分析
- **示例查询**:
  - 查询天一变的所有记录
  - 统计各变电站的事件数量
  - 查找特定区域的变电站问题

### 5. 技术参数字段

#### `设备电压等级`
- **类型**: TEXT
- **描述**: 设备的电压等级
- **枚举值**:
  - `500kV`: 超高压
  - `220kV`: 高压
  - `110kV`: 中压
  - `35kV`: 中低压
  - `10kV`: 低压
- **用途**: 用于按电压等级分类查询
- **示例查询**:
  - 查询500kV设备的问题
  - 统计各电压等级的事件分布
  - 分析高压设备故障率

#### `设备间隔名称`
- **类型**: TEXT
- **描述**: 设备在变电站中的间隔标识
- **示例值**: #1主变, #2主变, 1号主变, 2号主变
- **用途**: 用于精确定位具体设备
- **示例查询**:
  - 查询#1主变的所有问题
  - 查找特定间隔的设备故障

### 6. 跳闸相关字段

#### `跳闸设备分类`
- **类型**: TEXT
- **描述**: 跳闸设备的分类
- **示例值**: 主变, 线路, 开关, 保护装置
- **用途**: 用于分析跳闸事件
- **示例查询**:
  - 查询主变跳闸事件
  - 统计各设备类型的跳闸次数

#### `跳闸原因分类`
- **类型**: TEXT
- **描述**: 跳闸的原因分类
- **示例值**: 过载, 短路, 保护动作, 设备故障
- **用途**: 用于分析跳闸原因
- **示例查询**:
  - 查询因过载导致的跳闸
  - 分析跳闸原因分布

#### `重合情况`
- **类型**: TEXT
- **描述**: 跳闸后的重合闸情况
- **示例值**: 重合成功, 重合失败, 未重合
- **用途**: 用于分析重合闸效果
- **示例查询**:
  - 查询重合成功的跳闸事件
  - 统计重合闸成功率

### 7. 故障信息字段

#### `故障简报`
- **类型**: TEXT
- **描述**: 故障的简要描述
- **用途**: 用于故障信息查询
- **示例查询**:
  - 搜索包含特定关键词的故障
  - 查询故障描述

#### `故障录波`
- **类型**: TEXT
- **描述**: 故障录波相关信息
- **用途**: 用于故障分析
- **示例查询**:
  - 查询有故障录波的记录
  - 分析故障录波数据

### 8. 缺陷分析字段

#### `缺陷设备分类`
- **类型**: TEXT
- **描述**: 存在缺陷的设备分类
- **示例值**: 主变, 开关, 保护装置, 直流系统
- **用途**: 用于按设备类型分析缺陷
- **示例查询**:
  - 查询主变设备的缺陷
  - 统计各设备类型的缺陷数量

#### `问题类型`
- **类型**: TEXT
- **描述**: 问题的具体类型
- **示例值**: 告警, 异常, 故障, 维护
- **用途**: 用于问题分类查询
- **示例查询**:
  - 查询告警类型的问题
  - 统计各问题类型的分布

### 9. 厂商信息字段

#### `厂家`
- **类型**: TEXT
- **描述**: 设备制造厂家
- **示例值**: 南瑞继保, 许继电气, 国电南自, ABB
- **用途**: 用于按厂家分析设备质量
- **示例查询**:
  - 查询特定厂家的设备问题
  - 分析各厂家的设备故障率

### 10. 内容描述字段

#### `内容`
- **类型**: TEXT
- **描述**: 事件的详细描述内容
- **用途**: 用于详细内容查询和关键词搜索
- **示例查询**:
  - 搜索包含特定关键词的记录
  - 查询详细的事件描述
  - 分析事件内容模式

### 11. 处理状态字段

#### `是否遗留`
- **类型**: TEXT
- **描述**: 问题是否遗留未解决
- **枚举值**:
  - `是`: 问题尚未解决
  - `否`: 问题已解决
- **用途**: 用于查询遗留问题
- **示例查询**:
  - 查询所有遗留问题
  - 统计问题解决率

#### `是否移交综合室`
- **类型**: TEXT
- **描述**: 是否移交到综合室处理
- **枚举值**:
  - `是`: 已移交综合室
  - `否`: 未移交综合室
- **用途**: 用于查询移交情况
- **示例查询**:
  - 查询移交到综合室的记录
  - 统计移交比例

### 12. 处理信息字段

#### `消缺单位`
- **类型**: TEXT
- **描述**: 负责消除缺陷的单位
- **主要消缺单位** (前10名):
  - 检修中心: 427条
  - 超高压中心: 83条
  - 输电中心: 73条
  - 运维中心: 48条
  - 江北运检站: 33条
  - 北仑公司: 30条
  - 鄞州公司: 26条
  - 余姚公司: 25条
  - 海曙运检站: 23条
  - 慈溪运检站: 22条
- **用途**: 用于按处理单位查询和统计
- **示例查询**:
  - 查询检修中心处理的缺陷
  - 统计各消缺单位的工作量
  - 分析消缺效率

#### `后续措施`
- **类型**: TEXT
- **描述**: 采取的后续处理措施
- **用途**: 用于查询处理措施
- **示例查询**:
  - 查询特定缺陷的处理措施
  - 分析处理措施的有效性

### 13. 其他信息字段

#### `备注`
- **类型**: TEXT
- **描述**: 额外的备注信息
- **用途**: 用于查询备注信息
- **示例查询**:
  - 查询有备注的记录
  - 搜索备注中的特定信息

#### `值班人`
- **类型**: TEXT
- **描述**: 值班人员姓名
- **用途**: 用于查询值班人员
- **示例查询**:
  - 查询特定值班人的记录
  - 统计值班人员的工作量

#### `创建时间`
- **类型**: TIMESTAMP
- **描述**: 记录创建的时间戳
- **格式**: YYYY-MM-DD HH:MM:SS
- **用途**: 用于记录创建时间查询
- **示例查询**:
  - 查询最近创建的记录
  - 按创建时间排序

## 常用查询模式

### 1. 时间范围查询
- **描述**: 查询特定时间段内的记录
- **示例**: "查询2024年1月的所有缺陷"
- **适用字段**: 日期, 时间, 创建时间

### 2. 分类统计查询
- **描述**: 按某个字段分类统计数量
- **示例**: "统计各变电站的缺陷数量"
- **适用字段**: 事件类型, 缺陷等级, 变电站, 消缺单位

### 3. 关键词搜索
- **描述**: 在内容字段中搜索特定关键词
- **示例**: "搜索包含跳闸的记录"
- **适用字段**: 内容, 故障简报, 备注

### 4. 多条件组合查询
- **描述**: 组合多个条件进行查询
- **示例**: "查询天一变2024年的严重缺陷"
- **适用字段**: 任意多个字段组合

### 5. 趋势分析查询
- **描述**: 分析数据变化趋势
- **示例**: "分析各月份缺陷数量的变化趋势"
- **适用字段**: 日期, 时间, 数量统计

### 6. 关联分析查询
- **描述**: 分析不同字段之间的关联关系
- **示例**: "分析缺陷等级与消缺单位的关系"
- **适用字段**: 任意两个或多个字段

## 业务上下文

### 电力系统运维
- **用途**: 用于电力系统的日常运维管理，记录设备运行状态和问题
- **关键指标**: 设备缺陷率, 故障处理时间, 消缺效率

### 故障分析
- **用途**: 分析设备故障原因和处理过程，提高系统可靠性
- **关键指标**: 故障类型分布, 故障原因分析, 处理措施效果

### 预防性维护
- **用途**: 通过分析历史数据，制定预防性维护计划
- **关键指标**: 设备故障趋势, 维护周期优化, 成本效益分析

### 质量评估
- **用途**: 评估设备质量和厂家服务水平
- **关键指标**: 厂家故障率, 设备寿命分析, 质量改进建议

### 效率分析
- **用途**: 分析消缺效率和处理时间，优化工作流程
- **关键指标**: 响应时间, 处理时长, 人员效率

## 数据特点

### 数据完整性
- **总记录数**: 1,245条
- **完整率**: 99.5%
- **主要数据类型**: 缺陷、跳闸、问题、隐患

### 时间分布特点
- **覆盖时间**: 2024年1月 - 2025年5月
- **数据密度**: 1月、2月数据量较大，可能与季节性维护相关
- **实时性**: 数据实时更新，反映当前运维状态

### 地理分布特点
- **变电站覆盖**: 覆盖多个变电站，天一变、春晓变、明州变等为主要站点
- **区域分布**: 分布在不同区域，便于区域性问题分析

### 技术特点
- **电压等级**: 覆盖从10kV到500kV的多个电压等级
- **设备类型**: 涵盖主变、开关、保护装置等多种设备类型
- **故障模式**: 记录多种故障模式和原因，便于故障分析""",
        )
    )

    # 智能对话节点
    graph.add_node(
        id="ai_chat",
        position={'x': 296.06369942212564, 'y': -1700.1919105251395},
        state=AiChatState(
            historyText=0,
            model="doubao-pro-256k",
            systemPrompt="""当前时间：{{cTime}}

### 任务说明：

您是一个专业的电力行业数据库工程师，需要将用户提出的自然语言问题（可能包含口语化表达）转化为准确且可执行的SQL查询。

### 详细步骤：

请严格遵循以下步骤进行思考并生成SQL查询：

1. **理解问题**：用自己的话复述用户的问题，明确用户需要查询哪些信息（例如：哪些字段？满足什么条件？如何排序？有无聚合操作？）。

2. **提取关键元素**：

- 识别问题中提到的实体（如表名、字段名的描述词）和操作（如筛选、排序、分组、聚合）。

- 特别注意口语化表达（如“去年的数据”应转化为“年份是去年”）。

3. **数据库结构映射**：

- 仔细检查提供的数据库结构，将步骤2提取的元素与数据库中的表名和字段名进行匹配。

- 注意：一个概念可能有多种表达方式，需找到最匹配的字段（如“销售额”可能对应字段`sales_amount`或`revenue`）。

- 如果问题涉及多个表，确定这些表之间的关联关系（通常通过外键连接）。

4. **构建SQL查询**：

- 使用表别名（如`t1`, `t2`）来避免歧义，并在JOIN时使用别名。

- 确保SELECT、WHERE、GROUP BY、HAVING、ORDER BY等子句中使用的字段都明确指定了表别名（例如：`t1.name`）。

- 如果有多个表，必须使用JOIN并明确指定连接条件（如`ON t1.id = t2.t1_id`）。

- 如果问题要求聚合（如“每个部门的平均工资”），使用GROUP BY并选择合适的聚合函数（如AVG、SUM、COUNT等）。

- 如果问题要求排序，使用ORDER BY并指定排序方向（ASC或DESC）。
- 尽可能返回多一点相关的字段

5. **验证**：

- 检查生成的SQL中引用的每个字段和表名是否都存在于数据库结构中。

- 确保SQL逻辑与用户问题一致。

### 规则：

- **必须使用表别名**：任何字段引用都必须带表别名（例如：`employee.name`而不是`name`）。

- **禁止使用`*`**：必须明确列出所需字段。

- **处理无法回答的情况**：如果数据库结构中没有包含回答问题所需的信息（例如：缺少关键表或字段），则输出：“数据库无法回答该问题。”。

- **日期处理**：如果问题涉及日期（如“最近三个月”），请根据当前日期{{cTime}}计算具体日期范围，并在SQL中使用该范围。

- **避免使用数据库不支持的函数**：请使用标准SQL函数，或{{$db_type}}数据库支持的函数。

## 示例问题

【问题1:查询近三个月（2025年3月、2025年1月至2025年4月、……）以来110kv设备（xxx设备）的跳闸（/缺陷/问题/隐患）事件，进行统计分析并总结原因，给出相关的处置建议。
查询条件涵盖值班日志中的事件类型、日期时间、变电站、设备电压等级、设备间隔、设备分类等条件，对任意条件的检索。
回复：
通过你写的 sql 最后链接数据库的结果表头包含
「「序号
事件类型
事件日期
事件时间
变电站
设备电压等级
设备间隔名称
跳闸设备分类
跳闸原因分类
重合情况
故障简报
故障录波
缺陷设备分类
缺陷等级
问题类型
生产厂家
内容
是否遗留
消缺单位
后续措施
备注
值班人员
」」

】


### 输出格式：

请按照以下格式输出：

【复述问题】

... （这里用一句话复述问题）

【提取的关键元素】

- 涉及的表：...

- 涉及的字段：...

- 条件：...

- 排序要求：...

- 聚合要求：...

【生成的SQL】

```sql""",
            quotePrompt="""### 输入：

- 用户问题：{{ori_question}}

- 数据库结构：{{sql_structure}}""",
            temperature=0,
            maxToken=4000,
        )
    )

    # 确定回复节点
    graph.add_node(
        id="confirm_reply_1",
        position={'x': 1858.77379621562, 'y': -1739.8422932626484},
        state=ConfirmReplyState(
            isvisible=False,
            text="您可以输入希望用户看到的内容，当触发条件判定成立，将显示您输入的内容。",
        )
    )

    # 代码块节点
    graph.add_node(
        id="code_fragment",
        position={'x': 966.1452273108512, 'y': -1660.84372712498},
        state=CodeFragmentState(
            code="""import re

def userFunction(params):
    def extract_after_think(info):
        # 使用正则表达式匹配第一个</think>之后的所有内容
        match = re.search(r'</think>(.*)', info, re.DOTALL)
        if match:
            return match.group(1).strip()  # 返回匹配到的内容并去除首尾空白
        else:
            return info
            
    result = {}
    try:
        # 提取内容并保存到result中
        result['output_key'] = extract_after_think(params['input_key'])
    except Exception as e:
        # 捕获可能的异常并记录错误信息
        result['error'] = str(e)

    return result""",
        )
    )

    # 添加记忆变量节点
    graph.add_node(
        id="memory_var",
        position={'x': -189.60795910297736, 'y': -1378.3030203132323},
        state=AddMemoryVariableState(
            variables={'sql_structure': 'string', 'ori_question': 'string'},
        )
    )

    # 智能对话节点
    graph.add_node(
        id="ai_chat_1",
        position={'x': 2744.7449259121063, 'y': -2014.5515520911588},
        state=AiChatState(
            historyText=0,
            model="doubao-1.5-pro-256k",
            systemPrompt="""## 角色
电网 数据总结专家

## 任务
从用户问题和查询数据结果总结
尽可能按照如下维度进行分析
【
统计分析（暂时固定为三个纬度的统计，特点、典型表现、影响范围，需要结合值班日志的“内容“，知识库的资料，进行整合总结）
】
""",
            quotePrompt="""用户问题: {{ori_question}}

查询数据结果: {{text}}""",
            temperature=0,
            maxToken=12000,
        )
    )

    # 确定回复节点
    graph.add_node(
        id="confirm_reply_2",
        position={'x': -464.4246615314331, 'y': 2504.3336260932606},
        state=ConfirmReplyState(
            text="""## 数据库中包含的表及其说明
故障跳闸数据表：
表名	说明
T_EVENT_ZNJS_DWXXJS	电网事件信息表
T_OPERATIONAL_EVENT_NINGBO	监控大数据故障表	
T_ACCIDENT_SECOND_ANALYSIS	故障二次分析结果表
T_TH_LOGBOOK	生产指挥中心值班日志记录表
REAL_JXDATA	检修记录单表（实时）
T_YJ_ZM_WEATHER	管控平台天气信息
PMS_BD_EQUIP_INFO	管控平台-变电设备信息表
PMS_SD_EQUIP_INFO	管控平台-输电设备信息
PMS_FAC_INFO	管控平台-变电站信息
NUSP_FAC_EQUIPMENT	变电设备清单表
T_YJ_PMS_DEVICE	PMS设备信息
T_YJ_PMS_TREE_SUBSTATION	PMS变电站信息


## 不同表中字段的值

1.电网事件信息表
T_EVENT_ZNJS_DWXXJS
字段名	含义
ID	主键
BUSI_TYPE_CODE	业务类型编码（故障1000，异常1100，变位1200，越限1300，越限恢复1301，越限超时1302，缺陷1400，验收(包含重过载数据)1500）
BUSI_TYPE_NAME	业务类型名称
OCCUR_TIME	发生时间
YX_ID	关联遥信ID
CONTENT	事件内容
STATION_ID	厂站ID
STATION_NAME	厂站名称
BAY_ID	间隔名称
BAY_VLTY_ID	间隔电压等级ID
EQUIP_ID	设备ID
EQUIP_NAME	设备名称
EQUIP_VLTY_ID	设备电压等级
STATUS	流程状态
STATUS_NAME	流程状态名称
YW_CONTACT_USER	现场运维联系人 环节10
YW_CONTACT_TIME	现场运维联系时间  环节10
YW_CONTACT_CONTENT	现场运维联系内容 环节10
JKY_CONFIRM_USER	监控员确认人 环节20
JKY_CONFIRM_TIME	监控员确认时间 环节20
JKY_CONFIRM_CONTENT	监控员确认意见 环节20
IF_JKY_CONFIRM	是否监控员人工再确认，0否1是
YW_CONTACT2_USER	监控员人工确认时现场运维联系人
YW_CONTACT2_TIME	监控员人工确认时现场运维联系时间
YW_CONTACT2_CONTENT	监控员人工确认时现场运维联系内容
IF_NOTIFY_DDT	是否通知调度台
DDT_CONTACT_USER	调度台联系人
DDT_CONTACT_TIME	调度台联系时间
DDT_CONTACT_CONTENT	调度台联系内容
IF_CREATE_DEFECT	是否创建缺陷
LINK_DEFECT_ID	关联的缺陷ID
LAST_UPDATE_TIME	记录的最新更新时间
CREATETIME	创建时间
ISDEL	是否逻辑删除，0否，1是
AREANO	区域编码
CALL_STATUS	通话状态，0：默认值（待通话），1：通话中，2：通话异常，5：通话完成
BUSI_TYPE_SUBCLASS	业务子类名称，如：电网异常事件子类包括：未复归、频发等
RESP_AREA	责任分区ID
UPCALL_MAN	监控员确认（电话待呼出） 环节5
UPCALL_TIME	监控员确认时间（电话呼出） 环节5
SESSIONID	通话ID（保证和后续通话建立联系）
CZCL_ID	处置策略规则id
DISPOSAL_TACTI	处置策略文本内容
DISPOSAL_RESULT	处置结果
REF_QXFL_ID	缺陷等级分类关联th_robot.t_th_st_alarminfo_qxfl表主键
STATION_AREA_NAME	变电站所属区域的名称
IS_REAL_EVENT	是否为真实事件(0否1是)
REMARK	备注
SENDMEMS_NUM	消息推送次数
SENDMEMS_LASTTIME	最后一次消息推送时间
RESP_AREA_EXP	扩展责任分区编码
TYPE	判断是哪个类型0每日简报 1辅控
SECONDMEMS_NUM	二次短信提醒
COM_RESULT	研判结果(0:研判正确/1：研判错误)
REMARK_TIME	填写时间
CZMX_IDS	操作明细id集合
STATUS_IDS	用于存储中间状态的id


2.监控大数据故障表
T_OPERATIONAL_EVENT_NINGBO 
字段名	含义
ID	主键
CREATE_TIME	创建时间
STATION_ID	电站id
STATION_NAME	电站名称
BAY_NAME	间隔名称
EQUIP_ID	设备id
EQUIP_NAME	设备名称
VLTY_ID	电压等级id
VLTY_ID_ST	
EVENT_CONTENT	事件内容
CHZ_TYPE	重合闸类型
OCCUR_TIME	发生时间
AREANO	区域编码
RESP_AREA	责任区
END_TIME	结束时间
EQUIP_TYPE	设备类型
LAST_TIME	最后发生时间
FAC_ID	变电站ID(EMS)
BAY_ID	间隔ID(EMS)
DATA_JSON	原始数据字符串


3.故障二次分析结果表
T_ACCIDENT_SECOND_ANALYSIS
字段名	含义
ID	主键
ACCIDENT_ID	序号
WEATHER_INFO	气候信息
PROTECT_INFO	保护信息
FAULT_WAVE_INFO	故障录波信息
EQUIP_DESC	设备台账信息及线路故障定位
LIGHTNING_INFO	雷电信息
LOADRATE_INFO	负荷信息
OTHER_INFO	其他信息
ANALYSIS_STATUS	分析结果(0:分析后未发送，1：分析完毕（内容存在缺失），2.分析完毕（内容完整），3.分析完毕（超时不在分析）)
AREANO	区域编码
CREATE_USER_ID	创建人ID
CREATE_USER_NAME	创建人
CREATE_TIME	创建时间;默认系统时间
LAST_UPDATE_TIME	最后更新时间;默认系统时间
IS_DEL	是否删除;默认值0
REMARK	备注


4.生产指挥中心值班日志记录表
T_TH_LOGBOOK
字段名	含义
ID	主键
EVENT_TYPE	事件类型
EVENT_DATE	日期
EVENT_TIME	时间
STATION_NAME	变电站
STATION_ID	变电站ID
VOLTAGE	设备电压等级
BAY_NAME	设备间隔（名称）
BAY_ID	设备ID
TRIP_DEVICE_CLASS	跳闸设备分类
TRIP_CAUSE_CLASS	跳闸原因分类
COINCIDENCE	重合情况
FAULT_BRIE	故障简报
OSCILLOGRAPH	故障录波
FAULT_DEVICE	缺陷设备分类
FAULT_LEVEL	缺陷等级
ISSUE_TYPE	问题类型
VENDER	厂家
CONTENT	内容
ISLEGACY	是否遗留
FOLLOW_UP	后续措施
REMARKS	备注
DUTYMAN_NAME	值班人
CREATETIME	创建时间
CREATEMAN	创建人
AREANO	区域编码
ISDEL	是否删除
STAUTS	流程状态
SBDL	设备大类
SBFL	设备分类
HISQX	以前的缺陷处理情况
XQDW	消缺单位
LAST_UPDATE_TIME	最后更新时间
ISYJZHS	是否移交综合室
IFUPDATE	是否更新


5.检修记录单表（实时）
REAL_JXDATA
字段名	含义
work_ticket_no	工作票号
working_person	工作人员
job_description	工作内容
work_team	工作班组
work_date	工作时间
equip	设备
completion_status	完成情况
registration_person	登记人
registration_time	登记时间
registration_team	登记班组
acceptor	验收人
acceptence_opinion	验收意见
date_of_acceptance	验收日期
work_leader	工作负责人名称
work_type_code	工作类型
dt	分区字段
create_time	创建时间
update_time	更新时间
id	自增主键
insert_time	插入时间


6.管控平台天气信息
T_YJ_ZM_WEATHER
字段名	含义
ID	主键id
XJMC	县级名称
XJDM	县级代码
WEATHER_RESULT	天气结果
CREATE_TIME	创建时间
AREANO	区域编码
LAST_UPDATE_TIME	最新修改时间


7.管控平台-变电设备信息表
PMS_BD_EQUIP_INFO
字段名	含义
EQUIP_ID	设备ID
EQUIP_NAME	设备名称
YWDW_ID	运维单位ID
YWDW_NAME	运维单位
FAC_ID	变电站ID
FAC_NAME	变电站
IS_GIS	是否是GIS站
EQUIP_TYPE_ID	设备类型id
EQUIP_TYPE	设备类型
VLTY_ID	电压等级ID
VLTY_NAME	电压等级
BAY_ID	间隔类型
BAY_NAME	间隔单元
SCCJ_ID	生产厂家id
SCCJ_NAME	生产厂家
MODEL	型号
TYRQ	投运日期
CCRQ	出厂日期
QX_START	发生缺陷总数
QX_NOW	现存缺陷总数
ZXJCGJS	在线监控告警数
PJYCS	评价异常数
EQUIP_ADD_TYPE	设备增加方式
CREATEUSER	创建人
CREATETIME	创建时间
LAST_UPDATE_TIME	最新修改时间
AREANO	区域编码
ISDEL	逻辑删除0否1是


8.管控平台-输电设备信息
PMS_SD_EQUIP_INFO
字段名	含义
LINE_ID	线路ID
LINE_NAME	线路名称
YWDW_ID	运维单位ID
YWDW_NAME	运维单位
YWBZ_ID	运维班组ID
YWBZ_NAME	运维班组
VLTY_ID	电压等级ID
VLTY_NAME	电压等级
TYRQ	投运日期
LENGTH	长度
ASSET_UNIT	资产单位
METHOD	架设方式
POS_START	起始位置
POS_END	终点位置
NAT_ASSET	资产性质
FAC_START_ID	起始变电站id
FAC_START	起始变电站
FAC_END_ID	终点变电站id
FAC_END	终点变电站
CREATEUSER	创建人
CREATETIME	创建时间
LAST_UPDATE_TIME	最新修改时间
AREANO	区域编码
ISDEL	逻辑删除0否1是


9.管控平台-变电站信息
PMS_FAC_INFO
字段名	含义
FAC_ID	变电站ID
FAC_NAME	变电站名称
SSDW_ID	所属单位ID
SSDW_NAME	所属单位
YWDW_ID	运维单位ID
YWDW_NAME	运维单位
YWZ_ID	运维站ID
YWZ_NAME	运维站
VLTY_ID	电压等级ID
VLTY_NAME	电压等级
FAC_TYPE	变电站类型
WHDJ	污秽等级
IS_ZNZ	是否是智能站
IS_GIS	是否是GIS站
TYRQ	投运日期
IS_HNZ	是否是户内站
CREATEUSER	创建人
CREATETIME	创建时间
LAST_UPDATE_TIME	最新修改时间
AREANO	区域编码
ISDEL	逻辑删除0否1是


10.变电设备清单表
NUSP_FAC_EQUIPMENT
字段名	含义
XUHAO	序号
YWDW	运维单位
FAC_ID	变电站ID
FAC_NAME	变电站名称
SFGIS	是否GIS站
SBLX	设备类型
DYDJ	电压等级
BAY_ID	间隔ID
BAY_NAME	间隔名称
EQUIP_ID	设备ID
EQUIP_NAME	设备名称
TYRQ	投运日期
CZRQ	出厂日期
SCCJ	生产厂家
XH	型号
SBZJFS	设备增加方式
YXBH	运行编号
SSDS	所属地市
XJDW	县局单位
WHBZ	维护班组
SBZT	设备状态
XB	相别
XS	相数
ZJTYRQ	最近投运日期
SYHJ	使用环境
SFDW	是否代维
XINGH	型号
SHCCJ	生产厂家
CCBH	出厂编号
CPDH	产品代号
EDDY	额定电压
EDDL	额定电流
EDPL	额定频率
JGXS	结构型式
CZJGXS	操作机构型式
MHJZ	灭弧介质
EDJYSP	额定绝缘水平
EDDLDLDKCS	额定短路电流开断次数
EDDLGHDL	额定短路关合电流（KA）
DWDDL	动稳定电流
RWDDL	热稳定电流
EDDLCXSJ	额定短路持续时间
DKSL	断口数量
TGBDJL	套管爬电距离（MM）
TGGFJL	套管干弧距离（MM）
DLLBJL	对地泄漏比距（CM/KV）
JXSM	机械寿命（次）
HZDZ	合闸电阻（Ω）
HZSJ	合闸时间
FZSJ	分闸时间
FJSDJSJ	分（金属短接）时间（MS）
SF6	SF6气体额定压力（MPA）
ZCDW	资产单位
ZCXZ	资产性质
ZCBH	资产编码
GCBH	工程编号
GCMC	工程名称
SWID	实物ID
PMBM	PM编码
WBSBM	WBS编码


11.PMS设备信息
T_YJ_PMS_DEVICE
字段名	含义
ID	主键
NAME	设备名称
EQUIP_TYPE	设备类型
CORRECTED_NAME	修改过的名称
SUBSTATION	所属变电站
WORK_DATE	投运日期
PRODUCER	生产厂家
MODEL	设备型号
TYPE	设备类型
STATUS	运行状态  投运/退役
CREATE_TIME	创建时间
AREANO	区域编码
LAST_UPDATE_TIME	最新修改时间


12.PMS变电站信息
T_YJ_PMS_TREE_SUBSTATION
字段名	含义
COMPANY	所属供电公司
COMPANY_ID	所属供电公司ID
COMPANY_ITEM_TYPE	
VOLTAGE	电压等级
VOLTAGE_ID	电压等级ID
VOLTAGE_ITEM_TYPE	
SUBSTATION	变电站名称
SUBSTATION_ID	变电站ID
SUBSTATION_ITEM_TYPE	
AREANO	区域编码
LAST_UPDATE_TIME	最新修改时间
""",
        )
    )

    # 确定回复节点
    graph.add_node(
        id="confirm_reply_3",
        position={'x': -1907.0064271975132, 'y': 1609.8168871492817},
        state=ConfirmReplyState(
            text="不同设备类型正在开发中，敬请期待！",
        )
    )

    # 确定回复节点
    graph.add_node(
        id="confirm_reply_4",
        position={'x': -1052.8584732500724, 'y': 2462.5328826638624},
        state=ConfirmReplyState(
            text="断路器",
        )
    )

    # 用户提问节点
    graph.add_node(
        id="user_input",
        position={'x': -1538.2659872819645, 'y': 2527.411173098657},
        state=QuestionInputState(
            inputText=True,
            uploadFile=False,
            uploadPicture=False,
            fileUpload=False,
            fileContrast=False,
            initialInput=False,
        )
    )

    # 智能对话节点
    graph.add_node(
        id="ai_chat_2",
        position={'x': -861.8967916173706, 'y': 187.8637781812438},
        state=AiChatState(
            model="oneapi-siliconflow:deepseek-ai/DeepSeek-R1",
            systemPrompt="""你是一个地名匹配助手。
任务：从预设列表中匹配最合适的地名。
预设列表：【本部, 鄞州, 余姚, 慈溪, 宁海, 象山, 宁波】
要求：
1. 严格从预设列表中选择。
2. 只输出匹配到的地名，不多任何一个字。
3. 如果没有完全匹配的选项，请输出“无匹配”。


用户输入: {{text}}

输出：匹配好的地名

示例：
输入： 慈溪市 输出：慈溪""",
            quotePrompt="",
            isvisible=False,
            temperature=0,
            maxToken=4096,
        )
    )

    # 确定回复节点
    graph.add_node(
        id="confirm_reply_5",
        position={'x': 1338.9603325056646, 'y': 114.82823978954264},
        state=ConfirmReplyState(
            isvisible=False,
            text="""SELECT
  SBLX AS "设备类型",
  EQUIP_NAME AS "设备名称",
  SCCJ AS "生产厂家",
  TYRQ AS "投运日期"
FROM nusp_fac_equipment
WHERE xjdw LIKE {{geo}};""",
        )
    )

    # 代码块节点
    graph.add_node(
        id="code_fragment_1",
        position={'x': -381.7209874850624, 'y': 79.50333187259804},
        state=CodeFragmentState(
            code="""import re

def userFunction(params):
    def extract_after_think(info):
        # 使用正则表达式匹配第一个</think>之后的所有内容
        match = re.search(r'</think>(.*)', info, re.DOTALL)
        if match:
            return match.group(1).strip()  # 返回匹配到的内容并去除首尾空白
        else:
            return info
            
    result = {}
    try:
        # 提取内容并保存到result中
         temp = extract_after_think(params['input_key'])
         temprp = temp.replace('\\n', '')
         result['output_key'] = "'%" + temprp +"%'"
    except Exception as e:
        # 捕获可能的异常并记录错误信息
        result['error'] = str(e)

    return result""",
        )
    )

    # 添加记忆变量节点
    graph.add_node(
        id="memory_var_1",
        position={'x': 187.41334017570892, 'y': 131.6960333509331},
        state=AddMemoryVariableState(
            variables={'geo': 'string'},
        )
    )

    # 确定回复节点
    graph.add_node(
        id="confirm_reply_6",
        position={'x': 927.162774046186, 'y': 129.98973649196236},
        state=ConfirmReplyState(
            isvisible=False,
            text="您可以输入希望用户看到的内容，当触发条件判定成立，将显示您输入的内容。",
        )
    )

    # 确定回复节点
    graph.add_node(
        id="confirm_reply_7",
        position={'x': 1638.2634085153472, 'y': -522.0183931941859},
        state=ConfirmReplyState(
            text="基本信息如下",
        )
    )

    # 确定回复节点
    graph.add_node(
        id="confirm_reply_8",
        position={'x': 1067.1535700820075, 'y': 890.5267338164495},
        state=ConfirmReplyState(
            isvisible=False,
            text="""SELECT
CONTENT as '故障事件内容',
OCCUR_TIME as '故障发生时间',
BUSI_TYPE_NAME as '故障业务类型名称',
BUSI_TYPE_SUBCLASS as '故障业务子类名称'
FROM
    T_EVENT_ZNJS_DWXXJS t1
WHERE
    t1.EQUIP_ID in (select `EQUIP_ID` from nusp_fac_equipment 
where xjdw like {{geo}});""",
        )
    )

    # 确定回复节点
    graph.add_node(
        id="confirm_reply_9",
        position={'x': 1461.8012992739357, 'y': 1329.7203589787257},
        state=ConfirmReplyState(
            text="发生的历史故障如下",
        )
    )

    # 信息分类节点
    info_class_labels = {'9f4da034-1f5c-44d4-9345-1cb53dfcbd61': '查询地区设备清单', '1c8384d9-2910-4ae5-bb36-7b2853be955a': '不同设备'}
    graph.add_node(
        id="info_class",
        position={'x': -1479.7489037112273, 'y': 151.55533226592678},
        state=InfoClassState(
            model="qwen2.5-72b-instruct",
            quotePrompt="""你是电网行业问数智能体的二分类路由器。你的唯一任务：根据用户输入判定应走哪一个流程，并且只输出对应代号。

输出代号（严格二选一，且必须输出其一）：
查询地区设备清单
不同设备：指设备事件/缺陷/跳闸等记录或统计
决策优先级（从高到低，命中即停）：
事件/统计关键词命中 → 不同设备。 事件/统计关键词示例（包含但不限于）：跳闸、缺陷、故障、检修、告警、录波、重合、统计、次数、对比、比较、趋势、最近、近一周/上月/季度、原因、厂家、是否遗留、是否移交综合室、值班人、记录、日志、处理、事故。
清单/罗列关键词命中 → 查询地区设备清单。 清单关键词示例：清单、名单、有哪些、列出、罗列、一览、台账、盘点、汇总、分布、名录、列表。
地名/站名/区域线索命中（即使是冷门或不在词典中）→ 查询地区设备清单。 判定启发式（任一满足即可视为区域线索）：
后缀/词形：片区、区、市、县、旗、州、盟、镇、乡、村、园、园区、街、道、路、巷、岭、山、岛、湾、洲、滩、港、口、桥、湖、河、江、水库、矿、厂 等；
设施/站点：变电站、开闭所、运维站、开关站、枢纽、站、所、#×主变（如“#1主变”常与站点/设备清单相关）；
编码/别称：看似地名或站/所代号的短词/缩写/拼音/字母数字组合（如“GZ-01”“DF变”“临江新城”“洪泽洲”），即使很冷门也按区域线索处理；
含“kV + 站/所”（如“110kV××站”）。
模糊/极短输入的兜底：当未命中1)与2)，且输入很短或语义不明（如仅16个汉字或13个词），一律 → 查询地区设备清单。
若仍无法判断（几乎不可能出现），绝不空输出，强制 → 查询地区设备清单。
特殊歧义处理：
仅出现设备类别或设备名（如“主变”“断路器”“XX线路”）但无事件/统计词且无清单词：默认 → 查询地区设备清单（视为想看该类设备分布/清单）。
同时出现清单词与事件词时：以事件词优先 → 不同设备。
输出规范（务必遵守）：
严格只选择 查询地区设备清单 或 不同设备 之一。
不输出任何其他字符、标点、空格、换行、前后缀或解释。""",
            labels=info_class_labels,
        )
    )

    # 确定回复节点
    graph.add_node(
        id="confirm_reply_10",
        position={'x': 1954.5790409016909, 'y': 156.83070120629836},
        state=ConfirmReplyState(
            isvisible=False,
            text="""SELECT
  SBLX AS "设备类型",
  EQUIP_NAME AS "设备名称",
  SCCJ AS "生产厂家",
  TYRQ AS "投运日期"
FROM nusp_fac_equipment
WHERE xjdw LIKE '%慈溪%';""",
        )
    )

    # 知识库搜索节点
    graph.add_node(
        id="kb_search",
        position={'x': 2520.5119615134663, 'y': 117.09506828560988},
        state=KnowledgeSearchState(
            similarity=0.2,
            topK=20,
            rerankModelType="oneapi-xinference:bce-rerank",
        )
    )

    # 添加连接边
    graph.add_edge("confirm_reply", "ai_chat", "finish", "switchAny")
    graph.add_edge("ai_chat", "code_fragment", "finish", "switchAny")
    graph.add_edge("ai_chat", "code_fragment", "answerText", "input_key")
    graph.add_edge("confirm_reply", "memory_var", "text", "sql_structure")
    graph.add_edge("ai_chat_2", "code_fragment_1", "finish", "switchAny")
    graph.add_edge("ai_chat_2", "code_fragment_1", "answerText", "input_key")
    graph.add_edge("code_fragment_1", "memory_var_1", "output_key", "geo")
    graph.add_edge("code_fragment_1", "confirm_reply_6", "finish", "switchAny")
    graph.add_edge("code_fragment_1", "confirm_reply_6", "output_key", "text")
    graph.add_edge("confirm_reply_6", "confirm_reply_5", "finish", "switchAny")
    graph.add_edge("confirm_reply_5", "confirm_reply_7", "finish", "switchAny")
    graph.add_edge("confirm_reply_8", "confirm_reply_9", "finish", "switchAny")
    graph.add_edge("info_class", "ai_chat_2", list(info_class_labels.keys())[0], "switchAny")
    graph.add_edge(START, "info_class", "userChatInput", "text")
    graph.add_edge(START, "ai_chat_2", "userChatInput", "text")
    graph.add_edge("info_class", "confirm_reply_3", list(info_class_labels.keys())[1], "switchAny")
    graph.add_edge("confirm_reply_7", "confirm_reply_10", "finish", "switchAny")
    graph.add_edge(START, "ai_chat_2", "finish", "switchAny")
    graph.add_edge("confirm_reply_10", "kb_search", "finish", "switchAny")
    graph.add_edge("confirm_reply_5", "kb_search", "text", "text")
    graph.add_edge("kb_search", "confirm_reply_8", "finish", "switchAny")

    # 编译
    graph.compile(
        name="从json导出的工作流",
        intro="",
        category="自动生成",
        prologue="您好！我是从json导出的工作流"
    )

if __name__ == "__main__":
    main()