import re
import streamlit as st

# ----------------- CONFIG -----------------
MAX_FREE_LINES = 3  # number of free references allowed

APP_NAME = "KleenRef"
TAGLINE = "Smart reference cleaner for busy scholars"

PAYMENT_LINK = "https://paystack.shop/pay/lbynycw38e"  # Your Paystack Link


# ----------------- CORE CLEANING LOGIC -----------------

def clean_reference(ref: str) -> str:
    ref = ref.strip()
    if not ref:
        return ""

    ref = re.sub(r'\s+', ' ', ref)  # collapse multiple spaces
    ref = re.sub(r'\s+([,.;:!?])', r'\1', ref)  # remove spaces before punctuation
    ref = re.sub(r'([,.;:!?])(?=\w)', r'\1 ', ref)  # ensure space after punctuation
    ref = re.sub(r'\s+\)', ')', ref)  # fix spaces before )
    
    if not re.search(r'[.?!]$', ref):
        ref += '.'
    return ref


def clean_reference_block(text: str) -> str:
    lines = text.splitlines()
    cleaned = [clean_reference(line) for line in lines if line.strip()]
    return "\n".join(cleaned)


# ----------------- STREAMLIT APP UI -----------------

st.set_page_config(page_title=f"{APP_NAME} – Reference Cleaner", layout="wide")

st.title(f"🧼 {APP_NAME}")
st.caption(TAGLINE)

st.markdown(
    """
KleenRef helps you quickly tidy messy reference lists:

- fix extra spaces  
- tidy punctuation  
- make references neat and consistent  

### **Free plan:** Clean up to **3 references** at a time.  
For longer lists, upgrade to **KleenRef Pro** to unlock unlimited cleaning.
"""
)

example = """Chugh, R.,  &  Ruhi, U.  (2019)  .  Social media in higher education , a literature review 
Portman, M.E ,Smith, J. &   Jones, K.2025  .  Impact of science communication on youth .London: Sage"""

st.subheader("Step 1: Paste your references")
input_text = st.text_area(
    "Paste your references here (one per line):",
    value=example,
    height=200,
)

if st.button("✨ Clean References"):
    if not input_text.strip():
        st.warning("Please paste at least one reference.")
    else:
        lines = [line for line in input_text.splitlines() if line.strip()]
        num_refs = len(lines)

        # --- Soft Paywall ---
        if num_refs > MAX_FREE_LINES:
            st.error(
                f"You entered **{num_refs} references**, "
                f"but the free version cleans up to **{MAX_FREE_LINES} references**."
            )
            st.markdown(
                """
To clean longer reference lists, please upgrade to **KleenRef Pro**  
(perfect for theses, dissertations, and journal papers).
"""
            )
            st.link_button("💳 Upgrade to KleenRef Pro", PAYMENT_LINK)
            st.stop()

        cleaned = clean_reference_block(input_text)

        st.subheader("Step 2: Copy your cleaned references")
        st.success("Done! Copy your cleaned references below.")
        st.text_area("Cleaned references", value=cleaned, height=200)
