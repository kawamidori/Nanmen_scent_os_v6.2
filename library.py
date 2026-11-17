# library.py

# ==============================================================================
# LAYER 1: 底層化學核心 (CHEMICAL CORE DATABASE - Keyed by CAS Number)
# 僅記錄純物質/天然標準物性：分子量 (MW)、蒸氣壓 (mmHg @25°C)、香階、氣味描述符、IFRA 51st 限量
# ==============================================================================
CHEMICAL_CORE_DB = {
    "54464-57-2": {
        "cas": "54464-57-2", "name_cn": "龍涎酮 (Iso E Super)", "name_en": "Iso E Super",
        "note": "Base", "family": "Woody", "type": "Aroma Chemical",
        "mol_w": 234.38, "vapor_pressure_mmhg": 0.00042, "sg_pure": 0.963,
        "ifra_cat4_max": 21.4, "baseline_allergens": {},
        "desc_zh": "乾淨透明的雪松木質與天鵝絨般的偽體香，極佳的結構擴散劑。",
        "desc_en": "Clean, transparent cedarwood with velvety skin-like aura; exceptional structural diffuser."
    },
    "24851-98-7": {
        "cas": "24851-98-7", "name_cn": "二氫茉莉酮酸甲酯 (Hedione)", "name_en": "Hedione",
        "note": "Mid", "family": "Floral", "type": "Aroma Chemical",
        "mol_w": 226.31, "vapor_pressure_mmhg": 0.00120, "sg_pure": 1.000,
        "ifra_cat4_max": 100.0, "baseline_allergens": {},
        "desc_zh": "輕盈透明的水感茉莉微風，無形中提亮所有花香與柑橘輪廓。",
        "desc_en": "Airy, transparent watery jasmine breeze that effortlessly lifts floral and citrus accords."
    },
    "1222-05-5": {
        "cas": "1222-05-5", "name_cn": "佳樂麝香 (Galaxolide)", "name_en": "Galaxolide",
        "note": "Base", "family": "Sweet", "type": "Aroma Chemical",
        "mol_w": 258.40, "vapor_pressure_mmhg": 0.00015, "sg_pure": 1.005,
        "ifra_cat4_max": 100.0, "baseline_allergens": {},
        "desc_zh": "潔淨蓬鬆的現代白麝香，賦予配方持久貼膚的皂感與圓潤度。",
        "desc_en": "Clean, diffusive modern white musk imparting lasting skin-hugging soapy roundness."
    },
    "6790-58-5": {
        "cas": "6790-58-5", "name_cn": "降龍涎香醚 (Ambroxan)", "name_en": "Ambroxan",
        "note": "Base", "family": "Woody", "type": "Aroma Chemical",
        "mol_w": 236.39, "vapor_pressure_mmhg": 0.00009, "sg_pure": 0.980,
        "ifra_cat4_max": 100.0, "baseline_allergens": {},
        "desc_zh": "乾燥礦物感與溫暖龍涎香交織，提供強大尾韻支撐力。",
        "desc_en": "Dry mineral facets intertwined with warm ambergris, anchoring the dry-down."
    },
    "60-12-8": {
        "cas": "60-12-8", "name_cn": "苯乙醇 (PEA)", "name_en": "Phenethyl Alcohol (PEA)",
        "note": "Mid", "family": "Floral", "type": "Aroma Chemical",
        "mol_w": 122.16, "vapor_pressure_mmhg": 0.08600, "sg_pure": 1.020,
        "ifra_cat4_max": 100.0, "baseline_allergens": {},
        "desc_zh": "新鮮露水玫瑰花瓣的核心骨架，溫潤柔和。",
        "desc_en": "Core building block of dewy fresh rose petals; soft, honeyed, and warm."
    },
    "5392-40-5": {
        "cas": "5392-40-5", "name_cn": "檸檬醛 (Citral)", "name_en": "Citral",
        "note": "Top", "family": "Citrus", "type": "Aroma Chemical",
        "mol_w": 152.24, "vapor_pressure_mmhg": 0.09100, "sg_pure": 0.888,
        "ifra_cat4_max": 0.6, "baseline_allergens": {"Citral": 1.0},
        "desc_zh": "銳利清脆的檸檬皮汁液爆發感（IFRA 嚴格限量 0.6%）。",
        "desc_en": "Sharp, zesty burst of freshly squeezed lemon peel (strict IFRA Cat.4 limit: 0.6%)."
    },
    "8006-90-4": {
        "cas": "8006-90-4", "name_cn": "歐薄荷 (Peppermint)", "name_en": "Peppermint Oil",
        "note": "Top", "family": "Spicy", "type": "Natural Essential Oil",
        "mol_w": 156.27, "vapor_pressure_mmhg": 0.85000, "sg_pure": 0.898,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Limonene": 0.03, "Linalool": 0.01},
        "desc_zh": "強烈清涼薄荷腦穿透力，瞬間醒腦提神。",
        "desc_en": "Crisp, penetrating menthol freshness that awakens top notes."
    },
    "8022-91-1": {
        "cas": "8022-91-1", "name_cn": "芳樟 (Ho Wood)", "name_en": "Ho Wood Oil",
        "note": "Mid", "family": "Woody", "type": "Natural Essential Oil",
        "mol_w": 154.25, "vapor_pressure_mmhg": 0.16000, "sg_pure": 0.865,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Linalool": 0.92},
        "desc_zh": "富含天然右旋沉香醇，比花梨木更細膩的溫暖花香木質。",
        "desc_en": "Rich in natural linalool; smooth, floral-woody heart softer than rosewood."
    },
    "8001-61-4": {
        "cas": "8001-61-4", "name_cn": "古巴香脂 (Copaiba)", "name_en": "Copaiba Balsam Oil",
        "note": "Base", "family": "Woody", "type": "Natural Essential Oil",
        "mol_w": 204.35, "vapor_pressure_mmhg": 0.00850, "sg_pure": 0.900,
        "ifra_cat4_max": 100.0, "baseline_allergens": {},
        "desc_zh": "深沉溫和的木質樹脂底蘊，極佳的天然定香劑。",
        "desc_en": "Gentle, woody-balsamic base note; superb natural fixative."
    },
    "8006-81-3": {
        "cas": "8006-81-3", "name_cn": "完全伊蘭 (Ylang Complete)", "name_en": "Ylang Ylang Complete Oil",
        "note": "Mid", "family": "Floral", "type": "Natural Essential Oil",
        "mol_w": 180.24, "vapor_pressure_mmhg": 0.02400, "sg_pure": 0.930,
        "ifra_cat4_max": 0.8, "baseline_allergens": {"Benzyl Benzoate": 0.08, "Linalool": 0.12, "Geraniol": 0.02},
        "desc_zh": "濃郁異國感與奶油般醉人的熱帶白花香。",
        "desc_en": "Opulent, creamy, narcotic tropical white floral."
    },
    "8028-48-6": {
        "cas": "8028-48-6", "name_cn": "甜橙 (Sweet Orange)", "name_en": "Sweet Orange Oil",
        "note": "Top", "family": "Citrus", "type": "Natural Essential Oil",
        "mol_w": 136.24, "vapor_pressure_mmhg": 1.54000, "sg_pure": 0.844,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Limonene": 0.94, "Linalool": 0.01},
        "desc_zh": "陽光多汁、純真溫暖的鮮榨果實甜香。",
        "desc_en": "Radiant, juicy, sun-drenched sweet citrus burst."
    },
    "8000-28-0": {
        "cas": "8000-28-0", "name_cn": "真正薰衣草 (Lavender)", "name_en": "Lavender Angustifolia Oil",
        "note": "Mid", "family": "Floral", "type": "Natural Essential Oil",
        "mol_w": 196.29, "vapor_pressure_mmhg": 0.11000, "sg_pure": 0.880,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Linalool": 0.38, "Limonene": 0.01, "Coumarin": 0.005},
        "desc_zh": "酯類豐富，乾淨細緻且具安撫力的草本花香。",
        "desc_en": "Ester-rich, serene herbaceous floral heart."
    },
    "92201-50-8": {
        "cas": "92201-50-8", "name_cn": "羅溫莎葉 (Ravintsara)", "name_en": "Ravintsara Oil",
        "note": "Top", "family": "Spicy", "type": "Natural Essential Oil",
        "mol_w": 154.25, "vapor_pressure_mmhg": 1.85000, "sg_pure": 0.900,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Limonene": 0.03, "Linalool": 0.01},
        "desc_zh": "高含量 1,8-桉油醇，帶來通透潔淨的森林空氣感。",
        "desc_en": "Rich in 1,8-cineole; crisp, breathable camphoraceous forest air."
    },
    "8016-36-2": {
        "cas": "8016-36-2", "name_cn": "乳香 (Olibanum / Frankincense)", "name_en": "Olibanum Oil",
        "note": "Base", "family": "Woody", "type": "Natural Essential Oil",
        "mol_w": 136.24, "vapor_pressure_mmhg": 0.01800, "sg_pure": 0.875,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Limonene": 0.14},
        "desc_zh": "神聖靜謐的古老樹脂煙燻感，前調帶有清亮檸檬松針氣息。",
        "desc_en": "Sacred, tranquil ancient resin with bright lemon-pine top terpenes and balsamic depth."
    },
    "8008-31-9": {
        "cas": "8008-31-9", "name_cn": "紅橘 (Tangerine)", "name_en": "Tangerine Oil",
        "note": "Top", "family": "Citrus", "type": "Natural Essential Oil",
        "mol_w": 136.24, "vapor_pressure_mmhg": 1.48000, "sg_pure": 0.845,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Limonene": 0.90, "Linalool": 0.01},
        "desc_zh": "比甜橙更柔和微甜、帶有童趣與撫慰感的柑橘香氣。",
        "desc_en": "Softer, sweeter, and more comforting than sweet orange."
    },
    "8014-17-3": {
        "cas": "8014-17-3", "name_cn": "苦橙葉 (Petitgrain)", "name_en": "Petitgrain Oil",
        "note": "Top-Mid", "family": "Spicy", "type": "Natural Essential Oil",
        "mol_w": 196.29, "vapor_pressure_mmhg": 0.14000, "sg_pure": 0.885,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Linalool": 0.25, "Limonene": 0.08, "Geraniol": 0.03},
        "desc_zh": "微苦青澀枝葉中透出細緻橙花氣息，高酯類強力放鬆。",
        "desc_en": "Crisp, bittersweet green twigs and leaves revealing delicate neroli-like floralcy."
    },
    "8016-63-5": {
        "cas": "8016-63-5", "name_cn": "快樂鼠尾草 (Clary Sage)", "name_en": "Clary Sage Oil",
        "note": "Mid", "family": "Spicy", "cas_alt": "8016-63-5", "type": "Natural Essential Oil",
        "mol_w": 196.29, "vapor_pressure_mmhg": 0.07500, "sg_pure": 0.890,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Linalool": 0.22, "Geraniol": 0.02},
        "desc_zh": "堅果草本、微醺茶香與琥珀龍涎氣息交織，深層鎮靜。",
        "desc_en": "Nutty, tea-like herbaceous heart with ambery-musk undertones."
    },
    "91770-58-0": {
        "cas": "91770-58-0", "name_cn": "台灣肖楠 (Taiwan Incense Cedar)", "name_en": "Taiwan Incense Cedar Oil",
        "note": "Base", "family": "Woody", "type": "Natural Essential Oil",
        "mol_w": 220.35, "vapor_pressure_mmhg": 0.00320, "sg_pure": 0.940,
        "ifra_cat4_max": 100.0, "baseline_allergens": {},
        "desc_zh": "台灣特有種，沉穩內斂的百年古剎冷冽木質與溫潤奶香。",
        "desc_en": "Endemic Taiwanese wood oil; meditative, cool temple woodiness with creamy warmth."
    },
    "9000-05-9": {
        "cas": "9000-05-9", "name_cn": "安息香原精 (Benzoin Resinoid)", "name_en": "Benzoin Resinoid",
        "note": "Base", "family": "Sweet", "type": "Natural Essential Oil",
        "mol_w": 212.24, "vapor_pressure_mmhg": 0.00005, "sg_pure": 1.150,
        "ifra_cat4_max": 2.0, "baseline_allergens": {"Benzyl Benzoate": 0.15, "Cinnamal": 0.01},
        "desc_zh": "濃稠溫潤的香草焦糖樹脂香（高蠟質，強烈建議以 TEC 預溶）。",
        "desc_en": "Viscous, comforting vanilla-caramel resin (high wax; pre-dissolve in TEC)."
    },
    "8002-68-4": {
        "cas": "8002-68-4", "name_cn": "杜松子 (Juniper Berry)", "name_en": "Juniper Berry Oil",
        "note": "Top-Mid", "family": "Woody", "type": "Natural Essential Oil",
        "mol_w": 136.24, "vapor_pressure_mmhg": 0.92000, "sg_pure": 0.865,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Limonene": 0.05},
        "desc_zh": "琴酒般清脆冷冽的松柏果實木質，帶來通透的空氣感。",
        "desc_en": "Crisp, gin-like coniferous berry woodiness imparting clean vertical lift."
    },
    "8006-82-4": {
        "cas": "8006-82-4", "name_cn": "黑胡椒 (Black Pepper)", "name_en": "Black Pepper Oil",
        "note": "Top", "family": "Spicy", "type": "Natural Essential Oil",
        "mol_w": 204.35, "vapor_pressure_mmhg": 0.45000, "sg_pure": 0.875,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Limonene": 0.18, "Linalool": 0.01},
        "desc_zh": "乾燥微辛的木質胡椒粒氣息，給予前調躍動的立體能量。",
        "desc_en": "Dry, sparkling woody-spicy peppercorn note that energizes top structures."
    },
    "91745-96-9": {
        "cas": "91745-96-9", "name_cn": "台灣紅檜 (Taiwan Red Hinoki)", "name_en": "Taiwan Red Hinoki Oil",
        "note": "Mid-Base", "family": "Woody", "type": "Natural Essential Oil",
        "mol_w": 222.37, "vapor_pressure_mmhg": 0.00550, "sg_pure": 0.940,
        "ifra_cat4_max": 100.0, "baseline_allergens": {},
        "desc_zh": "台灣高山霧林紅檜，檸檬清香與深邃檜木醇完美平衡。",
        "desc_en": "Taiwanese alpine red cypress; lemon-zest clarity balanced with deep hinokitiol."
    },
    "8021-29-2": {
        "cas": "8021-29-2", "name_cn": "西伯利亞冷杉 (Siberian Fir)", "name_en": "Siberian Fir Needle Oil",
        "note": "Top", "family": "Woody", "type": "Natural Essential Oil",
        "mol_w": 196.29, "vapor_pressure_mmhg": 0.68000, "sg_pure": 0.900,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Limonene": 0.15},
        "desc_zh": "高比例乙酸龍腦酯，清冷雪松針葉與微甜樹脂香。",
        "desc_en": "High bornyl acetate content; crisp pine-needle freshness with sweet balsamic undertones."
    },
    "8014-19-5": {
        "cas": "8014-19-5", "name_cn": "玫瑰草 (Palmarosa)", "name_en": "Palmarosa Oil",
        "note": "Mid", "family": "Floral", "type": "Natural Essential Oil",
        "mol_w": 154.25, "vapor_pressure_mmhg": 0.04200, "sg_pure": 0.885,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Geraniol": 0.82, "Linalool": 0.03},
        "desc_zh": "富含天然牻牛兒醇，帶有清新青草露水感的玫瑰花香。",
        "desc_en": "Rich in natural geraniol; fresh, dewy, green-grassy rose heart."
    },
    "8000-25-7": {
        "cas": "8000-25-7", "name_cn": "桉油醇迷迭香 (Rosemary Cineole)", "name_en": "Rosemary Cineole Oil",
        "note": "Top", "family": "Spicy", "type": "Natural Essential Oil",
        "mol_w": 154.25, "vapor_pressure_mmhg": 1.62000, "sg_pure": 0.905,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Limonene": 0.04, "Linalool": 0.02},
        "desc_zh": "強烈草本清涼穿透力，提升專注力，馥奇調核心。",
        "desc_en": "Penetrating, cooling herbal clarity; classic aromatic fougère top note."
    },
    "8007-75-8": {
        "cas": "8007-75-8", "name_cn": "佛手柑 (Bergamot)", "name_en": "Bergamot Oil",
        "note": "Top", "family": "Citrus", "type": "Natural Essential Oil",
        "mol_w": 196.29, "vapor_pressure_mmhg": 0.82000, "sg_pure": 0.875,
        "ifra_cat4_max": 0.4, "baseline_allergens": {"Limonene": 0.42, "Linalool": 0.12, "Citral": 0.01},
        "desc_zh": "精緻伯爵茶清香，兼顧檸檬活力與薰衣草花香（未去光敏 IFRA 限值 0.4%）。",
        "desc_en": "Refined Earl Grey citrus-floral elegance (Non-FCF IFRA Cat.4 limit: 0.4%)."
    },
    "8014-68-4": {
        "cas": "8014-68-4", "name_cn": "綠花白千層 (Niaouli)", "name_en": "Niaouli Oil",
        "note": "Top", "family": "Spicy", "type": "Natural Essential Oil",
        "mol_w": 154.25, "vapor_pressure_mmhg": 1.75000, "sg_pure": 0.910,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Limonene": 0.08, "Linalool": 0.01},
        "desc_zh": "比茶樹溫和且帶有微甜花果尾韻的氧化物清新。",
        "desc_en": "Softer than tea tree; clean 1,8-cineole freshness with a subtly sweet fruity-floral undertone."
    },
    "8000-48-4": {
        "cas": "8000-48-4", "name_cn": "澳洲尤加利 (Eucalyptus Radiata)", "name_en": "Eucalyptus Radiata Oil",
        "note": "Top", "family": "Spicy", "type": "Natural Essential Oil",
        "mol_w": 154.25, "vapor_pressure_mmhg": 1.90000, "sg_pure": 0.910,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Limonene": 0.06, "Citral": 0.01},
        "desc_zh": "清澈微甜的澳洲森林氣息，呼吸感極佳且不嗆鼻。",
        "desc_en": "Crisp, slightly sweet Australian forest air; smooth and non-harsh."
    },
    "8013-86-3": {
        "cas": "8013-86-3", "name_cn": "絲柏 (Cypress)", "name_en": "Cypress Oil",
        "note": "Mid", "family": "Woody", "type": "Natural Essential Oil",
        "mol_w": 136.24, "vapor_pressure_mmhg": 0.54000, "sg_pure": 0.870,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Limonene": 0.04},
        "desc_zh": "冷冽乾燥的針葉柏木氣息，為木質調帶來垂直向上的森林骨架。",
        "desc_en": "Cool, dry needle-woody heart that builds vertical forest structure."
    },
    "8014-09-3": {
        "cas": "8014-09-3", "name_cn": "廣藿香 (Patchouli)", "name_en": "Patchouli Oil",
        "note": "Base", "family": "Woody", "type": "Natural Essential Oil",
        "mol_w": 222.37, "vapor_pressure_mmhg": 0.00210, "sg_pure": 0.965,
        "ifra_cat4_max": 100.0, "baseline_allergens": {},
        "desc_zh": "深邃陳香、微帶黑巧克力與雨後泥土的古老根系，西普調靈魂。",
        "desc_en": "Deep, aged earthy roots with dark cacao nuances; quintessential chypre anchor."
    },
    "8000-27-9": {
        "cas": "8000-27-9", "name_cn": "維吉尼亞雪松 (Cedarwood Virginia)", "name_en": "Cedarwood Virginia Oil",
        "note": "Base", "family": "Woody", "type": "Natural Essential Oil",
        "mol_w": 222.37, "vapor_pressure_mmhg": 0.00480, "sg_pure": 0.920,
        "ifra_cat4_max": 100.0, "baseline_allergens": {},
        "desc_zh": "乾燥削鉛筆木屑的經典冷冽木質，定香力極強。",
        "desc_en": "Classic dry pencil-shaving cedarwood with tenacious fixative power."
    },
    "8023-89-0": {
        "cas": "8023-89-0", "name_cn": "欖香脂 (Elemi)", "name_en": "Elemi Oil",
        "note": "Top-Mid", "family": "Citrus", "type": "Natural Essential Oil",
        "mol_w": 136.24, "vapor_pressure_mmhg": 0.76000, "sg_pure": 0.880,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Limonene": 0.52},
        "desc_zh": "帶有明亮檸檬與黑胡椒辛香的輕盈樹脂，銜接前調與後調的橋樑。",
        "desc_en": "Luminous lemon-pepper resin bridging bright citrus tops with olibanum base notes."
    },
    "68647-73-4": {
        "cas": "68647-73-4", "name_cn": "茶樹 (Tea Tree)", "name_en": "Tea Tree Oil",
        "note": "Top", "family": "Spicy", "type": "Natural Essential Oil",
        "mol_w": 154.25, "vapor_pressure_mmhg": 1.40000, "sg_pure": 0.900,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Limonene": 0.03, "Linalool": 0.01},
        "desc_zh": "純淨潔癖般的草本藥草氣息，賦予現代潔淨調真實感。",
        "desc_en": "Crisp, medicinal herbal clarity lending authentic cleanliness to modern accords."
    },
    "NCS-MALLOTUS-01": {
        "cas": "NCS-MALLOTUS-01", "name_cn": "白楸花天然複方基劑 (Mallotus NCS)", "name_en": "Mallotus Flower Natural Accord (NCS)",
        "note": "Mid", "family": "Floral", "type": "Natural Botanical Blend",
        "mol_w": 180.00, "vapor_pressure_mmhg": 0.05000, "sg_pure": 0.910,
        "ifra_cat4_max": 100.0, "baseline_allergens": {"Linalool": 0.10, "Limonene": 0.05},
        "desc_zh": "台灣野地白楸花原精結合尤加利與芳樟葉，清甜帶粉感的山野白花香。",
        "desc_en": "Wild Taiwanese Mallotus flower absolute blended with eucalyptus and ho leaf; powdery meadow floral."
    }
}

# ==============================================================================
# LAYER 2: 商業 SKU 庫 (COMMERCIAL SKU DATABASE - Mapped to Layer 1 CAS)
# 開放給原料商/代工廠上傳料號，掛載具體批號、效期、價格、純度與 COA/SDS/IFRA 文件狀態
# ==============================================================================
DEFAULT_COMMERCIAL_SKUS = {
    "SKU-CHEM-54464-50": {
        "sku_id": "SKU-CHEM-54464-50", "cas": "54464-57-2",
        "trade_name_cn": "龍涎酮 50% in DPG (實驗室預溶)", "trade_name_en": "Iso E Super 50% in DPG (Lab Pre-diluted)",
        "supplier_zh": "單體庫 / IFF 規格", "supplier_en": "Aroma Chem Lab (IFF Spec)",
        "lot_no": "LOT-IES-2601", "exp_date": "2029/12/31",
        "dilution_pct": 50.0, "solvent": "DPG (二丙二醇)", "sg": 0.993, "cost_per_g": 3.5,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {}
    },
    "SKU-CHEM-24851-50": {
        "sku_id": "SKU-CHEM-24851-50", "cas": "24851-98-7",
        "trade_name_cn": "Hedione 50% in DPG (Firmenich 規格)", "trade_name_en": "Hedione 50% in DPG (Firmenich Spec)",
        "supplier_zh": "單體庫 / Firmenich 規格", "supplier_en": "Aroma Chem Lab (Firmenich Spec)",
        "lot_no": "LOT-HED-2602", "exp_date": "2029/12/31",
        "dilution_pct": 50.0, "solvent": "DPG (二丙二醇)", "sg": 1.012, "cost_per_g": 4.2,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {}
    },
    "SKU-GIV-6790-100": {
        "sku_id": "SKU-GIV-6790-100", "cas": "6790-58-5",
        "trade_name_cn": "Givaudan Ambroxan 100% 純結晶粉末", "trade_name_en": "Givaudan Ambroxan 100% Crystalline Powder",
        "supplier_zh": "Givaudan 奇華頓", "supplier_en": "Givaudan",
        "lot_no": "GIV-AMB-9921", "exp_date": "2030/06/30",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.980, "cost_per_g": 18.0,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {}
    },
    "SKU-LAB-6790-10": {
        "sku_id": "SKU-LAB-6790-10", "cas": "6790-58-5",
        "trade_name_cn": "Ambroxan 10% in DPG (調香室預溶液)", "trade_name_en": "Ambroxan 10% in DPG (Lab Tincture)",
        "supplier_zh": "單體庫 (預溶規格)", "supplier_en": "Aroma Chem Lab (Pre-dissolved)",
        "lot_no": "LAB-AMB-10A", "exp_date": "2028/12/31",
        "dilution_pct": 10.0, "solvent": "DPG (二丙二醇)", "sg": 1.019, "cost_per_g": 18.0,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {}
    },
    "SKU-CHEM-1222-50": {
        "sku_id": "SKU-CHEM-1222-50", "cas": "1222-05-5",
        "trade_name_cn": "Galaxolide 50% in IPM", "trade_name_en": "Galaxolide 50% in IPM",
        "supplier_zh": "單體庫 / IFF 規格", "supplier_en": "Aroma Chem Lab (IFF Spec)",
        "lot_no": "LOT-GLX-50", "exp_date": "2029/10/01",
        "dilution_pct": 50.0, "solvent": "IPM (肉豆蔻酸異丙酯)", "sg": 0.929, "cost_per_g": 3.0,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {}
    },
    "SKU-CHEM-60128-50": {
        "sku_id": "SKU-CHEM-60128-50", "cas": "60-12-8",
        "trade_name_cn": "苯乙醇 PEA 50% in DPG", "trade_name_en": "Phenethyl Alcohol 50% in DPG",
        "supplier_zh": "單體庫", "supplier_en": "Aroma Chem Lab",
        "lot_no": "LOT-PEA-01", "exp_date": "2029/08/15",
        "dilution_pct": 50.0, "solvent": "DPG (二丙二醇)", "sg": 1.022, "cost_per_g": 2.5,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {}
    },
    "SKU-CHEM-5392-10": {
        "sku_id": "SKU-CHEM-5392-10", "cas": "5392-40-5",
        "trade_name_cn": "檸檬醛 Citral 10% in DPG", "trade_name_en": "Citral 10% in DPG",
        "supplier_zh": "單體庫", "supplier_en": "Aroma Chem Lab",
        "lot_no": "LOT-CIT-10", "exp_date": "2028/05/01",
        "dilution_pct": 10.0, "solvent": "DPG (二丙二醇)", "sg": 1.010, "cost_per_g": 1.5,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Citral": 1.0}
    },
    # --- 中興化工採購批次 ---
    "SKU-ZX-8006904": {
        "sku_id": "SKU-ZX-8006904", "cas": "8006-90-4",
        "trade_name_cn": "中興化工 法國歐薄荷精油 (100% 純油)", "trade_name_en": "Chunghsing French Peppermint EO (100% Neat)",
        "supplier_zh": "中興化工", "supplier_en": "Chunghsing Chem",
        "lot_no": "ZX-260526-PEP", "exp_date": "2028/09/14",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.898, "cost_per_g": 22.3,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Limonene": 0.03, "Linalool": 0.01}
    },
    "SKU-ZX-8022911": {
        "sku_id": "SKU-ZX-8022911", "cas": "8022-91-1",
        "trade_name_cn": "中興化工 中國芳樟葉精油 (100% 純油)", "trade_name_en": "Chunghsing Ho Wood EO (100% Neat)",
        "supplier_zh": "中興化工", "supplier_en": "Chunghsing Chem",
        "lot_no": "ZX-260526-HO", "exp_date": "2028/02/12",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.865, "cost_per_g": 23.1,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Linalool": 0.92}
    },
    "SKU-ZX-8001614": {
        "sku_id": "SKU-ZX-8001614", "cas": "8001-61-4",
        "trade_name_cn": "中興化工 古巴香脂精油 (100% 純油)", "trade_name_en": "Chunghsing Copaiba Balsam EO (100% Neat)",
        "supplier_zh": "中興化工", "supplier_en": "Chunghsing Chem",
        "lot_no": "ZX-260526-COP", "exp_date": "2027/02/27",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.900, "cost_per_g": 27.8,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {}
    },
    "SKU-ZX-8006813": {
        "sku_id": "SKU-ZX-8006813", "cas": "8006-81-3",
        "trade_name_cn": "中興化工 馬達加斯加完全伊蘭 (10% in DPG)", "trade_name_en": "Chunghsing Madagascar Ylang Complete (10% in DPG)",
        "supplier_zh": "中興化工", "supplier_en": "Chunghsing Chem",
        "lot_no": "ZX-260530-YLA", "exp_date": "2029/03/01",
        "dilution_pct": 10.0, "solvent": "DPG (二丙二醇)", "sg": 1.014, "cost_per_g": 40.9,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Benzyl Benzoate": 0.08, "Linalool": 0.12, "Geraniol": 0.02}
    },
    "SKU-ZX-8028486": {
        "sku_id": "SKU-ZX-8028486", "cas": "8028-48-6",
        "trade_name_cn": "中興化工 義大利冷壓甜橙精油 (100% 純油)", "trade_name_en": "Chunghsing Italian Sweet Orange EO (100% Neat)",
        "supplier_zh": "中興化工", "supplier_en": "Chunghsing Chem",
        "lot_no": "ZX-260603-ORG", "exp_date": "2028/09/07",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.844, "cost_per_g": 12.0,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Limonene": 0.94, "Linalool": 0.01}
    },
    "SKU-ZX-8000280": {
        "sku_id": "SKU-ZX-8000280", "cas": "8000-28-0",
        "trade_name_cn": "中興化工 法國高山薰衣草精油 (100% 純油)", "trade_name_en": "Chunghsing French Lavender Pop. EO (100% Neat)",
        "supplier_zh": "中興化工", "supplier_en": "Chunghsing Chem",
        "lot_no": "ZX-260603-LAV", "exp_date": "2029/02/09",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.880, "cost_per_g": 39.8,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Linalool": 0.38, "Limonene": 0.01, "Coumarin": 0.005}
    },
    "SKU-ZX-92201508": {
        "sku_id": "SKU-ZX-92201508", "cas": "92201-50-8",
        "trade_name_cn": "中興化工 馬達加斯加羅溫莎葉 (100% 純油)", "trade_name_en": "Chunghsing Madagascar Ravintsara EO (100% Neat)",
        "supplier_zh": "中興化工", "supplier_en": "Chunghsing Chem",
        "lot_no": "ZX-260603-RAV", "exp_date": "2028/08/11",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.900, "cost_per_g": 38.9,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Limonene": 0.03, "Linalool": 0.01}
    },
    "SKU-ZX-8016362": {
        "sku_id": "SKU-ZX-8016362", "cas": "8016-36-2",
        "trade_name_cn": "中興化工 索馬利亞乳香精油 (100% 純油)", "trade_name_en": "Chunghsing Somalia Olibanum EO (100% Neat)",
        "supplier_zh": "中興化工", "supplier_en": "Chunghsing Chem",
        "lot_no": "ZX-260603-OLI", "exp_date": "2028/12/01",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.875, "cost_per_g": 80.0,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Limonene": 0.14}
    },
    "SKU-ZX-8008319": {
        "sku_id": "SKU-ZX-8008319", "cas": "8008-31-9",
        "trade_name_cn": "中興化工 義大利紅橘精油 (100% 純油)", "trade_name_en": "Chunghsing Italian Tangerine EO (100% Neat)",
        "supplier_zh": "中興化工", "supplier_en": "Chunghsing Chem",
        "lot_no": "ZX-260603-TAN", "exp_date": "2028/06/05",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.845, "cost_per_g": 23.7,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Limonene": 0.90, "Linalool": 0.01}
    },
    "SKU-ZX-8014173": {
        "sku_id": "SKU-ZX-8014173", "cas": "8014-17-3",
        "trade_name_cn": "中興化工 南美苦橙葉精油 (100% 純油)", "trade_name_en": "Chunghsing South America Petitgrain EO (100% Neat)",
        "supplier_zh": "中興化工", "supplier_en": "Chunghsing Chem",
        "lot_no": "ZX-260626-PET", "exp_date": "2028/12/01",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.885, "cost_per_g": 28.3,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Linalool": 0.25, "Limonene": 0.08, "Geraniol": 0.03}
    },
    "SKU-ZX-8016635": {
        "sku_id": "SKU-ZX-8016635", "cas": "8016-63-5",
        "trade_name_cn": "中興化工 法國快樂鼠尾草精油 (100% 純油)", "trade_name_en": "Chunghsing French Clary Sage EO (100% Neat)",
        "supplier_zh": "中興化工", "supplier_en": "Chunghsing Chem",
        "lot_no": "ZX-260626-CLA", "exp_date": "2029/01/15",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.890, "cost_per_g": 33.7,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Linalool": 0.22, "Geraniol": 0.02}
    },
    "SKU-ZX-91770580": {
        "sku_id": "SKU-ZX-91770580", "cas": "91770-58-0",
        "trade_name_cn": "中興化工 台灣肖楠木精油 (100% 純油)", "trade_name_en": "Chunghsing Taiwan Incense Cedar EO (100% Neat)",
        "supplier_zh": "中興化工", "supplier_en": "Chunghsing Chem",
        "lot_no": "ZX-260727-CED", "exp_date": "2029/04/22",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.940, "cost_per_g": 74.5,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {}
    },
    "SKU-ZX-9000059": {
        "sku_id": "SKU-ZX-9000059", "cas": "9000-05-9",
        "trade_name_cn": "中興化工 蘇門答臘安息香 (50% in TEC 預溶)", "trade_name_en": "Chunghsing Sumatra Benzoin (50% in TEC)",
        "supplier_zh": "中興化工", "supplier_en": "Chunghsing Chem",
        "lot_no": "ZX-260811-BEN", "exp_date": "2029/08/11",
        "dilution_pct": 50.0, "solvent": "TEC (檸檬酸三乙酯)", "sg": 1.144, "cost_per_g": 17.4,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Benzyl Benzoate": 0.15, "Cinnamal": 0.01}
    },
    "SKU-ZX-8002684": {
        "sku_id": "SKU-ZX-8002684", "cas": "8002-68-4",
        "trade_name_cn": "中興化工 杜松子精油 (100% 純油)", "trade_name_en": "Chunghsing Juniper Berry EO (100% Neat)",
        "supplier_zh": "中興化工", "supplier_en": "Chunghsing Chem",
        "lot_no": "ZX-260927-JUN", "exp_date": "2029/09/27",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.865, "cost_per_g": 28.9,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Limonene": 0.05}
    },
    "SKU-ZX-8006824": {
        "sku_id": "SKU-ZX-8006824", "cas": "8006-82-4",
        "trade_name_cn": "中興化工 黑胡椒精油 (100% 純油)", "trade_name_en": "Chunghsing Black Pepper EO (100% Neat)",
        "supplier_zh": "中興化工", "supplier_en": "Chunghsing Chem",
        "lot_no": "ZX-260927-PEP", "exp_date": "2029/09/27",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.875, "cost_per_g": 34.3,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Limonene": 0.18, "Linalool": 0.01}
    },
    "SKU-ZX-91745969": {
        "sku_id": "SKU-ZX-91745969", "cas": "91745-96-9",
        "trade_name_cn": "中興化工 台灣紅檜樹心精油 (100% 純油)", "trade_name_en": "Chunghsing Taiwan Red Hinoki EO (100% Neat)",
        "supplier_zh": "中興化工", "supplier_en": "Chunghsing Chem",
        "lot_no": "ZX-261030-HIN", "exp_date": "2029/10/30",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.940, "cost_per_g": 37.2,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {}
    },
    "SKU-ZX-8021292": {
        "sku_id": "SKU-ZX-8021292", "cas": "8021-29-2",
        "trade_name_cn": "中興化工 西伯利亞冷杉精油 (100% 純油)", "trade_name_en": "Chunghsing Siberian Fir EO (100% Neat)",
        "supplier_zh": "中興化工", "supplier_en": "Chunghsing Chem",
        "lot_no": "ZX-261030-FIR", "exp_date": "2029/10/30",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.900, "cost_per_g": 22.2,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Limonene": 0.15}
    },
    # --- 精油好事多 & 沐禾芳療 & 樸草園 ---
    "SKU-OH-8014195": {
        "sku_id": "SKU-OH-8014195", "cas": "8014-19-5",
        "trade_name_cn": "精油好事多 印度玫瑰草精油 (100% 純油)", "trade_name_en": "Oilhausco Indian Palmarosa EO (100% Neat)",
        "supplier_zh": "精油好事多", "supplier_en": "Oilhausco",
        "lot_no": "OH-260510-PAL", "exp_date": "2027/08/31",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.885, "cost_per_g": 24.2,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Geraniol": 0.82, "Linalool": 0.03}
    },
    "SKU-OH-8000257": {
        "sku_id": "SKU-OH-8000257", "cas": "8000-25-7",
        "trade_name_cn": "精油好事多 桉油醇迷迭香 (100% 純油)", "trade_name_en": "Oilhausco Rosemary Cineole EO (100% Neat)",
        "supplier_zh": "精油好事多", "supplier_en": "Oilhausco",
        "lot_no": "OH-260510-ROS", "exp_date": "2030/06/30",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.905, "cost_per_g": 26.0,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Limonene": 0.04, "Linalool": 0.02}
    },
    "SKU-MH-8007758": {
        "sku_id": "SKU-MH-8007758", "cas": "8007-75-8",
        "trade_name_cn": "沐禾芳療 義大利佛手柑精油 (100% 純油)", "trade_name_en": "AromaHarvest Italian Bergamot EO (100% Neat)",
        "supplier_zh": "沐禾芳療", "supplier_en": "AromaHarvest",
        "lot_no": "MH-260429-BER", "exp_date": "2028/04/29",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.875, "cost_per_g": 68.6,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Limonene": 0.42, "Linalool": 0.12, "Citral": 0.01}
    },
    "SKU-MH-8014684": {
        "sku_id": "SKU-MH-8014684", "cas": "8014-68-4",
        "trade_name_cn": "沐禾芳療 綠花白千層精油 (100% 純油)", "trade_name_en": "AromaHarvest Niaouli EO (100% Neat)",
        "supplier_zh": "沐禾芳療", "supplier_en": "AromaHarvest",
        "lot_no": "MH-260519-NIA", "exp_date": "2030/06/30",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.910, "cost_per_g": 24.7,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Limonene": 0.08, "Linalool": 0.01}
    },
    "SKU-MH-8000484": {
        "sku_id": "SKU-MH-8000484", "cas": "8000-48-4",
        "trade_name_cn": "沐禾芳療 澳洲尤加利精油 (100% 純油)", "trade_name_en": "AromaHarvest Eucalyptus Radiata EO (100% Neat)",
        "supplier_zh": "沐禾芳療", "supplier_en": "AromaHarvest",
        "lot_no": "MH-260519-EUC", "exp_date": "2030/11/30",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.910, "cost_per_g": 26.4,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Limonene": 0.06, "Citral": 0.01}
    },
    "SKU-MH-8013863": {
        "sku_id": "SKU-MH-8013863", "cas": "8013-86-3",
        "trade_name_cn": "沐禾芳療 法國絲柏精油 (100% 純油)", "trade_name_en": "AromaHarvest French Cypress EO (100% Neat)",
        "supplier_zh": "沐禾芳療", "supplier_en": "AromaHarvest",
        "lot_no": "MH-260519-CYP", "exp_date": "2030/11/30",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.870, "cost_per_g": 33.9,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Limonene": 0.04}
    },
    "SKU-MH-8014093": {
        "sku_id": "SKU-MH-8014093", "cas": "8014-09-3",
        "trade_name_cn": "沐禾芳療 印尼廣藿香精油 (100% 純油)", "trade_name_en": "AromaHarvest Indonesian Patchouli EO (100% Neat)",
        "supplier_zh": "沐禾芳療", "supplier_en": "AromaHarvest",
        "lot_no": "MH-260609-PAT", "exp_date": "2031/01/31",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.965, "cost_per_g": 38.9,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {}
    },
    "SKU-MH-8000279": {
        "sku_id": "SKU-MH-8000279", "cas": "8000-27-9",
        "trade_name_cn": "沐禾芳療 維吉尼亞雪松精油 (100% 純油)", "trade_name_en": "AromaHarvest Cedarwood Virginia EO (100% Neat)",
        "supplier_zh": "沐禾芳療", "supplier_en": "AromaHarvest",
        "lot_no": "MH-260609-CED", "exp_date": "2030/01/31",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.920, "cost_per_g": 28.3,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {}
    },
    "SKU-MH-8023890": {
        "sku_id": "SKU-MH-8023890", "cas": "8023-89-0",
        "trade_name_cn": "沐禾芳療 欖香脂精油 (100% 純油)", "trade_name_en": "AromaHarvest Elemi EO (100% Neat)",
        "supplier_zh": "沐禾芳療", "supplier_en": "AromaHarvest",
        "lot_no": "MH-260609-ELE", "exp_date": "2029/07/31",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.880, "cost_per_g": 31.3,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Limonene": 0.52}
    },
    "SKU-MH-68647734": {
        "sku_id": "SKU-MH-68647734", "cas": "68647-73-4",
        "trade_name_cn": "沐禾芳療 澳洲茶樹精油 (100% 純油)", "trade_name_en": "AromaHarvest Australian Tea Tree EO (100% Neat)",
        "supplier_zh": "沐禾芳療", "supplier_en": "AromaHarvest",
        "lot_no": "MH-260609-TEA", "exp_date": "2031/04/30",
        "dilution_pct": 100.0, "solvent": "None (100%純原液)", "sg": 0.900, "cost_per_g": 28.3,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Limonene": 0.03, "Linalool": 0.01}
    },
    "SKU-PCY-MALLOTUS": {
        "sku_id": "SKU-PCY-MALLOTUS", "cas": "NCS-MALLOTUS-01",
        "trade_name_cn": "樸草園 清輕白楸花複方 (50% in Solketal/DPG)", "trade_name_en": "PuCaoYuan Mallotus Flower Accord (50% Diluted)",
        "supplier_zh": "樸草園", "supplier_en": "PuCaoYuan",
        "lot_no": "PCY-260415-MAL", "exp_date": "2028/04/15",
        "dilution_pct": 50.0, "solvent": "DPG (二丙二醇)", "sg": 0.966, "cost_per_g": 54.9,
        "docs": {"COA": True, "SDS": True, "IFRA": True},
        "allergens": {"Linalool": 0.10, "Limonene": 0.05}
    }
}
