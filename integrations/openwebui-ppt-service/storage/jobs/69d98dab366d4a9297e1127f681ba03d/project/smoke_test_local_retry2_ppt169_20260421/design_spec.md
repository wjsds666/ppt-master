# smoke_test_local_retry2 - Design Spec

            ## I. Project Information

            | Item | Value |
            | ---- | ----- |
            | **Project Name** | smoke_test_local_retry2 |
            | **Canvas Format** | ppt169 |
            | **Page Count** | 4 |
            | **Design Style** | general_versatile |
            | **Target Audience** | 内部业务团队与基层管理者 |
            | **Use Case** | 本地联调测试结果的快速经营复盘与内部汇报 |

            ---

            ## II. Canvas Specification

            | Property | Value |
            | -------- | ----- |
            | **Format** | ppt169 |
            | **Margins** | left/right 60px, top 50px, bottom 40px |

            ---

            ## III. Visual Theme

            - **Theme**: light
            - **Tone**: 简洁、专业、偏业务复盘导向
            - **Summary**: 基于源文档提炼为4页简报，核心传达“收入同比增长18%，华东区贡献主要增量，但新客成本上升，需依靠复购改善与区域经验复制来稳住增长质量”。已按用户要求自动确定为16:9、4页、浅色通用商务风、占位图方案与tabler-outline图标体系。

            | Role | HEX | Purpose |
            | ---- | --- | ------- |
            | **Background** | `#FFFFFF` | Page background |
            | **Secondary bg** | `#F8FAFC` | Card background |
            | **Primary** | `#1565C0` | Main emphasis |
            | **Accent** | `#16A34A` | Highlight |
            | **Secondary accent** | `#38BDF8` | Gradient / secondary highlight |
            | **Body text** | `#0F172A` | Main body text |
            | **Secondary text** | `#475569` | Notes |
            | **Tertiary text** | `#94A3B8` | Meta text |
            | **Border/divider** | `#CBD5E1` | Borders |
            | **Success** | `#16A34A` | Positive |
            | **Warning** | `#DC2626` | Risk |

            ---

            ## IV. Typography System

            - **Preset**: P1
            - **Title font**: Microsoft YaHei
            - **Body font**: Microsoft YaHei
            - **Emphasis font**: SimHei
            - **Body size**: 18px
            - **Content title size**: 30px

            ---

            ## V. Layout Principles

            - **Card gap**: 24px
            - **Card padding**: 24px
            - **Border radius**: 16px

            ---

            ## VI. Icon Usage Specification

            - **Mode**: built-in
            - **Library**: tabler-outline
            - **Notes**: 全篇统一使用 tabler-outline 线性图标，不混用 filled 风格；建议图标清单限定为：tabler-outline/chart-bar、tabler-outline/map-pin、tabler-outline/user-plus、tabler-outline/repeat。用于数据概览、区域增量、拉新成本、复购改善等表达。

            ---

            ## VII. Chart Reference List

            | Chart Type | Reference Template | Used In |
            | ---------- | ------------------ | ------- |
            | kpi_cards | kpi_cards.svg | 02_key_findings.svg |

            ---

            ## VIII. Image Resource List

            | Filename | Dimensions | Ratio | Purpose | Type | Status | Generation Description |
            | -------- | ---------- | ----- | ------- | ---- | ------ | --------------------- |
            | auto | auto | auto | 采用占位图方案，仅在封面与区域分析页预留图片/示意图容器；后续如补充真实区域地图、业务场景图或抽象背景，可直接替换占位资源。 | Mixed | placeholder | 采用占位图方案，仅在封面与区域分析页预留图片/示意图容器；后续如补充真实区域地图、业务场景图或抽象背景，可直接替换占位资源。 |

            ---

            ## IX. Content Outline

            #### Slide 01 - 本地联调测试：收入增长延续，但增长质量仍需观察

                  - **Layout**: full-screen cover
                  - **Template mapping**: free design
                  - **Takeaway**: 当前业务呈现“规模增长、区域集中、效率分化”的阶段性特征。
                  - **Content**:
                    - 收入同比增长18%
- 华东区贡献主要增量
- 新客成本上升，复购改善

#### Slide 02 - 核心结论：收入同比+18%，但拉新与复购表现出现分化

                    - **Layout**: three-column cards
                    - **Template mapping**: kpi cards
                    - **Takeaway**: 增长结果积极，但新增获客效率承压，复购成为当前质量修复点。
                    - **Chart**: kpi_cards
- **Content**:
                      - 结果面：收入同比增长18%，整体延续增长态势
  - 压力面：新客成本上升，说明拉新效率需要重点关注
  - 支撑面：复购改善，对经营稳定性形成一定支撑

#### Slide 03 - 增长来源：华东区是当前最主要的增量贡献区域

                  - **Layout**: left-right split (4:6)
                  - **Template mapping**: left-right split
                  - **Takeaway**: 区域贡献并不均衡，华东区是本轮增长判断中的关键支点。
                  - **Content**:
                    - 源文档明确指出：华东区贡献主要增量
- 建议将华东区作为复盘重点，提炼可复制的增长动作
- 其余区域在本轮汇报中以待补充数据形式呈现，避免过度推断

#### Slide 04 - 下一步重点：放大华东经验，同时优化新客获取效率

                  - **Layout**: single column centered
                  - **Template mapping**: summary close
                  - **Takeaway**: 后续应围绕“复制有效增长动作”和“修复拉新效率”两条主线推进。
                  - **Content**:
                    - 复盘华东区主要增量来源，沉淀可复制打法
- 重点跟踪新客成本变化，优化拉新投放与转化链路
- 持续观察复购改善是否能够稳定对冲获客成本压力

            ---

            ## X. Speaker Notes Plan

            - **Total duration**: 6 minutes
            - **Style**: professional
            - **Purpose**: report
