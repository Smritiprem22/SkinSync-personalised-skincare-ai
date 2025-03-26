import streamlit as st
import pandas as pd
import os
import re

st.set_page_config(page_title="SkinSync - Skincare Routine Generator", layout="wide")

st.title("💖 SkinSync – Personalized Skincare Assistant")
st.markdown("Use the tabs below to generate routines, check comedogenic ingredients, and explore ingredient info!")

# Load comedogenic ingredient database
if os.path.exists("data/comedogenic_ingredients_detailed.csv"):
    comedogenic_df = pd.read_csv("data/comedogenic_ingredients_detailed.csv")
    comedogenic_list = comedogenic_df["Ingredient"].str.lower().tolist()
else:
    st.warning("Comedogenic ingredient database not found!")
    comedogenic_df = pd.DataFrame()
    comedogenic_list = []

# --- TABS LAYOUT ---
tab1, tab2, tab3 = st.tabs(["🧴 Routine Generator", "⚠️ Comedogenic Checker", "💬 Ingredient Chatbot"])

# ---------------------------- TAB 1 ----------------------------
with tab1:
    st.header("🧴 Personalized Skincare Routine Generator")

    skin_type = st.selectbox("What is your skin type?", ["Dry","Oily","Combination","Sensitive","Normal"])
    concerns = st.multiselect("What are your main skin concerns?", ["Acne","Pigmentation","Redness","Dehydration","Aging","Texture"])
    current_routine = st.multiselect("What are the steps in your current routine?", ["Cleanser/Face-wash","Moisturizer","SPF/Sunscreen","Toner","Exfoliator","Serums","Mask"])
    allergies = st.multiselect("Any allergies or ingredient sensitivities?", ["Fragrance","Essential Oils","Parabens","Alcohol","None"])
    current_products = st.text_area("Which products do you currently use? (mention with brand name)",
                                     placeholder="Example: Cetaphil Cleanser, The Ordinary Niacinamide Serum")

    if st.button("✨ Generate My Routine"):
        st.subheader("🌞 Your Personalized Skincare Routine")

        am_routine = []
        pm_routine = []

        # Placeholder logic
        if "Cleanser" not in ",".join(current_routine):
            am_routine.append("🧼 Gentle Cleanser (e.g. Cetaphil, CeraVe)")
            pm_routine.append("🧼 Gentle Cleanser")

        if "Acne" in concerns:
            am_routine.append("💧 Niacinamide Serum")
            pm_routine.append("🧪 Salicylic Acid Serum")

        if "Pigmentation" in concerns:
            am_routine.append("✨ Vitamin C Serum")
            pm_routine.append("🧴 Azelaic Acid 10%")

        if "Dehydration" in concerns:
            am_routine.append("💦 Hyaluronic Acid Serum")
            pm_routine.append("💦 Hyaluronic Acid Serum")

        if "Moisturizer" not in ",".join(current_routine):
            am_routine.append("🧴 Light Moisturizer (non-comedogenic)")
            pm_routine.append("🧴 Barrier-repair Moisturizer")

        if "SPF" not in ",".join(current_routine):
            am_routine.append("🧿 Broad Spectrum SPF 50 Sunscreen")

        if "Fragrance" in allergies:
            am_routine = [step + " (Fragrance-Free)" for step in am_routine]
            pm_routine = [step + " (Fragrance-Free)" for step in pm_routine]
        if "Essential Oils" in allergies:
            am_routine = [step + " (No Essential Oils)" for step in am_routine]
            pm_routine = [step + " (No Essential Oils)" for step in pm_routine]

        st.markdown("#### 🌅 Morning Routine (AM)")
        for step in am_routine:
            st.markdown(f"- {step}")

        st.markdown("#### 🌙 Night Routine (PM)")
        for step in pm_routine:
            st.markdown(f"- {step}")

# ---------------------------- TAB 2 ----------------------------
with tab2:
    st.header("⚠️ Comedogenic Ingredient Checker")

    product_name = st.text_input("Enter product name (optional, not yet connected to web scraping):")
    manual_ingredients = st.text_area("Paste the product's ingredient list (comma-separated)",
                                     placeholder="Water, Niacinamide, Zinc PCA, Dimethicone, ...")

    if st.button("🧪 Check Ingredients"):
        if manual_ingredients:
            st.subheader("🔍 Comedogenic Ingredient Analysis")
            user_ingredients = [i.strip().lower() for i in manual_ingredients.split(",")]

            warnings_found = []
            for ingredient in user_ingredients:
                if ingredient in comedogenic_list:
                    row = comedogenic_df[comedogenic_df["Ingredient"].str.lower() == ingredient]
                    acne = row["Acne Rating"].values[0]
                    irritant = row["Irritant Rating"].values[0] if not pd.isna(row["Irritant Rating"].values[0]) else "N/A"
                    safety = row["Safety Rating"].values[0] if not pd.isna(row["Safety Rating"].values[0]) else "N/A"
                    warnings_found.append((ingredient.title(), acne, irritant, safety))

            if warnings_found:
                for ing, acne, irritant, safety in warnings_found:
                    st.markdown(f"- **{ing}** → Acne: `{acne}`, Irritant: `{irritant}`, Safety: `{safety}`")
            else:
                st.success("✅ No comedogenic ingredients found in the provided list.")
        else:
            st.warning("Please paste the ingredient list to proceed.")

# ---------------------------- TAB 3 ----------------------------
with tab3:
    st.header("💬 Ingredient Chatbot (Coming Soon)")
    st.markdown("Ask questions like 'What does azelaic acid do?', or 'Is niacinamide safe for sensitive skin?' ✨")
    st.info("This feature will use GenAI to explain ingredients based on your concerns.")
