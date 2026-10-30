# 固定架构，按资料扩展

以后默认不重新设计首页。新增产品更新目录资料；新增商家更新案例资料；服务和法律事实按需核实更新。

## 产品

资料源：public/product-catalog.json；模板：PRODUCT-TEMPLATE.json。

模板默认不允许发布。完整填入真实中英文、状态、正式入口、客户对象、公开批准及证据后，再进入公开目录。内部或未完成产品不得写进 public/ 中的 JSON。`available` 必须同时通过正式发布核验，不能用“构建成功”代替真实产品验收。现有公开工具仍保留“可用性需确认”，学校支持仍保留“试点咨询”，没有包装成已上线 SaaS。

生成与检查：

```sh
python scripts/render-product-catalog.py
python scripts/render-projects.py
python scripts/sync-public-mirror.py
python scripts/render-product-catalog.py --check
python tests/stable-asset-lock.py
python tests/final-visual-regression.py
```

当前静态模板支持统一名称、说明、适用客户、状态及入口。将来在模板内增加真实截图或功能字段时，做向后兼容扩展；不要重排整个首页或改旧网址。目录 HTML 在构建前生成，客户和搜索系统不需要执行 JavaScript 才能阅读。

## 案例

资料源：public/projects.json。需要真实已发布网址、已交付范围、实际截图及公开展示批准。默认只新增完整案例目录；首页精选固定最多3项，不因客户增加而不断堆叠。

## 不变的边界

导航与现有页面职责、网址、语言关系保持稳定。公司官网负责品牌和入口，具体软件在独立平台运行，CRM保持内部。原法律、咨询表单、邮箱、付款和客户数据不属于视觉维护范围。

“长期稳定”指架构和设计系统持续复用；必要的资料、安全、兼容和可访问性维护仍正常进行。保护检查不能证明保留的旧资产，一律保持 RELEASE HOLD。
