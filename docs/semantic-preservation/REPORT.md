# BB369TECH 数字资产与语义保留验收

日期：2026-10-30（洛杉矶）

**结论：静态语义保留 PASS；整体验收仍为 RELEASE HOLD，不申请正式合并。**

本次是原站视觉与体验升级。主基线为正式 main `b553356528d097632f4f30da40258af4501f8212`，并独立读取了正式站 24 个原有 HTML 入口的浏览器 DOM。正式站标题、Canonical、Robots 与 main 对应页面一致；6 个既有别名入口仍进入原来的目标页。

最新稳定版汇总：原 Customer access 主题完整移到 Services，因此3条镜像/生产观察记录由 PRESERVED 转为 RELOCATED；没有删除。整体视觉与运行验收见 [稳定架构报告](../stable-architecture/REPORT.md)。

## 对照结果

| 标记 | 数量 | 含义 |
|---|---:|---|
| PRESERVED | 2051 | 原页面信息、目标链接、元数据或文件内容完整保留 |
| RELOCATED | 333 | 信息或位置调整，原文及稳定 HTML 访问仍保留 |
| IMPROVED | 25 | 已验证的排版、表达、可访问性或新增对应页面改进 |
| REMOVED | 0 | 未发现未获批准的语义／原网址／受保护数据删除 |

以上是 2,409 条对照记录，**不是 2,409 项互不重复的独立资产**。清单包含根目录与 public 镜像、导航和页脚中的重复链接，以及生产 DOM 的独立交叉核查。完整 Before / After 见 BEFORE-AFTER.csv；逐 URL 对照见 URL-BEFORE-AFTER.csv。

## 关键 Before / After

| 项目 | Before（正式 main／生产） | After（隔离候选） | 标记 |
|---|---|---|---|
| 英文首页主标题 | Clear digital tools for real business work. | 首页以网站与业务软件为主标题；旧标题原文仍在 /services.html | RELOCATED；新版主标题单列 IMPROVED |
| 中文首页主标题 | 让客户更容易找到、了解并联系你的企业。 | 新首页明确网站与软件；旧标题原文在 /zh/services.html | RELOCATED |
| 原首页快捷入口 | Improve customer access、Build or improve a business website、Discuss a business project 及完整说明 | 原文与 href 补回 /services.html 的静态 HTML | RELOCATED |
| 中文快捷入口 | 新建或改善企业网站、持续业务支持、咨询定制需求及完整说明 | 原文与 href 补回 /zh/services.html | RELOCATED |
| View Services | 首页按钮指向 /services.html | /contact.html 保留同名、同目标的可点击入口 | RELOCATED |
| 详细 Services／Products／What We Do | 首页重复展示 | 进入既有 Services／Products／Industries 页面，逐段原文核对 | RELOCATED |
| FAQ、行业、服务及原案例说明 | 原有 HTML 正文 | 同页保留或明确迁入现有业务页；未改成图片或运行时 JS | PRESERVED / RELOCATED |
| Title、Description、Canonical、Schema、Open Graph | 原正式页面值 | 原值保留 | PRESERVED |
| Industries / Resources 导航 | 顶部导航与页脚 | 顶部简化，页脚继续直接链接；详细页面不删 | RELOCATED（位置）；链接地址 PRESERVED |
| Sitemap | 原正式 URL 列表 | 原条目保留，增加三个真实中文对应页 | IMPROVED |
| Hreflang | Company／Products／Projects 无中文对应声明 | 真实中文页面与互返链接已存在并通过检查 | IMPROVED |
| 404 Robots | 正式 main 仍为 index,follow | 先前隔离候选修正为 noindex,follow，未修改正式站 | IMPROVED，正式发布仍需审核 |
| 表单 | 原 action、method、字段、选项、隐私同意与提交脚本 | 原契约保留；新增 View Services 在表单之外 | PRESERVED |
| 机构数据与机器引用 | 根目录及 public 各自既有 JSON | 两份原文件及其中 URL 原样保留，不相互覆盖 | PRESERVED |
| 法律页面 | Privacy、Terms、Security 原正文 | 正文不改 | PRESERVED |
| 既有机器人 | 当前 main 与生产页面未发现可识别的机器人嵌入 | 未删除不存在的入口，也未宣称接通真实 AI | PRESERVED（基线状态） |

详细的 15 项补回记录见 RESTORED-FROM-MAIN.json。这里的“迁移”是调整段落所在位置，**不是更改或重定向原有公开 URL**。

## 视觉与功能回归

- 首页仍为 Hero、Services、Solutions、Featured Projects、Contact 五个区域。
- 3 项精选真实公开项目：SJ、Botánica de la Luz、Productos La Rosa；其余授权不足、转介性质或演示项目不冒充正式客户成果。
- 全部业务文字与案例说明为静态 HTML；案例图片仅作辅助。项目资料在构建时生成 HTML，不依赖浏览器运行 JavaScript 才能被读取。
- 12 项自动完整性测试 PASS；原有 4 项联系人恢复／后端隔离契约测试 PASS。
- 80 组全站响应式浏览器检查 PASS；补回语义后，3 个受影响页面 × 4 种宽度的 12 组补充检查 PASS。
- 12 条主要中英文路径菜单、Escape 和语言往返 PASS；6 组行业筛选 PASS。
- 8 组真实浏览器隔离表单成功／失败检查 PASS，真实网络提交为 0；原正式表单未发送测试咨询。

## 外部引用范围

已核对原 HTML 中的站外链接、机器可读 JSON 中的来源 URL、现有产品／平台入口及原机构数据记录。站内链接检查包含页脚与导航，并保留链接目标和可抓取的静态入口。

**未取得全网反向链接或搜索引擎索引的完整数据，不声称已核查所有站外提及或排名。** 此项需另行依据 Search Console、Bing 等实际数据核查。抓取、索引、检索引用与模型训练不是同一件事；本次不推断模型训练状态，也不承诺排名不变。

## 剩余验收门槛

1. 本轮未移动远端设计分支，因此尚未生成这一版新的 Cloudflare 预览。旧预览不能充当本轮验收结果。
2. 新隔离预览生成后，仍需检查真实 HTTP 状态、未知路径 404、重定向及部署版本一致性。
3. 真实邮件／CRM 投递和完整 Lighthouse／HTML 标准验证未通过本次隔离测试证明；无真实客户数据写入、付款或邮件发送。
4. 用户查看最终新预览并明确确认之前，不合并 main、不发布生产。

原 main、DNS、CRM、支付、后台、客户数据及生产部署均未修改。允许的下一步是单独确认是否更新隔离预览；这不是正式合并授权。
