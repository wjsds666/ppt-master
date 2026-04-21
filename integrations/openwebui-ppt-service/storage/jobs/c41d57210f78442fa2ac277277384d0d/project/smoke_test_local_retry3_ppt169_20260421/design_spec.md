# smoke_test_local_retry3 - Design Spec

            ## I. Project Information

            | Item | Value |
            | ---- | ----- |
            | **Project Name** | smoke_test_local_retry3 |
            | **Canvas Format** | ppt169 |
            | **Page Count** | 3 |
            | **Design Style** | general_versatile |
            | **Target Audience** | 内部业务团队与管理层 |
            | **Use Case** | 本地联调阶段的经营结果快速汇报与内部同步 |

            ---

            ## II. Canvas Specification

            | Property | Value |
            | -------- | ----- |
            | **Format** | ppt169 |
            | **Margins** | left/right 60px, top 50px, bottom 40px |

            ---

            ## III. Visual Theme

            - **Theme**: light
            - **Tone**: 专业、简洁、偏业务复盘
            - **Summary**: 基于“本地联调测试”源内容制作的3页简报，核心传达为：收入同比增长18%，主要增量来自华东区，但新客成本上升，需依靠复购改善来平衡增长质量。

            | Role | HEX | Purpose |
            | ---- | --- | ------- |
            | **Background** | `#FFFFFF` | Page background |
            | **Secondary bg** | `#F8FAFC` | Card background |
            | **Primary** | `#0F62FE` | Main emphasis |
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
            - **Notes**: 全篇统一使用tabler-outline描边图标，不混用填充风格。建议图标库存限定为：tabler-outline/chart-bar、tabler-outline/map-pin、tabler-outline/user-plus、tabler-outline/refresh，用于增长、区域、新客、复购四类语义。

            ---

            ## VII. Chart Reference List

            | Chart Type | Reference Template | Used In |
            | ---------- | ------------------ | ------- |
            | kpi_cards | kpi_cards.svg | 02_growth_summary |

            ---

            ## VIII. Image Resource List

            | Filename | Dimensions | Ratio | Purpose | Type | Status | Generation Description |
            | -------- | ---------- | ----- | ------- | ---- | ------ | --------------------- |
            | auto | auto | auto | 不依赖真实图片；仅在封面或结束页保留弱化装饰性占位背景，正文以卡片和图标为主，确保本地联调与快速生成稳定。 | Mixed | placeholder | 不依赖真实图片；仅在封面或结束页保留弱化装饰性占位背景，正文以卡片和图标为主，确保本地联调与快速生成稳定。 |

            ---

            ## IX. Content Outline

            #### Slide 01 - 本地联调测试：收入实现增长，但增长质量需持续观察

                  - **Layout**: full-screen cover
                  - **Template mapping**: free design
                  - **Takeaway**: 本次汇报的核心是“增长成立，但结构与效率出现分化”。
                  - **Content**:
                    - 主题：本地联调测试经营概览
- 核心结论：收入同比增长18%
- 关注点：华东区拉动增长，新客成本上升、复购改善

#### Slide 02 - 增长已被验证：同比+18%，主要增量集中于华东区

                    - **Layout**: three-card KPI layout
                    - **Template mapping**: general versatile cards
                    - **Takeaway**: 业绩增长明确成立，但增长来源较为集中。
                    - **Chart**: kpi_cards
- **Content**:
                      - 收入同比增长18%，为本轮联调结果中的最明确信号
  - 华东区贡献主要增量，说明区域表现存在明显拉动作用
  - 建议将“整体增长”与“区域集中度”放在同一页同步表达

#### Slide 03 - 下一步重点应转向增长质量：控制获客成本，放大复购改善

                  - **Layout**: left-right split (5:5)
                  - **Template mapping**: free design
                  - **Takeaway**: 后续经营动作应从“追求增量”转向“兼顾效率与留存”。
                  - **Content**:
                    - 风险点：新客成本上升，可能压缩增长效率
- 积极信号：复购改善，说明存量经营质量有所提升
- 建议方向：一手优化新客获取效率，一手继续强化复购运营

            ---

            ## X. Speaker Notes Plan

            - **Total duration**: 3 minutes
            - **Style**: professional
            - **Purpose**: inform
