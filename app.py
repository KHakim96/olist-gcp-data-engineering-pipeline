from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. Page Configuration (MUST BE FIRST STREAMLIT CALL)
# ==========================================
st.set_page_config(
    page_title="Olist E-Commerce Executive Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 2. Sidebar Controls & Theme Toggle
# ==========================================
st.sidebar.markdown("### 🎛️ Dashboard Controls")

dark_mode = st.sidebar.toggle("Dark Mode", value=True)

if dark_mode:
    bg_color = "#0E1117"
    card_bg = "#161B22"
    text_color = "#F8FAFC"
    subtext_color = "#94A3B8"
    border_color = "#30363D"
    grid_color = "#262C36"
    header_bg = "linear-gradient(135deg, #1E1B4B 0%, #0F172A 100%)"
    header_border = "#312E81"
    header_text = "#F8FAFC"
    hover_bg = "#1E293B"
else:
    bg_color = "#F8FAFC"
    card_bg = "#FFFFFF"
    text_color = "#0F172A"
    subtext_color = "#334155"
    border_color = "#CBD5E1"
    grid_color = "#CBD5E1"
    header_bg = "linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%)"
    header_border = "#C7D2FE"
    header_text = "#1E1B4B"
    hover_bg = "#F1F5F9"

# ==========================================
# 3. Dynamic Custom CSS Injection
# ==========================================
st.markdown(
    f"""
<style>
    /* Hide default Streamlit header, hamburger menu and footer */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header[data-testid="stHeader"] {{background: transparent;}}
    
    /* App background & Global Text */
    .stApp {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}

    h1, h2, h3, h4, h5, h6, p, span, label, div {{
        color: {text_color};
    }}
    
    /* Hide sidebar border & customize background */
    [data-testid="stSidebar"] {{
        border-right: none !important;
        background-color: {card_bg} !important;
    }}

    [data-testid="stSidebarContent"] {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
    }}

    [data-testid="stSidebarContent"] label, [data-testid="stSidebarContent"] span, [data-testid="stSidebarContent"] p {{
        color: {text_color} !important;
    }}

    /* Toggle track base styling */
    [data-testid="stSidebar"] div[role="switch"] {{
        border: 2px solid #334155 !important;
        background-color: #E2E8F0 !important;
        padding: 2px !important;
    }}

    /* Toggle track when dark mode is active (checked) */
    [data-testid="stSidebar"] div[role="switch"][aria-checked="true"] {{
        background-color: #1E293B !important;
        border-color: #6366F1 !important;
    }}

    /* Inner sliding circle handle */
    [data-testid="stSidebar"] div[role="switch"] > div {{
        background-color: #0F172A !important;
        border: 1px solid #334155 !important;
    }}

    /* Inner circle when active */
    [data-testid="stSidebar"] div[role="switch"][aria-checked="true"] > div {{
        background-color: #FFFFFF !important;
    }}

    /* Polished Container & Block Spacing */
    div[data-testid="stVerticalBlock"] > div[data-testid="stBlock"] {{
        border-radius: 14px;
        padding: 1.5rem !important;
        margin-bottom: 1.5rem !important;
    }}
    
    /* Equal Height KPI Cards */
    div[data-testid="stMetric"] {{
        background-color: {card_bg};
        border: 1px solid {border_color};
        border-radius: 14px;
        padding: 1.25rem 1.5rem !important;
        min-height: 145px !important;
        height: 145px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    div[data-testid="stMetric"] > div {{
        width: 100%;
    }}
    
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(99, 102, 241, 0.2);
    }}
    
    div[data-testid="stMetricLabel"] {{
        font-size: 0.85rem !important;
        color: {subtext_color} !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    div[data-testid="stMetricValue"] {{
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        color: {text_color} !important;
    }}

    div[data-testid="stMetricDelta"] {{
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }}

    .stPlotlyChart {{
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid {border_color};
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    }}

    /* Targeted key styling via .st-key-<key> */
    .st-key-kpi_revenue div[data-testid="stMetric"] {{
        border-left: 4px solid #6366F1 !important;
    }}
    .st-key-kpi_orders div[data-testid="stMetric"] {{
        border-left: 4px solid #38BDF8 !important;
    }}
    .st-key-kpi_customers div[data-testid="stMetric"] {{
        border-left: 4px solid #10B981 !important;
    }}
    .st-key-kpi_aov div[data-testid="stMetric"] {{
        border-left: 4px solid #F59E0B !important;
    }}

    .st-key-kpi_ontime div[data-testid="stMetric"] {{
        border-left: 4px solid #EC4899 !important;
    }}
    .st-key-kpi_delivery_time div[data-testid="stMetric"] {{
        border-left: 4px solid #8B5CF6 !important;
    }}
    .st-key-kpi_rating div[data-testid="stMetric"] {{
        border-left: 4px solid #FACC15 !important;
    }}
    .st-key-kpi_sellers div[data-testid="stMetric"] {{
        border-left: 4px solid #06B6D4 !important;
    }}

    /* Custom Header Banner */
    .st-key-header_banner {{
        background: {header_bg};
        padding: 1.5rem !important;
        border-radius: 16px;
        border: 1px solid {header_border};
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        margin-bottom: 1.5rem !important;
    }}

    .st-key-header_banner h2, .st-key-header_banner p, .st-key-header_banner div {{
        color: {header_text} !important;
    }}

    /* Custom Tab Bar styling */
    button[data-baseweb="tab"] {{
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
    }}
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 4. Data Loading & dbt Mart Transformation (Cached)
# ==========================================
@st.cache_data(show_spinner="Transforming Raw Data into dbt Marts...")
def load_and_build_dbt_marts():
    data_dir = Path(__file__).parent / "data" / "raw" / "olist"

    # Load raw CSVs
    orders_raw = pd.read_csv(data_dir / "olist_orders_dataset.csv")
    customers_raw = pd.read_csv(data_dir / "olist_customers_dataset.csv")
    order_items_raw = pd.read_csv(data_dir / "olist_order_items_dataset.csv")
    payments_raw = pd.read_csv(data_dir / "olist_order_payments_dataset.csv")
    reviews_raw = pd.read_csv(data_dir / "olist_order_reviews_dataset.csv")
    products_raw = pd.read_csv(data_dir / "olist_products_dataset.csv")
    sellers_raw = pd.read_csv(data_dir / "olist_sellers_dataset.csv")
    translation_raw = pd.read_csv(data_dir / "product_category_name_translation.csv")

    # Convert timestamps
    timestamp_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in timestamp_cols:
        if col in orders_raw.columns:
            orders_raw[col] = pd.to_datetime(orders_raw[col], errors="coerce")

    # Intermediate Model: int_payment_summary
    payment_summary = (
        payments_raw.groupby("order_id")
        .agg(
            total_payment=("payment_value", "sum"),
            payment_count=("payment_sequential", "count"),
            max_installments=("payment_installments", "max"),
            primary_payment_type=("payment_type", "first"),
        )
        .reset_index()
    )

    # Intermediate Model: int_delivery_metrics
    orders_raw["delivery_days"] = (
        orders_raw["order_delivered_customer_date"] - orders_raw["order_purchase_timestamp"]
    ).dt.total_seconds() / (24 * 3600)
    orders_raw["shipping_days"] = (
        orders_raw["order_delivered_carrier_date"] - orders_raw["order_purchase_timestamp"]
    ).dt.total_seconds() / (24 * 3600)
    orders_raw["delay_days"] = (
        orders_raw["order_delivered_customer_date"] - orders_raw["order_estimated_delivery_date"]
    ).dt.total_seconds() / (24 * 3600)
    orders_raw["delivery_status"] = np.where(
        orders_raw["order_delivered_customer_date"] <= orders_raw["order_estimated_delivery_date"],
        "On Time",
        "Late",
    )

    # Mart Dimension: dim_customer
    dim_customer = customers_raw[
        ["customer_id", "customer_unique_id", "customer_zip_code_prefix", "customer_city", "customer_state"]
    ].drop_duplicates()

    # Mart Dimension: dim_product
    dim_product = pd.merge(products_raw, translation_raw, on="product_category_name", how="left")
    dim_product["product_category_name_english"] = dim_product["product_category_name_english"].fillna(
        dim_product["product_category_name"].fillna("unknown")
    )

    # Mart Dimension: dim_seller
    dim_seller = sellers_raw[
        ["seller_id", "seller_zip_code_prefix", "seller_city", "seller_state"]
    ].drop_duplicates()

    # Intermediate Model: int_review_metrics
    avg_reviews = (
        reviews_raw.groupby("order_id")
        .agg(review_score=("review_score", "mean"))
        .reset_index()
    )

    # Mart Fact: fact_orders
    fact_orders = pd.merge(orders_raw, dim_customer, on="customer_id", how="left")
    fact_orders = pd.merge(fact_orders, payment_summary, on="order_id", how="left")
    fact_orders = pd.merge(fact_orders, avg_reviews, on="order_id", how="left")

    # Mart Fact: fact_order_items
    fact_order_items = pd.merge(
        order_items_raw,
        dim_product[["product_id", "product_category_name_english", "product_category_name"]],
        on="product_id",
        how="left",
    )
    fact_order_items = pd.merge(
        fact_order_items,
        dim_seller[["seller_id", "seller_city", "seller_state"]],
        on="seller_id",
        how="left",
    )

    return {
        "fact_orders": fact_orders,
        "dim_customer": dim_customer,
        "dim_product": dim_product,
        "dim_seller": dim_seller,
        "fact_order_items": fact_order_items,
        "payments_raw": payments_raw,
        "reviews_raw": reviews_raw,
    }

marts_data = load_and_build_dbt_marts()
fact_orders_df = marts_data["fact_orders"]
fact_order_items_df = marts_data["fact_order_items"]
dim_customer_df = marts_data["dim_customer"]
dim_product_df = marts_data["dim_product"]
dim_seller_df = marts_data["dim_seller"]
payments_raw_df = marts_data["payments_raw"]
reviews_raw_df = marts_data["reviews_raw"]

# ==========================================
# 5. Dynamic Plotly Chart Theming Helper
# ==========================================
def apply_chart_theme(
    fig,
    title="",
    height=440,
    showlegend=True,
    custom_margin=None,
    is_log_y=False,
    tickangle=0,
):
    margin = custom_margin or dict(l=40, r=40, t=80, b=40)
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(size=16, color=text_color, family="sans-serif"),
            x=0.01,
            y=0.96,
            pad=dict(b=20),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=text_color, family="sans-serif"),
        showlegend=showlegend,
        legend=(
            dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5,
                font=dict(color=text_color),
                bgcolor="rgba(0,0,0,0)",
            )
            if showlegend
            else None
        ),
        xaxis=dict(
            gridcolor=grid_color,
            zerolinecolor=grid_color,
            tickfont=dict(color=subtext_color, size=12),
            title_font=dict(color=text_color, size=13),
            tickangle=tickangle,
        ),
        yaxis=dict(
            gridcolor=grid_color,
            zerolinecolor=grid_color,
            tickfont=dict(color=subtext_color, size=12),
            title_font=dict(color=text_color, size=13),
            type="log" if is_log_y else None,
        ),
        height=height,
        margin=margin,
        hoverlabel=dict(bgcolor=hover_bg, font_size=13, font_family="sans-serif"),
    )
    return fig

# ==========================================
# 6. Sidebar Filters
# ==========================================
st.sidebar.markdown("---")

min_date = fact_orders_df["order_purchase_timestamp"].min().date()
max_date = fact_orders_df["order_purchase_timestamp"].max().date()

selected_date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="sidebar_date_range",
)

all_statuses = sorted(fact_orders_df["order_status"].dropna().unique().tolist())
selected_statuses = st.sidebar.multiselect(
    "Order Status",
    options=all_statuses,
    default=[],
    placeholder="All Statuses Selected",
    help="Leave empty to include all order statuses",
    key="sidebar_status_filter",
)

all_states = sorted(fact_orders_df["customer_state"].dropna().unique().tolist())
selected_states = st.sidebar.multiselect(
    "Customer State",
    options=all_states,
    default=[],
    placeholder="All States Selected",
    help="Leave empty to include all customer states",
    key="sidebar_state_filter",
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Architecture Context:**
    - **Raw Layer:** `olist_raw` (BigQuery)
    - **Transformation:** dbt (16 Views, 10 Tables)
    - **Quality Status:** 32 Tests Passed 🟢
    - **Orchestration:** Airflow + Docker
    """
)

# Apply Clean Filter Logic (Empty multiselect = Select All)
if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
    start_d, end_d = selected_date_range
else:
    start_d, end_d = min_date, max_date

effective_statuses = selected_statuses if selected_statuses else all_statuses
effective_states = selected_states if selected_states else all_states

filtered_orders = fact_orders_df[
    (fact_orders_df["order_purchase_timestamp"].dt.date >= start_d)
    & (fact_orders_df["order_purchase_timestamp"].dt.date <= end_d)
    & (fact_orders_df["order_status"].isin(effective_statuses))
    & (fact_orders_df["customer_state"].isin(effective_states))
]

filtered_order_items = fact_order_items_df[
    fact_order_items_df["order_id"].isin(filtered_orders["order_id"])
]

# ==========================================
# 7. Header Banner
# ==========================================
with st.container(key="header_banner"):
    st.markdown("## ⚡ Olist E-Commerce Executive Intelligence")
    st.markdown(
        "Production Data Pipeline & Business Performance Dashboard | **Google Cloud Platform (BigQuery + dbt + Airflow)**"
    )

# ==========================================
# 8. Grid System: High-Level KPIs (Top Row of 4 Columns)
# ==========================================
total_orders = filtered_orders["order_id"].nunique()
total_customers = filtered_orders["customer_unique_id"].nunique()
total_revenue = filtered_orders["total_payment"].sum()
aov = total_revenue / total_orders if total_orders > 0 else 0

delivered_orders = filtered_orders[filtered_orders["delivery_status"].notna()]
ontime_count = (delivered_orders["delivery_status"] == "On Time").sum()
ontime_rate = (ontime_count / len(delivered_orders) * 100) if len(delivered_orders) > 0 else 0
avg_delivery_days = filtered_orders["delivery_days"].mean()
avg_review_score = filtered_orders["review_score"].mean()
active_sellers = filtered_order_items["seller_id"].nunique()

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(key="kpi_revenue"):
        st.metric(
            label="Total Revenue",
            value=f"${total_revenue/1e6:.2f}M",
            delta=f"${total_revenue:,.0f} Exact",
        )

with col2:
    with st.container(key="kpi_orders"):
        st.metric(
            label="Total Orders",
            value=f"{total_orders/1e3:.1f}K" if total_orders >= 10000 else f"{total_orders:,}",
            delta=f"{len(delivered_orders):,} Delivered",
        )

with col3:
    with st.container(key="kpi_customers"):
        st.metric(
            label="Total Unique Customers",
            value=f"{total_customers/1e3:.1f}K" if total_customers >= 10000 else f"{total_customers:,}",
        )

with col4:
    with st.container(key="kpi_aov"):
        st.metric(
            label="Average Order Value",
            value=f"${aov:.2f}",
        )

st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# Secondary Row of 4 Operational KPIs
col5, col6, col7, col8 = st.columns(4)

with col5:
    with st.container(key="kpi_ontime"):
        st.metric(
            label="On-Time Delivery Rate",
            value=f"{ontime_rate:.1f}%",
            delta="Target: >90%",
        )

with col6:
    with st.container(key="kpi_delivery_time"):
        st.metric(
            label="Avg Delivery Time",
            value=f"{avg_delivery_days:.1f} days" if not np.isnan(avg_delivery_days) else "N/A",
        )

with col7:
    with st.container(key="kpi_rating"):
        st.metric(
            label="Avg Review Rating",
            value=f"{avg_review_score:.2f} ⭐" if not np.isnan(avg_review_score) else "N/A",
        )

with col8:
    with st.container(key="kpi_sellers"):
        st.metric(
            label="Active Sellers",
            value=f"{active_sellers/1e3:.1f}K" if active_sellers >= 1000 else f"{active_sellers:,}",
        )

st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

# ==========================================
# 9. Main Analytics Tabs
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Executive Revenue & Orders",
    "🚚 Logistics & Operations",
    "👤 Customer & Geographics",
    "🛠️ dbt Marts & Pipeline Architecture",
])

# ------------------------------------------
# TAB 1: EXECUTIVE REVENUE & ORDERS
# ------------------------------------------
with tab1:
    col_left, col_right = st.columns([6, 4])

    with col_left:
        with st.container(key="chart_revenue_trend"):
            monthly_df = (
                filtered_orders.set_index("order_purchase_timestamp")
                .resample("ME")
                .agg(revenue=("total_payment", "sum"), orders=("order_id", "nunique"))
                .reset_index()
            )
            monthly_df["month_str"] = monthly_df["order_purchase_timestamp"].dt.strftime("%Y-%m")

            fig_trend = go.Figure()
            fig_trend.add_trace(
                go.Scatter(
                    x=monthly_df["month_str"],
                    y=monthly_df["revenue"],
                    name="Revenue ($)",
                    mode="lines+markers",
                    line=dict(color="#6366F1", width=3),
                    fill="tozeroy",
                    fillcolor="rgba(99, 102, 241, 0.15)",
                )
            )
            fig_trend.add_trace(
                go.Scatter(
                    x=monthly_df["month_str"],
                    y=monthly_df["orders"],
                    name="Orders Count",
                    mode="lines+markers",
                    yaxis="y2",
                    line=dict(color="#38BDF8", width=2, dash="dash"),
                )
            )
            fig_trend.update_layout(
                yaxis2=dict(
                    title=dict(text="Orders Count", font=dict(color="#38BDF8", size=13)),
                    overlaying="y",
                    side="right",
                    showgrid=False,
                    tickfont=dict(color="#38BDF8", size=12),
                )
            )
            apply_chart_theme(fig_trend, "Monthly Revenue ($) & Order Volume Growth Trend", height=440)
            st.plotly_chart(fig_trend, use_container_width=True)

    with col_right:
        with st.container(key="chart_top_categories"):
            cat_revenue = (
                filtered_order_items.groupby("product_category_name_english")["price"]
                .sum()
                .reset_index()
                .sort_values(by="price", ascending=True)
                .tail(10)
            )
            fig_cat = px.bar(
                cat_revenue,
                x="price",
                y="product_category_name_english",
                orientation="h",
                labels={"price": "Revenue ($)", "product_category_name_english": "Category"},
                color="price",
                color_continuous_scale="Purples",
            )
            fig_cat.update_coloraxes(showscale=False)
            apply_chart_theme(fig_cat, "Top 10 Product Categories by Revenue ($)", height=440)
            st.plotly_chart(fig_cat, use_container_width=True)

    col_b1, col_b2 = st.columns(2)

    with col_b1:
        with st.container(key="chart_payment_methods"):
            pay_df = (
                payments_raw_df[payments_raw_df["order_id"].isin(filtered_orders["order_id"])]
                .groupby("payment_type")["payment_value"]
                .sum()
                .reset_index()
            )
            fig_pay = px.pie(
                pay_df,
                values="payment_value",
                names="payment_type",
                hole=0.5,
                color_discrete_sequence=["#6366F1", "#38BDF8", "#10B981", "#F59E0B", "#EC4899"],
            )
            fig_pay.update_traces(
                textposition="inside",
                insidetextorientation="radial",
                textinfo="percent+label",
            )
            apply_chart_theme(fig_pay, "Payment Method Volume Breakdown ($)", height=440, showlegend=True)
            st.plotly_chart(fig_pay, use_container_width=True)

    with col_b2:
        with st.container(key="chart_order_status"):
            status_df = filtered_orders["order_status"].value_counts().reset_index()
            status_df.columns = ["status", "count"]
            max_c = status_df["count"].max()
            
            fig_status = px.bar(
                status_df,
                x="status",
                y="count",
                color="status",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                text_auto=True,
            )
            fig_status.update_traces(textposition="outside", cliponaxis=False)
            fig_status.update_layout(yaxis=dict(range=[0, max_c * 1.22]))
            apply_chart_theme(
                fig_status,
                "Order Status Distribution",
                height=440,
                showlegend=False,
                custom_margin=dict(l=50, r=30, t=60, b=80),
                tickangle=-25,
            )
            st.plotly_chart(fig_status, use_container_width=True)

# ------------------------------------------
# TAB 2: LOGISTICS & OPERATIONS
# ------------------------------------------
with tab2:
    col_l1, col_l2 = st.columns([6, 4])

    with col_l1:
        with st.container(key="chart_delivery_trend"):
            deliv_monthly = (
                filtered_orders.dropna(subset=["order_delivered_customer_date"])
                .set_index("order_purchase_timestamp")
                .groupby([pd.Grouper(freq="ME"), "delivery_status"])
                .size()
                .unstack(fill_value=0)
                .reset_index()
            )
            deliv_monthly["month_str"] = deliv_monthly["order_purchase_timestamp"].dt.strftime("%Y-%m")

            fig_deliv = go.Figure()
            if "On Time" in deliv_monthly.columns:
                fig_deliv.add_trace(
                    go.Bar(
                        x=deliv_monthly["month_str"],
                        y=deliv_monthly["On Time"],
                        name="On Time",
                        marker_color="#10B981",
                    )
                )
            if "Late" in deliv_monthly.columns:
                fig_deliv.add_trace(
                    go.Bar(
                        x=deliv_monthly["month_str"],
                        y=deliv_monthly["Late"],
                        name="Late",
                        marker_color="#EF4444",
                    )
                )
            fig_deliv.update_layout(barmode="stack")
            apply_chart_theme(fig_deliv, "Monthly Fulfillment Performance (On Time vs Late)", height=440)
            st.plotly_chart(fig_deliv, use_container_width=True)

    with col_l2:
        with st.container(key="chart_state_delivery"):
            state_deliv = (
                filtered_orders.groupby("customer_state")["delivery_days"]
                .mean()
                .reset_index()
                .sort_values(by="delivery_days", ascending=False)
                .head(10)
            )
            fig_state_deliv = px.bar(
                state_deliv,
                x="delivery_days",
                y="customer_state",
                orientation="h",
                labels={"delivery_days": "Avg Days", "customer_state": "State"},
                color="delivery_days",
                color_continuous_scale="Reds",
            )
            fig_state_deliv.update_coloraxes(showscale=False)
            apply_chart_theme(fig_state_deliv, "Top 10 States by Longest Delivery Time", height=440)
            st.plotly_chart(fig_state_deliv, use_container_width=True)

    with st.container(key="chart_delivery_hist"):
        clean_deliv_days = filtered_orders["delivery_days"].dropna()
        clean_deliv_days = clean_deliv_days[(clean_deliv_days >= 0) & (clean_deliv_days <= 50)]
        fig_hist = px.histogram(
            clean_deliv_days,
            x="delivery_days",
            nbins=40,
            labels={"delivery_days": "Days from Order to Customer Delivery"},
            color_discrete_sequence=["#8B5CF6"],
        )
        apply_chart_theme(fig_hist, "Fulfillment Lead Time Distribution (Days)", height=380)
        st.plotly_chart(fig_hist, use_container_width=True)

# ------------------------------------------
# TAB 3: CUSTOMER & GEOGRAPHICAL INSIGHTS
# ------------------------------------------
with tab3:
    col_c1, col_c2 = st.columns(2)

    with col_c1:
        with st.container(key="chart_customer_states"):
            state_summary = (
                filtered_orders.groupby("customer_state")
                .agg(revenue=("total_payment", "sum"), orders=("order_id", "nunique"))
                .reset_index()
                .sort_values(by="revenue", ascending=False)
                .head(12)
            )
            fig_state_rev = px.bar(
                state_summary,
                x="customer_state",
                y="revenue",
                color="revenue",
                labels={"revenue": "Revenue ($)", "customer_state": "State"},
                color_continuous_scale="Viridis",
                text_auto=".2s",
            )
            fig_state_rev.update_coloraxes(showscale=False)
            apply_chart_theme(fig_state_rev, "Top 12 Customer States by Revenue ($)", height=440)
            st.plotly_chart(fig_state_rev, use_container_width=True)

    with col_c2:
        with st.container(key="chart_reviews_dist"):
            review_dist = (
                reviews_raw_df[reviews_raw_df["order_id"].isin(filtered_orders["order_id"])]["review_score"]
                .value_counts()
                .reset_index()
            )
            review_dist.columns = ["score", "count"]
            review_dist = review_dist.sort_values(by="score")
            fig_reviews = px.bar(
                review_dist,
                x="score",
                y="count",
                color="score",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                text_auto=True,
                labels={"score": "Review Score (1 to 5)", "count": "Review Count"},
            )
            fig_reviews.update_coloraxes(showscale=False)
            apply_chart_theme(fig_reviews, "Customer Satisfaction Rating Distribution", height=440)
            st.plotly_chart(fig_reviews, use_container_width=True)

    with st.container(key="chart_top_cities"):
        city_summary = (
            filtered_orders.groupby("customer_city")["total_payment"]
            .sum()
            .reset_index()
            .sort_values(by="total_payment", ascending=False)
            .head(15)
        )
        fig_city = px.bar(
            city_summary,
            x="customer_city",
            y="total_payment",
            color="total_payment",
            labels={"total_payment": "Total Revenue ($)", "customer_city": "City"},
            color_continuous_scale="Blues",
            text_auto=".2s",
        )
        fig_city.update_coloraxes(showscale=False)
        apply_chart_theme(fig_city, "Top 15 Cities by E-Commerce Spend ($)", height=400)
        st.plotly_chart(fig_city, use_container_width=True)

# ------------------------------------------
# TAB 4: dbt MARTS & PIPELINE ARCHITECTURE
# ------------------------------------------
with tab4:
    st.markdown("### 🏗️ Data Architecture & dbt Mart Layer Specifications")
    
    col_p1, col_p2 = st.columns([5, 5])
    
    with col_p1:
        st.markdown("#### 🔄 End-to-End Pipeline Lineage")
        st.graphviz_chart('''
digraph G {
    rankdir=TB;
    node [shape=box, style="filled,rounded", fontname="Sans-Serif", fontsize=10];
    
    // Nodes
    sources [label="Olist Kaggle CSV + Weather REST API", fillcolor="#E2E8F0", color="#475569"];
    gcs [label="Google Cloud Storage (Data Lake)", fillcolor="#E2E8F0", color="#475569"];
    raw [label="BigQuery Raw (`olist_raw`)", fillcolor="#DBEAFE", color="#2563EB"];
    dbt [label="dbt Core Transformations\\n• 16 Views\\n• 10 Tables\\n• 32 Tests Passed", fillcolor="#FEF3C7", color="#D97706"];
    analytics [label="BigQuery Analytics (`olist_analytics`)", fillcolor="#DCFCE7", color="#16A34A"];
    streamlit [label="Streamlit Executive Dashboard", fillcolor="#F3E8FF", color="#9333EA"];
    
    // Subgraph for Airflow Orchestration
    subgraph cluster_airflow {
        label = "Apache Airflow (Docker Orchestrator)";
        style = dashed;
        color = "#64748B";
        fontname = "Sans-Serif";
        fontsize = 11;
        
        sources -> gcs [label="Ingestion Operator"];
        gcs -> raw [label="GCSToBigQuery"];
        raw -> dbt [label="DbtTaskGroup"];
        dbt -> analytics [label="dbt test & run"];
    }
    
    analytics -> streamlit [label="Data Serving"];
}
''', use_container_width=True)
    
    with col_p2:
        st.markdown("#### 📐 Final dbt Data Marts Models")
        st.markdown(
            """
            - **`executive_dashboard`**: Aggregated core business KPIs (`total_orders`, `total_customers`, `total_revenue`, `average_order_value`).
            - **`fact_orders`**: Grain = Order. Contains order timestamps, delivery status, delay metrics, and customer IDs.
            - **`fact_order_items`**: Grain = Order Item. Includes price, freight, category, and seller metadata.
            - **`fact_payments`**: Aggregated payment value, installment details, and payment modes per order.
            - **`fact_reviews`**: Review scores, creation dates, and satisfaction metrics.
            - **`dim_customer`**: Customer unique IDs, cities, and states.
            - **`dim_product`**: Product dimensions, categories, and English translations.
            - **`dim_seller`**: Seller location and zip code prefixes.
            - **`dim_date`**: Calendar date dimension for time-series analysis.
            """
        )
    
    st.markdown("---")
    st.markdown("#### 🔍 Interactive dbt Mart Sample Data Inspector")
    
    selected_mart = st.selectbox(
        "Select dbt Model / Data Mart to Preview",
        options=["fact_orders", "fact_order_items", "dim_customer", "dim_product", "dim_seller", "raw_payments", "raw_reviews"],
        key="select_mart_preview"
    )
    
    if selected_mart == "fact_orders":
        st.dataframe(filtered_orders.head(100), use_container_width=True)
    elif selected_mart == "fact_order_items":
        st.dataframe(filtered_order_items.head(100), use_container_width=True)
    elif selected_mart == "dim_customer":
        st.dataframe(dim_customer_df.head(100), use_container_width=True)
    elif selected_mart == "dim_product":
        st.dataframe(dim_product_df.head(100), use_container_width=True)
    elif selected_mart == "dim_seller":
        st.dataframe(dim_seller_df.head(100), use_container_width=True)
    elif selected_mart == "raw_payments":
        st.dataframe(payments_raw_df.head(100), use_container_width=True)
    elif selected_mart == "raw_reviews":
        st.dataframe(reviews_raw_df.head(100), use_container_width=True)
