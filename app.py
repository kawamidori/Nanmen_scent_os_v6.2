# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import copy
import hmac
from datetime import datetime

from config import (
    PERFUME_CONCENTRATION_PRESETS, SOLVENT_CHOICES, REGULATORY_REGIONS,
    DILUTION_TIERS, SOLVENT_DATABASE, STANDARD_ALLERGENS
)
from library import CHEMICAL_CORE_DB, DEFAULT_COMMERCIAL_SKUS
import core

st.set_page_config(page_title="Nanmen Scent Lab OS", layout="wide", page_icon="🧪")

# ------------------------------------------------------------------------------
# 🔒 Password Protection
# ------------------------------------------------------------------------------
def check_password():
    if st.session_state.get("authenticated"):
        return True

    st.markdown("""
        <div style='text-align:center; padding-top:40px;'>
            <h1>🧪 Nanmen Scent Lab OS</h1>
            <p style='color:#64748B;'>Enterprise Perfumery Operating System — 3-Layer Metadata Architecture</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        pwd = st.text_input("🔒 實驗室門禁密碼 / Access Password", type="password", placeholder="Enter password...")
        correct_pwd = st.secrets.get("APP_PASSWORD", "nanmen2026")
        if st.button("登入系統 / Login", use_container_width=True, type="primary"):
            if hmac.compare_digest(pwd, correct_pwd):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ 密碼錯誤 / Incorrect password.")
    return False

if not check_password():
    st.stop()

# ------------------------------------------------------------------------------
# UI CSS (Desktop + Mobile Responsive)
# ------------------------------------------------------------------------------
st.markdown("""
<style>
    @media (max-width: 768px) {
        .block-container { padding: 4.2rem 0.4rem 1rem 0.4rem !important; }
        .stTabs [data-baseweb="tab-list"] { display: flex; overflow-x: auto; white-space: nowrap; -webkit-overflow-scrolling: touch; }
        .stats-bar { flex-direction: column; gap: 6px; text-align: left; align-items: flex-start !important; }
        input[type="number"] { font-size: 16px !important; }
    }
    .mod-pill { background: #0F172A; color: #38BDF8; padding: 3px 10px; border-radius: 6px; font-weight: bold; border: 1px solid #0284C7; font-size: 13px; }
    .mat-card { background: #F8FAFC; border: 1px solid #CBD5E1; padding: 12px; border-radius: 8px; margin-top: 8px; }
    .scale-chip { background: #064E3B; color: #6EE7B7; padding: 3px 8px; border-radius: 4px; font-family: monospace; font-size: 13px; font-weight: bold; display: inline-block; }
    .cas-badge { background: #F1F5F9; color: #475569; padding: 2px 5px; border-radius: 4px; font-family: monospace; font-size: 11px; border: 1px solid #CBD5E1; }
    .layer-l1 { background: #E0F2FE; color: #0369A1; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: bold; }
    .layer-l2 { background: #DCFCE7; color: #15803D; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: bold; }
    .layer-l3 { background: #F3E8FF; color: #7E22CE; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: bold; }
    .stats-bar { background: #0F172A; color: white; padding: 12px 18px; border-radius: 8px; margin-top: 14px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .sample-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
    .doc-sheet { background: white; padding: 20px; border: 1px solid #CBD5E1; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); color: #0F172A; margin-bottom: 14px; }
    .doc-title { border-bottom: 2px solid #0F172A; padding-bottom: 8px; margin-bottom: 14px; }
    .cert-box { background: #FFFFFF; border: 2px solid #0F172A; border-radius: 8px; padding: 18px; margin-bottom: 14px; }
    .nda-box { background: #FFFBEB; border: 2px solid #D97706; border-radius: 8px; padding: 18px; margin-bottom: 14px; color: #78350F; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# SESSION STATE INITIALIZATION (3-Layer Databases)
# ------------------------------------------------------------------------------
if "lang" not in st.session_state:
    st.session_state.lang = "zh"
if "core_db" not in st.session_state:
    st.session_state.core_db = copy.deepcopy(CHEMICAL_CORE_DB)
if "commercial_skus" not in st.session_state:
    st.session_state.commercial_skus = copy.deepcopy(DEFAULT_COMMERCIAL_SKUS)
if "custom_materials" not in st.session_state:
    st.session_state.custom_materials = {
        "CUST-ROSE-TINC": {
            "custom_id": "CUST-ROSE-TINC",
            "cas": "60-12-8",
            "name_cn": "自製大馬士革玫瑰酊劑 (10% in Ethanol)",
            "name_en": "House Damask Rose Tincture (10% in Ethanol)",
            "note": "Mid",
            "family": "Floral",
            "dilution_pct": 10.0,
            "solvent": "Ethanol (95%變性酒精)",
            "sg_pure": 0.980,
            "cost_per_g": 45.0,
            "ifra_cat4_max": 100.0,
            "allergens": {"Geraniol": 0.25, "Citronellol": 0.35},
            "lot_no": "PRIV-2026-R01",
            "exp_date": "2028/12/31"
        }
    }
if "mods" not in st.session_state:
    # Default Mod 1 demonstrates both L2 mapped SKUs and an L1 unmapped CAS ready for Phase 2 SKU mapping!
    st.session_state.mods = {
        "Mod 1": {
            "L2_SKU-CHEM-54464-50": {"layer": "L2_SKU", "cas": "54464-57-2", "sku_id": "SKU-CHEM-54464-50", "gross_g": 1.500, "dilution_pct": 50.0, "solvent": "DPG (二丙二醇)"},
            "L2_SKU-CHEM-24851-50": {"layer": "L2_SKU", "cas": "24851-98-7", "sku_id": "SKU-CHEM-24851-50", "gross_g": 1.200, "dilution_pct": 50.0, "solvent": "DPG (二丙二醇)"},
            "L1_6790-58-5": {"layer": "L1_CORE", "cas": "6790-58-5", "sku_id": None, "gross_g": 0.300, "dilution_pct": 10.0, "solvent": "DPG (二丙二醇)"},
            "L2_SKU-MH-8007758": {"layer": "L2_SKU", "cas": "8007-75-8", "sku_id": "SKU-MH-8007758", "gross_g": 0.200, "dilution_pct": 100.0, "solvent": "None (100%純原液)"},
            "L2_SKU-ZX-91770580": {"layer": "L2_SKU", "cas": "91770-58-0", "sku_id": "SKU-ZX-91770580", "gross_g": 0.400, "dilution_pct": 100.0, "solvent": "None (100%純原液)"}
        }
    }
if "active_mod" not in st.session_state:
    st.session_state.active_mod = "Mod 1"
if "mod_notes" not in st.session_state:
    st.session_state.mod_notes = {"Mod 1": "初始版：台灣肖楠與佛手柑骨架（含 1 項待映射 L1 Ambroxan，可於 Phase 2 選擇 Givaudan 100% 粉末或 10% 預溶液）。"}
if "dosed_checklist" not in st.session_state:
    st.session_state.dosed_checklist = {}
if "region_id" not in st.session_state or st.session_state.region_id not in REGULATORY_REGIONS:
    st.session_state.region_id = "EU"
if "tier_id" not in st.session_state or st.session_state.tier_id not in PERFUME_CONCENTRATION_PRESETS:
    st.session_state.tier_id = "EdP_15"
if "locked_for_pif" not in st.session_state:
    st.session_state.locked_for_pif = False
if "phase_idx" not in st.session_state:
    st.session_state.phase_idx = 0

# ------------------------------------------------------------------------------
# BILINGUAL DICTIONARY
# ------------------------------------------------------------------------------
UI = {
    "zh": {
        "mod_label": "📂 當前操作版本 (Mod)",
        "reg_label": "🌐 專案法規基準 (Regulatory)",
        "dos_label": "🎯 目標成品賦香率 (Dosage)",
        "btn_copy": "➕ 複製",
        "btn_clear": "🗑️ 清空",
        "phases": [
            "💻 Phase 1：數位配方創作 (3層庫)",
            "⚖️ Phase 2：SKU映射與實驗室放樣",
            "📑 Phase 3：PIF 產品資訊與合規證書",
            "🏭 Phase 4：商業量產與投遞框架"
        ],
        "p1_banner": "💻 Phase 1：數位配方創作（支援 L1 純化學核心 / L2 商業SKU / L3 自建私有庫）",
        "p1_w_lbl": "配方總重",
        "p1_act_lbl": "純香精淨重",
        "p1_t1": "🎛️ 1-A：互動式三欄調香機艙",
        "p1_t2": "🧪 1-B：三層資料庫管理（L2 供應商上傳 / L3 自建私有庫）",
        "p1_t3": "📄 1-C：配方總表 (Print-ready Snapshot)",
        "layer_sel": "選擇選料層級：",
        "layer_opts": ["L1 底層化學核心 (CAS 靈感創作)", "L2 商業 SKU 庫 (實際供應商料號)", "L3 調香師自建私有庫 (Custom)"],
        "lib_search": "🔍 搜尋 (CAS / 名稱 / 廠商)：",
        "lib_ph": "例如: 54464-57-2, 肖楠, Givaudan",
        "all_notes": "全部香階",
        "note_lbl": "香階",
        "sg_lbl": "比重 ρ",
        "cost_lbl": "純油單價",
        "ifra_lbl": "IFRA Cat.4 上限",
        "btn_add": "➕ 加入當前配方表",
        "warn_exists": "⚠️ 此料號已在配方中。",
        "ai_exp": "🤖 AI 靈感骨架助理 (從 L1 CAS 核心生成)",
        "ai_cap": "依據五維權重與蒸氣壓計算 5.000g 抽象 CAS 起手骨架：",
        "sl_citrus": "🍊 柑橘清新 (Citrus)",
        "sl_floral": "🌸 優雅花香 (Floral)",
        "sl_woody": "🌲 沉穩木質 (Woody)",
        "sl_spicy": "🌶️ 辛香草本 (Spicy)",
        "sl_sweet": "🍦 溫潤樹脂 (Sweet)",
        "btn_gen": "✨ 生成 L1 骨架並覆蓋當前 Mod",
        "grid_hdr": "#### 🔵 數位配方矩陣 (Formulation Grid)",
        "unit_opts": ["克數 (g) + 佔比", "千分比 (PPT ‰)"],
        "scale_pop": "⚖️ 等比縮放",
        "scale_tgt": "目標總克數 (g)",
        "scale_btn": "執行縮放",
        "empty_form": "👈 當前配方為空。請從左側選擇 L1/L2/L3 原料加入。",
        "pure_price": "純油價",
        "pure_oil": "純油",
        "drops_unit": "滴",
        "probe_hdr": "#### 🟡 即時智慧探針",
        "probe_t1": "🛡️ 金字塔與法規",
        "probe_t2": "🎡 風味輪與揮發",
        "pyr_title": "**嗅覺金字塔結構 (純油有效佔比)：**",
        "top_l": "Top 前調", "mid_l": "Heart 中調", "base_l": "Base 後調",
        "tenacity_lbl": "蒸氣壓留香力指數 (AI Tenacity)",
        "ifra_radar": "IFRA 51st 合規雷達 (跨層同 CAS 合併)",
        "over_limit": "超標！殘留", "limit_word": "限值",
        "near_warn": "逼近警戒",
        "ifra_ok": "✅ 符合 IFRA Cat.4 限值（最高安全賦香率上限：",
        "allg_warn_hdr": "**⚠️ 須外盒標示之致敏原 (>10 ppm)：**",
        "evap_cap": "⏳ 24h 揮發動態模擬：",
        "notes_hdr": "**📝 調香師版本筆記：**",
        "bar_cost": "已映射商業料號純油成本：",
        "bar_base": "基準成本",
        "bar_jus": "原油",
        "bar_ratio": "純香精有效淨重 vs 載體溶劑：",
        "bar_pure": "純油",
        "bar_sol": "溶劑",
        "dl_sheet": "📥 下載配方總表 (CSV)",
        # Phase 2
        "p2_banner": "⚖️ Phase 2：商業 SKU 映射閘門 & 實驗室放樣投料單",
        "p2_tgt_jus": "目標原油母液總重",
        "p2_t0": "🔗 2-A：CAS ➔ 商業 SKU 映射閘門 (L1 轉 L2 必經檢核)",
        "p2_t1": "⚖️ 2-B：天平放樣工作站與實驗室投料單 (100% Jus)",
        "p2_t2": "🧪 2-C：多濃度成品取樣與熟成冷濾 (Phase B 酒精)",
        "p2_sop": "🛡️ **大廠放樣 SOP**：系統已自動將配方強制轉換為 **「後調定香 (Base) ➔ 中調 (Mid) ➔ 高揮發前調 (Top)」** 工業投料序。",
        "p2_prog": "📊 天平累計進度：已完成",
        "p2_items": "項（已投",
        "p2_reset": "🔄 重置打勾記錄",
        "p2_net_add": "本次淨投：",
        "p2_tare": "天平累計：",
        "p2_dosing_hdr": "📋 實驗室標準投料單 (Lab Dosing / Compounding Sheet)",
        "dl_dosing": "📥 下載實驗室投料單 (Lab Dosing Sheet CSV)",
        "p2_samp_hdr": "🧪 多濃度成品取樣計算機 & 熟成冷濾預測",
        "p2_samp_cap": "從調好的 Jus 中取出定量樣品，系統自動扣除載體並加入 3% 低溫冷濾損耗裕度。",
        "samp_a": "#### 樣品 A：日常清新版 (預設 EdT)",
        "samp_b": "#### 樣品 B：沙龍留香版 (預設 EdP)",
        "conc_a": "樣品 A 濃度", "conc_b": "樣品 B 濃度",
        "bot_a": "瓶數 (A)", "bot_b": "瓶數 (B)",
        "vol_a": "單瓶容量 (A)", "vol_b": "單瓶容量 (B)",
        "overfill_lbl": "含 3% 冷濾損耗總投料：",
        "take_jus": "Phase A 取用原油：",
        "add_alc": "Phase B 補入酒精：",
        "lock_a": "✅ 定案採用樣品 A 濃度並送交 Phase 3 PIF",
        "lock_b": "✅ 定案採用樣品 B 濃度並送交 Phase 3 PIF",
        "bal_hdr": "##### 📊 原油母瓶庫存平衡結算：",
        "mac_title": "⏳ 雙階段熟成時鐘：",
        "days_unit": "天",
        # Phase 3
        "p3_banner": "📑 Phase 3：PIF 產品資訊與合規證書 (B2B / OEM / SA Compliance Dossier)",
        "p3_reg": "法規轄區", "p3_dos": "成品賦香率",
        "m_ifra": "IFRA 51st 審查判定",
        "m_max_dos": "Cat.4 香水最高安全賦香率",
        "m_allg": "須展開標示致敏原 (>10ppm)",
        "m_sg": "原油混合比重 / 天然佔比",
        "p3_t1": "1️⃣ 香精全成分比例表 (100% Q&Q)",
        "p3_t2": "2️⃣ 過敏原清單與 INCI 標籤",
        "p3_t3": "3️⃣ IFRA 51st 符合性證書",
        "p3_t4": "4️⃣ 物質安全資料表 (MSDS)",
        "p3_t5": "🔒 5️⃣ 三方保密協議 (NDA) 直傳 SA 模式",
        # Phase 4
        "p4_banner": "🏭 Phase 4：商業量產工單與落地成本框架",
        "p4_deliv": "交付賦香率",
        "p4_s1": "1. 量產批次規模與工單表頭 (Batch Sizing & Dispatch Info)",
        "p4_bot": "首批量產瓶數 (Bottles)",
        "p4_vol": "單瓶容量規格 (ml)",
        "p4_ovf": "冷濾與灌裝損耗裕度 (%)",
        "p4_disp_tgt": "投遞 / 生產單位名稱（空白欄位）",
        "p4_disp_no": "生產批號 / 工單編號（空白欄位）",
        "p4_m1": "成品總預投料重 (含損耗)",
        "p4_m2": "Phase A 調香室投料重 (Jus)",
        "p4_m3": "Phase B 95% 酒精淨投重",
        "p4_m4": "本批次純香精內料基準成本",
        "p4_s2": "2. 工廠生產投料與投遞工單 (Factory BMR Dosing & Dispatch Sheet)",
        "dl_bmr": "📥 下載工廠投料與投遞工單 (Factory BMR & Dispatch Sheet CSV)",
        "p4_s3": "3. 單瓶落地成本框架 (Unit Landed Cost / COGS Framework)"
    },
    "en": {
        "mod_label": "📂 Active Formula Mod",
        "reg_label": "🌐 Regulatory Standard",
        "dos_label": "🎯 Target Dosage",
        "btn_copy": "➕ Copy",
        "btn_clear": "🗑️ Clear",
        "phases": [
            "💻 Phase 1: Formulation (3-Layer DB)",
            "⚖️ Phase 2: SKU Mapping & Lab Dosing",
            "📑 Phase 3: PIF & Compliance Dossier",
            "🏭 Phase 4: Commercial Scale-up & COGS"
        ],
        "p1_banner": "💻 Phase 1: Digital Formulation (L1 Chemical Core / L2 Commercial SKU / L3 Custom Library)",
        "p1_w_lbl": "Total Jus Weight",
        "p1_act_lbl": "Pure Active Oil",
        "p1_t1": "🎛️ 1-A: Interactive 3-Pane Cockpit",
        "p1_t2": "🧪 1-B: 3-Layer Library Manager (L2 Vendor Upload / L3 Custom Material)",
        "p1_t3": "📄 1-C: Formulation Record Sheet (Print-ready)",
        "layer_sel": "Select Metadata Layer:",
        "layer_opts": ["L1 Chemical Core (CAS Inspiration)", "L2 Commercial SKU Library (Vendor Lot)", "L3 Private Custom Library (In-House)"],
        "lib_search": "🔍 Search (CAS / Name / Vendor):",
        "lib_ph": "e.g., 54464-57-2, Cedar, Givaudan",
        "all_notes": "All Notes",
        "note_lbl": "Olfactory Note",
        "sg_lbl": "Specific Gravity ρ",
        "cost_lbl": "Pure Oil Cost",
        "ifra_lbl": "IFRA Cat.4 Limit",
        "btn_add": "➕ Add to Formula Grid",
        "warn_exists": "⚠️ Item already exists in this Mod.",
        "ai_exp": "🤖 AI Skeleton Assistant (L1 CAS Core)",
        "ai_cap": "Synthesize a 5.000g abstract L1 CAS skeleton using vapor pressure & family weights:",
        "sl_citrus": "🍊 Citrus Freshness",
        "sl_floral": "🌸 Elegant Floral",
        "sl_woody": "🌲 Deep Woody",
        "sl_spicy": "🌶️ Spicy / Herbal",
        "sl_sweet": "🍦 Warm Resinous / Sweet",
        "btn_gen": "✨ Synthesize L1 Skeleton",
        "grid_hdr": "#### 🔵 Formulation Grid",
        "unit_opts": ["Weight (g) + %", "Parts Per Thousand (PPT ‰)"],
        "scale_pop": "⚖️ Auto-Scale",
        "scale_tgt": "Target Batch Weight (g)",
        "scale_btn": "Apply Scale",
        "empty_form": "👈 Formula is empty. Add materials from L1, L2, or L3 on the left.",
        "pure_price": "Oil Cost",
        "pure_oil": "Active",
        "drops_unit": "drops",
        "probe_hdr": "#### 🟡 Real-Time Smart Probes",
        "probe_t1": "🛡️ Pyramid & IFRA",
        "probe_t2": "🎡 Wheel & Kinetics",
        "pyr_title": "**Olfactory Pyramid (Pure Active Share):**",
        "top_l": "Top Note", "mid_l": "Heart Note", "base_l": "Base Note",
        "tenacity_lbl": "Vapor Pressure Tenacity Index",
        "ifra_radar": "IFRA 51st Radar (Cross-Layer CAS Sum)",
        "over_limit": "EXCEEDS LIMIT! Finished:", "limit_word": "Max:",
        "near_warn": "Approaching Limit",
        "ifra_ok": "✅ IFRA Cat.4 Compliant (Max Safe Dosage Limit: ",
        "allg_warn_hdr": "**⚠️ Mandatory Label Allergens (>10 ppm):**",
        "evap_cap": "⏳ 24h Evaporation Kinetics Simulation:",
        "notes_hdr": "**📝 Perfumer Mod Notes:**",
        "bar_cost": "Mapped SKU Pure Oil Cost:",
        "bar_base": "Unit Cost",
        "bar_jus": "Jus",
        "bar_ratio": "Pure Active Oil vs. Carrier Solvent:",
        "bar_pure": "Pure Oil",
        "bar_sol": "Solvent",
        "dl_sheet": "📥 Download Formula Sheet (CSV)",
        # Phase 2
        "p2_banner": "⚖️ Phase 2: Commercial SKU Mapping Gate & Lab Dosing",
        "p2_tgt_jus": "Target Jus Batch Weight",
        "p2_t0": "🔗 2-A: CAS ➔ Commercial SKU Mapping Gate (L1 to L2)",
        "p2_t1": "⚖️ 2-B: Running Tare Bench & Lab Dosing Sheet (100% Jus)",
        "p2_t2": "🧪 2-C: Multi-Concentration Sampler & Filtration",
        "p2_sop": "🛡️ **Industrial Compounding SOP**: Materials are automatically sorted in **Base ➔ Heart (Mid) ➔ Top** order. Zero your scale (Tare) and check off each addition.",
        "p2_prog": "📊 Bench Progress: Completed",
        "p2_items": "items (Dosed",
        "p2_reset": "🔄 Reset Checklist",
        "p2_net_add": "Net Addition:",
        "p2_tare": "Running Tare:",
        "p2_dosing_hdr": "📋 Standard Lab Dosing / Compounding Sheet",
        "dl_dosing": "📥 Download Lab Dosing Sheet (CSV)",
        "p2_samp_hdr": "🧪 Multi-Concentration Sampler & Maceration Predictor",
        "p2_samp_cap": "Draw aliquots from your compounded Jus; automatically deducts carrier solvents and adds a 3% chill-filtration overfill buffer.",
        "samp_a": "#### Sample A: Fresh Daily (Default EdT)",
        "samp_b": "#### Sample B: Long-Lasting (Default EdP)",
        "conc_a": "Sample A Concentration", "conc_b": "Sample B Concentration",
        "bot_a": "Bottles (A)", "bot_b": "Bottles (B)",
        "vol_a": "Bottle Vol (A)", "vol_b": "Bottle Vol (B)",
        "overfill_lbl": "Total Batch w/ 3% Overfill:",
        "take_jus": "Phase A Draw Jus:",
        "add_alc": "Phase B Add Ethanol:",
        "lock_a": "✅ Approve Sample A & Send to Phase 3 PIF",
        "lock_b": "✅ Approve Sample B & Send to Phase 3 PIF",
        "bal_hdr": "##### 📊 Mother Jus Bottle Inventory Balance:",
        "mac_title": "⏳ Dual-Phase Maceration Clock:",
        "days_unit": "Days",
        # Phase 3
        "p3_banner": "📑 Phase 3: Product Information File (PIF) & Compliance Certificates",
        "p3_reg": "Jurisdiction", "p3_dos": "Target Dosage",
        "m_ifra": "IFRA 51st Status",
        "m_max_dos": "Cat.4 Max Safe Dosage",
        "m_allg": "Declarable Allergens (>10ppm)",
        "m_sg": "Jus SG / Natural Share",
        "p3_t1": "1️⃣ 100% Quantitative Formula",
        "p3_t2": "2️⃣ Allergens & INCI Label",
        "p3_t3": "3️⃣ IFRA 51st Certificate",
        "p3_t4": "4️⃣ MSDS / Safety Summary",
        "p3_t5": "🔒 5️⃣ Tri-Party NDA Direct-to-SA Mode",
        # Phase 4
        "p4_banner": "🏭 Phase 4: Commercial Scale-up BMR & Landed Cost Framework",
        "p4_deliv": "Delivery Dosage",
        "p4_s1": "1. Production Batch Sizing & Dispatch Header",
        "p4_bot": "Production Batch Size (Bottles)",
        "p4_vol": "Unit Volume (ml)",
        "p4_ovf": "Filtration & Filling Overfill (%)",
        "p4_disp_tgt": "Dispatch / OEM Facility Name (Blank Field)",
        "p4_disp_no": "Batch / Work Order No. (Blank Field)",
        "p4_m1": "Total Gross Batch (w/ Overfill)",
        "p4_m2": "Phase A Compounding Jus",
        "p4_m3": "Phase B Net 95% Ethanol",
        "p4_m4": "Batch Pure Fragrance Cost",
        "p4_s2": "2. Factory BMR Dosing & Dispatch Sheet",
        "dl_bmr": "📥 Download Factory BMR & Dispatch Sheet (CSV)",
        "p4_s3": "3. Unit Landed Cost / COGS Framework (Blank Vendor Fields)"
    }
}

lang = st.session_state.lang
t = UI[lang]

# ==============================================================================
# TOP GLOBAL PROJECT BRIEF RIBBON + LANGUAGE SWITCHER
# ==============================================================================
c_hdr1, c_hdr2 = st.columns([5.2, 1.0])
c_hdr1.markdown("### 🧪 Nanmen Scent Lab OS")
chosen_lang = c_hdr2.radio("Lang", ["中文", "EN"], index=0 if lang == "zh" else 1, horizontal=True, label_visibility="collapsed")
new_lang = "zh" if chosen_lang == "中文" else "en"
if new_lang != lang:
    st.session_state.lang = new_lang
    st.rerun()

with st.container():
    tb1, tb2, tb3, tb4 = st.columns([1.3, 1.5, 1.5, 1.0])
    with tb1:
        mod_list = list(st.session_state.mods.keys())
        st.session_state.active_mod = st.selectbox(t["mod_label"], mod_list, index=mod_list.index(st.session_state.active_mod))
    with tb2:
        reg_keys = list(REGULATORY_REGIONS.keys())
        st.session_state.region_id = st.selectbox(
            t["reg_label"], reg_keys,
            index=reg_keys.index(st.session_state.region_id),
            format_func=lambda k: REGULATORY_REGIONS[k][f"name_{lang}"]
        )
    with tb3:
        tier_keys = list(PERFUME_CONCENTRATION_PRESETS.keys())
        st.session_state.tier_id = st.selectbox(
            t["dos_label"], tier_keys,
            index=tier_keys.index(st.session_state.tier_id),
            format_func=lambda k: PERFUME_CONCENTRATION_PRESETS[k][lang]
        )
    with tb4:
        st.write("")
        c_m1, c_m2 = st.columns(2)
        if c_m1.button(t["btn_copy"], use_container_width=True):
            new_name = f"Mod {len(mod_list) + 1}"
            st.session_state.mods[new_name] = copy.deepcopy(st.session_state.mods[st.session_state.active_mod])
            st.session_state.mod_notes[new_name] = f"Copy of {st.session_state.active_mod}"
            st.session_state.active_mod = new_name
            st.session_state.locked_for_pif = False
            st.rerun()
        if c_m2.button(t["btn_clear"], use_container_width=True):
            st.session_state.mods[st.session_state.active_mod] = {}
            st.session_state.locked_for_pif = False
            st.rerun()

region_info = REGULATORY_REGIONS[st.session_state.region_id]
tier_info = PERFUME_CONCENTRATION_PRESETS[st.session_state.tier_id]
dosage_ratio = tier_info["ratio"]
current_formula = st.session_state.mods[st.session_state.active_mod]
total_jus_g = sum([d.get("gross_g", 0.0) for d in current_formula.values()])

core_db = st.session_state.core_db
sku_db = st.session_state.commercial_skus
custom_db = st.session_state.custom_materials

rt_calc = core.analyze_formula_realtime(current_formula, dosage_ratio, core_db, sku_db, custom_db, lang=lang)
mod_calc = core.calculate_mod_profile(current_formula, dosage_ratio, {"bottles": 1, "vol_ml": 10}, core_db, sku_db, custom_db, lang=lang)
mac_meta = core.predict_maceration_and_filtration(current_formula, dosage_ratio, {"bottles": 1, "vol_ml": 10}, core_db, sku_db, custom_db, lang=lang)

# ==============================================================================
# LINEAR 4-PHASE TOP NAVIGATION
# ==============================================================================
selected_phase_label = st.radio(
    "Phase Navigation",
    t["phases"],
    index=st.session_state.phase_idx,
    horizontal=True,
    label_visibility="collapsed"
)
st.session_state.phase_idx = t["phases"].index(selected_phase_label)
st.divider()

# ==============================================================================
# PHASE 1: Digital Formulation + 3-Layer DB Manager + Print Sheet
# ==============================================================================
if st.session_state.phase_idx == 0:
    st.markdown(f"""
    <div style="background:#0F172A; padding:8px 16px; border-radius:6px; color:white; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
        <div><b>{t['p1_banner']}</b> ｜ Mod: <span class="mod-pill">{st.session_state.active_mod}</span></div>
        <div style="font-size:13px; color:#94A3B8;">{t['p1_w_lbl']}: <b style="color:#FBBF24; font-size:15px;">{total_jus_g:.3f} g</b> ｜ {t['p1_act_lbl']}: <b style="color:#38BDF8;">{rt_calc['total_active_g']:.3f} g</b></div>
    </div>
    """, unsafe_allow_html=True)

    ph1_tab_edit, ph1_tab_db, ph1_tab_print = st.tabs([t["p1_t1"], t["p1_t2"], t["p1_t3"]])

    # --------------------------------------------------------------------------
    # 1-A: Interactive 3-Pane Cockpit (Select from Layer 1, Layer 2, or Layer 3)
    # --------------------------------------------------------------------------
    with ph1_tab_edit:
        p_left, p_mid, p_right = st.columns([1.2, 2.2, 1.25])

        with p_left:
            layer_idx = st.selectbox(t["layer_sel"], [0, 1, 2], format_func=lambda i: t["layer_opts"][i])
            c_f1, c_f2 = st.columns([1.4, 1.0])
            lib_search = c_f1.text_input(t["lib_search"], placeholder=t["lib_ph"], label_visibility="collapsed")
            note_filter = c_f2.selectbox("Note", [t["all_notes"], "Top", "Mid", "Base"], label_visibility="collapsed")

            selected_hero_cas = None

            # --- LAYER 1: Chemical Core (CAS) ---
            if layer_idx == 0:
                filtered_cas = []
                for cas, v in core_db.items():
                    txt_ok = (lib_search.lower() in v["name_cn"].lower() or lib_search.lower() in v["name_en"].lower() or lib_search.lower() in cas.lower())
                    note_ok = True if note_filter == t["all_notes"] else (note_filter in v.get("note", ""))
                    if txt_ok and note_ok:
                        filtered_cas.append(cas)

                chosen_cas = st.selectbox(
                    "L1 CAS", filtered_cas if filtered_cas else list(core_db.keys()),
                    format_func=lambda c: f"[{core_db[c]['note'][:1]}] {core_db[c]['name_en'] if lang == 'en' else core_db[c]['name_cn']} ({c})",
                    label_visibility="collapsed"
                )
                selected_hero_cas = chosen_cas
                if chosen_cas:
                    cm = core_db[chosen_cas]
                    tier_color = "#10B981" if "Top" in cm["note"] else ("#F59E0B" if "Mid" in cm["note"] else "#78350F")
                    disp_n = cm["name_en"] if lang == "en" else cm["name_cn"]
                    disp_d = cm["desc_en"] if lang == "en" else cm["desc_zh"]
                    mapped_skus = [s for s in sku_db.values() if s["cas"] == chosen_cas]
                    st.markdown(f"""
                    <div class="mat-card" style="border-left: 4px solid {tier_color};">
                        <span class="layer-l1">LAYER 1: CHEMICAL CORE</span>
                        <div style="font-weight:bold; font-size:14px; color:#0F172A; margin-top:4px;">{disp_n}</div>
                        <div style="margin:4px 0;"><span class="cas-badge">CAS: {cm['cas']}</span> <span style="font-size:11px; color:#0284C7;">({len(mapped_skus)} SKUs)</span></div>
                        <div style="font-size:12px; color:#475569; margin-top:4px;">
                            • MW: <b>{cm['mol_w']} g/mol</b> ｜ VP: <b>{cm['vapor_pressure_mmhg']} mmHg</b><br>
                            • {t['note_lbl']}: <b>{cm['note']}</b> ({cm['family']}) ｜ {t['ifra_lbl']}: <b>{cm['ifra_cat4_max']}%</b>
                        </div>
                        <div style="font-size:12px; color:#334155; font-style:italic; margin-top:6px; padding-top:6px; border-top:1px dashed #CBD5E1;">"{disp_d}"</div>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button(t["btn_add"], key="add_l1", use_container_width=True, type="primary"):
                        lid = f"L1_{chosen_cas}"
                        if lid not in current_formula:
                            st.session_state.mods[st.session_state.active_mod][lid] = {
                                "layer": "L1_CORE", "cas": chosen_cas, "sku_id": None,
                                "gross_g": 0.200, "dilution_pct": 100.0 if cm["ifra_cat4_max"] > 5.0 else 10.0,
                                "solvent": "None (100%純原液)" if cm["ifra_cat4_max"] > 5.0 else "DPG (二丙二醇)"
                            }
                            st.rerun()
                        else:
                            st.warning(t["warn_exists"])

            # --- LAYER 2: Commercial SKU Library ---
            elif layer_idx == 1:
                filtered_skus = []
                for sid, s in sku_db.items():
                    cm = core_db.get(s["cas"], {})
                    txt_ok = (
                        lib_search.lower() in s["trade_name_cn"].lower() or lib_search.lower() in s["trade_name_en"].lower()
                        or lib_search.lower() in s["cas"].lower() or lib_search.lower() in s["supplier_zh"].lower()
                        or lib_search.lower() in s["supplier_en"].lower()
                    )
                    note_ok = True if note_filter == t["all_notes"] else (note_filter in cm.get("note", ""))
                    if txt_ok and note_ok:
                        filtered_skus.append(sid)

                chosen_sku = st.selectbox(
                    "L2 SKU", filtered_skus if filtered_skus else list(sku_db.keys()),
                    format_func=lambda sid: f"[{sku_db[sid]['supplier_en' if lang=='en' else 'supplier_zh']}] {sku_db[sid]['trade_name_en' if lang=='en' else 'trade_name_cn']}",
                    label_visibility="collapsed"
                )
                if chosen_sku:
                    sm = sku_db[chosen_sku]
                    cm = core_db.get(sm["cas"], {})
                    selected_hero_cas = sm["cas"]
                    disp_n = sm["trade_name_en"] if lang == "en" else sm["trade_name_cn"]
                    disp_sup = sm["supplier_en"] if lang == "en" else sm["supplier_zh"]
                    docs_str = " ".join([f"✅{k}" for k, v in sm.get("docs", {}).items() if v])
                    st.markdown(f"""
                    <div class="mat-card" style="border-left: 4px solid #16A34A;">
                        <span class="layer-l2">LAYER 2: COMMERCIAL SKU</span>
                        <div style="font-weight:bold; font-size:14px; color:#0F172A; margin-top:4px;">{disp_n}</div>
                        <div style="margin:4px 0;"><span class="cas-badge">CAS: {sm['cas']}</span> <span style="font-size:11px; color:#15803D; font-weight:bold;">{disp_sup}</span></div>
                        <div style="font-size:12px; color:#475569; margin-top:4px;">
                            • Lot: <code>{sm['lot_no']}</code> ｜ EXP: <b>{sm['exp_date']}</b><br>
                            • Purity: <b>{sm['dilution_pct']:.0f}%</b> ｜ {t['cost_lbl']}: <b>NT$ {sm['cost_per_g']}/g</b><br>
                            • Docs: <b>{docs_str}</b>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button(t["btn_add"], key="add_l2", use_container_width=True, type="primary"):
                        lid = f"L2_{chosen_sku}"
                        if lid not in current_formula:
                            st.session_state.mods[st.session_state.active_mod][lid] = {
                                "layer": "L2_SKU", "cas": sm["cas"], "sku_id": chosen_sku,
                                "gross_g": 0.200, "dilution_pct": sm["dilution_pct"], "solvent": sm["solvent"]
                            }
                            st.rerun()
                        else:
                            st.warning(t["warn_exists"])

            # --- LAYER 3: Custom Private Library ---
            else:
                if not custom_db:
                    st.info("No custom materials yet. Add one in Tab 1-B.")
                else:
                    chosen_cust = st.selectbox(
                        "L3 Custom", list(custom_db.keys()),
                        format_func=lambda cid: f"{custom_db[cid]['name_en' if lang=='en' else 'name_cn']} ({custom_db[cid]['dilution_pct']:.0f}%)",
                        label_visibility="collapsed"
                    )
                    if chosen_cust:
                        cu = custom_db[chosen_cust]
                        selected_hero_cas = cu["cas"]
                        disp_n = cu["name_en"] if lang == "en" else cu["name_cn"]
                        st.markdown(f"""
                        <div class="mat-card" style="border-left: 4px solid #7E22CE;">
                            <span class="layer-l3">LAYER 3: PRIVATE CUSTOM</span>
                            <div style="font-weight:bold; font-size:14px; color:#0F172A; margin-top:4px;">{disp_n}</div>
                            <div style="margin:4px 0;"><span class="cas-badge">Mapped CAS: {cu['cas']}</span></div>
                            <div style="font-size:12px; color:#475569; margin-top:4px;">
                                • Concentration: <b>{cu['dilution_pct']:.1f}%</b> in {cu['solvent'].split(' ')[0]}<br>
                                • {t['sg_lbl']}: <b>{cu['sg_pure']}</b> ｜ {t['cost_lbl']}: <b>NT$ {cu['cost_per_g']}/g</b>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        if st.button(t["btn_add"], key="add_l3", use_container_width=True, type="primary"):
                            lid = f"L3_{chosen_cust}"
                            if lid not in current_formula:
                                st.session_state.mods[st.session_state.active_mod][lid] = {
                                    "layer": "L3_CUSTOM", "cas": cu["cas"], "custom_id": chosen_cust,
                                    "gross_g": 0.200, "dilution_pct": cu["dilution_pct"], "solvent": cu["solvent"]
                                }
                                st.rerun()
                            else:
                                st.warning(t["warn_exists"])

            with st.expander(t["ai_exp"]):
                st.caption(t["ai_cap"])
                w_citrus = st.slider(t["sl_citrus"], 0, 100, 25, 5)
                w_floral = st.slider(t["sl_floral"], 0, 100, 25, 5)
                w_woody = st.slider(t["sl_woody"], 0, 100, 35, 5)
                w_spicy = st.slider(t["sl_spicy"], 0, 100, 10, 5)
                w_sweet = st.slider(t["sl_sweet"], 0, 100, 5, 5)
                if st.button(t["btn_gen"], use_container_width=True):
                    s_dict = {"Citrus": w_citrus, "Floral": w_floral, "Woody": w_woody, "Spicy": w_spicy, "Sweet": w_sweet}
                    st.session_state.mods[st.session_state.active_mod] = core.synthesize_canvas_formula(s_dict, selected_hero_cas, 5.0, core_db)
                    st.rerun()

        # 🔵 CENTER PANE: Formulation Grid
        with p_mid:
            c_title, c_tools = st.columns([1.4, 1.3])
            with c_title:
                st.markdown(t["grid_hdr"])
            with c_tools:
                t_col1, t_col2 = st.columns(2)
                with t_col1:
                    display_unit = st.selectbox("Unit", t["unit_opts"], label_visibility="collapsed")
                with t_col2:
                    with st.popover(t["scale_pop"]):
                        target_g = st.number_input(t["scale_tgt"], min_value=1.0, max_value=5000.0, value=max(5.0, round(total_jus_g, 2)), step=1.0)
                        if st.button(t["scale_btn"], use_container_width=True) and total_jus_g > 0:
                            mult = target_g / total_jus_g
                            for k in current_formula:
                                current_formula[k]["gross_g"] = round(current_formula[k]["gross_g"] * mult, 3)
                            st.session_state.mods[st.session_state.active_mod] = current_formula
                            st.rerun()

            creation_rows = core.build_compounding_sheet(current_formula, dosage_ratio, core_db, sku_db, custom_db, sort_by_compounding=False, lang=lang)

            if not creation_rows:
                st.info(t["empty_form"])
            else:
                for row in creation_rows:
                    lid = row["line_id"]
                    layer_badge = (
                        "<span class='layer-l2'>L2 SKU</span>" if row["layer"] == "L2_SKU"
                        else ("<span class='layer-l3'>L3 CUSTOM</span>" if row["layer"] == "L3_CUSTOM" else "<span class='layer-l1'>L1 CAS</span>")
                    )
                    with st.container(border=True):
                        r1, r2, r3, r4, r5 = st.columns([2.2, 1.1, 1.3, 1.4, 0.45])
                        r1.markdown(
                            f"**{row['name_disp']}**<br>{layer_badge} <span class='cas-badge'>{row['note']}</span> "
                            f"<span style='font-size:11px; color:#64748B;'>{t['pure_price']}: ${row['cost']:.1f}</span>",
                            unsafe_allow_html=True
                        )
                        new_dil = r2.selectbox("Dil", DILUTION_TIERS, index=DILUTION_TIERS.index(float(row["dilution_pct"])) if float(row["dilution_pct"]) in DILUTION_TIERS else 0, key=f"p1_dil_{st.session_state.active_mod}_{lid}", label_visibility="collapsed")
                        new_sol = r3.selectbox(
                            "Sol", SOLVENT_CHOICES,
                            index=SOLVENT_CHOICES.index(row["solvent"]) if row["solvent"] in SOLVENT_CHOICES else 0,
                            format_func=lambda s: SOLVENT_DATABASE[s][lang],
                            key=f"p1_sol_{st.session_state.active_mod}_{lid}",
                            label_visibility="collapsed"
                        )
                        new_g = r4.number_input("g", min_value=0.001, max_value=1000.0, value=float(row["gross_g"]), step=0.010, format="%.3f", key=f"p1_g_{st.session_state.active_mod}_{lid}", label_visibility="collapsed")
                        if "PPT" in display_unit:
                            r4.caption(f"📊 **{row['ppt']:.1f} ‰** ({t['pure_oil']} {row['active_g']:.3f}g)")
                        else:
                            r4.caption(f"📊 **{row['pct']:.1f}%** ({row['drops']} {t['drops_unit']})")

                        if r5.button("🗑️", key=f"p1_del_{st.session_state.active_mod}_{lid}"):
                            del st.session_state.mods[st.session_state.active_mod][lid]
                            st.rerun()

                        if abs(new_dil - row["dilution_pct"]) > 1e-4 or new_sol != row["solvent"] or abs(new_g - row["gross_g"]) > 1e-4:
                            st.session_state.mods[st.session_state.active_mod][lid]["gross_g"] = new_g
                            st.session_state.mods[st.session_state.active_mod][lid]["dilution_pct"] = new_dil
                            st.session_state.mods[st.session_state.active_mod][lid]["solvent"] = new_sol
                            st.rerun()

        # 🟡 RIGHT PANE: Real-Time Smart Probes
        with p_right:
            st.markdown(t["probe_hdr"])
            probe_tab1, probe_tab2 = st.tabs([t["probe_t1"], t["probe_t2"]])

            with probe_tab1:
                if mod_calc:
                    st.markdown(t["pyr_title"])
                    top_p, mid_p, base_p = mod_calc["notes_pct"]["Top"], mod_calc["notes_pct"]["Mid"], mod_calc["notes_pct"]["Base"]
                    st.caption(f"{t['top_l']}: {top_p:.1f}%")
                    st.progress(min(1.0, top_p / 100.0))
                    st.caption(f"{t['mid_l']}: {mid_p:.1f}%")
                    st.progress(min(1.0, mid_p / 100.0))
                    st.caption(f"{t['base_l']}: {base_p:.1f}%")
                    st.progress(min(1.0, base_p / 100.0))
                    st.caption(f"⏳ {t['tenacity_lbl']}: **{rt_calc['tenacity_score']} / 100**")

                st.divider()
                st.markdown(f"**{t['ifra_radar']} ({region_info['code']} @ {dosage_ratio*100:.0f}%)：**")
                all_safe = True
                for lid, stat in rt_calc["ifra_status"].items():
                    if not stat["is_safe"]:
                        all_safe = False
                        st.error(f"❌ **{stat['name_disp']}** {t['over_limit']} {stat['finished_pct']:.2f}% > {t['limit_word']} {stat['limit']}%")
                    elif stat["is_warn"]:
                        st.warning(f"⚠️ **{stat['name_disp']}** {t['near_warn']} ({stat['risk_ratio']*100:.0f}%)")
                if all_safe and current_formula:
                    st.success(f"{t['ifra_ok']}{rt_calc['max_safe_dosage_pct']:.1f}%）")

                allg_dict = rt_calc.get("allergen_summary", {})
                over_allg = {k: v for k, v in allg_dict.items() if v >= region_info["allergen_ppm_threshold"]}
                if over_allg:
                    st.markdown(t["allg_warn_hdr"])
                    for a_k, a_v in sorted(over_allg.items(), key=lambda x: x[1], reverse=True):
                        st.caption(f"• `{a_k}`: **{a_v:.1f} ppm**")

            with probe_tab2:
                if mod_calc:
                    sb_items = [{"Family": v["family"], "Name": v["name_disp"], "ActiveWeight": v["active_pct"]} for v in mod_calc["norm_active"].values()]
                    if sb_items:
                        fig_sb = px.sunburst(
                            pd.DataFrame(sb_items), path=["Family", "Name"], values="ActiveWeight",
                            color="Family",
                            color_discrete_map={"Woody": "#78350F", "Floral": "#EC4899", "Citrus": "#F59E0B", "Sweet": "#EF4444", "Spicy": "#B45309"},
                            height=240
                        )
                        fig_sb.update_layout(margin=dict(l=0, r=0, t=0, b=0))
                        st.plotly_chart(fig_sb, use_container_width=True)

                    st.caption(t["evap_cap"])
                    fig_traj = px.line(
                        mod_calc["trajectory"], x="Hour", y=["Top", "Mid", "Base"],
                        color_discrete_map={"Top": "#10B981", "Mid": "#F59E0B", "Base": "#6B7280"},
                        height=200
                    )
                    fig_traj.update_layout(margin=dict(l=0, r=0, t=0, b=0), hovermode="x unified", showlegend=True)
                    st.plotly_chart(fig_traj, use_container_width=True)

            st.divider()
            st.markdown(t["notes_hdr"])
            c_n = st.session_state.mod_notes.get(st.session_state.active_mod, "")
            n_n = st.text_area("Notes", value=c_n, height=85, label_visibility="collapsed")
            if n_n != c_n:
                st.session_state.mod_notes[st.session_state.active_mod] = n_n

        # 🏁 BOTTOM STATS BAR
        if mod_calc:
            est_cost = mod_calc.get("total_cost", 0.0)
            est_cost_per_10g = (est_cost / total_jus_g * 10.0) if total_jus_g > 0 else 0.0
            unmapped_note = f" | ⚠️ {rt_calc['unmapped_count']} L1 CAS unmapped" if rt_calc["unmapped_count"] > 0 else ""
            st.markdown(f"""
            <div class="stats-bar">
                <div>
                    <span style="color:#94A3B8; font-size:12px;">{t['bar_cost']}</span>
                    <b style="color:#FBBF24; font-size:16px;">NT$ {est_cost:.1f}</b>
                    <span style="color:#64748B; font-size:12px; margin-left:8px;">({t['bar_base']}: NT$ {est_cost_per_10g:.1f} / 10g {t['bar_jus']}{unmapped_note})</span>
                </div>
                <div>
                    <span style="color:#94A3B8; font-size:12px;">{t['bar_ratio']}</span>
                    <b style="color:#38BDF8; font-size:15px;">{rt_calc['total_active_g']:.3f} g {t['bar_pure']}</b>
                    <span style="color:#94A3B8; font-size:12px;"> + {rt_calc['total_carrier_g']:.3f} g {t['bar_sol']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # 1-B: 3-Layer Metadata Manager (Layer 2 Vendor SKU Upload & Layer 3 Custom Material)
    # --------------------------------------------------------------------------
    with ph1_tab_db:
        with st.expander("🌐 Layer 1 擴充：輸入 CAS 線上抓取純物質物性 (PubChem API Auto-Fetch)", expanded=False):
            st.caption("輸入新單體的 CAS 號碼，系統自動連線 PubChem 抓取標準英文學名與分子量（MW），再補上香階與 IFRA Cat.4 限量即可寫入 Layer 1 核心庫。")
            pc1, pc2, pc3 = st.columns([1.4, 1.0, 2.0])
            query_cas = pc1.text_input("輸入 CAS 號碼", placeholder="例如: 78-70-6 (Linalool)", key="pubchem_cas_in")
            if pc2.button("🔍 線上查詢 PubChem", use_container_width=True):
                fetched, err = core.fetch_pubchem_metadata_by_cas(query_cas)
                if fetched:
                    st.session_state["pubchem_preview"] = fetched
                else:
                    st.warning(f"查詢未成功 ({err})，您仍可在下方手動建檔。")
                    st.session_state["pubchem_preview"] = {"cas": query_cas.strip(), "name_en": "", "mol_w": 200.0}

            prev = st.session_state.get("pubchem_preview")
            if prev and prev.get("cas"):
                with st.form("save_l1_cas_form", clear_on_submit=True):
                    f_c1, f_c2, f_c3 = st.columns(3)
                    l1_cas = f_c1.text_input("CAS No.", value=prev.get("cas", ""))
                    l1_en = f_c2.text_input("英文名稱 (Name EN)", value=prev.get("name_en", ""))
                    l1_cn = f_c3.text_input("中文名稱 (Name CN)", value=prev.get("name_en", ""))
                    f_c4, f_c5, f_c6, f_c7 = st.columns(4)
                    l1_mw = f_c4.number_input("分子量 MW", 50.0, 1000.0, float(prev.get("mol_w", 200.0)), 0.1)
                    l1_vp = f_c5.number_input("蒸氣壓 VP (mmHg)", 0.00001, 50.0, 0.05, format="%.5f")
                    l1_note = f_c6.selectbox("香階 Note", ["Top", "Top-Mid", "Mid", "Mid-Base", "Base"], index=2)
                    l1_fam = f_c7.selectbox("香調家族 Family", ["Citrus", "Floral", "Woody", "Spicy", "Sweet"], index=1)
                    l1_ifra = st.number_input("IFRA 51st Cat.4 最高限量 (%)", 0.01, 100.0, 100.0, 0.1)
                    if st.form_submit_button("➕ 寫入 Layer 1 化學核心庫", type="primary"):
                        if l1_cas and l1_en:
                            st.session_state.core_db[l1_cas.strip()] = {
                                "cas": l1_cas.strip(),
                                "name_cn": l1_cn.strip() or l1_en.strip(),
                                "name_en": l1_en.strip(),
                                "note": l1_note,
                                "family": l1_fam,
                                "type": "Aroma Chemical",
                                "mol_w": l1_mw,
                                "vapor_pressure_mmhg": l1_vp,
                                "sg_pure": 0.950,
                                "ifra_cat4_max": l1_ifra,
                                "baseline_allergens": {},
                                "desc_zh": f"透過 PubChem 建檔之單體 (MW: {l1_mw})。",
                                "desc_en": f"Monomer indexed via PubChem (MW: {l1_mw})."
                            }
                            del st.session_state["pubchem_preview"]
                            st.success(f"✅ 已將 CAS {l1_cas} ({l1_en}) 加入 Layer 1 化學核心庫！")
                            st.rerun()

        db_col_l2, db_col_l3 = st.columns(2)

        # --- Layer 2: Vendor / OEM Commercial SKU Upload ---
        with db_col_l2:
            st.subheader("📦 Layer 2：商業 SKU 庫上傳 (Vendor / OEM SKU Registry)")
            st.caption("供原料商或代工廠匯入具體商業料號，必須映射至 Layer 1 的 CAS 號碼，並可上傳批號、效期與單價。")

            with st.form("add_l2_sku_form", clear_on_submit=True):
                new_sku_id = st.text_input("商業料號 SKU ID *", placeholder="例如: SKU-GIV-54464-100")
                map_cas = st.selectbox(
                    "映射底層純物質 CAS *", list(core_db.keys()),
                    format_func=lambda c: f"{c} — {core_db[c]['name_en'] if lang=='en' else core_db[c]['name_cn']}"
                )
                s_c1, s_c2 = st.columns(2)
                trade_cn = s_c1.text_input("中文商品名稱 *", placeholder="例如: 奇華頓龍涎酮 100%")
                trade_en = s_c2.text_input("英文商品名稱 *", placeholder="e.g., Givaudan Iso E Super 100%")
                v_c1, v_c2 = st.columns(2)
                sup_zh = v_c1.text_input("供應商名稱", value="Givaudan / 代工廠")
                lot_no = v_c2.text_input("批號 (Lot No.)", value=f"LOT-{datetime.now().strftime('%y%m%d')}")
                p_c1, p_c2, p_c3 = st.columns(3)
                sku_dil = p_c1.number_input("商業純度 (%)", 1.0, 100.0, 100.0, 1.0)
                sku_sol = p_c2.selectbox("預設溶劑", SOLVENT_CHOICES, index=0)
                sku_cost = p_c3.number_input("純油單價 (NT$/g)", 0.0, 5000.0, 10.0, 0.5)

                d_c1, d_c2, d_c3 = st.columns(3)
                has_coa = d_c1.checkbox("掛載 COA 檢驗單", value=True)
                has_sds = d_c2.checkbox("掛載 SDS 安全表", value=True)
                has_ifra = d_c3.checkbox("掛載 IFRA 證書", value=True)

                if st.form_submit_button("➕ 註冊商業 SKU 至 Layer 2", type="primary", use_container_width=True):
                    if new_sku_id and trade_cn:
                        st.session_state.commercial_skus[new_sku_id.strip()] = {
                            "sku_id": new_sku_id.strip(),
                            "cas": map_cas,
                            "trade_name_cn": trade_cn.strip(),
                            "trade_name_en": trade_en.strip() or trade_cn.strip(),
                            "supplier_zh": sup_zh.strip(),
                            "supplier_en": sup_zh.strip(),
                            "lot_no": lot_no.strip(),
                            "exp_date": "2029/12/31",
                            "dilution_pct": sku_dil,
                            "solvent": sku_sol,
                            "sg": core_db[map_cas]["sg_pure"],
                            "cost_per_g": sku_cost,
                            "docs": {"COA": has_coa, "SDS": has_sds, "IFRA": has_ifra},
                            "allergens": core_db[map_cas].get("baseline_allergens", {})
                        }
                        st.success(f"✅ 已成功新增商業 SKU：{new_sku_id}")
                        st.rerun()

            # Batch CSV upload for Layer 2 SKUs
            uploaded_sku_csv = st.file_uploader("📂 或批次上傳供應商 SKU 清單 (CSV)", type=["csv"], key="sku_csv_up")
            if uploaded_sku_csv is not None:
                try:
                    df_up = pd.read_csv(uploaded_sku_csv)
                    added_n = 0
                    for _, r in df_up.iterrows():
                        sid = str(r.get("sku_id", "")).strip()
                        cas_val = str(r.get("cas", "")).strip()
                        if sid and cas_val in core_db:
                            st.session_state.commercial_skus[sid] = {
                                "sku_id": sid,
                                "cas": cas_val,
                                "trade_name_cn": str(r.get("trade_name_cn", sid)),
                                "trade_name_en": str(r.get("trade_name_en", sid)),
                                "supplier_zh": str(r.get("supplier", "Uploaded Vendor")),
                                "supplier_en": str(r.get("supplier", "Uploaded Vendor")),
                                "lot_no": str(r.get("lot_no", "LOT-CSV")),
                                "exp_date": str(r.get("exp_date", "2029/12/31")),
                                "dilution_pct": float(r.get("dilution_pct", 100.0)),
                                "solvent": str(r.get("solvent", "None (100%純原液)")),
                                "sg": float(r.get("sg", core_db[cas_val]["sg_pure"])),
                                "cost_per_g": float(r.get("cost_per_g", 0.0)),
                                "docs": {"COA": True, "SDS": True, "IFRA": True},
                                "allergens": core_db[cas_val].get("baseline_allergens", {})
                            }
                            added_n += 1
                    if added_n > 0:
                        st.success(f"✅ 已匯入 {added_n} 筆供應商 SKU！")
                except Exception as e:
                    st.error(f"CSV 格式錯誤: {e}")

        # --- Layer 3: Perfumer Custom Private Material ---
        with db_col_l3:
            st.subheader("🧪 Layer 3：調香師自建私有庫 (Custom Material)")
            st.caption("輸入手邊特殊酊劑、複方基劑或實驗室自配原料的稀釋濃度與致敏原比例，系統會自動換算回純物質濃度進行法規加總。")

            with st.form("add_l3_custom_form", clear_on_submit=True):
                c_name_cn = st.text_input("私有原料名稱 (中文) *", placeholder="例如: 桂花 CO2 萃取液 20%")
                c_name_en = st.text_input("私有原料名稱 (英文)", placeholder="e.g., Osmanthus CO2 Extract 20%")
                c_cas_map = st.selectbox(
                    "關聯底層 CAS 標準（供 IFRA 限量比對）", list(core_db.keys()),
                    format_func=lambda c: f"{c} — {core_db[c]['name_en'] if lang=='en' else core_db[c]['name_cn']}"
                )
                cc1, cc2, cc3 = st.columns(3)
                c_dil = cc1.number_input("有效純度 (%)", 0.1, 100.0, 20.0, 1.0)
                c_sol = cc2.selectbox("溶劑載體", SOLVENT_CHOICES, index=1)
                c_cost = cc3.number_input("純油單價 (NT$/g)", 0.0, 10000.0, 50.0, 5.0)

                st.markdown("**純油中之法定致敏原百分比（輸入 0~100%，系統自動依稀釋度折算）：**")
                ac1, ac2, ac3 = st.columns(3)
                a_lim = ac1.number_input("Limonene (%)", 0.0, 100.0, 0.0, 0.5)
                a_lin = ac2.number_input("Linalool (%)", 0.0, 100.0, 0.0, 0.5)
                a_ger = ac3.number_input("Geraniol (%)", 0.0, 100.0, 0.0, 0.5)
                ac4, ac5, ac6 = st.columns(3)
                a_cit = ac4.number_input("Citral (%)", 0.0, 100.0, 0.0, 0.5)
                a_bb = ac5.number_input("Benzyl Benzoate (%)", 0.0, 100.0, 0.0, 0.5)
                a_cou = ac6.number_input("Coumarin (%)", 0.0, 100.0, 0.0, 0.5)

                if st.form_submit_button("➕ 儲存至調香師私有庫 (Layer 3)", type="primary", use_container_width=True):
                    if c_name_cn:
                        cid = f"CUST-{len(custom_db) + 1:03d}"
                        allg_map = {}
                        for aname, apct in [
                            ("Limonene", a_lim), ("Linalool", a_lin), ("Geraniol", a_ger),
                            ("Citral", a_cit), ("Benzyl Benzoate", a_bb), ("Coumarin", a_cou)
                        ]:
                            if apct > 0:
                                allg_map[aname] = apct / 100.0
                        st.session_state.custom_materials[cid] = {
                            "custom_id": cid,
                            "cas": c_cas_map,
                            "name_cn": c_name_cn.strip(),
                            "name_en": c_name_en.strip() or c_name_cn.strip(),
                            "note": core_db[c_cas_map]["note"],
                            "family": core_db[c_cas_map]["family"],
                            "dilution_pct": c_dil,
                            "solvent": c_sol,
                            "sg_pure": core_db[c_cas_map]["sg_pure"],
                            "cost_per_g": c_cost,
                            "ifra_cat4_max": core_db[c_cas_map]["ifra_cat4_max"],
                            "allergens": allg_map,
                            "lot_no": f"PRIV-{cid}",
                            "exp_date": "2028/12/31"
                        }
                        st.success(f"✅ 已建立私有原料 {cid}：{c_name_cn}")
                        st.rerun()

    # --------------------------------------------------------------------------
    # 1-C: Formulation Record Sheet (Print-ready Snapshot)
    # --------------------------------------------------------------------------
    with ph1_tab_print:
        if not mod_calc or not current_formula:
            st.warning(t["empty_form"])
        else:
            st.markdown(f"""
            <div class="doc-sheet">
                <div class="doc-title">
                    <h3 style="margin:0;">FORMULATION RECORD SHEET — {st.session_state.active_mod}</h3>
                    <div style="color:#64748B; font-size:13px; margin-top:4px;">Date: {datetime.now().strftime("%Y-%m-%d")} | Regulatory: {region_info['code']} | Design Dosage: {dosage_ratio*100:.0f}%</div>
                </div>
                <p style="margin:4px 0;"><b>Perfumer Notes:</b> {st.session_state.mod_notes.get(st.session_state.active_mod, 'N/A')}</p>
                <p style="margin:4px 0;">
                    <b>Total Jus Weight:</b> {total_jus_g:.3f} g &nbsp;|&nbsp;
                    <b>Pure Active Oil:</b> {rt_calc['total_active_g']:.3f} g &nbsp;|&nbsp;
                    <b>Carrier Solvent:</b> {rt_calc['total_carrier_g']:.3f} g &nbsp;|&nbsp;
                    <b>Est. Raw Cost:</b> NT$ {mod_calc['total_cost']:.1f}
                </p>
            </div>
            """, unsafe_allow_html=True)

            print_rows = core.build_compounding_sheet(current_formula, dosage_ratio, core_db, sku_db, custom_db, sort_by_compounding=True, lang=lang)
            df_print = pd.DataFrame([{
                "Seq": r["seq"],
                "Layer": r["layer"],
                "SKU / Lot": r["sku_id"] or "UNMAPPED-L1",
                "CAS": r["cas"],
                "Material Name": r["name_disp"],
                "Spec": f"{r['dilution_pct']:.0f}% in {r['solvent'].split(' ')[0]}" if r["dilution_pct"] < 100 else "100% Neat",
                "Weight (g)": f"{r['gross_g']:.3f}",
                "Pure Active (g)": f"{r['active_g']:.3f}",
                "Share (%)": f"{r['pct']:.2f}%",
                "PPT (‰)": f"{r['ppt']:.1f}",
                "Cost (NT$)": f"{r['cost']:.1f}"
            } for r in print_rows])

            st.dataframe(df_print, use_container_width=True, hide_index=True)
            csv_f = df_print.to_csv(index=False).encode('utf-8-sig')
            st.download_button(t["dl_sheet"], data=csv_f, file_name=f"Formula_Sheet_{st.session_state.active_mod}_{lang.upper()}.csv", mime="text/csv", use_container_width=True)

# ==============================================================================
# PHASE 2: SKU Mapping Gate & Lab Compounding Dosing Sheet
# ==============================================================================
elif st.session_state.phase_idx == 1:
    st.markdown(f"""
    <div style="background:#0F172A; padding:8px 16px; border-radius:6px; color:white; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
        <div><b>{t['p2_banner']}</b> ｜ Mod: <span class="mod-pill">{st.session_state.active_mod}</span></div>
        <div style="font-size:13px; color:#94A3B8;">{t['p2_tgt_jus']}：<b style="color:#FBBF24; font-size:15px;">{total_jus_g:.3f} g</b></div>
    </div>
    """, unsafe_allow_html=True)

    p2_sub0, p2_sub1, p2_sub2 = st.tabs([t["p2_t0"], t["p2_t1"], t["p2_t2"]])

    # --------------------------------------------------------------------------
    # 2-A: Mandatory CAS -> Commercial SKU Mapping Gate
    # --------------------------------------------------------------------------
    with p2_sub0:
        st.subheader("🔗 創作轉打樣／量產閘門：抽象 CAS ➔ 商業供應商料號映射" if lang == "zh" else "🔗 Creation-to-Production Gate: Abstract CAS ➔ Commercial SKU Mapping")
        st.caption("系統在切換料號（例如從 10% 實驗室預溶液切換為 100% 純粉末）時，會自動鎖定「純物質有效淨重（Pure Active Mass）」並等比換算實際投料克數，確保香氣比例零誤差。" if lang == "zh" else "When switching SKUs (e.g., from 10% lab tincture to 100% neat powder), the engine locks Pure Active Mass and recalculates gross dosing weight so fragrance proportions stay 100% identical.")

        if not current_formula:
            st.warning(t["empty_form"])
        else:
            unmapped_lines = [
                (lid, entry) for lid, entry in current_formula.items()
                if entry.get("layer", "L1_CORE") == "L1_CORE" and entry.get("gross_g", 0) > 0
            ]

            g_col1, g_col2 = st.columns([2.2, 1.3])
            with g_col1:
                conserve_active = st.checkbox(
                    "⚖️ 啟用「純物質淨重守恆自動換算」(Auto-Conserve Pure Active Mass)" if lang == "zh" else "⚖️ Enable Auto-Conserve Pure Active Mass (Recalculate Gross Weight on Dilution Change)",
                    value=True,
                    key="chk_conserve_active"
                )
            with g_col2:
                if unmapped_lines:
                    if st.button("⚡ 一鍵自動映射所有未綁定 CAS" if lang == "zh" else "⚡ One-Click Auto-Map All Unmapped CAS", type="primary", use_container_width=True):
                        updated_f, cnt = core.auto_map_formula_skus(current_formula, sku_db, conserve_active=conserve_active)
                        st.session_state.mods[st.session_state.active_mod] = updated_f
                        st.rerun()

            if not unmapped_lines:
                st.success("✅ **全配方已完成商業料號映射！** 所有原料皆已綁定具體供應商 SKU（Layer 2）或私有庫規格（Layer 3），可直接進行天平放樣與 PIF 匯出。" if lang == "zh" else "✅ **All Materials Mapped!** Every line item is bound to a specific Commercial SKU (Layer 2) or Private Custom Material (Layer 3).")
            else:
                st.warning(f"⚠️ 尚有 **{len(unmapped_lines)} 項** Layer 1 抽象 CAS 原料尚未映射至具體商業供應商料號：" if lang == "zh" else f"⚠️ **{len(unmapped_lines)}** Layer 1 abstract CAS item(s) still require Commercial SKU mapping:")

            for lid, entry in list(current_formula.items()):
                if entry.get("gross_g", 0) <= 0:
                    continue
                res = core.resolve_formula_item(lid, entry, core_db, sku_db, custom_db, lang=lang)
                cas_no = res["cas"]
                cur_active_g = res["gross_g"] * (res["dilution_pct"] / 100.0)
                matching_skus = [sid for sid, s in sku_db.items() if s["cas"] == cas_no]

                with st.container(border=True):
                    mc1, mc2, mc3 = st.columns([1.8, 2.2, 1.0])
                    status_icon = "✅" if res["is_mapped"] else "⚠️ 待映射"
                    mc1.markdown(
                        f"{status_icon} **{res['core_name_disp']}**<br>"
                        f"<span class='cas-badge'>CAS: {cas_no}</span> ｜ 毛重: <b>{res['gross_g']:.3f} g</b> (<span style='color:#0284C7;'>純油 {cur_active_g:.3f} g</span>)",
                        unsafe_allow_html=True
                    )
                    if res["layer"] == "L3_CUSTOM":
                        mc2.info(f"🔒 已綁定調香師私有庫：`{res['sku_id']}` ({res['dilution_pct']:.0f}% in {res['solvent'].split(' ')[0]})")
                    elif matching_skus:
                        default_idx = matching_skus.index(res["sku_id"]) if res["sku_id"] in matching_skus else 0
                        chosen_map_sku = mc2.selectbox(
                            "選擇商業供應商料號 (SKU)",
                            matching_skus,
                            index=default_idx,
                            format_func=lambda s: f"{s} | {sku_db[s]['trade_name_en' if lang=='en' else 'trade_name_cn']} (Lot: {sku_db[s]['lot_no']})",
                            key=f"map_sel_{st.session_state.active_mod}_{lid}",
                            label_visibility="collapsed"
                        )
                        s_obj = sku_db[chosen_map_sku]
                        doc_badges = " ".join([f"📄{dk}" for dk, dv in s_obj.get("docs", {}).items() if dv])
                        preview_mapped = core.map_line_to_sku_conserving_active(entry, s_obj, conserve_active=conserve_active)
                        conv_hint = ""
                        if abs(preview_mapped["gross_g"] - res["gross_g"]) > 1e-4:
                            conv_hint = f" ｜ ⚖️ 淨重守恆換算: **{res['gross_g']:.3f}g ({res['dilution_pct']:.0f}%) ➔ {preview_mapped['gross_g']:.3f}g ({s_obj['dilution_pct']:.0f}%)**"
                        mc2.caption(f"供應商: **{s_obj['supplier_en' if lang=='en' else 'supplier_zh']}** ｜ 效期: {s_obj['exp_date']} ｜ NT${s_obj['cost_per_g']}/g ｜ {doc_badges}{conv_hint}")

                        btn_txt = ("🔗 套用並換算" if lang == "zh" else "🔗 Map & Conserve") if not res["is_mapped"] else ("🔄 切換並換算" if lang == "zh" else "🔄 Switch SKU")
                        if mc3.button(btn_txt, key=f"btn_map_{st.session_state.active_mod}_{lid}", use_container_width=True, type="primary" if not res["is_mapped"] else "secondary"):
                            st.session_state.mods[st.session_state.active_mod][lid] = preview_mapped
                            st.rerun()
                    else:
                        mc2.error("❌ 商業庫尚無此 CAS 料號，請至 Phase 1-B 上傳供應商 SKU。")

    # --------------------------------------------------------------------------
    # 2-B: Lab Compounding Bench & Dosing Sheet
    # --------------------------------------------------------------------------
    with p2_sub1:
        st.info(t["p2_sop"])
        if rt_calc["unmapped_count"] > 0:
            st.warning(f"⚠️ 提醒：配方中仍有 {rt_calc['unmapped_count']} 項原料未在「2-A」映射商業 SKU，建議先完成映射以確保批號與稀釋度準確。")

        bench_rows = core.build_compounding_sheet(current_formula, dosage_ratio, core_db, sku_db, custom_db, sort_by_compounding=True, lang=lang)

        if not bench_rows:
            st.warning(t["empty_form"])
        else:
            current_checks = st.session_state.dosed_checklist.setdefault(st.session_state.active_mod, {})
            dosed_count = sum(1 for r in bench_rows if current_checks.get(r["line_id"], False))
            dosed_weight = sum(r["gross_g"] for r in bench_rows if current_checks.get(r["line_id"], False))

            c_prog, c_reset = st.columns([3.5, 1])
            with c_prog:
                st.progress(dosed_count / len(bench_rows) if len(bench_rows) > 0 else 0)
                st.caption(f"{t['p2_prog']} **{dosed_count}/{len(bench_rows)}** {t['p2_items']} **{dosed_weight:.3f} g** / {total_jus_g:.3f} g）")
            with c_reset:
                if st.button(t["p2_reset"], use_container_width=True):
                    st.session_state.dosed_checklist[st.session_state.active_mod] = {}
                    st.rerun()

            for row in bench_rows:
                lid = row["line_id"]
                is_done = current_checks.get(lid, False)
                with st.container(border=True):
                    b1, b2, b3, b4, b5 = st.columns([0.5, 0.7, 2.5, 1.5, 1.5])
                    chk = b1.checkbox("Done", value=is_done, key=f"bench_chk_{st.session_state.active_mod}_{lid}", label_visibility="collapsed")
                    current_checks[lid] = chk

                    b2.markdown(f"**#{row['seq']}**<br>`{row['note']}`", unsafe_allow_html=True)
                    name_css = "text-decoration: line-through; color: #94A3B8;" if chk else "font-weight: 700; color: #0F172A;"
                    sol_short = row["solvent"].split(" ")[0]
                    spec_txt = ("100% Neat" if lang == "en" else "100% 純原液") if row["dilution_pct"] >= 100 else f"{row['dilution_pct']:.0f}% in {sol_short}"
                    b3.markdown(
                        f"<span style='{name_css}'>{row['name_disp']}</span><br>"
                        f"<span class='cas-badge'>{spec_txt}</span> <span style='font-size:11px; color:#64748B;'>Lot: {row['lot_no']}</span>",
                        unsafe_allow_html=True
                    )
                    b4.markdown(f"{t['p2_net_add']}<br><b style='font-size:16px; color:#0284C7;'>{row['gross_g']:.3f} g</b> <span style='font-size:12px; color:#64748B;'>({row['drops']} {t['drops_unit']})</span>", unsafe_allow_html=True)
                    b5.markdown(f"{t['p2_tare']}<br><span class='scale-chip'>⚖️ {row['cumulative_g']:.3f} g</span>", unsafe_allow_html=True)

            st.divider()
            st.subheader(t["p2_dosing_hdr"])
            dosing_df = pd.DataFrame([{
                "Seq": r["seq"],
                "SKU / Lot": f"{r['sku_id'] or 'UNMAPPED'} ({r['lot_no']})",
                "Note": r["note"],
                "CAS": r["cas"],
                "Material Name": r["name_disp"],
                "Dilution & Carrier": f"{r['dilution_pct']:.0f}% in {r['solvent'].split(' ')[0]}" if r["dilution_pct"] < 100 else "100% Neat",
                "Net Addition (g)": r["gross_g"],
                "Est. Drops": r["drops"],
                "Running Tare (g)": r["cumulative_g"],
                "Pure Active (g)": r["active_g"],
                "Checked": "✅" if current_checks.get(r["line_id"], False) else "⬜"
            } for r in bench_rows])
            st.dataframe(dosing_df, hide_index=True, use_container_width=True)
            dosing_csv = dosing_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(t["dl_dosing"], data=dosing_csv, file_name=f"Lab_Dosing_Sheet_{st.session_state.active_mod}_{lang.upper()}.csv", mime="text/csv", use_container_width=True)

    # --------------------------------------------------------------------------
    # 2-C: Multi-Concentration Sampler & Filtration
    # --------------------------------------------------------------------------
    with p2_sub2:
        st.subheader(t["p2_samp_hdr"])
        st.caption(t["p2_samp_cap"])

        if total_jus_g <= 0:
            st.warning(t["empty_form"])
        else:
            tier_keys = list(PERFUME_CONCENTRATION_PRESETS.keys())
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.markdown(t["samp_a"])
                s1_tier_id = st.selectbox(t["conc_a"], tier_keys, index=1, format_func=lambda k: PERFUME_CONCENTRATION_PRESETS[k][lang], key="p2_s1_tier")
                s1_bot = st.number_input(t["bot_a"], 1, 50, 1, 1, key="p2_s1_bot")
                s1_vol = st.selectbox(t["vol_a"], [5, 10, 15, 30, 50], index=1, key="p2_s1_vol")
                res_s1 = core.compute_sample_application(current_formula, PERFUME_CONCENTRATION_PRESETS[s1_tier_id]["ratio"], s1_bot, s1_vol)
                if res_s1:
                    st.markdown(f"""
                    <div class="sample-card" style="border-left:4px solid #10B981;">
                        <div style="font-size:12px; color:#64748B;">{t['overfill_lbl']}<b>{res_s1['overfill_total_g']:.2f} g</b></div>
                        <div style="margin-top:8px;">{t['take_jus']}<b style="color:#10B981; font-size:16px;">{res_s1['req_jus_g']:.3f} g</b></div>
                        <div>{t['add_alc']}<b style="color:#3B82F6; font-size:16px;">{res_s1['net_alcohol_g']:.2f} g</b></div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(t["lock_a"], key="lock_s1", use_container_width=True):
                        st.session_state.tier_id = s1_tier_id
                        st.session_state.locked_for_pif = True
                        st.rerun()

            with col_s2:
                st.markdown(t["samp_b"])
                s2_tier_id = st.selectbox(t["conc_b"], tier_keys, index=2, format_func=lambda k: PERFUME_CONCENTRATION_PRESETS[k][lang], key="p2_s2_tier")
                s2_bot = st.number_input(t["bot_b"], 1, 50, 1, 1, key="p2_s2_bot")
                s2_vol = st.selectbox(t["vol_b"], [5, 10, 15, 30, 50], index=1, key="p2_s2_vol")
                res_s2 = core.compute_sample_application(current_formula, PERFUME_CONCENTRATION_PRESETS[s2_tier_id]["ratio"], s2_bot, s2_vol)
                if res_s2:
                    st.markdown(f"""
                    <div class="sample-card" style="border-left:4px solid #3B82F6;">
                        <div style="font-size:12px; color:#64748B;">{t['overfill_lbl']}<b>{res_s2['overfill_total_g']:.2f} g</b></div>
                        <div style="margin-top:8px;">{t['take_jus']}<b style="color:#10B981; font-size:16px;">{res_s2['req_jus_g']:.3f} g</b></div>
                        <div>{t['add_alc']}<b style="color:#3B82F6; font-size:16px;">{res_s2['net_alcohol_g']:.2f} g</b></div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(t["lock_b"], key="lock_s2", use_container_width=True):
                        st.session_state.tier_id = s2_tier_id
                        st.session_state.locked_for_pif = True
                        st.rerun()

            if st.session_state.locked_for_pif:
                st.success(f"🔒 Locked **{st.session_state.active_mod}** ({PERFUME_CONCENTRATION_PRESETS[st.session_state.tier_id][lang]}) for Phase 3 PIF!")

            total_req = (res_s1["req_jus_g"] if res_s1 else 0.0) + (res_s2["req_jus_g"] if res_s2 else 0.0)
            remaining = total_jus_g - total_req
            st.divider()

            c_bal, c_mac = st.columns([1.3, 1.2])
            with c_bal:
                st.markdown(t["bal_hdr"])
                if remaining >= 0:
                    st.success(f"✅ Required Jus: **{total_req:.3f} g** | Remaining in Mother Bottle: **{remaining:.3f} g**.")
                else:
                    st.error(f"🚨 Insufficient Jus! Required **{total_req:.3f} g**, available **{total_jus_g:.3f} g** (Shortage: {-remaining:.3f} g).")

            with c_mac:
                if mac_meta:
                    st.markdown(f"""
                    <div style="background:#F8FAFC; border:1px solid #CBD5E1; padding:12px; border-radius:8px; margin-bottom:8px;">
                        <div style="font-size:14px; font-weight:bold; color:#0F172A;">{t['mac_title']}<span style="color:#D97706; font-size:18px;">{mac_meta['maceration']['days']} {t['days_unit']}</span></div>
                        <div style="font-size:12px; color:#475569; margin-top:4px;">{mac_meta['maceration']['desc']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    for alert in mac_meta["alerts"]:
                        if alert["level"] == "danger":
                            st.error(alert["msg"])
                        else:
                            st.success(alert["msg"])

# ==============================================================================
# PHASE 3: PIF & Compliance Dossier (All 5 Tabs + Tri-Party NDA Direct-to-SA)
# ==============================================================================
elif st.session_state.phase_idx == 2:
    st.markdown(f"""
    <div style="background:#0F172A; padding:8px 16px; border-radius:6px; color:white; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
        <div><b>{t['p3_banner']}</b> ｜ Mod: <span class="mod-pill">{st.session_state.active_mod}</span></div>
        <div style="font-size:13px; color:#38BDF8;">{t['p3_reg']}: <b>{region_info['code']}</b> ｜ {t['p3_dos']}: <b>{dosage_ratio*100:.1f}%</b></div>
    </div>
    """, unsafe_allow_html=True)

    if not mod_calc or total_jus_g <= 0:
        st.warning(t["empty_form"])
    else:
        if rt_calc["unmapped_count"] > 0:
            st.warning(f"⚠️ 偵測到 **{rt_calc['unmapped_count']} 項** Layer 1 抽象 CAS 尚未映射商業 SKU。建議先回 **Phase 2-A** 完成料號映射，以掛載正式批號與 COA 檢驗文件。")

        all_ifra_pass = all(stat["is_safe"] for stat in rt_calc["ifra_status"].values())
        over_10ppm_list = [a for a in mod_calc["declared_allergens"] if a["ppm"] >= region_info["allergen_ppm_threshold"]]

        k1, k2, k3, k4 = st.columns(4)
        k1.metric(t["m_ifra"], "✅ PASS" if all_ifra_pass else "❌ FAIL")
        k2.metric(t["m_max_dos"], f"{rt_calc['max_safe_dosage_pct']:.2f} %")
        k3.metric(t["m_allg"], f"{len(over_10ppm_list)}")
        k4.metric(t["m_sg"], f"ρ {mod_calc['jus_sg']} / {mac_meta['natural_pct'] if mac_meta else 0}%")

        p3_t1, p3_t2, p3_t3, p3_t4, p3_t5 = st.tabs([t["p3_t1"], t["p3_t2"], t["p3_t3"], t["p3_t4"], t["p3_t5"]])

        pif_rows = []
        for lid, item in mod_calc["norm_active"].items():
            pct_in_finished_active = (item["active_pct"] / 100.0) * dosage_ratio * 100.0
            pct_in_finished_carrier = (item["carrier_g"] / mod_calc["total_active_g"]) * dosage_ratio * 100.0 if mod_calc["total_active_g"] > 0 else 0.0
            docs_ok = " ".join([f"✅{dk}" for dk, dv in item.get("docs", {}).items() if dv]) or "⚠️ Pending SKU"
            pif_rows.append({
                "Layer": item["layer"],
                "SKU / Lot": f"{item['sku_id'] or 'UNMAPPED'} ({item['lot_no']})",
                "CAS No.": item["cas"],
                "Material Name": item["name_disp"],
                "Supplier": item["supplier"],
                "Docs": docs_ok,
                "Dilution": f"{item['dilution_pct']:.0f}% in {item['solvent'].split(' ')[0]}" if item["dilution_pct"] < 100 else "100% Pure",
                "% in Pure Oil": round(item["active_pct"], 3),
                f"% in Finished (@{dosage_ratio*100:.0f}%)": round(pct_in_finished_active, 4),
                f"Carrier in Finished (@{dosage_ratio*100:.0f}%)": round(pct_in_finished_carrier, 4)
            })
        df_pif_a = pd.DataFrame(pif_rows).sort_values(by="% in Pure Oil", ascending=False)

        carrier_incis = []
        for sol_name in mod_calc["batch"]["carrier_solvents"].keys():
            inci_s = SOLVENT_DATABASE.get(sol_name, {}).get("inci", "")
            if inci_s and inci_s not in carrier_incis:
                carrier_incis.append(inci_s)
        inci_allergens = [a["name"].upper() for a in over_10ppm_list]
        base_incis = ["ALCOHOL DENAT.", "PARFUM (FRAGRANCE)", "AQUA (WATER)"] + carrier_incis + inci_allergens
        inci_final_str = ", ".join(base_incis)
        cert_no = f"IFRA-51-{datetime.now().strftime('%Y%m%d')}-{st.session_state.active_mod.replace(' ', '')}"

        # --- PIF-1: 100% Q&Q Formula ---
        with p3_t1:
            st.subheader("1. Full Quantitative Fragrance Composition (100% Q&Q)" if lang == "en" else "1. 香精全成分比例表 (100% Full Quantitative Composition)")
            st.dataframe(df_pif_a, hide_index=True, use_container_width=True)
            st.download_button(
                "📥 Download 100% Quantitative Formula (CSV)" if lang == "en" else "📥 下載 100% 香精全成分比例表 (CSV)",
                data=df_pif_a.to_csv(index=False).encode("utf-8-sig"),
                file_name=f"PIF_100pct_Composition_{st.session_state.active_mod}_{lang.upper()}.csv",
                mime="text/csv"
            )

        # --- PIF-2: Allergens & INCI ---
        with p3_t2:
            st.subheader("2. Fragrance Allergen Declaration & INCI Labeling" if lang == "en" else "2. 法定香精過敏原清單聲明書與外盒 INCI 標籤")
            allg_summary = rt_calc.get("allergen_summary", {})
            allg_sources = rt_calc.get("allergen_sources", {})
            if allg_summary:
                allg_detail_rows = []
                for a_name, ppm in sorted(allg_summary.items(), key=lambda x: x[1], reverse=True):
                    is_declare = ppm >= region_info["allergen_ppm_threshold"]
                    allg_detail_rows.append({
                        "Allergen (INCI)": a_name.upper(),
                        "Primary Sources": ", ".join(set(allg_sources.get(a_name, []))),
                        "% in Pure Oil": round((ppm / 10000.0) / dosage_ratio, 4) if dosage_ratio > 0 else 0.0,
                        "% in Finished": f"{ppm / 10000.0:.5f}%",
                        "PPM in Finished": round(ppm, 2),
                        "Labeling Status": ("⚠️ Mandatory (>10 ppm)" if lang == "en" else "⚠️ 強制外盒標示 (>10 ppm)") if is_declare else ("✅ Exempt (<10 ppm)" if lang == "en" else "✅ 免標示 (<10 ppm)")
                    })
                df_allg = pd.DataFrame(allg_detail_rows)
                st.dataframe(df_allg, hide_index=True, use_container_width=True)
                st.download_button(
                    "📥 Download Allergen Declaration (CSV)" if lang == "en" else "📥 下載過敏原清單聲明書 (CSV)",
                    data=df_allg.to_csv(index=False).encode("utf-8-sig"),
                    file_name=f"PIF_Allergens_{st.session_state.active_mod}_{lang.upper()}.csv",
                    mime="text/csv"
                )
            else:
                st.success("✅ No regulated fragrance allergens detected." if lang == "en" else "✅ 經 GC-MS 成分穿透計算，此配方在最終成品中未檢出任何法定致敏原。")

            st.divider()
            st.markdown("#### 🏷️ Official INCI Packaging Label (Sorted Descending)" if lang == "en" else "#### 🏷️ 外包裝法定 INCI 全成分展開標籤 (依含量降冪排列)")
            st.code(inci_final_str, language="text")

        # --- PIF-3: IFRA 51st Certificate ---
        with p3_t3:
            st.subheader("3. IFRA 51st Amendment Conformity Certificate")
            st.markdown(f"""
            <div class="cert-box">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #CBD5E1; padding-bottom:8px; margin-bottom:10px;">
                    <div>
                        <h4 style="margin:0; color:#0F172A;">CERTIFICATE OF CONFORMITY WITH IFRA STANDARDS (51st Amendment)</h4>
                        <span style="font-size:12px; color:#64748B;">Certificate No.: <code>{cert_no}</code> ｜ Issue Date: {datetime.now().strftime("%Y-%m-%d")}</span>
                    </div>
                    <div style="background:{'#DCFCE7' if all_ifra_pass else '#FEE2E2'}; color:{'#15803D' if all_ifra_pass else '#B91C1C'}; padding:4px 12px; border-radius:4px; font-weight:bold;">
                        {'CONFORMING (PASS)' if all_ifra_pass else 'EXCEEDS LIMIT (FAIL)'}
                    </div>
                </div>
                <div style="font-size:13px; color:#334155;">
                    We certify that fragrance compound <b>{st.session_state.active_mod}</b> complies with the Standards of the International Fragrance Association (IFRA 51st Amendment). Maximum allowable concentrations in finished products (Categories 1–12) are listed below:
                </div>
            </div>
            """, unsafe_allow_html=True)

            df_ifra_cats = pd.DataFrame(rt_calc["ifra_categories"])
            st.dataframe(df_ifra_cats, hide_index=True, use_container_width=True)

            with st.expander("🔍 Ingredient-Level Cross-Layer CAS Mass Aggregation Audit" if lang == "en" else "🔍 檢視跨層單體級 CAS 質量合併限制明細"):
                ifra_rows = []
                for lid, stat in rt_calc["ifra_status"].items():
                    ifra_rows.append({
                        "Layer": stat["layer"],
                        "Material": stat["name_disp"],
                        "CAS No.": stat["cas"],
                        "CAS Share in Pure Oil": f"{stat['active_share_pct']:.2f}%",
                        f"Finished (@{dosage_ratio*100:.0f}%)": f"{stat['finished_pct']:.4f}%",
                        "IFRA Cat.4 Limit": f"{stat['limit']:.2f}%",
                        "Status": "✅ PASS" if stat["is_safe"] else "❌ FAIL"
                    })
                st.dataframe(pd.DataFrame(ifra_rows), hide_index=True, use_container_width=True)

            st.download_button(
                "📥 Download IFRA 51st Certificate (CSV)" if lang == "en" else "📥 下載 IFRA 51st 跨品類符合性證書表 (CSV)",
                data=df_ifra_cats.to_csv(index=False).encode("utf-8-sig"),
                file_name=f"IFRA_51st_Certificate_{st.session_state.active_mod}_{lang.upper()}.csv",
                mime="text/csv"
            )

        # --- PIF-4: MSDS / SDS ---
        with p3_t4:
            st.subheader("4. Material Safety Data Sheet Summary (MSDS / SDS)")
            c_sds1, c_sds2 = st.columns(2)
            with c_sds1:
                st.markdown(f"""
                <div class="doc-sheet">
                    <div class="doc-title"><h4 style="margin:0;">Section 1–3 & 9: Identification & Physical Properties</h4></div>
                    <ul style="font-size:13px; line-height:1.75;">
                        <li><b>Product Name:</b> Fragrance Compound — {st.session_state.active_mod}</li>
                        <li><b>Appearance & Odor:</b> Pale yellow to amber clear oily liquid, characteristic aromatic odor.</li>
                        <li><b>Relative Density (20°C):</b> ρ = <b>{mod_calc['jus_sg']}</b> g/cm³</li>
                        <li><b>Solubility:</b> Insoluble in water; miscible with 95% Ethanol, DPG, TEC, IPM.</li>
                        <li><b>Flash Point (Closed Cup):</b> ~68°C (Pure Jus) / ~<b>14°C</b> (Finished perfume at {dosage_ratio*100:.0f}%).</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            with c_sds2:
                st.markdown(f"""
                <div class="doc-sheet">
                    <div class="doc-title"><h4 style="margin:0;">Section 2, 7 & 10: GHS Hazards & Handling</h4></div>
                    <ul style="font-size:13px; line-height:1.75;">
                        <li><b>GHS Classification:</b> Flammable Liquid Cat. 2 (H225), Skin Sensitization Cat. 1 (H317), Aquatic Chronic Cat. 2 (H411).</li>
                        <li><b>Safe Handling (Sec. 7):</b> Wear nitrile gloves and eye protection; keep away from heat/sparks/open flames.</li>
                        <li><b>Storage & Maceration:</b> Store sealed in cool dark place (15–20°C); macerate <b>{mac_meta['maceration']['days'] if mac_meta else 14} days</b> & chill-filter at -4°C (0.45μm).</li>
                        <li><b>Phototoxicity Note:</b> {"⚠️ Contains non-FCF Bergamot EO (0.4% max limit)." if (mac_meta and mac_meta["has_bergamot_phototoxic"]) else "✅ No high-risk phototoxic furocoumarin oils detected."}</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

        # --- PIF-5: Tri-Party NDA Direct-to-SA Mode ---
        with p3_t5:
            st.subheader("🔒 Tri-Party NDA Direct-to-Safety Assessor (SA) Mode" if lang == "en" else "🔒 三方保密協議（Tri-Party NDA）直傳安全評估人員（SA）模式")
            st.markdown("""
            <div class="nda-box">
                <h4 style="margin:0 0 6px 0; color:#92400E;">🛡️ Intellectual Property Isolation Protocol (IP Protection)</h4>
                <div style="font-size:13px; line-height:1.6;">
                    Under EU EC 1223/2009 and Taiwan TFDA PIF regulations, the Safety Assessor (SA) requires the <b>100% full quantitative formula</b> (with SKU & Lot traceability) to sign off the Cosmetic Product Safety Report (CPSR).<br>
                    To protect trade secrets from leaking to brand marketing or third-party OEM factories, execute a <b>Tri-Party NDA (Fragrance Creator × Brand Owner × Independent SA)</b> and transmit the encrypted SA Dossier directly to the SA.
                </div>
            </div>
            """, unsafe_allow_html=True)

            c_nda1, c_nda2 = st.columns(2)
            with c_nda1:
                nda_perfumer = st.text_input("① Disclosing Party (Fragrance Creator)", value="Nanmen Scent Lab", key="nda_perfumer")
                nda_brand = st.text_input("② Commissioning Party (Brand Owner)", value="", placeholder="Enter Brand Owner name...", key="nda_brand")
            with c_nda2:
                nda_sa_name = st.text_input("③ Receiving Party (Authorized Safety Assessor / SA)", value="", placeholder="Enter SA name / credentials / institution...", key="nda_sa_name")
                nda_ref_no = st.text_input("④ Tri-Party NDA Reference No.", value=f"NDA-{datetime.now().strftime('%Y%m%d')}-01", key="nda_ref_no")

            nda_confirmed = st.checkbox("✅ Confirm Tri-Party NDA is executed to unlock 100% Confidential SA Dossier download", key="nda_chk")

            allergen_lines = "\n".join([f"- {a['name'].upper()}: {a['ppm']} ppm ({a['pct_finished']}%)" for a in over_10ppm_list]) if over_10ppm_list else "- None above 10 ppm threshold."
            ifra_cat_lines = "\n".join([f"- {list(c.values())[0]} ({list(c.values())[1]}): Max {list(c.values())[2]}" for c in rt_calc["ifra_categories"]])
            comp_lines_100 = "\n".join([
                f"- [{r['Layer']}] [CAS: {r['CAS No.']}] {r['Material Name']} ({r['SKU / Lot']}) | Pure Oil: {r['% in Pure Oil']}% | Finished: {r[f'% in Finished (@{dosage_ratio*100:.0f}%)']}% | Spec: {r['Dilution']}"
                for r in pif_rows
            ])

            sa_confidential_dossier = f"""# STRICTLY CONFIDENTIAL — DIRECT-TO-SAFETY ASSESSOR (SA) PIF PACKAGE
## UNDER TRI-PARTY NON-DISCLOSURE AGREEMENT (NDA)

- **NDA Reference No.**: {nda_ref_no}
- **Disclosing Party (Fragrance Creator)**: {nda_perfumer}
- **Commissioning Party (Brand Owner)**: {nda_brand if nda_brand else '[Pending Brand Name]'}
- **Receiving Party (Authorized Safety Assessor / SA)**: {nda_sa_name if nda_sa_name else '[Pending SA Name]'}
- **Issue Date**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
- **Formula / Mod Code**: {st.session_state.active_mod}
- **Target Product Application & Dosage**: {tier_info['en']} ({dosage_ratio*100:.1f}%)
- **Regulatory Framework**: {region_info['name_en']}

> **CONFIDENTIALITY NOTICE**: This document contains 100% proprietary fragrance formulation data disclosed solely to the designated Safety Assessor (SA) under the executed Tri-Party NDA ({nda_ref_no}) for toxicological safety evaluation (CPSR / PIF) purposes only.

---

## PART 1: 100% FULL QUANTITATIVE FRAGRANCE COMPOSITION (PROPRIETARY)
- **Pure Active Fragrance Concentrate Share in Jus**: {round(mod_calc['total_active_g'] / mod_calc['total_gross_g'] * 100.0, 2)}%
- **Carrier Solvent Share in Jus**: {round(mod_calc['total_carrier_g'] / mod_calc['total_gross_g'] * 100.0, 2)}%

{comp_lines_100}

---

## PART 2: IFRA 51st AMENDMENT CONFORMITY CERTIFICATE ({cert_no})
- **Overall Compliance Status**: {'CONFORMING (PASS)' if all_ifra_pass else 'EXCEEDS LIMIT (FAIL)'}
- **Maximum Allowable Concentration in Cat. 4 (Fine Fragrance)**: {rt_calc['max_safe_dosage_pct']:.2f}%

{ifra_cat_lines}

---

## PART 3: MATERIAL SAFETY DATA SHEET (MSDS / GHS SUMMARY)
- **Product Identification**: Fragrance Compound — {st.session_state.active_mod}
- **Relative Density (20°C)**: {mod_calc['jus_sg']} g/cm3
- **Flash Point**: ~68°C (Pure Jus, closed cup) / ~14°C (Finished alcoholic perfume at {dosage_ratio*100:.0f}%)
- **GHS Classification**: Flammable Liquid Cat. 2 (H225), Skin Sensitization Cat. 1 (H317), Aquatic Chronic Cat. 2 (H411).
- **Recommended Maceration & Filtration**: {mac_meta['maceration']['days'] if mac_meta else 14} days maturation; -4°C chilling followed by 0.45μm filtration.

---

## PART 4: REGULATED ALLERGEN DECLARATION & INCI LABELING
- **Official INCI String**: {inci_final_str}
- **Allergens > 10 ppm in Finished Product**:
{allergen_lines}
"""

            if nda_confirmed:
                c_dl1, c_dl2 = st.columns(2)
                c_dl1.download_button(
                    "🔒 Download Confidential SA Dossier (100% Formula + MSDS + IFRA)",
                    data=sa_confidential_dossier.encode("utf-8"),
                    file_name=f"CONFIDENTIAL_SA_PIF_{st.session_state.active_mod}_{nda_ref_no}.md",
                    mime="text/markdown",
                    type="primary",
                    use_container_width=True
                )
                c_dl2.download_button(
                    "📊 Download Confidential 100% Formula CSV",
                    data=df_pif_a.to_csv(index=False).encode("utf-8-sig"),
                    file_name=f"CONFIDENTIAL_SA_100pct_Formula_{st.session_state.active_mod}_{nda_ref_no}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.warning("☝️ Check the Tri-Party NDA confirmation box above to unlock the 100% confidential SA package.")

# ==============================================================================
# PHASE 4: Commercial Scale-up, BMR Dispatch & Blank Landed Cost Framework
# ==============================================================================
elif st.session_state.phase_idx == 3:
    st.markdown(f"""
    <div style="background:#0F172A; padding:8px 16px; border-radius:6px; color:white; display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
        <div><b>{t['p4_banner']}</b> ｜ Mod: <span class="mod-pill">{st.session_state.active_mod}</span></div>
        <div style="font-size:13px; color:#38BDF8;">{t['p4_deliv']}: <b>{dosage_ratio*100:.1f}%</b></div>
    </div>
    """, unsafe_allow_html=True)

    if not mod_calc or total_jus_g <= 0:
        st.warning(t["empty_form"])
    else:
        st.subheader(t["p4_s1"])
        c_b1, c_b2, c_b3 = st.columns(3)
        target_bottles = c_b1.number_input(t["p4_bot"], min_value=50, max_value=50000, value=500, step=50)
        target_vol = c_b2.selectbox(t["p4_vol"], [10, 15, 30, 50, 100], index=2)
        overfill_pct = c_b3.number_input(t["p4_ovf"], min_value=0.0, max_value=15.0, value=3.0, step=0.5)

        c_d1, c_d2 = st.columns(2)
        dispatch_target = c_d1.text_input(t["p4_disp_tgt"], value="", placeholder="OEM Factory / Compounding Lab...")
        dispatch_batch_no = c_d2.text_input(t["p4_disp_no"], value="", placeholder="e.g., BMR-2026-001...")

        scale_calc = core.calculate_mod_profile(
            current_formula, dosage_ratio,
            {"bottles": target_bottles, "vol_ml": target_vol},
            core_db, sku_db, custom_db, overfill_pct=overfill_pct, lang=lang
        )
        b_info = scale_calc["batch"]

        m1, m2, m3, m4 = st.columns(4)
        m1.metric(t["p4_m1"], f"{b_info['total_g']:,.1f} g")
        m2.metric(t["p4_m2"], f"{b_info['target_jus_g']:,.1f} g")
        m3.metric(t["p4_m3"], f"{b_info['alcohol_g']:,.1f} g")
        m4.metric(t["p4_m4"], f"NT$ {b_info['batch_fragrance_cost']:,.0f}")

        st.divider()
        st.subheader(t["p4_s2"])

        bmr_df = pd.DataFrame([{
            "Work Order / 工單": dispatch_batch_no if dispatch_batch_no else "-",
            "Dispatch To / 投遞對象": dispatch_target if dispatch_target else "-",
            "Seq": r["seq"],
            "SKU ID": r["sku_id"],
            "Lot No.": r["lot_no"],
            "CAS No.": r["cas"],
            "Material Name": r["name"],
            "Spec": r["spec"],
            "Pure Oil (%)": r["active_w_pct"],
            "100% Pure Active (g)": r["pure_active_g"],
            "Actual Dosing / Dispatch (g)": r["target_batch_g"],
            "Sign-off": "⬜"
        } for r in scale_calc["bmr_rows"]])

        st.dataframe(bmr_df, hide_index=True, use_container_width=True)
        bmr_csv = bmr_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            t["dl_bmr"],
            data=bmr_csv,
            file_name=f"Factory_BMR_Dispatch_{st.session_state.active_mod}_{target_bottles}pcs_{lang.upper()}.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True
        )

        st.divider()
        st.subheader(t["p4_s3"])
        st.info("💡 **Blank Framework Notice**: No default unit prices or assumed totals are pre-calculated here. All vendor and cost fields are intentionally left blank for future supplier quotes." if lang == "en" else "💡 **架構預留說明**：此區塊僅建立落地成本結構框架，**不設任何預設單位價格、不作假設性加總計算**。所有項目名稱、廠商與報價備註皆保留為空白欄位，待未來洽談廠商後再行納入系統。")

        fragrance_cost_per_bottle = b_info["batch_fragrance_cost"] / target_bottles if target_bottles > 0 else 0.0

        with st.container(border=True):
            if lang == "en":
                st.markdown(f"**[System Calculated] Fragrance Juice Cost per Unit**: **`NT$ {fragrance_cost_per_bottle:.2f} / bottle`**")
                st.divider()
                st.markdown("**[Future Vendor Integration] Blank Custom Cost Line Items:**")
            else:
                st.markdown(f"**[已建檔項目] 香精內料單瓶基準成本**（由 Phase 1 原料庫自動換算）：**`NT$ {fragrance_cost_per_bottle:.2f} / 瓶`**")
                st.divider()
                st.markdown("**[未來廠商對接空白框架] 自訂成本項目與廠商名稱欄位：**")

            for idx in range(1, 7):
                fc1, fc2, fc3 = st.columns([1.4, 1.4, 1.0])
                fc1.text_input(f"Cost Item #{idx}" if lang == "en" else f"成本項目名稱 #{idx}", value="", placeholder=f"Blank Item #{idx} (Glass Bottle / Pump / Alcohol / OEM...)", key=f"cogs_name_{idx}")
                fc2.text_input(f"Vendor & Spec #{idx}" if lang == "en" else f"合作廠商與規格 #{idx}", value="", placeholder="Blank Vendor / MOQ / Lead Time", key=f"cogs_vendor_{idx}")
                fc3.text_input(f"Unit Quote #{idx}" if lang == "en" else f"單位報價欄位 #{idx}", value="", placeholder="Pending Quote (No Default)", key=f"cogs_quote_{idx}")
