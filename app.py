import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Smart Mess Manager", page_icon="🏢", layout="wide")

st.title("🏢 Smart Mess Management System")
st.write("মেসের যাবতীয় হিসাব-নিকাশ, মিল ট্র্যাকিং, বাজার খরচ ও ফিক্সড বিল ব্যবস্থাপনা")

# Initialize Session State
if 'members' not in st.session_state:
    st.session_state.members = ["Shabuj", "Suborno", "Dihan", "Rigan", "Sihan", "Tanvir", "Sinan", "Monir", "Miskat"]
if 'deposits' not in st.session_state:
    st.session_state.deposits = {
        "Shabuj": 2079.0, "Suborno": 2717.0, "Dihan": 1315.0, 
        "Rigan": 2594.0, "Sihan": 2744.0, "Tanvir": 5293.0, 
        "Sinan": 580.0, "Monir": 2490.0, "Miskat": 2050.0
    }
if 'meals' not in st.session_state:
    st.session_state.meals = {
        "Shabuj": 51.0, "Suborno": 50.0, "Dihan": 18.0, 
        "Rigan": 56.0, "Sihan": 31.0, "Tanvir": 47.0, 
        "Sinan": 50.0, "Monir": 39.0, "Miskat": 50.0
    }
if 'markets' not in st.session_state:
    st.session_state.markets = []

# Sidebar - Member Management
st.sidebar.header("⚙️ মেস কন্ট্রোল প্যানেল")
new_member = st.sidebar.text_input("নতুন সদস্যের নাম:")
if st.sidebar.button("সদস্য যুক্ত করুন"):
    if new_member and new_member not in st.session_state.members:
        st.session_state.members.append(new_member)
        st.session_state.deposits[new_member] = 0.0
        st.session_state.meals[new_member] = 0.0
        st.sidebar.success(f"{new_member} সফলভাবে যুক্ত হয়েছেন!")

# Tabs Layout
tab1, tab2, tab3, tab4 = st.tabs(["📊 চূড়ান্ত হিসাব (Summary)", "🍲 মিল ইনপুট (Meals)", "🛒 বাজার খরচ (Market)", "💡 ফিক্সড বিল (Utility)"])

# Utility Bills Section
with tab4:
    st.header("💡 মাসের ফিক্সড / শেয়ার্ড উপযোগ বিল")
    col1, col2 = st.columns(2)
    with col1:
        e_bill = st.number_input("বিদ্যুৎ বিল (Electricity Bill):", value=2000.0, step=100.0)
        g_bill = st.number_input("গ্যাস বিল (Gas Bill):", value=1000.0, step=100.0)
        i_bill = st.number_input("ইন্টারনেট বিল (Internet Bill):", value=1000.0, step=100.0)
    with col2:
        cook_bill = st.number_input("বাবুর্চি/বুয়ার বিল (Cook Bill):", value=2500.0, step=100.0)
        other_bill = st.number_input("অন্যান্য ফিক্সড খরচ (Others):", value=0.0, step=50.0)
    
    total_fixed_bill = e_bill + g_bill + i_bill + cook_bill + other_bill
    num_members = len(st.session_state.members)
    per_person_fixed = total_fixed_bill / num_members if num_members > 0 else 0
    
    st.info(f"💰 **মোট ফিক্সড বিল:** {total_fixed_bill:,.2f} টাকা  |  **জনপ্রতি ফিক্সড বিল ({num_members} জন):** {per_person_fixed:,.2f} টাকা")

# Meal & Deposit Section
with tab2:
    st.header("🍲 সদস্যভিত্তিক মোট মিল ও জমা টাকা ইনপুট")
    for m in st.session_state.members:
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"### **{m}**")
        st.session_state.deposits[m] = c2.number_input(f"{m}-এর জমা (Tk)", value=float(st.session_state.deposits[m]), key=f"dep_{m}")
        st.session_state.meals[m] = c3.number_input(f"{m}-এর মোট মিল", value=float(st.session_state.meals[m]), key=f"meal_{m}")

# Market Register Section
with tab3:
    st.header("🛒 বাজার খরচের বিবরণী এন্ট্রি")
    with st.form("market_form"):
        m_person = st.selectbox("বাজারকারী সদস্য:", st.session_state.members)
        m_amount = st.number_input("বাজার খরচের পরিমাণ (Tk):", min_value=0.0, step=50.0)
        m_date = st.date_input("তারিখ:")
        submit = st.form_submit_button("বাজার এন্ট্রি যোগ করুন")
        if submit and m_amount > 0:
            st.session_state.markets.append({"Date": str(m_date), "Member": m_person, "Amount": m_amount})
            st.success("বাজার খরচ সফলভাবে নথিভুক্ত হয়েছে!")

    if st.session_state.markets:
        df_market = pd.DataFrame(st.session_state.markets)
        st.dataframe(df_market, use_container_width=True)
        total_market_cost = df_market["Amount"].sum()
    else:
        total_market_cost = 21862.0 - 6500.0 # Default market cost
        st.caption("ডিফল্ট বাজার খরচ প্রাক্কলন ধরা রয়েছে।")

# Overall Summary Section
with tab1:
    st.header("📊 চলতি মাসের চূড়ান্ত হিসাব বিবরণী")
    
    total_meals = sum(st.session_state.meals.values())
    per_meal_rate = total_market_cost / total_meals if total_meals > 0 else 0.0
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("মোট বাজার খরচ", f"{total_market_cost:,.2f} Tk")
    m2.metric("মোট মিল সংখ্যা", f"{total_meals} টি")
    m3.metric("বর্তমান মিল রেট", f"{per_meal_rate:.2f} Tk")
    m4.metric("জনপ্রতি ফিক্সড বিল", f"{per_person_fixed:.2f} Tk")
    
    st.divider()
    
    summary_data = []
    for m in st.session_state.members:
        dep = st.session_state.deposits[m]
        ml = st.session_state.meals[m]
        meal_cost = ml * per_meal_rate
        meal_bal = meal_cost - dep
        final_payable = meal_bal + per_person_fixed
        
        status = f"🔴 Payable: {final_payable:,.2f} Tk" if final_payable > 0 else f"🟢 Refund: {abs(final_payable):,.2f} Tk"
        
        summary_data.append({
            "Member Name": m,
            "Total Meals": int(ml),
            "Meal Rate": f"{per_meal_rate:.2f} Tk",
            "Meal Cost": f"{meal_cost:,.2f} Tk",
            "Total Deposit": f"{dep:,.2f} Tk",
            "Fixed Bill": f"{per_person_fixed:,.2f} Tk",
            "Final Status": status
        })
    
    df_summary = pd.DataFrame(summary_data)
    st.table(df_summary)
