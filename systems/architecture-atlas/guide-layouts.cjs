/* Authored reading paths, not additional semantic truth. Each selected relation
 * must resolve to an actual model edge. Short verbs are display paraphrases;
 * the complete original action and evidence remain in the full plate below.
 * Row position belongs to this explanatory sibling, not to runtime topology.
 */
const chain=(ids,verbs,note)=>({rows:[ids.slice(0,3),ids.slice(3)].filter(r=>r.length),edges:verbs.map((label,i)=>[ids[i],ids[i+1],label]),note});
module.exports={
 'mem0':{
  overview:chain(['extract','vector_store','select','results','app'],['追加事实','选择候选','返回条目','交回调用者'],'从抽取后的事实进入应用；托管 client 与诊断出站另见完整图。'),
  flow:chain(['api','scope','mode','context','llm','batch'],['规范化','选择路径','默认 infer','请求抽取','解析模型输出'],'这里展开默认抽取路径；raw / procedural 分支、写入与查询见完整图。'),
  revision:{rows:[['update','vector_store','select'],['entity_cleanup','entity_store','results']],edges:[['update','vector_store','覆盖主事实'],['vector_store','select','读取当前条目'],['select','results','返回可见结果'],['update','entity_cleanup','文本变化时清旧建新'],['entity_cleanup','entity_store','重建实体关联']],note:'显式 update 的主事实与实体关联分支；history、delete、reset 的不同边界见下方。'}
 },
 'graphiti':{
  overview:chain(['mediation','graph_driver','facts','search','projection','generation'],['交付解析对象','保存事实与时间','召回事实','返回图对象','示例投影事实串'],'图中事实经检索与应用投影进入模型；投影可能舍去时间与来源。'),
  flow:chain(['caller','ingest','previous','node_extract','edge_resolve','hydrate'],['提交 episode','读取历史上下文','消歧与抽取','解析关系','更新属性与摘要'],'写入阶段的顺序导读；批量保存与独立查询链继续见下方。'),
  revision:{rows:[['edge_resolve','exact','conflict_llm'],['hydrate','temporal','facts']],edges:[['edge_resolve','exact','比较同文同端点'],['exact','conflict_llm','非 exact 请求裁决'],['conflict_llm','temporal','给出候选索引'],['temporal','facts','写失效时间'],['exact','facts','exact 复用旧边'],['edge_resolve','hydrate','仅新边更新摘要']],note:'同文复用、语义冲突和派生摘要有不同更新条件；删除 episode 是另一支路。'}
 },
 'letta':{
  overview:chain(['memfs','compiler','compiled','bridge','model','edit'],['读已提交 HEAD','保存编译状态','装配 prompt','交付本次 context','模型选择工具'],'先读 committed memory，再看模型能否选择 memory tool；工具提交会回到 MemFS。'),
  flow:chain(['entry','backend','active','bridge','model','edit'],['进入 turn','加入活动消息','提供当前消息','发送 context','可选工具调用'],'这是 local turn 的使用路径；MemFS 编译与后台 reflection 分别补入和修订状态。'),
  revision:chain(['edit','working','memfs','check','compiler','compiled'],['编辑工作区','stage 后 commit','读取 revision','变更才重编译','保存新 prompt'],'修改只有进入 Git HEAD 才被编译；历史 transcript 和旧版本不自动清除。')
 },
 'lmc-5':{
  overview:{rows:[['min_curated','min_read','runtime'],['pg_curated','pipeline']],edges:[['min_curated','min_read','live 候选与 M'],['min_read','runtime','返回 recall'],['pg_curated','pipeline','curated 候选'],['pipeline','runtime','注入来源分层文本']],note:'Minimal 与 Production 是两条独立实现路径，均交给外部 runtime 使用。'},
  flow:chain(['min_raw','min_consolidate','min_chunks','min_hippo','min_curated','min_read'],['整理事件窗口','绑定来源块','构造候选原子','apply 写 review','仅 live 可被选中'],'Minimal 从 raw 到候选再到读取；review 不等于已经 live，Production 接线另列。'),
  revision:{rows:[['runtime','e_guard','pg_curated'],['min_curated','min_audit','min_pending']],edges:[['runtime','e_guard','提交 E 作者信息'],['e_guard','pg_curated','首写可入；拒绝改 E'],['runtime','min_curated','同 fact_key 替代'],['min_curated','min_audit','读取冲突候选'],['min_audit','min_pending','仅登记 pending']],note:'上下两条实现分别看：E 的数据库约束与 Minimal 的替代／待审；不是统一自动修订链。'}
 },
 'tideline-memory':{
  overview:chain(['sqlite','provider','context_frame','current_model'],['读取身份与记忆','生成自动块','host 交付上下文'],'SQLite 当前状态经 provider 进入模型；显式 MCP、epilogue 与维护是并行路径。'),
  flow:chain(['runtime','capture','context','epilogue','narratives','auto_recall'],['同步或补录','保存角色片段','结束时选材料','成功写叙事','选择原始候选'],'这条路径串起采集、会话固化和自动召回；DREAM 与显式搜索使用不同入口。'),
  revision:{labelOffsets:{'memory_amend>amendment_vectors':[0,-32]},rows:[['memory_amend','amendments','explicit_search'],['amendment_vectors','trajectories','auto_recall']],edges:[['memory_amend','amendments','先提交修订'],['amendments','explicit_search','完整修订回显'],['memory_amend','amendment_vectors','随后尽力补向量'],['memory_amend','trajectories','重建 mech 轨迹'],['trajectories','auto_recall','T1 命中才附带']],note:'修订、补向量、轨迹和消费是分步路径；自动选择仍依赖原叙事。'}
 },
 'aelios':{
  overview:chain(['memories','recall','gateway','upstream'],['读取 D1 当前事实','返回原文补丁','转发含补丁请求'],'当前事实通过受预算约束的补丁进入聊天上游；Client 仍拥有工具循环。'),
  flow:chain(['client','gateway','recall','selector','patch','upstream'],['发送请求','提供本轮 query','合并各空间','筛选少量原文','追加 user 尾部'],'即时召回路径；原话保存、队列与夜间候选形成另一个写回循环。'),
  revision:{rows:[['candidates','judge','mutate'],['memories','vectors','extensions']],edges:[['candidates','judge','提交提案'],['judge','mutate','批准 add / update'],['mutate','memories','原改或建立版本链'],['mutate','vectors','新索引／旧下架'],['mutate','extensions','建立 supersedes']],note:'候选批准后分别改变事实版本、索引和关系；删除与保留期限另有路径。'}
 },
 'hindsight':{
  overview:chain(['retain','facts','recall','integration','app'],['保存事实与 links','供四路检索','返回结构化记忆','注入应用上下文'],'已保存的事实通过 recall 交回应用；后台 observations 与 reflect 是不同支路。'),
  flow:chain(['api','auth','queue','worker','retain','facts'],['校验请求','异步返回 operation','claim 任务','执行 retain','保存原文与事实'],'这里展开 async retain；同步 retain 直接等待，后台 consolidation 与使用路径另列。'),
  revision:chain(['edit','cleanup','queue','worker','consolidator','observations'],['使旧来源失效','条件满足才重排','claim / retry','重新 consolidation','提交派生观察'],'编辑后清理并重建 observation 的路径；mental model 刷新还有独立 trigger 与 scope。')
 },
 'openviking':{
  overview:chain(['api','retrieve','assemble','context','caller'],['query 与范围','交付候选','按预算渲染','交给 agent'],'检索与预算组装把内容交给调用方；assemble 按 tier 从文件读取正文。'),
  flow:chain(['session','queue','extract','files','assemble','context'],['归档后入队','恢复 Phase 2','合并后写文件','按需读取正文','预算内 render'],'会话提交到记忆文件、再到使用的一条阅读路径；摘要与向量异步派生。'),
  revision:{rows:[['edit','write','files'],['freshness','queue','summary']],edges:[['edit','write','请求 create / replace'],['write','files','权限与锁后写入'],['write','freshness','触发后处理策略'],['freshness','queue','立即刷新或 pending'],['queue','summary','消费后重建摘要']],note:'当前文件先写入，派生摘要随后刷新；向量更新、删除与 restore 的阶段另列。'}
 },
 'langmem':{
  overview:{rows:[['agent','search','store'],['manage','context']],edges:[['agent','search','按需检索工具'],['search','store','限定 namespace 搜索'],['search','context','序列化命中'],['context','agent','交付上下文'],['agent','manage','选择变更动作'],['manage','store','put 或 delete']],note:'热路径的写入、搜索和返回上下文；Store 的耐久性与索引由 adapter 决定。'},
  flow:chain(['input','executor','manager','select','extractor','delta'],['提交 payload','延迟到期后调用','检索与候选选择','供给选中对象','无 phase 时形成差异'],'展开本地延迟整理路径；可选 phases 和最终 Store 写回继续见下方。'),
  revision:chain(['manager','select','extractor','delta','store','backend'],['搜索有限候选','仅选中对象参与','提出对象差异','put / delete','委托实际删除语义'],'模型修订限于选中的 existing；prompt 与已用 context 没有自动失效传播。')
 },
 'a-mem':{
  overview:chain(['evolve','notes','expand','prompt','controller','output'],['保存并改写对象','读取对象与 links','拼 raw context','发送 QA prompt','解析预测与评估'],'当前笔记与单跳链接进入 QA；索引、磁盘 cache 和 canonical 对象仍是不同状态。'),
  flow:chain(['harness','add','construct','evolve','notes','index'],['逐轮同步摄入','构造 UUID note','供演化判断','更新邻居／存新 note','追加索引文档'],'同步写入顺序；threshold 全量重建与 question 检索各有独立分支。'),
  revision:chain(['controller','update','notes','rebuild','index','cache'],['选择 UPDATE 结果','原位改 context / tags','供重建读取','替换索引','分别保存缓存'],'对象改写到派生索引与缓存；是否启动重建仍受 threshold 分支约束。')
 }
};
