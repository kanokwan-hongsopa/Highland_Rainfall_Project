# -*- coding: utf-8 -*-
with open("dashboard/halloween_app.py", "r", encoding="utf-8") as f:
    text = f.read()

insights_css = """
        /* 6 PROVINCE INSIGHT CARDS */
        .insight-cards-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-top: 0.75rem;
        }}

        @media (max-width: 1024px) {{
            .insight-cards-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        @media (max-width: 640px) {{
            .insight-cards-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .insight-card {{
            background: rgba(33, 22, 49, 0.82);
            border: 1px solid rgba(167, 120, 232, 0.28);
            border-radius: 12px;
            padding: 1rem 1.15rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 0.65rem;
            cursor: pointer;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
        }}

        .insight-card:hover {{
            transform: translateY(-3px);
            border-color: rgba(255, 138, 50, 0.65);
            box-shadow: 0 8px 24px rgba(255, 138, 50, 0.25), 0 0 12px rgba(167, 120, 232, 0.2);
            background: rgba(43, 28, 66, 0.92);
        }}

        .insight-card.active {{
            border-color: #FF8A32;
            background: linear-gradient(135deg, rgba(58, 38, 88, 0.9), rgba(33, 22, 49, 0.95));
            box-shadow: 0 0 18px rgba(255, 138, 50, 0.45);
        }}

        .insight-card-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.5rem;
        }}

        .insight-badge {{
            font-size: 0.7rem;
            font-weight: 600;
            padding: 2px 7px;
            border-radius: 6px;
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
        }}

        .badge-orange {{
            background: rgba(255, 138, 50, 0.18);
            color: #FF8A32;
            border: 1px solid rgba(255, 138, 50, 0.4);
        }}

        .badge-purple {{
            background: rgba(167, 120, 232, 0.18);
            color: #A778E8;
            border: 1px solid rgba(167, 120, 232, 0.4);
        }}

        .badge-cyan {{
            background: rgba(56, 189, 248, 0.18);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.4);
        }}

        .badge-green {{
            background: rgba(52, 211, 153, 0.18);
            color: #34d399;
            border: 1px solid rgba(52, 211, 153, 0.4);
        }}

        .badge-amber {{
            background: rgba(251, 191, 36, 0.18);
            color: #fbbf24;
            border: 1px solid rgba(251, 191, 36, 0.4);
        }}

        .insight-category-title {{
            font-size: 0.78rem;
            color: var(--text-muted);
            font-weight: 500;
        }}

        .insight-prov-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #FFFFFF;
            letter-spacing: 0.2px;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }}

        .insight-main-val {{
            font-size: 1.4rem;
            font-weight: 800;
            line-height: 1.2;
            display: flex;
            align-items: baseline;
            gap: 0.35rem;
        }}

        .insight-val-unit {{
            font-size: 0.75rem;
            font-weight: 400;
            color: var(--text-muted);
        }}

        .insight-meta-details {{
            font-size: 0.74rem;
            line-height: 1.4;
            color: var(--text-muted);
            border-top: 1px dashed rgba(167, 120, 232, 0.18);
            padding-top: 0.45rem;
            margin-top: 0.2rem;
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}

        .insight-card-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.72rem;
            color: var(--primary-orange);
            font-weight: 500;
            padding-top: 0.25rem;
        }}

        .spearman-rho-badge {{
            background: rgba(255, 138, 50, 0.12);
            border: 1px solid rgba(255, 138, 50, 0.35);
            border-radius: 8px;
            padding: 0.3rem 0.65rem;
            font-size: 0.78rem;
            font-weight: 600;
            color: #FF8A32;
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
        }}
"""

target = "    </style>"
idx = text.find(target)
if idx != -1:
    text = text[:idx] + insights_css + "\n" + text[idx:]
    with open("dashboard/halloween_app.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("Successfully added insights_css before </style>")
else:
    print("Could not find </style>")
