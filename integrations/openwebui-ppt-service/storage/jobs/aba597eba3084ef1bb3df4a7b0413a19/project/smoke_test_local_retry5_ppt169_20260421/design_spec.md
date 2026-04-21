# smoke_test_local_retry5 - Design Spec

            ## I. Project Information

            | Item | Value |
            | ---- | ----- |
            | **Project Name** | smoke_test_local_retry5 |
            | **Canvas Format** | ppt169 |
            | **Page Count** | 2 |
            | **Design Style** | general_versatile |
            | **Target Audience** | 内部业务团队与管理层 |
            | **Use Case** | 本地联调演示与阶段性经营情况快速汇报 |

            ---

            ## II. Canvas Specification

            | Property | Value |
            | -------- | ----- |
            | **Format** | ppt169 |
            | **Margins** | left/right 60px, top 50px, bottom 40px |

            ---

            ## III. Visual Theme

            - **Theme**: light
            - **Tone**: 专业、简洁、业务导向
            - **Summary**: 基于“本地联调测试”简要素材，输出一份2页的中文业务快报型演示，聚焦收入同比增长18%、华东区贡献主要增量，以及新客成本上升与复购改善这三项核心经营信号。

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
            - **Notes**: 全稿统一使用 tabler-outline 线性图标，不混用填充风格。建议仅使用已锁定图标：tabler-outline/chart-bar、tabler-outline/map-pin、tabler-outline/user-plus、tabler-outline/refresh。

            ---

            ## VII. Chart Reference List

            | Chart Type | Reference Template | Used In |
            | ---------- | ------------------ | ------- |
            | kpi_cards | kpi_cards.svg | 02_summary.svg |

            ---

            ## VIII. Image Resource List

            | Filename | Dimensions | Ratio | Purpose | Type | Status | Generation Description |
            | -------- | ---------- | ----- | ------- | ---- | ------ | --------------------- |
            | auto | auto | auto | 本项目不依赖真实图片，若需增强封面表现，可在封面使用抽象商务背景占位图；内容页以图标、卡片和数据块为主。 | Mixed | placeholder | 本项目不依赖真实图片，若需增强封面表现，可在封面使用抽象商务背景占位图；内容页以图标、卡片和数据块为主。 |

            ---

            ## IX. Content Outline

            #### Slide 01 - 本地联调测试：经营表现呈现增长但结构信号分化

                  - **Layout**: full-screen cover
                  - **Template mapping**: free design
                  - **Takeaway**: 当前业务表现可概括为“收入增长明确、区域驱动集中、获客效率承压但存量经营改善”。
                  - **Content**:
                    - 主题：本地联调测试
- 核心看点：收入同比增长18%
- 补充信息：华东区贡献主要增量，新客成本上升、复购改善

#### Slide 02 - 收入同比增长18%，华东拉动增量，但新客成本上升需持续关注

                    - **Layout**: three-column cards
                    - **Template mapping**: card-based summary
                    - **Takeaway**: 短期增长由收入提升与区域贡献支撑，但增长质量仍需平衡拉新成本与复购改善。
                    - **Chart**: kpi_cards
- **Content**:
                      - 增长结果：收入同比增长18%，可作为当前阶段最明确的正向信号
  - 区域贡献：华东区贡献主要增量，说明增长来源相对集中
  - 经营结构：新客成本上升，表明拉新效率承压；复购改善，反映存量经营有所优化

            ---

            ## X. Speaker Notes Plan

            - **Total duration**: 3 minutes
            - **Style**: professional
            - **Purpose**: inform
