# BB369TECH — Final Semantic Asset & Release Review

日期：2026-10-30（America/Los_Angeles）。结论：**候选通过本轮四项验收；RELEASE HOLD，等待人工审阅，不合并、不发布生产。**

## 版本与范围

- 正式 main：`b553356528d097632f4f30da40258af4501f8212`，未修改。
- 本轮开始的远程设计分支：`49c4bf9ce734b44694d1f33fcf85973cbe8b60d8`。
- 已完成视觉及语义候选：`bd748d122ffd3c7c394fd3a5bc9b767085e6656c`，本轮同步到原设计分支。
- 运行修复：`89219448627dcd7034152afaf3defaf5d45e79e5`、`29bd38e66e825176e60b99c1218c56a4df41e04e`。后续报告提交只含审查证据和复现脚本，运行内容相同。
- 分支：`design/premium-visual-baseline-20261030`。部署目录仍为 `public/`，Worker 名称和 previews 配置保留。
- 独立预览：https://design-premium-visual-baseline-2026-bb369tech-corporate-website.bb369-ai.workers.dev/
- 该 URL 为分支别名，会随该设计分支更新；版本以提交和 Cloudflare 构建记录为准。

本轮没有重新设计页面，没有新建仓库，也没有修改 DNS、生产流量、真实接收邮箱、CRM、付款和客户数据。

## Before / After

| 项目 | Before | After | 标记 |
|---|---|---|---|
| 首页业务折叠内容 | 远程旧候选 EN/ZH 共 6 个 details | 60 条标题/正文/链接逐项映射到 Services、Products、Industries 等可见静态 HTML；首页无 details，仍有导航/页脚入口 | RELOCATED；一个标题 IMPROVED |
| Business Website 标题 | Business Website | Services 的 Business Website Design，服务主题相同，增加明确修饰词 | IMPROVED |
| 原有独特内容及搜索语义 | 正式 main 的 36 份根目录/部署目录 HTML 和实际生产 24 URL | 2,409 条完整对照：2,054 PRESERVED、330 RELOCATED、25 IMPROVED、0 REMOVED | PASS |
| 真实案例 | 原有公开案例和平台发布记录 | 保留 SJ Home Improvement、Botánica de la Luz、Productos La Rosa 三项真实案例与截图，首页精选及 Projects 目录使用同一资料源 | IMPROVED（保留原条目） |
| 公司邮箱 | 官网、Schema、联系页、组织资料、平台商家登记均为 business@bb369tech.com | 原样保留；无邮箱替换 | PRESERVED |
| 原咨询接收路径 | https://bb369-sendgrid-api.onrender.com/api/corporate-inquiry | EN/ZH 表单 action、字段、topic 兼容、隐私同意及提交脚本不变 | PRESERVED |
| Cloudflare HTML 路由 | 默认可把 .html 临时转到无后缀路径 | assets.html_handling=none，旧 .html 直接返回 200，无服务器路径跳转 | IMPROVED |
| 根目录入口 | 依赖自动 HTML 路由 | public/_redirects 对 / 与 /zh/ 做内部 200 代理到原 index.html，地址不变、原 canonical 不变 | PRESERVED |
| 未知路径 | 原预览纯文本 404 | assets.not_found_handling=404-page；真实 HTTP 404，浏览器呈现已有 404 页面及 noindex,follow | IMPROVED |
| 历史别名 | 6 个原有 meta refresh 文档 | 原文档保留，真实浏览器跳转目标逐项正确；没有改为新的永久重定向 | PRESERVED |

上述 2,409 行包含镜像、重复导航和生产观察记录，不代表 2,409 个独立资产。本轮额外路由审查不冒充新增业务语义。原始逐项表见 `docs/semantic-preservation/BEFORE-AFTER.csv`；本轮折叠区详表为 `DETAILS-BEFORE-AFTER.json`，URL/HTTP 详表为 `HTTP-RESULTS.json`。

## 真实案例与公开范围

只读复查平台 main：`e1b2c679fe8c6d448840e435251ac73f6d415e3c`，与已审查基线相同。重新读取合并 PR #14、#33、#34 的授权/发布说明（完整证据见 CASE-AND-BUILD-EVIDENCE.json）。

- SJ：PR #14 明确记录用户批准公开 Featured；实际网站、产品分类及咨询入口可访问。
- La Rosa：PR #33 明确记录用户发布批准和公开索引；实际双语页面及询盘入口存在。
- Botánica：PR #34 发布已批准设计；实际双语门店页和单独产品目录存在。

只复用公开网站及实际页面功能，不声称客户评价、经营成果或单独签署了宣传授权书。未提供新的客户宣传协议。既有发布记录之外的权利范围仍需业务方确认。Henry、Golden Star、JL Curtains、Yiminle 等没有足够新增展示证据的项目不扩充；学校独立转介页不作为官方学校网站交付案例；Demo、超市和古董店未加入。完整 12 项清单见上一轮 CASE-AUDIT.md。

## 联系信息核查

- 所有实际业务 HTML、内嵌 Organization Schema、public/data/organization.json 和历史根目录 data/organization.json 的公司邮箱均为 business@bb369tech.com。
- 平台 merchant/index.html 使用相同邮箱。平台首页的公开公司电话为 +1 626 234 5998；官网现有公司资料未列电话，不据此擅自新增或替换号码。
- 公司名称 BB369TECH、洛杉矶/加州描述与平台业务入口无相互冲突项。客户门店各自地址、电话不属于公司联系方式，不统一覆盖。
- **NOT VERIFIED：**后端实际路由到哪个收件箱、SMTP/SendGrid 投递、自动回复、CRM 落库。只核查公开配置，不查看秘密、不触发正式提交；未将公开邮箱一致性等同于邮件成功投递。

## 本轮测试

| 项目 | 结果 | 证据/边界 |
|---|---|---|
| 自动化前端/功能/语义保留 | PASS | 13 项，STATIC-TESTS.txt；完整基线逐项核查再次通过 |
| 原折叠区直接可见内容 | PASS | 60 项主题记录有静态对应内容；另对全部文本节点及链接进行防丢核查，见 DETAILS-ALL-TEXT-AND-LINKS.json |
| Cloudflare 预览构建 | PASS | 29bd38e6 构建成功；不是仅凭构建作验收 |
| HTTP GET | PASS | 71 个请求，0 传输错误；预览 32 项：31 个 200 和一个正确未知地址 404 |
| 旧 .html、根目录、中英文 | PASS | 原路径直接返回，无新增服务器重定向；新增 3 个中文页面预览 200，生产尚为 404，未冒称已生产发布 |
| 真实 HTTP 404 | PASS | GET 状态 404、预览 X-Robots-Tag:noindex；真实浏览器标题/正文为原错误页，meta noindex,follow，返回首页按钮正常 |
| 历史别名重定向 | PASS | credentials→company、media/news→resources、partners→contact、platforms→products、why-us→company，浏览器逐项验证 |
| 手机布局 | PASS | 新 Cloudflare 预览 EN/ZH 首页、案例、联系 6 页，无横向溢出、单一 h1；390px 框架，滚动条占用时内容宽375px |
| 菜单和语言切换 | PASS | 手机菜单展开/ESC 关闭，中文回英文地址/语言正确 |
| 真实浏览器咨询模拟 | PASS | EN/ZH 共8例：成功、503、200但success=false、网络异常；成功清空输入、失败保留输入，按钮恢复，字段/隐私/topic正确；0真实请求 |
| 浏览器控制台 | PASS | 预览网站自身无观察到的 warn/error；浏览器扩展 metadata 日志单列排除，不声称浏览器所有扩展无错误 |
| 重要业务入口 | PASS | 三个真实案例、商家咨询、Business Website 及 monthly-support、工具入口 GET200；未执行付款或客户数据写入 |
| 原视觉多尺寸验收 | PASS（复用同内容证据） | 上轮本地20页×4宽度80项及修复后12项记录保留；本轮不重新设计、不改变页面/CSS |
| 最新手机截图文件 | NOT VERIFIED | 新截图捕获超时；手机 DOM/布局验收通过，旧候选同内容手机截图保留并标明来源 |
| 真实收件、CRM、付款 | NOT VERIFIED | 本轮明确不做真实提交或付款 |
| 搜索排名、全网反向引用、完整 Lighthouse/标准验证 | NOT VERIFIED | 不作不变承诺，也不把检索/抓取等同模型训练 |

HTTP 结果采集端对 404 的响应体显示纯文本，与浏览器观察不同；因此不从该采集端正文推断定制错误页缺失。404 状态来自真实 GET，定制页面正文/meta 来自独立真实浏览器观察，二者证据分别保留。

隔离预览统一带平台 X-Robots-Tag:noindex，HTML canonical 仍指向正式域名。这是预览隔离，不应把预览索引指令反写到正式业务页面。原 robots.txt、Sitemap、FAQ、法律正文和业务接口未改；原 404 页的 noindex 修正已在候选中保留。

## 变更和回滚

运行代码补回上述原有标签，并增加必要路由设置（wrangler.jsonc）和 public/_redirects，增加测试断言；其余为已完成的候选同步及本轮报告/复现脚本。本轮只在 Services 可见区补回原折叠区的 By consultation 标签（public/ 及根目录镜像），没有更改页面布局或 CSS；新增全量文本节点/链接防丢检查。

官方配置依据：
- https://github.com/cloudflare/cloudflare-docs/blob/production/src/content/docs/workers/wrangler/configuration.mdx
- https://github.com/cloudflare/cloudflare-docs/blob/production/src/content/docs/workers/static-assets/routing/advanced/html-handling.mdx
- https://github.com/cloudflare/cloudflare-docs/blob/production/src/content/docs/workers/static-assets/redirects.mdx

如需回退本轮路由修复，在设计分支使用 revert 8921944 和 29bd38e，保留修复前候选 bd748d1；不得对 main 使用 reset/force push。生产未变，因此无生产回滚操作。完整旧候选回滚方案见 docs/final-visual/ROLLBACK.md。

**发布判断：可供人工审阅最终隔离预览；不自动合并、不部署生产。真实邮件/CRM验收若为正式发布门槛，需要隔离后端机制或人工另行授权。**
