import re
import streamlit as st

# ----------------- CONFIG -----------------
MAX_FREE_LINES = 10  # free references allowed (recommend 10 for better UX)

APP_NAME = "KleenRef"
TAGLINE = "Clean your academic references in one calm click"

PAYMENT_LINK = "https://paystack.shop/pay/lbynycw38e"

# Simple manual premium codes (you can change anytime)
PREMIUM_CODES = {"KLEENREFPRO", "MIRA2026", "SALPREMIUM"}


# ----------------- STYLING -----------------
st.set_page_config(page_title=f"{APP_NAME} – Reference Cleaner", layout="wide")

st.markdown(
    """
<style>
/* Page background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #f7fbf8 0%, #ffffff 55%);
}

/* Main container feel */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Title styling */
.kleenref-title {
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 0.25rem;
}

.kleenref-subtitle {
    color: rgba(0,0,0,0.65);
    font-size: 1.05rem;
    margin-top: 0;
}

/* Card sections */
.kleen-card {
    background: white;
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 18px;
    padding: 18px 18px 6px 18px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.04);
    margin-bottom: 18px;
}

/* Subtle helper text */
.kleen-muted {
    color: rgba(0,0,0,0.60);
    font-size: 0.95rem;
}

/* Make buttons slightly nicer */
.stButton button, .stDownloadButton button {
    border-radius: 12px !important;
    padding: 0.65rem 1rem !important;
    font-weight: 700 !important;
}

/* Sidebar spacing */
section[data-testid="stSidebar"] .block-container {
    padding-top: 1.2rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# ----------------- CORE CLEANING LOGIC -----------------
def clean_reference(ref: str) -> str:
    ref = ref.strip()
    if not ref:
        return ""

    # collapse multiple whitespace
    ref = re.sub(r"\s+", " ", ref)

    # remove spaces before punctuation
    ref = re.sub(r"\s+([,.;:!?])", r"\1", ref)

    # ensure a space after punctuation when followed by a word/number
    ref = re.sub(r"([,.;:!?])(?=\w)", r"\1 ", ref)

    # fix spaces before closing parentheses
    ref = re.sub(r"\s+\)", ")", ref)

    # collapse repeated punctuation like ",,", "..", ";;"
    ref = re.sub(r"([,.;:!?])\1+", r"\1", ref)

    # add final period if missing
    if not re.search(r"[.?!]$", ref):
        ref += "."

    return ref


def clean_reference_block(text: str, numbered: bool = False) -> str:
    lines = [line for line in text.splitlines() if line.strip()]
    cleaned_lines = [clean_reference(line) for line in lines]

    if numbered:
        cleaned_lines = [f"{i+1}. {line}" for i, line in enumerate(cleaned_lines)]

    return "\n".join(cleaned_lines)


# ----------------- SESSION STATE -----------------
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False

# ----------------- HEADER -----------------
st.markdown(f'<div class="kleenref-title">🧼 {APP_NAME}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="kleenref-subtitle">{TAGLINE}</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="kleen-muted">Note: If this app seems “asleep”, give it a few seconds — it may be waking up.</div>',
    unsafe_allow_html=True
)

# ----------------- SIDEBAR (PREMIUM) -----------------
with st.sidebar:
    st.markdown("### Go Premium (one-time)")
    st.markdown(
        "Unlimited cleaning • Download export • No subscription",
    )

    st.link_button("💳 Upgrade via Paystack", PAYMENT_LINK)

    st.markdown("---")
    code = st.text_input("Enter Premium Access Code", type="password", placeholder="e.g., KLEENREFPRO")
    if code:
        if code.strip().upper() in PREMIUM_CODES:
            st.session_state.is_premium = True
            st.success("Premium unlocked ✅")
        else:
            st.warning("Code not recognized.")

    if st.session_state.is_premium:
        st.info("You are using Premium mode.")

# ----------------- MAIN UI (TWO COLUMNS) -----------------
example = """Chugh, R.,  &  Ruhi, U.  (2019)  .  Social media in higher education , a literature review
Portman, M.E ,Smith, J. &   Jones, K.2025  .  Impact of science communication on youth .London: Sage"""

st.markdown("#### Reference style context")

style = st.selectbox(
    "Select the referencing style you are working with:",
    ["APA (recommended)", "MLA", "Chicago", "Harvard", "Other"],
    index=0
)

st.caption(
    "KleenRef currently cleans references for readability and consistency. "
    "It does not fully reformat citation styles yet."
)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="kleen-card">', unsafe_allow_html=True)
    st.subheader("Paste references")
    st.caption("One reference per line. KleenRef fixes spacing, punctuation, and messy line breaks.")
    input_text = st.text_area("Input", value=example, height=260, label_visibility="collapsed")
    numbered = st.checkbox("Number output (1., 2., 3…)", value=False)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="kleen-card">', unsafe_allow_html=True)
    st.subheader("Cleaned output")
    st.caption("Copy the cleaned list or download it as a .txt file.")
    output_placeholder = st.empty()
    download_placeholder = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- ACTION -----------------
if st.button("✨ Clean References", use_container_width=True):
    if not input_text.strip():
        st.warning("Please paste at least one reference.")
    else:
        lines = [line for line in input_text.splitlines() if line.strip()]
        num_refs = len(lines)

        # Paywall logic
        if (not st.session_state.is_premium) and (num_refs > MAX_FREE_LINES):
            st.error(
                f"You entered **{num_refs} references**, but the free version cleans up to **{MAX_FREE_LINES}**."
            )
            st.markdown("Upgrade to unlock unlimited cleaning and downloads.")
        else:
            with st.spinner("Cleaning your references…"):
                cleaned = clean_reference_block(input_text, numbered=numbered)

            output_placeholder.text_area("Output", value=cleaned, height=260, label_visibility="collapsed")
            download_placeholder.download_button(
                label="⬇️ Download .txt",
                data=cleaned.encode("utf-8"),
                file_name="kleenref_cleaned_references.txt",
                mime="text/plain",
                use_container_width=True,
            )

st.markdown(
    '<div class="kleen-muted" style="text-align:center; margin-top: 8px;">Made for students & researchers • KleenRef</div>',
    unsafe_allow_html=True
)

