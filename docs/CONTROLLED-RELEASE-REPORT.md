# BB369TECH — 受控发布与长期资产保护报告

2026-10-30（美国太平洋时间）。**决定：NO-GO / RELEASE HOLD。** 本轮只增加发布检查和资产契约，未修改任何 public 运行文件，没有新设计、新业务功能或 ZIP。未合并 main，未部署 Render、操作 DNS、修改数据库或环境变量、发送真实邮件。

## 固定版本与实际运行

| 对象 | 版本 / 核实状态 |
|---|---|
| 前端运行文件基线 | `ec9240b2c229515dce4016f9d3d3ddc0c587165c`；本轮 public 文件与其完全相同 |
| 正式 main | `5281d59c9d93e94d2862391060ffaae115f36008`，未变更 |
| 隔离后台候选 | `4a70df17dbd72727664e40893860739feb8ddfd4`，未部署 |
| Render 实际 live / 回退记录 | `1f4602b18e18da87af9a135fc36b0e55d9137cda`，`dep-dbe8ehgm7kps73d18st0` |
| Render 当前设置 | main、自动部署关闭、free 单实例；没有修改 |
| 数据库 | bb369-growth-db / PostgreSQL 18，available；没有读取客户记录、执行写入或迁移 |

### 后台候选范围不能混淆

GitHub 比较正式 1f4602b 与候选 4a70df1：4 个提交、22 个变动文件。生产差异包括 `server.js`、`growth/routes.js`、持久邮件账本与 CRM 捕获、聊天事务、预检脚本及测试文档；不是只有 CORS 两行。只有 4a70df1 相对其父候选的增量是 CORS 错误分类修正。发布前必须按完整候选范围审核，不能将其当作不涉及持久化的补丁。

## 两项阻碍现状

1. **机器图谱已修复并实测。** 正式和独立预览同一路径 `/data/organization.json` 均为 19,321 字节、四节点图谱，SHA-256 `391f76ae12888a73465ec31d7dd55bc67e7a8aa64dd044a8c4d195001e29c40a`。原节点 ID、关系、字段、所有原 URL/reference 保留；旧 public 简版逐字节归档于已提交的 two-blocker-resolution 文档。
2. **咨询已完成根因复现与隔离修正，未进入正式。** 原预览来源被 CORS 拒绝，错误又被正文解析中间件误报为资料无效 400。隔离候选转交既有 403 处理器；普通缺字段/隐私同意仍返回 400，安全来源、机器人拦截、限流、去重和邮件保护未取消。正式来源 OPTIONS 204，预览真实 OPTIONS 仍为旧策略的 400。隔离成功不能替代生产入库、收件或投递验证。

## 自动保护机制

`docs/asset-protection/manifest.json` 冻结 211 个路径（包含原 205 个及此前获准的归档/恢复测试），51 个 public 文件、27 个 HTML 页面，及 main、367cf29、ec9240b、既有 912 条语义证据的来源记录。记录 SHA-256、公开 URL/状态/Content-Type、Title、Description、Canonical、Hreflang、Robots、JSON-LD、四节点图谱、字段/关系、业务与 FAQ 语义、图片、链接、重定向、表单、平台入口和生产响应。211 包含 205，不是替换原清单。

`scripts/check-asset-manifest.py` 为可执行契约：缺历史文件、旧节点/ID/字段变化、矛盾的重复图谱 ID、原链接/图片丢失、SEO 或表单变化、旧直接可见语义变为折叠专有、未登记公开资产、源/镜像漂移均返回非零退出码。新增 JSON 字段或节点可通过；原有值不得被静默更改。新增公开文件必须登记追加契约。没有忽略失败或跳过保护的开关。

GitHub workflow `Asset Protection Gate` / job `asset-preservation` 在 main 的 PR、main 和现有设计分支 push 时运行。先从受信 base commit 读取旧检查器与旧清单验证，再执行候选检查器，防止只修改清单就把删除包装成通过。CI 工作流/治理文件需要 CODEOWNERS 人工审核；首次引入清单属于明确的 bootstrap，不能声称已有受信治理基线。工作流权限仅 contents:read，不含部署、数据库或邮件权限。

检查复用现有生成器、资产锁、静态回归、组织图谱测试及原浏览器/表单测试。只在 HTML/CSS/JS/图片/浏览器测试或工作流实际变化时运行浏览器步骤；其他修改复用被冻结的 UI 证据。原浏览器测试入口被更新为先前已通过的 21 页面测试实现，修正“返回英文首页只能是 /”的旧假设，接受已有 /index.html 路径；没有第二套重复浏览器运行器。旧静态测试放在临时 worktree 执行，其生成的历史对照结果不覆盖源工作区中的冻结报告。HTTP 检查只 GET 已批准的公开来源，可通过 workflow_dispatch 选择独立预览；不提交真实表单。

**限制必须保留：** GitHub 返回 main `protected:false`，仓库 rulesets 为空。目前没有证据表明必需状态检查或 CODEOWNERS 评审已强制启用。CI 会失败，但没有分支规则时，人仍可绕过检查直接推送/合并，自动 Pages 发布也可能继续。因此不能宣称“永久阻止合并/发布”已经完全落实。最小治理修复：仓库管理员把 `asset-preservation` 设为 main 的必需状态检查，限制直接更新/绕过，并为治理文件启用可实际执行的人工评审。当前连接器没有这些设置的写入能力；本轮没有另建绕过发布入口。

## PASS / FAIL / NOT VERIFIED

| 门槛 | 状态与证据 |
|---|---|
| 原资产、公开语义、四节点恢复 | PASS；复用已完成的 912 条对照与原始 HTTP/SHA 证据，运行文件无变化 |
| 新资产保护检查器 | 本地 PASS；14 项反向/正常测试覆盖删文件、丢语义、少节点、改 ID、重复 ID、丢链接、表单同意、SEO、重定向、镜像漂移、新资产登记及允许纯新增 |
| 组织恢复、原资产锁、静态回归 | 4 + 10 + 13 PASS；生成器与镜像 PASS |
| 浏览器测试入口适配 | 本地 PASS：105 响应式、10 语言切换、30 筛选、10 FAQ、8 模拟表单；只因运行器/工作流发生变化验证一次，没有改视觉 |
| 既有前端表单与恢复 | 本地 13 PASS；零真实邮件和生产 POST |
| 后台隔离安全/事务验证 | 复用 72 PASS；本轮未改后台代码或重跑无关后台功能 |
| main 合并冲突 | 无冲突（只用 merge-tree 计算，不移动分支） |
| GitHub 托管 CI | 完整运行 41167439947 已 success，包含资产门禁、14 项反向/正常测试、27 项静态/恢复、13 项表单与 105 项响应式；后续提交以 PR Checks 最新实际终态为准 |
| 强制阻止合并 | NOT VERIFIED / 未配置：main 无保护、rulesets 为空，不能标 PASS |
| Render 精确 SHA 部署能力 | 当前 connector 不支持 commit 参数，不能直接触发 latest main；Dashboard/官方 API 的指定提交部署需独立受控操作 |
| 数据库备份可恢复 | NOT VERIFIED：先前用户截图有成功导出，现有连接器不提供导出文件及恢复验证；available 不是恢复证明，不创建新库或执行生产恢复 |
| 邮件费用总上限 | NOT VERIFIED：候选代码有次数预算、paused 模式可零官网发信，但账户套餐/美元硬上限、其他接口用量没有核验；环境变量已保存不等于正式旧版具备新保护 |
| 正式咨询投递/CRM 闭环 | NOT VERIFIED；没有获准的最小生产验证，预览实际来源仍被旧策略拒绝 |
| Cloudflare 正式发布与回退 | 见下方来源核对；不能将 Worker 成功构建当作当前正式流量版本 |

## 正式发布来源与回退

生产实际响应含 `x-github-request-id`、GitHub edge / Fastly 信息，同时存在 Cloudflare 的邮箱保护和 robots 内容信号。GitHub Actions run `41136311137` 名称为 **pages build and deployment**、路径 `dynamic/pages/pages-build-deployment`，对应正式 `5281d59` 并已成功。另一个 Cloudflare Workers Builds 记录 `8bcdd2b7-ae0b-4839-9128-5f228ef94949` 成功，但尚未核实它是否承接正式域名流量。

这些证据支持“正式内容经 GitHub Pages 提供、Cloudflare 参与代理/转换”，不能替代 Cloudflare 路由/域名绑定的实际配置证明。首次升级前需确认当前正式域名的实际源站、Pages 发布源和 Worker 路由；不得为凑发布流程改 DNS。GitHub Pages 与 Worker 两条自动链路应分别记录，不能盲目切换。

回退基线保留 main `5281d59`、正式 Render `1f4602b` 和先前冻结的公开 HTTP 响应。未经部署没有生产变更可回滚。未来回退需用已确认的实际托管平台版本/部署记录，并在同一次验收中验证四节点、表单、robots 附加规则；仅恢复 Git 不能保证平台转换/路由也恢复。候选后台一旦写入新咨询，旧版本回退不会撤销这些记录，也不会自动补发邮件；旧版不具备新持久预算，不能把回退到旧代码理解为邮件费用仍受新保护。不得删记录、重放邮件或恢复数据库来代替应用回退。

## 唯一候选与下一步

本轮仅在现有设计分支追加资产保护/CI 治理提交，public 运行字节仍锁定 ec9240b；不产生新设计版本。客户网站沿用既有独立 clients/ 产品边界与案例资料模板，本轮不增加客户站生成器或修改商家平台，以遵守最后的固定发布范围。

可以创建一个 **Draft PR** 集中展示前端修复与治理检查，标记 RELEASE HOLD。不能把它标为可合并最终版本，不能自动合并。生产最小阻碍为：强制状态检查未配置、真实部署来源/回退版本未完整确认、备份恢复及邮件账户上限/配置未验证、正式咨询闭环未验证；另需明确的生产发布授权。任何一个未通过，不执行阶段 A/B。

预览：https://design-premium-visual-baseline-2026-bb369tech-corporate-website.bb369-ai.workers.dev/zh/index.html

生产（本轮未变）：https://bb369tech.com/

唯一草稿 PR：https://github.com/bb369tech/bb369tech-corporate-website/pull/14

已验证的完整托管验收：https://github.com/bb369tech/bb369tech-corporate-website/actions/runs/41167439947 。公开运行字节仍锁定 ec9240b。后续 PR synchronize 以实际 before/head 差异决定是否重跑浏览器，避免仅修改报告也重复整轮 UI 测试。
