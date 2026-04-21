# smoke_test_local_retry4 - Design Spec

            ## I. Project Information

            | Item | Value |
            | ---- | ----- |
            | **Project Name** | smoke_test_local_retry4 |
            | **Canvas Format** | ppt169 |
            | **Page Count** | 3 |
            | **Design Style** | general_versatile |
            | **Target Audience** | 内部业务团队与基层管理者 |
            | **Use Case** | 本地联调演示与简要经营进展汇报 |

            ---

            ## II. Canvas Specification

            | Property | Value |
            | -------- | ----- |
            | **Format** | ppt169 |
            | **Margins** | left/right 60px, top 50px, bottom 40px |

            ---

            ## III. Visual Theme

            - **Theme**: light
            - **Tone**: 专业、简洁、偏业务汇报
            - **Summary**: 基于“本地联调测试”源内容，生成一份3页的简短业务回顾型演示文稿，围绕收入同比增长、区域增量来源以及获客与复购变化三项关键信息，适合内部同步与快速汇报。

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
            - **Notes**: 全篇统一使用 tabler-outline 线性图标风格，建议仅使用已规划图标：tabler-outline/chart-bar、tabler-outline/map-pin、tabler-outline/user-plus、tabler-outline/refresh。用于经营亮点、区域贡献、获客成本与复购主题提示，不混用填充图标。

            ---

            ## VII. Chart Reference List

            | Chart Type | Reference Template | Used In |
            | ---------- | ------------------ | ------- |
            | kpi_cards | kpi_cards.svg | 02_经营亮点概览 |

            ---

            ## VIII. Image Resource List

            | Filename | Dimensions | Ratio | Purpose | Type | Status | Generation Description |
            | -------- | ---------- | ----- | ------- | ---- | ------ | --------------------- |
            | auto | auto | auto | 采用占位策略，仅在封面预留一张16:9横版背景占位区，可后续替换为抽象蓝色商务背景或城市/数据感背景；内容页以图形卡片和文字信息为主，无需强依赖图片。 | Mixed | placeholder | 采用占位策略，仅在封面预留一张16:9横版背景占位区，可后续替换为抽象蓝色商务背景或城市/数据感背景；内容页以图形卡片和文字信息为主，无需强依赖图片。 |

            ---

            ## IX. Content Outline

            #### Slide 01 - 本地联调测试：经营表现呈现增长韧性

                  - **Layout**: full-screen cover
                  - **Template mapping**: free design
                  - **Takeaway**: 本次汇报聚焦增长结果、区域来源与经营质量变化三项核心信息。
                  - **Content**:
                    - 主题：本地联调测试
- 核心结论：收入同比增长18%
- 关注点：区域增量、新客成本、复购改善

#### Slide 02 - 收入同比增长18%，华东区是主要增量来源

                    - **Layout**: three-column cards
                    - **Template mapping**: card summary
                    - **Takeaway**: 增长已经出现明确结果，且区域贡献具有集中性。
                    - **Chart**: kpi_cards
- **Content**:
                      - KPI卡片1：收入同比增长18%
  - KPI卡片2：华东区贡献主要增量
  - KPI卡片3：新客成本上升，但复购表现改善

#### Slide 03 - 增长延续的关键在于控新客成本、放大复购价值

                  - **Layout**: left-right split (5:5)
                  - **Template mapping**: conclusion slide
                  - **Takeaway**: 下一步应围绕获客效率优化与重点区域复用增长经验展开。
                  - **Content**:
                    - 经营判断：当前增长具备延续基础，但新增获客效率承压
- 动作建议：复盘华东区增长来源，提炼可复制打法
- 管理重点：关注新客成本趋势，并持续追踪复购改善质量

            ---

            ## X. Speaker Notes Plan

            - **Total duration**: 3 minutes
            - **Style**: professional
            - **Purpose**: inform
