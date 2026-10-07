import base64
import re
from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_DIR = Path(__file__).parent
DATA_PATH = PROJECT_DIR / "data" / "processed" / "laptops_cleaned.csv"
SMARTPRIX_PATH = PROJECT_DIR / "data" / "raw" / "smartprix_laptop.csv"
IMAGE_DIR = PROJECT_DIR / "assets" / "laptops"
DATASET_URL = "https://github.com/abhinavflac/laptops-specs-dataset"
SMARTPRIX_URL = "https://www.kaggle.com/datasets/souravghosh999/laptop-specifications-and-prices-smartprix"

st.set_page_config(page_title="SpecFinder India", page_icon="💻", layout="wide")
st.markdown(
    """
    <style>
      :root { color-scheme: light; }
      [data-testid="stAppViewContainer"] {background:#f4f8fd;color:#14243a;}
      [data-testid="stHeader"] {background:rgba(255,255,255,.94);border-bottom:1px solid #e8eef5;}
      .block-container {max-width:1480px;padding:0 2rem 3rem;}
      div[data-testid="stMarkdownContainer"] .site-nav {height:64px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #e8eef5;margin-bottom:0;color:#132c4b;}
      div[data-testid="stMarkdownContainer"] .brand {display:flex;align-items:center;gap:.65rem;font-size:1rem;font-weight:760;letter-spacing:-.025em;}
      div[data-testid="stMarkdownContainer"] .brand-icon {width:2rem;height:2rem;display:grid;place-items:center;background:#e7f1ff;border-radius:9px;font-size:1.15rem;}
      div[data-testid="stMarkdownContainer"] .nav-links {display:flex;gap:1.35rem;color:#526981;font-size:.78rem;}
      div[data-testid="stMarkdownContainer"] .hero {position:relative;overflow:hidden;text-align:center;padding:1.55rem 1rem 2.15rem;margin:0 -2rem 1.25rem;background:linear-gradient(112deg,#eef6ff 0%,#f7fbff 53%,#e9f4ff 100%);}
      div[data-testid="stMarkdownContainer"] .hero:after {content:"";position:absolute;left:-4%;right:-4%;height:46px;bottom:-27px;background:#f4f8fd;border-radius:50% 50% 0 0 / 78% 78% 0 0;}
      div[data-testid="stMarkdownContainer"] .hero-art {position:absolute;right:max(38px,calc((100% - 1270px)/2));top:50%;transform:translateY(-43%);opacity:.68;}
      div[data-testid="stMarkdownContainer"] .hero-art svg {width:128px;height:88px;}
      div[data-testid="stMarkdownContainer"] .hero-title {font-size:2rem !important;font-weight:770 !important;letter-spacing:-.045em !important;color:#172c49 !important;line-height:1.12 !important;margin:0 !important;}
      div[data-testid="stMarkdownContainer"] .hero-copy {font-size:.98rem;color:#61768e;margin:.48rem 0 0;}
      div[data-testid="stMarkdownContainer"] .hero-kicker {font-size:.67rem;font-weight:750;color:#3275bd;letter-spacing:.11em;text-transform:uppercase;margin-bottom:.35rem;}
      div[data-testid="stMarkdownContainer"] .page-section-title {font-size:1rem;font-weight:730;color:#18304e;margin:0 0 .8rem;}
      div[data-testid="stVerticalBlockBorderWrapper"] {background:#fff;border:1px solid #e6edf5;border-radius:16px;box-shadow:0 8px 28px rgba(27,58,91,.045);}
      div[data-testid="stVerticalBlockBorderWrapper"] > div {padding:1rem 1.05rem;}
      div[data-testid="stMarkdownContainer"] .muted {font-size:.77rem;color:#718198;line-height:1.45;}
      div[data-testid="stMarkdownContainer"] .soft-callout {display:flex;gap:.65rem;align-items:flex-start;background:#edf6ff;border:1px solid #dcecff;border-radius:10px;padding:.66rem .75rem;color:#38638d;font-size:.76rem;line-height:1.4;margin:.75rem 0 .85rem;}
      div[data-testid="stMarkdownContainer"] .why-box {display:flex;gap:.8rem;align-items:flex-start;background:#edf6ff;border:1px solid #dbeaff;border-radius:12px;padding:.8rem .9rem;margin:.85rem 0;color:#284b70;}
      div[data-testid="stMarkdownContainer"] .why-icon {font-size:1.35rem;line-height:1.2;}
      div[data-testid="stMarkdownContainer"] .why-title {font-size:.88rem;font-weight:750;margin-bottom:.18rem;color:#1e4f82;}
      div[data-testid="stMarkdownContainer"] .why-copy {font-size:.73rem;line-height:1.42;color:#59738e;}
      div[data-testid="stMarkdownContainer"] .product-image {height:106px;width:132px;object-fit:contain;border-radius:9px;background:#f1f6fc;}
      div[data-testid="stMarkdownContainer"] .photo-placeholder {height:106px;width:132px;border-radius:9px;background:linear-gradient(145deg,#f3f8fd,#eaf2fb);display:grid;place-items:center;}
      div[data-testid="stMarkdownContainer"] .photo-placeholder svg {width:102px;height:72px;}
      div[data-testid="stMarkdownContainer"] .product-title {font-size:.88rem;font-weight:740;line-height:1.32;color:#182d49;margin:.05rem 0 .22rem;}
      div[data-testid="stMarkdownContainer"] .product-desc {font-size:.7rem;line-height:1.35;color:#718198;margin:0 0 .45rem;}
      div[data-testid="stMarkdownContainer"] .badge {display:inline-block;border-radius:99px;padding:.23rem .53rem;font-size:.64rem;font-weight:700;white-space:nowrap;background:#e9f7ee;color:#2f8050;}
      div[data-testid="stMarkdownContainer"] .spec-grid {display:flex;gap:.35rem;flex-wrap:wrap;margin-top:.32rem;}
      div[data-testid="stMarkdownContainer"] .spec-pill {display:inline-flex;gap:.3rem;align-items:center;border:1px solid #e7edf4;border-radius:7px;padding:.26rem .42rem;background:#fff;color:#435970;font-size:.65rem;line-height:1.2;}
      div[data-testid="stMarkdownContainer"] .spec-icon {color:#2874c4;font-weight:800;}
      div[data-testid="stMarkdownContainer"] .price {font-size:.98rem;font-weight:780;color:#142944;white-space:nowrap;text-align:right;}
      div[data-testid="stMarkdownContainer"] .price-note {font-size:.64rem;color:#7a899b;text-align:right;margin-top:.08rem;}
      div[data-testid="stMarkdownContainer"] .match-count {font-size:.74rem;color:#718198;}
      div[data-testid="stExpander"] {border:1px solid #e5ebf2;border-radius:10px;background:#fbfdff;}
      div[data-testid="stExpander"] summary {font-size:.79rem;color:#2d5e8d;font-weight:680;}
      div[data-testid="stButton"] button {border-radius:8px;border:0;background:#216fca;color:#fff;font-size:.69rem;font-weight:700;padding:.45rem .6rem;white-space:nowrap;}
      div[data-testid="stButton"] button:hover {background:#155ba9;color:#fff;border:0;}
      div[data-testid="stRadio"] [role="radiogroup"] {gap:.45rem;}
      div[data-testid="stRadio"] [role="radiogroup"] label {padding:.42rem .58rem;border:1px solid #e1e8f0;border-radius:9px;background:#fff;}
      div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {border-color:#8ebbea;background:#f0f7ff;}
      div[data-testid="stSlider"] [data-testid="stThumbValue"] {color:#1d65b2;font-weight:700;}
      div[data-testid="stSelectbox"] label,div[data-testid="stSlider"] label,div[data-testid="stNumberInput"] label {font-size:.75rem;font-weight:650;color:#30445d;}
      div[data-testid="stCaptionContainer"] {font-size:.69rem;color:#728198;}
      @media(max-width:900px) {.block-container{padding:0 1rem 2rem;} div[data-testid="stMarkdownContainer"] .hero{margin:0 -1rem 1rem;} div[data-testid="stMarkdownContainer"] .nav-links{gap:.7rem;} div[data-testid="stMarkdownContainer"] .hero-art{display:none;}}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="site-nav"><div class="brand"><span class="brand-icon">💻</span><span>SpecFinder India</span></div><div class="nav-links"><span>A simpler way to choose</span><span>How it works</span><span>About</span></div></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero"><div class="hero-kicker">Your next laptop starts here</div><h1 class="hero-title">Find a laptop that fits your life.</h1><p class="hero-copy">Tell us what you need. We’ll help you make sense of the specs.</p><div class="hero-art" aria-hidden="true"><svg viewBox="0 0 150 100" fill="none"><path d="M25 17h91a5 5 0 0 1 5 5v53H20V22a5 5 0 0 1 5-5Z" stroke="#5d8fc2" stroke-width="2.2"/><path d="M29 25h83v43H29z" stroke="#9bb9d8" stroke-width="1.5"/><path d="M10 80h121l-10 10H20L10 80Z" stroke="#5d8fc2" stroke-width="2.2" stroke-linejoin="round"/><path d="M61 83h20" stroke="#5d8fc2" stroke-width="2" stroke-linecap="round"/><path d="m126 20 8-8m1 17 11-2m-21-15 1-9" stroke="#5d8fc2" stroke-width="2" stroke-linecap="round"/></svg></div></div>',
    unsafe_allow_html=True,
)


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path)
    data["data_source"] = "Laptop specifications dataset"
    data["image_url"] = ""
    supplemental_path = path.parent.parent / "raw" / "smartprix_laptop.csv"
    if supplemental_path.exists():
        smartprix = normalize_smartprix(pd.read_csv(supplemental_path))
        data = pd.concat([data, smartprix], ignore_index=True, sort=False)
    for column in ["price", "rating", "ram_gb", "storage_gb", "gpu_vram_gb", "display_size_inch"]:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors="coerce")
    return data


def normalize_smartprix(source: pd.DataFrame) -> pd.DataFrame:
    """Map Smartprix listing columns into the app's common laptop schema."""
    rows = pd.DataFrame(index=source.index)
    names = source["name"].fillna("").astype(str).str.replace("\u200e", "", regex=False).str.strip()
    lower_names = names.str.casefold()
    processor = source["processor"].fillna("").astype(str).str.replace("\u200e", "", regex=False).str.strip()
    processor_lower = processor.str.casefold()
    gpu = source["graphics_card"].fillna("").astype(str).str.replace("\u200e", "", regex=False).str.strip()
    gpu_lower = gpu.str.casefold()

    rows["brand"] = names.str.extract(r"^\s*([A-Za-z]+)", expand=False).fillna("Unknown").str.casefold()
    rows["model"] = names
    rows["price"] = pd.to_numeric(source["price"], errors="coerce")

    rows["cpu_brand"] = "Other"
    for token, label in [("intel", "Intel"), ("amd", "AMD"), ("apple", "Apple"), ("snapdragon", "Qualcomm"), ("kirin", "Huawei"), ("mediatek", "MediaTek")]:
        rows.loc[processor_lower.str.contains(token, na=False), "cpu_brand"] = label
    cpu_pattern = r"(Core\s+Ultra\s+[3579]|Core\s+i[3579]|Ryzen\s+[3579]|Apple\s+M\d+(?:\s+(?:Pro|Max|Ultra))?|M\d+(?:\s+(?:Pro|Max|Ultra))?|Snapdragon\s+X(?:\s+(?:Plus|Elite))?)"
    rows["cpu_series"] = processor.str.extract(cpu_pattern, flags=re.IGNORECASE, expand=False).fillna("").str.replace(r"\s+", " ", regex=True).str.strip()
    rows["cpu_family"] = rows["cpu_series"].str.extract(r"^(Core\s+Ultra|Core|Ryzen|Apple|Snapdragon)", flags=re.IGNORECASE, expand=False).fillna("")
    rows["cpu_model"] = processor
    rows["cpu_suffix"] = processor.str.extract(r"([A-Z]{1,3})\s*$", expand=False).fillna("")
    rows["cpu_core_count"] = pd.to_numeric(source["cores"].astype(str).str.extract(r"(\d+)", expand=False), errors="coerce")
    rows["cpu_thread_count"] = pd.to_numeric(source["threads"].astype(str).str.extract(r"(\d+)", expand=False), errors="coerce")
    rows["cpu_p_cores"] = pd.to_numeric(source["cores"].astype(str).str.extract(r"(\d+)\s*P", flags=re.IGNORECASE, expand=False), errors="coerce")
    rows["cpu_e_cores"] = pd.to_numeric(source["cores"].astype(str).str.extract(r"(\d+)\s*E", flags=re.IGNORECASE, expand=False), errors="coerce")
    rows["cpu_lp_e_cores"] = pd.NA

    rows["ram_gb"] = pd.to_numeric(source["ram"].astype(str).str.extract(r"(\d+(?:\.\d+)?)", expand=False), errors="coerce")
    def storage_gb(value: str) -> float:
        amounts = re.findall(r"(\d+(?:\.\d+)?)\s*(TB|GB)", value.upper())
        return sum(float(amount) * (1024 if unit == "TB" else 1) for amount, unit in amounts)
    rows["storage_gb"] = source["storage"].fillna("").astype(str).map(storage_gb)

    screen = source["screen_size.1"].fillna("").astype(str)
    rows["display_size_inch"] = pd.to_numeric(screen.str.extract(r"([\d.]+)", expand=False), errors="coerce")
    resolution = source["screen_pixels"].fillna("").astype(str).str.extract(r"(\d+)\s*x\s*(\d+)", flags=re.IGNORECASE)
    rows["display_width_px"] = pd.to_numeric(resolution[0], errors="coerce")
    rows["display_height_px"] = pd.to_numeric(resolution[1], errors="coerce")

    rows["gpu_brand"] = "Other"
    for token, label in [("nvidia", "NVIDIA"), ("geforce", "NVIDIA"), ("amd", "AMD"), ("radeon", "AMD"), ("intel", "Intel"), ("apple", "Apple"), ("qualcomm", "Qualcomm")]:
        rows.loc[gpu_lower.str.contains(token, na=False), "gpu_brand"] = label
    rows["gpu_model"] = gpu
    rows["gpu_series"] = gpu.str.extract(r"(GeForce\s+(?:RTX|GTX)|Radeon\s+(?:RX|Graphics)|Apple\s+\d+[- ]Core\s+GPU|Iris\s+Xe|Arc)", flags=re.IGNORECASE, expand=False).fillna("")
    rows["gpu_vram_gb"] = pd.to_numeric(gpu.str.extract(r"(\d+(?:\.\d+)?)\s*GB", flags=re.IGNORECASE, expand=False), errors="coerce")
    discrete = gpu_lower.str.contains(r"nvidia|geforce\s+(?:rtx|gtx)|radeon\s+rx", regex=True, na=False)
    rows["gpu_type"] = "Integrated"
    rows.loc[discrete, "gpu_type"] = "Dedicated"
    rows["device_category"] = "General"
    gaming = lower_names.str.contains("gaming", na=False) | gpu_lower.str.contains(r"geforce\s+(?:rtx|gtx)|radeon\s+rx", regex=True, na=False)
    rows.loc[gaming, "device_category"] = "Gaming"
    rows.loc[lower_names.str.contains(r"thinkpad|latitude|probook|elitebook|precision|thinkbook", regex=True, na=False), "device_category"] = "Business"
    rows.loc[lower_names.str.contains(r"macbook|vivobook|ideapad|zenbook|swift|air", regex=True, na=False) & ~gaming, "device_category"] = "Thin & Light"
    rows["os_name"] = source["os"].fillna("").astype(str).str.replace(r"\s+OS$", "", regex=True).str.strip()
    rows["warranty_years"] = pd.to_numeric(source["warranty"].astype(str).str.extract(r"(\d+)", expand=False), errors="coerce")
    rows["rating"] = pd.to_numeric(source["score"], errors="coerce")
    rows["source_rating"] = pd.to_numeric(source["rating"], errors="coerce")
    rows["image_url"] = source["img"].fillna("").astype(str)
    rows["data_source"] = "Smartprix"
    return rows


def processor_tier(series: object) -> int:
    """Map common CPU families to a broad, beginner-friendly tier."""
    name = str(series).casefold().replace(" ", "")
    if any(token in name for token in ("i9", "ryzen9", "ultra9", "ai9")):
        return 4
    if any(token in name for token in ("i7", "ryzen7", "ultra7", "core7", "ai7")):
        return 3
    if any(token in name for token in ("i5", "ryzen5", "ultra5", "core5", "ai5")):
        return 2
    return 1


def safe_text(value: object, fallback: str = "Not listed") -> str:
    if pd.isna(value) or not str(value).strip():
        return fallback
    return str(value)


def image_for_laptop(row: pd.Series) -> Path | None:
    """Look for a user-provided product image matching the laptop model slug."""
    model = safe_text(row.get("model"), "laptop")
    slug = re.sub(r"[^a-z0-9]+", "-", model.casefold()).strip("-")
    for extension in (".webp", ".jpg", ".jpeg", ".png"):
        image_path = IMAGE_DIR / f"{slug}{extension}"
        if image_path.is_file():
            return image_path
    return None


def image_markup(row: pd.Series) -> str:
    image_path = image_for_laptop(row)
    if image_path:
        encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
        mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}[image_path.suffix.lower()]
        return f'<img class="product-image" src="data:{mime};base64,{encoded}" alt="{escape(safe_text(row.get("model"), "Laptop photo"))}">'
    image_url = safe_text(row.get("image_url"), "")
    if image_url.startswith("https://"):
        return f'<img class="product-image" src="{escape(image_url, quote=True)}" alt="{escape(safe_text(row.get("model"), "Laptop photo"))}">'
    return """
    <div class="photo-placeholder" aria-label="Laptop photo can be added here">
      <svg viewBox="0 0 120 82" role="img" aria-hidden="true">
        <rect x="22" y="10" width="76" height="51" rx="4" fill="#dce9f7" stroke="#83a8d1" stroke-width="2"/>
        <rect x="28" y="16" width="64" height="39" rx="2" fill="#f8fbff"/>
        <path d="M12 65h96l-7 8H19z" fill="#aac3df" stroke="#83a8d1" stroke-width="2" stroke-linejoin="round"/>
        <path d="M49 67h22" stroke="#7196bf" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </div>
    """


if not DATA_PATH.exists():
    st.error(f"Dataset not found at {DATA_PATH}. Put laptops_cleaned.csv in data/processed/ and restart the app.")
    st.stop()

df = load_data(DATA_PATH)
if df.empty:
    st.error("The laptop dataset is empty. Check data/processed/laptops_cleaned.csv.")
    st.stop()

left, right = st.columns([0.82, 1.55], gap="medium", vertical_alignment="top")

with left:
    with st.container(border=True):
        st.markdown('<div class="page-section-title">Let’s find your laptop</div>', unsafe_allow_html=True)
        st.markdown('<div class="muted">What will you mainly use it for?</div>', unsafe_allow_html=True)
        profile = st.radio(
            "Main use",
            ["🎮 Gaming for college", "🎓 Study & everyday", "⚙️ I know my specs"],
            horizontal=True,
            label_visibility="collapsed",
            key="shopping_profile",
        )
        is_gaming = profile.startswith("🎮")
        profile_key = "gaming" if is_gaming else ("study" if profile.startswith("🎓") else "custom")

        price_values = df["price"].dropna()
        data_min_price = int(price_values.min()) if not price_values.empty else 20_000
        data_max_price = int(price_values.max()) if not price_values.empty else 300_000
        budget_min = max(0, (data_min_price // 5_000) * 5_000)
        budget_max = max(300_000, ((data_max_price + 4_999) // 5_000) * 5_000)
        default_budget = min(max(100_000 if is_gaming else 80_000, budget_min), budget_max)
        for key in ("budget_slider", "budget_amount"):
            if key not in st.session_state or not budget_min <= st.session_state[key] <= budget_max:
                st.session_state[key] = default_budget

        def sync_budget_from_slider() -> None:
            st.session_state.budget_amount = st.session_state.budget_slider

        def sync_budget_from_input() -> None:
            st.session_state.budget_slider = st.session_state.budget_amount

        st.markdown('<div class="page-section-title" style="font-size:.79rem;margin:.75rem 0 .15rem">Your budget</div>', unsafe_allow_html=True)
        slider_col, amount_col = st.columns([2.15, 0.9], vertical_alignment="bottom")
        with slider_col:
            budget = st.slider(
                "Budget range",
                min_value=budget_min,
                max_value=budget_max,
                step=5_000,
                key="budget_slider",
                on_change=sync_budget_from_slider,
                label_visibility="collapsed",
            )
            st.caption(f"₹{budget_min:,}  ·  up to ₹{budget_max:,}")
        with amount_col:
            budget = st.number_input(
                "Exact budget (₹)",
                min_value=budget_min,
                max_value=budget_max,
                step=5_000,
                key="budget_amount",
                on_change=sync_budget_from_input,
                label_visibility="collapsed",
            )

        gpu_options = [
            "Mid-range (e.g. RTX 4050)",
            "Entry gaming (e.g. RTX 3050)",
            "Higher-end gaming (RTX 4060+)",
            "Dedicated graphics",
            "Built-in graphics",
            "Any graphics",
        ]
        # Entry gaming includes RTX 3050, which is common in this price range.
        gpu_default = 1 if is_gaming else 5
        gpu_preference = st.selectbox("Graphics power (GPU)", gpu_options, index=gpu_default, key=f"main_gpu_{profile_key}")
        st.caption("Good for gaming and creative work.")

        cpu_options = ["Intel Core i5 / AMD Ryzen 5", "Intel Core i7 / AMD Ryzen 7", "Any processor"]
        cpu_default = 0 if is_gaming else 2
        cpu_preference = st.selectbox("Processor (CPU)", cpu_options, index=cpu_default, key=f"main_cpu_{profile_key}")
        st.caption("A good balance of performance and battery life.")

        ram_options = ["8 GB", "16 GB", "32 GB", "Any RAM"]
        ram_default = "16 GB" if is_gaming else "8 GB"
        ram_preference = st.selectbox("Memory (RAM)", ram_options, index=ram_options.index(ram_default), key=f"main_ram_{profile_key}")
        st.caption("More memory helps games and apps run together smoothly.")

        if profile.startswith("🎮"):
            callout_text = "These specs are a balanced starting point for gaming and college."
        elif profile.startswith("🎓"):
            callout_text = "These specs are a practical starting point for everyday student use."
        else:
            callout_text = "Your specifications are set. Review the matches and open details to compare."
        st.markdown(
            f'<div class="soft-callout"><span>✓</span><span><strong>Great choice!</strong><br>{callout_text}</span></div>',
            unsafe_allow_html=True,
        )

        with st.expander("Know more · fine-tune your search"):
            brands = sorted(df["brand"].dropna().astype(str).unique()) if "brand" in df else []
            categories = sorted(df["device_category"].dropna().astype(str).unique()) if "device_category" in df else []
            gpu_models = sorted(df["gpu_model"].dropna().astype(str).unique()) if "gpu_model" in df else []
            cpu_series = sorted(df["cpu_series"].dropna().astype(str).unique()) if "cpu_series" in df else []
            brand = st.selectbox("Brand", ["Any brand"] + brands, key="advanced_brand")
            exact_gpu = st.selectbox("Exact GPU model", ["Any GPU"] + gpu_models, key="advanced_gpu")
            exact_cpu = st.selectbox("Processor family", ["Any processor family"] + cpu_series, key="advanced_cpu")
            min_storage = st.selectbox(
                "Minimum storage",
                [0, 256, 512, 1024, 2048],
                format_func=lambda value: "Any storage" if value == 0 else (f"{value // 1024} TB" if value >= 1024 else f"{value} GB"),
                key="advanced_storage",
            )
            screen_sizes = sorted(df["display_size_inch"].dropna().unique()) if "display_size_inch" in df else []
            min_screen = st.selectbox(
                "Minimum screen size", [0] + screen_sizes,
                format_func=lambda value: "Any size" if value == 0 else f"{value:g} inches",
                key="advanced_screen",
            )
            model_query = st.text_input("Model name contains", placeholder="e.g. Legion, Victus", key="advanced_query")
            category_default = categories.index("Gaming") + 1 if is_gaming and "Gaming" in categories else 0
            category = st.selectbox("Laptop category", ["Any category"] + categories, index=category_default, key=f"advanced_category_{profile_key}")
            sort_by = st.selectbox("Sort by", ["Recommended", "Lowest price", "Highest RAM", "Largest storage", "Highest dataset rating"], key="advanced_sort")

results = df.copy()
if profile.startswith("🎮"):
    results = results[results["device_category"].astype(str).str.casefold() == "gaming"]
elif profile.startswith("🎓"):
    results = results[results["device_category"].astype(str).str.casefold() != "gaming"]
results = results[results["price"].notna() & (results["price"] <= budget)]

gpu_names = results.get("gpu_model", pd.Series(index=results.index, dtype=str)).fillna("").astype(str).str.casefold()
gpu_type = results.get("gpu_type", pd.Series(index=results.index, dtype=str)).fillna("").astype(str).str.casefold()
if gpu_preference.startswith("Mid-range"):
    results = results[gpu_names.str.contains(r"rtx\s?(?:4050|4060|5050|5060)", regex=True)]
elif gpu_preference.startswith("Entry gaming"):
    results = results[gpu_names.str.contains(r"rtx\s?(?:2050|3050)|rx\s?6500m", regex=True)]
elif gpu_preference.startswith("Higher-end"):
    results = results[gpu_names.str.contains(r"rtx\s?(?:4070|4080|4090|5070|5080|5090)", regex=True)]
elif gpu_preference == "Dedicated graphics":
    results = results[gpu_type == "dedicated"]
elif gpu_preference == "Built-in graphics":
    results = results[gpu_type == "integrated"]

if cpu_preference != "Any processor" and "cpu_series" in results:
    required_tier = 3 if "Core i7" in cpu_preference else 2
    results = results[results["cpu_series"].map(processor_tier) >= required_tier]
if ram_preference != "Any RAM" and "ram_gb" in results:
    results = results[results["ram_gb"] >= int(ram_preference.split()[0])]

if brand != "Any brand":
    results = results[results["brand"].astype(str) == brand]
if exact_gpu != "Any GPU":
    results = results[results["gpu_model"].astype(str) == exact_gpu]
if exact_cpu != "Any processor family":
    results = results[results["cpu_series"].astype(str) == exact_cpu]
if min_storage:
    results = results[results["storage_gb"] >= min_storage]
if min_screen:
    results = results[results["display_size_inch"] >= min_screen]
if model_query.strip():
    results = results[results["model"].astype(str).str.contains(model_query.strip(), case=False, na=False)]
if category != "Any category":
    results = results[results["device_category"].astype(str) == category]

sort_map = {
    "Recommended": ("rating", False),
    "Lowest price": ("price", True),
    "Highest RAM": ("ram_gb", False),
    "Largest storage": ("storage_gb", False),
    "Highest dataset rating": ("rating", False),
}
sort_column, ascending = sort_map[sort_by]
if sort_column in results:
    results = results.sort_values(sort_column, ascending=ascending, na_position="last")

with right:
    with st.container(border=True):
        result_title, result_count = st.columns([1.4, 0.6], vertical_alignment="center")
        with result_title:
            st.markdown('<div class="page-section-title">Good matches for you</div>', unsafe_allow_html=True)
        with result_count:
            st.markdown(f'<div class="match-count" style="text-align:right">{len(results):,} laptops</div>', unsafe_allow_html=True)

        if results.empty:
            st.info("No laptops match every choice. Try raising your budget or selecting “Any graphics” or “Any processor”.")
        else:
            top_results = results.head(3)
            best_price = results["price"].min()
            best_rating = results["rating"].max() if "rating" in results else None

            for row_index, (_, laptop) in enumerate(top_results.iterrows()):
                with st.container(border=True):
                    photo_col, detail_col, price_col = st.columns([0.67, 1.8, 0.85], vertical_alignment="center")
                    with photo_col:
                        image_path = image_for_laptop(laptop)
                        if image_path:
                            st.image(image_path, width="stretch")
                        else:
                            st.markdown(image_markup(laptop), unsafe_allow_html=True)
                    with detail_col:
                        brand_name = safe_text(laptop.get("brand"), "Laptop")
                        model_name = safe_text(laptop.get("model"), "Model unavailable")
                        title = model_name if brand_name.casefold() in model_name.casefold() else f"{brand_name.title()} {model_name}"
                        st.markdown(f'<div class="product-title">{escape(title)}</div>', unsafe_allow_html=True)
                        source_label = safe_text(laptop.get("data_source"), "Dataset")
                        if profile.startswith("🎮"):
                            desc = f"A solid all-rounder for gaming and college · {source_label} listing."
                        elif profile.startswith("🎓"):
                            desc = f"A practical option for study and everyday use · {source_label} listing."
                        else:
                            desc = f"Matches your selected laptop specifications · {source_label} listing."
                        st.markdown(f'<div class="product-desc">{desc}</div>', unsafe_allow_html=True)

                        gpu_value = safe_text(laptop.get("gpu_model"), "Not listed")
                        cpu_value = safe_text(laptop.get("cpu_model"), safe_text(laptop.get("cpu_series"), "Not listed"))
                        ram_value = laptop.get("ram_gb")
                        storage_value = laptop.get("storage_gb")
                        ram_label = f"{ram_value:g} GB" if pd.notna(ram_value) else "Not listed"
                        storage_label = f"{storage_value:g} GB" if pd.notna(storage_value) else "Not listed"
                        gpu_vram = laptop.get("gpu_vram_gb")
                        gpu_label = f"{gpu_value} · {gpu_vram:g} GB" if pd.notna(gpu_vram) else gpu_value
                        st.markdown(
                            f'<div class="spec-grid"><span class="spec-pill"><span class="spec-icon">▧</span>{escape(gpu_label)}</span><span class="spec-pill"><span class="spec-icon">◉</span>{escape(cpu_value)}</span><span class="spec-pill"><span class="spec-icon">▤</span>{ram_label} RAM</span><span class="spec-pill"><span class="spec-icon">▣</span>{storage_label} SSD</span></div>',
                            unsafe_allow_html=True,
                        )
                    with price_col:
                        listed_price = laptop.get("price")
                        price_text = f"₹{listed_price:,.0f}" if pd.notna(listed_price) else "Price unavailable"
                        rating_value = laptop.get("rating")
                        if pd.notna(best_price) and listed_price == best_price:
                            badge_text = "Best value"
                        elif pd.notna(best_rating) and pd.notna(rating_value) and rating_value == best_rating:
                            badge_text = "Top rated"
                        else:
                            badge_text = "Good match"
                        st.markdown(f'<div class="badge">✦ {badge_text}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="price" style="margin-top:.38rem">{price_text}</div><div class="price-note">Dataset listed price</div>', unsafe_allow_html=True)
                        model_key = re.sub(r"[^a-z0-9]+", "-", safe_text(laptop.get("model"), str(row_index)).casefold()).strip("-")
                        details_key = f"show_details_{model_key}_{row_index}"
                        if st.button("View details →", key=details_key, width="stretch"):
                            st.session_state["selected_laptop_details"] = (
                                None if st.session_state.get("selected_laptop_details") == details_key else details_key
                            )

                    if st.session_state.get("selected_laptop_details") == details_key:
                        details = [
                            f"**Processor:** {safe_text(laptop.get('cpu_model'), safe_text(laptop.get('cpu_series')))}",
                            f"**Graphics:** {safe_text(laptop.get('gpu_model'))}",
                            f"**Memory:** {ram_label}",
                            f"**Storage:** {storage_label}",
                            f"**Screen:** {safe_text(laptop.get('display_size_inch'))} inches",
                            f"**Rating in dataset:** {safe_text(laptop.get('rating'))}/100",
                        ]
                        st.markdown("  ·  ".join(details))

            st.markdown(
                '<div class="why-box"><div class="why-icon">✦</div><div><div class="why-title">Why these laptops?</div><div class="why-copy">They match your budget and the graphics, processor, and memory choices you selected. Prices come from the dataset and may not match today’s store prices.</div></div></div>',
                unsafe_allow_html=True,
            )
            with st.expander("Compare all matching laptops"):
                columns = ["brand", "model", "price", "cpu_series", "cpu_model", "gpu_model", "gpu_vram_gb", "ram_gb", "storage_gb", "display_size_inch", "rating"]
                columns = [column for column in columns if column in results.columns]
                labels = {
                    "brand": "Brand", "model": "Model", "price": "Price (₹)", "cpu_series": "Processor family",
                    "cpu_model": "Processor model", "gpu_model": "Graphics model", "gpu_vram_gb": "GPU memory (GB)",
                    "ram_gb": "RAM (GB)", "storage_gb": "Storage (GB)", "display_size_inch": "Screen (inches)",
                    "rating": "Dataset rating (0–100)",
                }
                st.dataframe(results[columns].rename(columns=labels), width="stretch", hide_index=True)
                st.bar_chart(results.head(15).set_index("model")["price"], y_label="Listed price (₹)")

        st.markdown('<div class="muted" style="margin-top:.75rem">Prices are dataset listings, not live offers. Retailer links and live availability are not included in this dataset.</div>', unsafe_allow_html=True)

with st.expander("About this dataset"):
    st.write(
        f"This prototype combines {len(df):,} laptop listings from two India-focused datasets. "
        "The original specifications dataset reports 992 listings; the supplemental Smartprix CSV adds 947 listings with image URLs, prices and ratings. "
        "These are dataset prices rather than live offers; retailer names and product-page URLs are not included."
    )
    st.markdown(f"Dataset source: [{DATASET_URL}]({DATASET_URL})")
    st.markdown(f"Supplemental dataset: [{SMARTPRIX_URL}]({SMARTPRIX_URL})")
