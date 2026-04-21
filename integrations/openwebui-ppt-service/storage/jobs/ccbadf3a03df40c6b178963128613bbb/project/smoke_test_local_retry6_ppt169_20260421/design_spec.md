# smoke_test_local_retry6 - Design Spec

            ## I. Project Information

            | Item | Value |
            | ---- | ----- |
            | **Project Name** | smoke_test_local_retry6 |
            | **Canvas Format** | ppt169 |
            | **Page Count** | 2 |
            | **Design Style** | general_versatile |
            | **Target Audience** | 内部业务团队与项目管理相关人员 |
            | **Use Case** | 本地联调测试场景下的阶段性业务结果简报 |

            ---

            ## II. Canvas Specification

            | Property | Value |
            | -------- | ----- |
            | **Format** | ppt169 |
            | **Margins** | left/right 60px, top 50px, bottom 40px |

            ---

            ## III. Visual Theme

            - **Theme**: light
            - **Tone**: 专业、简洁、清晰、偏业务汇报
            - **Summary**: 基于《本地联调测试》源内容，建议采用 PPT 16:9、2页、中文轻量汇报结构：封面页明确主题，正文页集中呈现3个核心业务结论。目标受众自动判断为内部业务团队/管理者，用途为本地联调测试场景下的阶段性业务概览。风格按用户指定采用 General Versatile，但内容表达保持结论先行、简洁专业。配色使用明亮商务蓝绿体系，图标统一使用 tabler-outline，图片采用占位符策略，便于后续替换。

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
            - **Notes**: 全篇统一使用描边图标，不混用 filled 风格。建议图标清单：tabler-outline/presentation、tabler-outline/chart-bar、tabler-outline/map-pin、tabler-outline/arrow-up-right、tabler-outline/repeat。用于封面识别与正文三条业务结论的可视化辅助。

            ---

            ## VII. Chart Reference List

            | Chart Type | Reference Template | Used In |
            | ---------- | ------------------ | ------- |
            | None | - | - |

            ---

            ## VIII. Image Resource List

            | Filename | Dimensions | Ratio | Purpose | Type | Status | Generation Description |
            | -------- | ---------- | ----- | ------- | ---- | ------ | --------------------- |
            | auto | auto | auto | 当前不依赖真实图片，封面可使用浅色抽象背景占位，正文页如需增强视觉，可预留右上角小型装饰图占位区域，后续再替换。 | Mixed | placeholder | 当前不依赖真实图片，封面可使用浅色抽象背景占位，正文页如需增强视觉，可预留右上角小型装饰图占位区域，后续再替换。 |

            ---

            ## IX. Content Outline

            #### Slide 01 - 本地联调测试显示业务延续增长态势

                  - **Layout**: full-screen cover
                  - **Template mapping**: free design
                  - **Takeaway**: 本次测试样本显示收入增长、区域增量集中、用户经营结构正在变化。
                  - **Content**:
                    - 主标题：本地联调测试
- 副标题：阶段性业务结果概览
- 信息行：基于 source_text.md 提炼

#### Slide 02 - 增长由华东拉动，但获客效率承压、复购表现改善

                  - **Layout**: three-column cards
                  - **Template mapping**: free design
                  - **Takeaway**: 当前业务信号呈现“收入增长 + 区域集中 + 拉新承压但留存改善”的组合特征。
                  - **Content**:
                    - 收入同比增长18%
- 华东区贡献主要增量
- 新客成本上升，复购改善

            ---

            ## X. Speaker Notes Plan

            - **Total duration**: 3 minutes
            - **Style**: professional
            - **Purpose**: inform
