from pathlib import Path
import pandas as pd
import streamlit as st

BASE = Path(__file__).parent
DATA = BASE / "data"
st.set_page_config(page_title="Investment Data Hub", page_icon="📊", layout="wide")

@st.cache_data
def load(name):
    return pd.read_csv(DATA / name)

st.title("📊 Arcesium Opterra Project")
st.caption("Independent financial data management product case study")
st.info("Synthetic demonstration data only. This is not an Arcesium product or a production investment platform.")

sec, prices, exc, trades, lineage = [load(x) for x in [
    "securities.csv", "prices.csv", "exceptions.csv", "transactions.csv", "lineage.csv"
]]
with st.sidebar:
    page = st.radio("Workspace", ["Executive overview","Security master","Pricing hierarchy",
        "Data quality & exceptions","Transactions","Data lineage","Product documentation"])
    st.caption("Snapshot: 21 November 2026 | Synthetic records")

if page == "Executive overview":
    st.subheader("Data operations overview")
    a,b,c,d = st.columns(4)
    a.metric("Securities", len(sec)); b.metric("Price observations", len(prices))
    c.metric("Open exceptions", int((exc.status=="Open").sum())); d.metric("Transactions", len(trades))
    x,y = st.columns(2)
    with x:
        st.markdown("**Exceptions by severity**"); st.bar_chart(exc.groupby("severity").size())
    with y:
        st.markdown("**Price observations by vendor**"); st.bar_chart(prices.groupby("vendor").size())
    st.markdown("**Recent exceptions**")
    st.dataframe(exc.sort_values("created_at", ascending=False), use_container_width=True, hide_index=True)
    st.markdown("**Product objective**")
    st.write("Create a governed data foundation to ingest, standardise, validate, master and distribute trusted investment data.")

elif page == "Security master":
    st.subheader("Security master")
    q = st.text_input("Search by name, ticker or identifier")
    classes = st.multiselect("Asset class", sorted(sec.asset_class.unique()), default=sorted(sec.asset_class.unique()))
    view = sec[sec.asset_class.isin(classes)]
    if q:
        view = view[view.astype(str).apply(lambda col: col.str.contains(q, case=False, na=False)).any(axis=1)]
    st.dataframe(view, use_container_width=True, hide_index=True)
    st.caption("Canonical records and cross-referenced identifiers — illustrative dataset.")

elif page == "Pricing hierarchy":
    st.subheader("Pricing source hierarchy")
    st.write("Select the highest-priority eligible vendor observation, subject to freshness.")
    ticker = st.selectbox("Security", sec.ticker.tolist())
    age = st.slider("Maximum price age (hours)", 1, 72, 24)
    p = prices[prices.ticker == ticker].copy()
    p["price_time"] = pd.to_datetime(p.price_time)
    reference_time = pd.Timestamp("2026-11-21 12:00:00")
    p["fresh"] = p.price_time >= reference_time - pd.Timedelta(hours=age)
    priority = {"Vendor Alpha":1,"Vendor Beta":2,"Vendor Gamma":3}
    p["priority"] = p.vendor.map(priority).fillna(99)
    st.dataframe(p.sort_values("priority"), use_container_width=True, hide_index=True)
    eligible = p[p.fresh].sort_values(["priority","price_time"], ascending=[True,False])
    if len(eligible):
        r = eligible.iloc[0]
        st.success(f"Selected: {r.price} {r.currency} from {r.vendor} (priority {int(r.priority)}).")
    else:
        st.warning("No eligible price. Route to exception review or approved fallback.")
    st.caption("Simplified demo logic, not a valuation recommendation or actual Opterra implementation.")

elif page == "Data quality & exceptions":
    st.subheader("Data quality exception workbench")
    c1,c2,c3 = st.columns(3)
    statuses = c1.multiselect("Status", sorted(exc.status.unique()), default=sorted(exc.status.unique()))
    severities = c2.multiselect("Severity", sorted(exc.severity.unique()), default=sorted(exc.severity.unique()))
    categories = c3.multiselect("Category", sorted(exc.category.unique()), default=sorted(exc.category.unique()))
    view = exc[exc.status.isin(statuses)&exc.severity.isin(severities)&exc.category.isin(categories)]
    st.dataframe(view, use_container_width=True, hide_index=True)
    if len(view):
        choice = st.selectbox("Exception detail", view.exception_id.tolist())
        r = view[view.exception_id==choice].iloc[0]
        st.write("**Issue:**", r.description)
        st.write("**Recommended action:**", r.recommended_action)
        st.write(f"**Owner:** {r.owner} | **SLA:** {r.sla_hours} hours")
    st.caption("Filtering is interactive; status changes are not persisted.")

elif page == "Transactions":
    st.subheader("Transaction data workbench")
    s = st.multiselect("Lifecycle status", sorted(trades.status.unique()), default=sorted(trades.status.unique()))
    a = st.multiselect("Asset class", sorted(trades.asset_class.unique()), default=sorted(trades.asset_class.unique()))
    st.dataframe(trades[trades.status.isin(s)&trades.asset_class.isin(a)], use_container_width=True, hide_index=True)
    st.write("Prototype control concepts: mandatory fields, recognised identifiers, positive quantity, currency presence and lifecycle validation.")

elif page == "Data lineage":
    st.subheader("Data lineage explorer")
    obj = st.selectbox("Data object", sorted(lineage.object_name.unique()))
    st.dataframe(lineage[lineage.object_name==obj], use_container_width=True, hide_index=True)
    st.caption("Lineage is illustrative, not generated from a live pipeline.")

else:
    st.subheader("Product documentation")
    st.markdown("**Vision**")
    st.write("Provide investment operations teams with a governed, explainable foundation for trusted reference and transactional data.")
    st.markdown("**Personas**")
    st.write("Reference Data Analyst · Pricing Analyst · Investment Operations Analyst · Data Operations Manager · Product and Engineering")
    st.markdown("**MVP**")
    st.write("Security master; vendor price comparison; configurable source priority and freshness; exception workbench; transaction view; lineage; operational dashboard.")
    st.markdown("**Out of scope**")
    st.write("Live vendor integrations, trade execution, official NAV/valuation, regulatory reporting, authentication, persistent workflow updates and enterprise-scale performance.")
    st.markdown("**Illustrative success measures**")
    st.write("Identifier completeness · Price freshness · Exceptions per 1,000 observations · Average exception age · Manual investigation time · Lineage coverage")
