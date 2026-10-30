# BB369TECH — 首页构图与质感升级

日期：2026-10-30，洛杉矶时间。工作分支：design/premium-visual-baseline-20261030。RELEASE HOLD。

## 本轮视觉变化

- 首屏改为左侧价值说明、咨询入口，右侧原有界面示意。示意模块仍完整标注“非已上线软件”，未制造客户数据或经营指标。
- 三项服务使用统一的编号、边框、留白与标题比例，保留完整说明和原入口。
- 原 Solutions 正文、三步流程及咨询链接仍直接可见；原有界面模块整体移动到同页 Hero，没有重写内容。
- 首页真实案例采用一张重点、两张辅助的构图。原三家商户、完整说明、功能、真实截图和链接全部保留；目录页仍使用可扩展静态模板。
- 中英文各自校准字号、行宽、间距，手机恢复单列；共享组件继续统一。

没有新增外部图像、字体、依赖、运行脚本或业务数据。原 supplied premium 样式被整理为同一个有序样式文件，没有继续叠加新 CSS 文件。

## 数字资产保护

本轮基线是上一轮候选 ec90d20cbf3cd7f6e69fe3969fd33e4f0012cd45。正式 main 基线仍为 b553356528d097632f4f30da40258af4501f8212。

| Before | After | 分类 |
|---|---|---|
| Solutions 的完整界面示意块 | 原块原字节移动到同页 Hero；全部原文本、链接、aria 标签保留 | RELOCATED |
| 首页其他 HTML | 除上述块的位置外逐字节相同；head 完全相同 | PRESERVED |
| 原共享 premium-polish.css | 在同一个文件内重新组织构图、层级及响应式规则，根目录镜像同步 | IMPROVED |
| 其他公开 HTML、FAQ、行业、Resources、法律页、表单、脚本、Sitemap、Robots、产品与案例 JSON、业务图片、Wrangler、重定向 | 逐字节不变 | PRESERVED |
| 原有效资产删除 | 无 | 0 REMOVED |

108 个原运行文件：102 PRESERVED、4 RELOCATED（两个首页及镜像）、2 IMPROVED（CSS及镜像）。详表见 BEFORE-AFTER.csv。没有调整 URL、Canonical、Title、Description、Hreflang、JSON-LD 或内部链接目标。

新的保留测试不仅比较语义：抽出前后相同的界面块后，首页其他字节必须完全一致；同时检查 head、全部文本节点和 href 多重集一致，防止漏项。其他运行文件必须逐字节一致。

原 CSS-only 历史测试已允许这次明确授权的完整块移动，但仍严格检查其他原字节；历史报告保留，本次结果写入 composition-upgrade/patch-baseline-check，不覆盖历史快照。

## 验收

- PASS：3 项新构图保留测试、3 项原补丁兼容保留测试、13 项既有回归，总计19项。
- PASS：21页×320/390/768/1440四种宽度84项真实浏览器检查，未发现横向溢出、重复h1或首屏图片加载错误。EN/ZH界面示意保留。
- PASS：静态案例生成与 public/ 根目录镜像一致；原表单、隐私同意、邮箱、接口及JS不变。
- 远程独立预览构建及真实截图证据随最终验收包交付；不把构建成功当成浏览器验收通过。
- NOT VERIFIED：真实邮件投递、自动回复、CRM落库、真实付款、实体手机、多浏览器全面矩阵、完整无障碍/性能标准及排名影响。本轮不发送真实咨询，不写入客户数据。

原先隐藏的示意导航在新Hero中作为可见标签展示；新增CSS不使用 display:none 或 visibility:hidden 隐藏业务内容。原FAQ文字仍在原HTML页面，未转成图片或JavaScript生成内容。

## 发布与回滚

只更新现有设计分支和隔离预览，不合并main，不部署生产，不修改DNS、CRM、支付或客户资料。

预览：https://design-premium-visual-baseline-2026-bb369tech-corporate-website.bb369-ai.workers.dev/

需要回退时在设计分支revert本次提交，恢复上一轮ec90d20视觉；不要reset或force-push main。最终预览需用户审阅后另行批准正式发布。
