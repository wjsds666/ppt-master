# qwen_image_test - Design Spec

            ## I. Project Information

            | Item | Value |
            | ---- | ----- |
            | **Project Name** | qwen_image_test |
            | **Canvas Format** | ppt169 |
            | **Page Count** | 2 |
            | **Design Style** | general_versatile |
            | **Target Audience** | 潜在客户、媒体、合作伙伴及发布会现场观众 |
            | **Use Case** | 新能源汽车新品发布会现场展示 |

            ---

            ## II. Canvas Specification

            | Property | Value |
            | -------- | ----- |
            | **Format** | ppt169 |
            | **Margins** | left/right 60px, top 50px, bottom 40px |

            ---

            ## III. Visual Theme

            - **Theme**: light
            - **Tone**: 科技感、未来感、高端、动感
            - **Summary**: 为“新能源汽车发布会”规划一套2页PPT设计方案：第1页为封面主视觉，用于建立高端、科技、未来感的发布会第一印象；第2页为产品卖点图文页，用简洁有力的图文结构呈现核心优势。整体采用通用型展示风格，偏科技发布会表达，适合现场演讲与品牌展示。

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
            - **Notes**: 全稿统一使用 tabler-outline 线性图标风格，不混用填充图标。建议仅使用已验证且语义安全的图标：tabler-outline/bolt、tabler-outline/battery、tabler-outline/shield-check、tabler-outline/rocket。封面尽量少图标，卖点页用于对应产品优势标签。

            ---

            ## VII. Chart Reference List

            | Chart Type | Reference Template | Used In |
            | ---------- | ------------------ | ------- |
            | None | - | - |

            ---

            ## VIII. Image Resource List

            | Filename | Dimensions | Ratio | Purpose | Type | Status | Generation Description |
            | -------- | ---------- | ----- | ------- | ---- | ------ | --------------------- |
            | auto | auto | auto | 需要生成2张AI图片：1张16:9封面主视觉背景，突出新能源汽车、舞台灯光与未来科技感；1张用于卖点页的产品展示图，建议为车辆三分之二侧前视角或科技感场景图，适合左图右文或右图左文排版。 | Mixed | ai_generation | 需要生成2张AI图片：1张16:9封面主视觉背景，突出新能源汽车、舞台灯光与未来科技感；1张用于卖点页的产品展示图，建议为车辆三分之二侧前视角或科技感场景图，适合左图右文或右图左文排版。 |

            ---

            ## IX. Content Outline

            #### Slide 01 - 以未来科技形象建立新品发布第一印象

                  - **Layout**: full-screen cover
                  - **Template mapping**: free design
                  - **Takeaway**: 封面需以强主视觉传达新能源汽车新品发布的科技感与高端定位。
                  - **Content**:
                    - 主标题：新能源汽车发布会
- 副标题可选：智驱未来，焕新出行
- 保留品牌/日期/发布地点信息区

#### Slide 02 - 三大产品卖点共同支撑新品竞争力

                  - **Layout**: left-right split
                  - **Template mapping**: image-text split
                  - **Takeaway**: 卖点页应以大图强化产品质感，并用3个清晰标签概括核心优势。
                  - **Content**:
                    - 卖点1：长续航出行，突出新能源使用场景价值
- 卖点2：智能科技体验，体现座舱或辅助驾驶亮点
- 卖点3：安全与性能兼顾，建立信任与购买理由

            ---

            ## X. Speaker Notes Plan

            - **Total duration**: 3 minutes
            - **Style**: professional
            - **Purpose**: inform
