import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# REPLACE your existing initialize_db function with this:
def initialize_db(engine):
    with engine.connect() as conn:
        try:
            count = conn.execute(text("SELECT COUNT(*) FROM providers")).scalar()
            if count > 0:
                return  # Already initialized, skip
        except:
            pass  # Tables don't exist yet, continue

    providers = pd.read_csv("data/providers_data.csv")
    receivers = pd.read_csv("data/receivers_data.csv")
    food      = pd.read_csv("data/food_listings_data.csv")
    claims    = pd.read_csv("data/claims_data.csv")

    providers.columns = providers.columns.str.lower()
    receivers.columns = receivers.columns.str.lower()
    food.columns      = food.columns.str.lower()
    claims.columns    = claims.columns.str.lower()

    providers.to_sql("providers",     engine, if_exists="replace", index=False)
    receivers.to_sql("receivers",     engine, if_exists="replace", index=False)
    food.to_sql("food_listings",      engine, if_exists="replace", index=False)
    claims.to_sql("claims",           engine, if_exists="replace", index=False)
st.set_page_config(
    page_title="Food Wastage Management System",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
    /* ── Main background ── */
    .stApp {
        background-color: #0a0a0a !important;
    }

    /* ── Main content area ── */
    [data-testid="stAppViewContainer"] {
        background-color: #0a0a0a !important;
    }

    /* ── Top header bar ── */
    [data-testid="stHeader"] {
        background-color: #0a0a0a !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: #111111 !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* ── All main text ── */
    .main p, .main span, .main label,
    .main div, .main li,
    .main h1, .main h2, .main h3 {
        color: #f0f0f0 !important;
    }

    /* ── Expander headers (SQL query titles) ── */
    .streamlit-expanderHeader,
    .streamlit-expanderHeader p,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] p {
        color: #f0f0f0 !important;
    }

    /* ── Expander body background ── */
    [data-testid="stExpander"] {
        background-color: #1a1a1a !important;
        border: 1px solid #333333 !important;
        border-radius: 8px !important;
    }

    /* ── Dataframe / table ── */
    [data-testid="stDataFrame"] {
        background-color: #1a1a1a !important;
    }

    /* ── Metric cards ── */
    [data-testid="stMetric"] {
        background-color: #1a1a1a !important;
        border-radius: 8px !important;
        padding: 12px !important;
        border: 1px solid #2a2a2a !important;
    }
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"] {
        color: #f0f0f0 !important;
    }

    /* ── Input boxes, selectbox, text input ── */
    .stTextInput input,
    .stSelectbox div,
    .stMultiSelect div {
        background-color: #1a1a1a !important;
        color: #f0f0f0 !important;
        border: 1px solid #333333 !important;
    }

    /* ── Buttons ── */
    .stButton button {
        background-color: #222222 !important;
        color: #f0f0f0 !important;
        border: 1px solid #444444 !important;
    }
    .stButton button:hover {
        background-color: #333333 !important;
        border-color: #4caf50 !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a1a !important;
        color: #f0f0f0 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2a2a2a !important;
        border-bottom: 2px solid #4caf50 !important;
    }

    /* ── Code blocks (SQL display) ── */
    .stCode, code {
        background-color: #1a1a1a !important;
        color: #4caf50 !important;
    }

    /* ── Slider ── */
    .stSlider label {
        color: #f0f0f0 !important;
    }

    /* ── Radio buttons ── */
    .stRadio label {
        color: #f0f0f0 !important;
    }

    /* ── Divider ── */
    hr {
        border-color: #333333 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    /* ── Main background ── */
    .stApp { background-color: #f7f5f0; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1b4332 0%, #2d6a4f 100%);
    }
    [data-testid="stSidebar"] * { color: #d8f3dc !important; }
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background: #1b4332 !important;
        border-color: #40916c !important;
    }

    /* ── Metric cards ── */
    [data-testid="metric-container"] {
        background: white;
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 4px solid #40916c;
        box-shadow: 0 2px 8px rgba(0,0,0,.06);
    }

    /* ── Section headers ── */
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1b4332;
        margin: 1.2rem 0 0.6rem;
        padding-bottom: 6px;
        border-bottom: 2px solid #95d5b2;
    }

    /* ── Query card ── */
    .query-box {
        background: white;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #52b788;
        box-shadow: 0 2px 6px rgba(0,0,0,.05);
    }

    /* ── Dataframe header ── */
    .stDataFrame thead th {
        background-color: #2d6a4f !important;
        color: white !important;
    }

    /* ── Hide default header ── */
    #MainMenu, footer { visibility: hidden; }

    /* ── Success/info message ── */
    .stSuccess { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)
from sqlalchemy import create_engine
import streamlit as st

@st.cache_resource
def get_engine():
    return create_engine("sqlite:///food_waste.db")

engine = get_engine()
initialize_db(engine)

def run_query(sql, params=None):
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params)

@st.cache_data(ttl=30)
def load_food_data():
    q = """
        SELECT f.food_id, f.food_name, f.quantity, f.expiry_date,
               p.name AS provider_name, f.provider_type, f.location,
               f.food_type, f.meal_type
        FROM food_listings f
        JOIN providers p ON f.provider_id = p.provider_id
    """
    df = run_query(q)
    df['meal_type']   = df['meal_type'].str.replace('\r', '').str.strip()
    df['expiry_date'] = pd.to_datetime(df['expiry_date'], errors='coerce')
    return df

df = load_food_data()

st.sidebar.image("https://img.icons8.com/color/80/salad.png", width=70)
st.sidebar.title("🥗 Food Waste Mgmt")
st.sidebar.markdown("---")

page = st.sidebar.radio("📌 Navigate to", [
    "🏠 Dashboard",
    "📋 Food Listings",
    "📊 SQL Queries (15)",
    "✏️  CRUD Operations",
    "📈 EDA & Charts",
])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filters")
sel_cities = st.sidebar.multiselect(
    "City / Location",
    sorted(df['location'].dropna().unique())
)
sel_ftypes = st.sidebar.multiselect(
    "Food Type",
    sorted(df['food_type'].dropna().unique())
)
sel_mtypes = st.sidebar.multiselect(
    "Meal Type",
    sorted(df['meal_type'].dropna().unique())
)

# Apply sidebar filters to main df
filtered = df.copy()
if sel_cities:  filtered = filtered[filtered['location'].isin(sel_cities)]
if sel_ftypes:  filtered = filtered[filtered['food_type'].isin(sel_ftypes)]
if sel_mtypes:  filtered = filtered[filtered['meal_type'].isin(sel_mtypes)]

if page == "🏠 Dashboard":
    st.title("🥗 Local Food Wastage Management System")
    st.caption("Connecting surplus food providers to those in need — powered by MySQL + Streamlit")
    st.divider()

    # ── KPI Row ──
    c1, c2, c3, c4 = st.columns(4)
    total_providers = run_query("SELECT COUNT(*) AS n FROM providers").iloc[0,0]
    total_receivers = run_query("SELECT COUNT(*) AS n FROM receivers").iloc[0,0]
    total_qty       = run_query("SELECT SUM(quantity) AS n FROM food_listings").iloc[0,0]
    total_claims    = run_query("SELECT COUNT(*) AS n FROM claims").iloc[0,0]

    c1.metric("🏪 Providers",      f"{total_providers:,}")
    c2.metric("🤝 Receivers",      f"{total_receivers:,}")
    c3.metric("🍱 Total Quantity", f"{int(total_qty):,} kg")
    c4.metric("📦 Total Claims",   f"{total_claims:,}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section-title">Claims by Status</p>', unsafe_allow_html=True)
        status_df = run_query("SELECT status, COUNT(*) AS count FROM claims GROUP BY status")
        fig = px.pie(status_df, values='count', names='status', hole=0.42,
                     color_discrete_map={"Completed":"#52b788","Pending":"#f4a261","Cancelled":"#e76f51"})
        fig.update_layout(margin=dict(t=10,b=10), height=280)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">Food Type Distribution</p>', unsafe_allow_html=True)
        ft_df = run_query("SELECT food_type, COUNT(*) AS count FROM food_listings GROUP BY food_type")
        fig2 = px.bar(ft_df, x='food_type', y='count', color='food_type',
                      color_discrete_sequence=["#52b788","#95d5b2","#b7e4c7"])
        fig2.update_layout(showlegend=False, margin=dict(t=10,b=10), height=280)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-title">Top 10 Cities by Food Listings</p>', unsafe_allow_html=True)
    city_df = run_query("""
        SELECT location AS city, COUNT(*) AS listings
        FROM food_listings GROUP BY location ORDER BY listings DESC LIMIT 10
    """)
    fig3 = px.bar(city_df, x='city', y='listings',
                  color='listings', color_continuous_scale='Greens')
    fig3.update_layout(margin=dict(t=10,b=10), height=300)
    st.plotly_chart(fig3, use_container_width=True)

elif page == "📋 Food Listings":
    st.title("📋 Food Listings")

    # Search bar
    search = st.text_input("🔎 Search food name", placeholder="e.g. Rice, Bread, Soup...")
    if search:
        filtered = filtered[filtered['food_name'].str.contains(search, case=False, na=False)]

    # KPIs for filtered view
    c1, c2, c3 = st.columns(3)
    c1.metric("🍽 Total Quantity",   f"{int(filtered['quantity'].sum()):,}")
    c2.metric("📦 Total Listings",   filtered.shape[0])
    c3.metric("🏢 Unique Providers", filtered['provider_name'].nunique())

    st.markdown('<p class="section-title">Filtered Food Listings</p>', unsafe_allow_html=True)
    st.dataframe(
        filtered[['food_name','quantity','expiry_date','provider_name',
                  'provider_type','location','food_type','meal_type']].reset_index(drop=True),
        use_container_width=True, height=420
    )

    # Quick charts
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-title">Meal Type Distribution</p>', unsafe_allow_html=True)
        fig = px.bar(filtered['meal_type'].value_counts().reset_index(),
                     x='meal_type', y='count', color_discrete_sequence=["#52b788"])
        fig.update_layout(margin=dict(t=5,b=5), height=260, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown('<p class="section-title">City-wise Quantity</p>', unsafe_allow_html=True)
        city_qty = filtered.groupby('location')['quantity'].sum().reset_index()
        fig2 = px.bar(city_qty.sort_values('quantity', ascending=False).head(10),
                      x='location', y='quantity', color_discrete_sequence=["#40916c"])
        fig2.update_layout(margin=dict(t=5,b=5), height=260, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Provider contact lookup
    st.markdown('<p class="section-title">📞 Provider Contact Lookup</p>', unsafe_allow_html=True)
    providers_df = run_query("SELECT provider_id, name, type, city, contact FROM providers ORDER BY name")
    chosen = st.selectbox("Select Provider", providers_df['name'].tolist())
    row = providers_df[providers_df['name'] == chosen].iloc[0]
    st.info(f"**{row['name']}** | Type: {row['type']} | City: {row['city']} | 📞 {row['contact']}")

elif page == "📊 SQL Queries (15)":
    st.title("📊 SQL Analysis — All 15 Queries")
    st.caption("Each query runs live against your MySQL database")

    QUERIES = [
        {
            "title": "Q1 — Providers & receivers count per city",
            "sql": """
                SELECT p.city,
                       COUNT(DISTINCT p.provider_id) AS providers,
                       COUNT(DISTINCT r.receiver_id) AS receivers
                FROM providers p
                LEFT JOIN receivers r ON p.city = r.city
                GROUP BY p.city
                ORDER BY providers DESC
                LIMIT 15
            """
        },
        {
            "title": "Q2 — Provider type that contributes the most food",
            "sql": """
                SELECT f.provider_type,
                       SUM(f.quantity) AS total_quantity,
                       COUNT(*) AS listings
                FROM food_listings f
                GROUP BY f.provider_type
                ORDER BY total_quantity DESC
            """
        },
        {
            "title": "Q3 — Contact info of providers in a specific city",
            "sql": """
                SELECT name, type, city, contact
                FROM providers
                ORDER BY city, name
                LIMIT 20
            """,
            "city_filter": True
        },
        {
            "title": "Q4 — Receivers who claimed the most food",
            "sql": """
                SELECT r.name, r.type, r.city,
                       COUNT(c.claim_id) AS total_claims
                FROM claims c
                JOIN receivers r ON c.receiver_id = r.receiver_id
                GROUP BY r.receiver_id, r.name, r.type, r.city
                ORDER BY total_claims DESC
                LIMIT 10
            """
        },
        {
            "title": "Q5 — Total quantity of food available",
            "sql": """
                SELECT
                    COUNT(*) AS total_listings,
                    SUM(quantity) AS total_quantity,
                    ROUND(AVG(quantity), 2) AS avg_quantity
                FROM food_listings
            """
        },
        {
            "title": "Q6 — City with highest number of food listings",
            "sql": """
                SELECT location AS city,
                       COUNT(*) AS listings,
                       SUM(quantity) AS total_quantity
                FROM food_listings
                GROUP BY location
                ORDER BY listings DESC
                LIMIT 10
            """
        },
        {
            "title": "Q7 — Most commonly available food types",
            "sql": """
                SELECT food_type,
                       COUNT(*) AS count,
                       SUM(quantity) AS total_quantity
                FROM food_listings
                GROUP BY food_type
                ORDER BY count DESC
            """
        },
        {
            "title": "Q8 — Number of claims per food item",
            "sql": """
                SELECT f.food_name,
                       COUNT(c.claim_id) AS total_claims
                FROM claims c
                JOIN food_listings f ON c.food_id = f.food_id
                GROUP BY f.food_name
                ORDER BY total_claims DESC
                LIMIT 15
            """
        },
        {
            "title": "Q9 — Provider with most successful (Completed) claims",
            "sql": """
                SELECT p.name AS provider, p.type, p.city,
                       COUNT(c.claim_id) AS completed_claims
                FROM claims c
                JOIN food_listings f ON c.food_id = f.food_id
                JOIN providers p     ON f.provider_id = p.provider_id
                WHERE c.status = 'Completed'
                GROUP BY p.provider_id, p.name, p.type, p.city
                ORDER BY completed_claims DESC
                LIMIT 10
            """
        },
        {
            "title": "Q10 — Claim status percentage breakdown",
            "sql": """
                SELECT status,
                       COUNT(*) AS count,
                       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS percentage
                FROM claims
                GROUP BY status
            """
        },
        {
            "title": "Q11 — Average quantity claimed per receiver",
            "sql": """
                SELECT r.name, r.type,
                       COUNT(c.claim_id) AS total_claims,
                       ROUND(AVG(f.quantity), 2) AS avg_quantity
                FROM claims c
                JOIN receivers r    ON c.receiver_id = r.receiver_id
                JOIN food_listings f ON c.food_id = f.food_id
                GROUP BY r.receiver_id, r.name, r.type
                ORDER BY avg_quantity DESC
                LIMIT 10
            """
        },
        {
            "title": "Q12 — Most claimed meal type",
            "sql": """
                SELECT f.meal_type,
                       COUNT(c.claim_id) AS total_claims
                FROM claims c
                JOIN food_listings f ON c.food_id = f.food_id
                GROUP BY f.meal_type
                ORDER BY total_claims DESC
            """
        },
        {
            "title": "Q13 — Total food donated by each provider",
            "sql": """
                SELECT p.name AS provider, p.type, p.city,
                       SUM(f.quantity) AS total_donated
                FROM food_listings f
                JOIN providers p ON f.provider_id = p.provider_id
                GROUP BY p.provider_id, p.name, p.type, p.city
                ORDER BY total_donated DESC
                LIMIT 10
            """
        },
        {
            "title": "Q14 — Food items expiring soon (next 30 days)",
            "sql": """
                SELECT food_name, quantity, expiry_date, location, food_type
                FROM food_listings
                WHERE expiry_date BETWEEN DATE('now') AND DATE('now', '+30 days')
                ORDER BY expiry_date ASC
                LIMIT 20
            """
        },
        {
            "title": "Q15 — Monthly claim trend",
            "sql": """
                SELECT strftime('%Y-%m', timestamp) AS month,
                       COUNT(*) AS total_claims,
                       SUM(CASE WHEN status='Completed' THEN 1 ELSE 0 END) AS completed,
                       SUM(CASE WHEN status='Pending'   THEN 1 ELSE 0 END) AS pending,
                       SUM(CASE WHEN status='Cancelled' THEN 1 ELSE 0 END) AS cancelled
                FROM claims
                GROUP BY month
                ORDER BY month
            """
        },
    ]

    for i, q in enumerate(QUERIES):
        with st.expander(f"**{q['title']}**"):

            # Optional city filter for Q3
            sql = q['sql']
            if q.get("city_filter"):
                cities_list = run_query("SELECT DISTINCT city FROM providers ORDER BY city")['city'].tolist()
                chosen_city = st.selectbox("Select city", cities_list, key=f"city_{i}")
                sql = f"""
                    SELECT name, type, city, contact
                    FROM providers
                    WHERE city = '{chosen_city}'
                    ORDER BY name
                """

            # Show SQL
            st.code(sql.strip(), language="sql")

            # Run & display
            try:
                result = run_query(sql)
                st.dataframe(result, use_container_width=True)

                # Auto chart for numeric results
                num_cols = result.select_dtypes('number').columns.tolist()
                str_cols = result.select_dtypes('object').columns.tolist()
                if num_cols and str_cols and len(result) > 1 and len(result) <= 30:
                    fig = px.bar(result, x=str_cols[0], y=num_cols[0],
                                 color_discrete_sequence=["#52b788"])
                    fig.update_layout(margin=dict(t=5,b=5), height=280, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Query error: {e}")

elif page == "✏️  CRUD Operations":
    st.title("✏️ CRUD Operations")
    st.caption("Add, Update, or Delete records directly in MySQL")

    tab_add, tab_update, tab_delete, tab_view = st.tabs([
        "➕ Add Food Listing",
        "✏️ Update Record",
        "🗑️ Delete Record",
        "👁️ View Live Table"
    ])

    # ── ADD ──────────────────────────────────────────
    with tab_add:
        st.markdown('<p class="section-title">Add a New Food Listing</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        food_name    = c1.text_input("Food Name")
        quantity     = c2.number_input("Quantity", min_value=1, value=10)
        expiry_date  = c1.date_input("Expiry Date")
        provider_id  = c2.number_input("Provider ID", min_value=1, value=1)
        prov_type    = c1.selectbox("Provider Type", ["Restaurant","Grocery Store","Supermarket","Catering Service"])
        location     = c2.text_input("Location / City")
        food_type    = c1.selectbox("Food Type", ["Vegetarian","Non-Vegetarian","Vegan"])
        meal_type    = c2.selectbox("Meal Type", ["Breakfast","Lunch","Dinner","Snacks"])

        if st.button("➕ Add Listing", type="primary"):
            if food_name and location:
                try:
                    with engine.connect() as conn:
                        conn.execute(text("""
                            INSERT INTO food_listings
                            (food_name, quantity, expiry_date, provider_id,
                             provider_type, location, food_type, meal_type)
                            VALUES (:fn, :qty, :exp, :pid, :pt, :loc, :ft, :mt)
                        """), {
                            "fn":food_name, "qty":quantity, "exp":str(expiry_date),
                            "pid":provider_id,  "pt":prov_type, "loc":location,
                            "ft":food_type,     "mt":meal_type
                        })
                        conn.commit()
                    st.success(f"✅ '{food_name}' added to food_listings!")
                    load_food_data.clear()
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please fill in Food Name and Location.")

    # ── UPDATE ───────────────────────────────────────
    with tab_update:
        st.markdown('<p class="section-title">Update Food Listing Quantity</p>', unsafe_allow_html=True)
        food_ids = run_query("SELECT food_id, food_name, quantity FROM food_listings ORDER BY food_id LIMIT 100")
        food_ids['label'] = food_ids.apply(lambda r: f"ID {r['food_id']} — {r['food_name']} (qty: {r['quantity']})", axis=1)
        sel_label = st.selectbox("Select Food Item", food_ids['label'].tolist())
        sel_row   = food_ids[food_ids['label'] == sel_label].iloc[0]
        new_qty   = st.number_input("New Quantity", min_value=0, value=int(sel_row['quantity']))

        if st.button("✅ Update Quantity", type="primary"):
            try:
                with engine.connect() as conn:
                    conn.execute(text(
                        "UPDATE food_listings SET quantity = :q WHERE food_id = :id"
                    ), {"q": new_qty, "id": int(sel_row['food_id'])})
                    conn.commit()
                st.success(f"✅ Quantity updated to {new_qty}!")
                load_food_data.clear()
            except Exception as e:
                st.error(f"Error: {e}")

        st.divider()
        st.markdown('<p class="section-title">Update Claim Status</p>', unsafe_allow_html=True)
        claims_df = run_query("SELECT claim_id, food_id, status FROM claims ORDER BY claim_id LIMIT 100")
        claims_df['label'] = claims_df.apply(lambda r: f"Claim {r['claim_id']} — Food ID {r['food_id']} [{r['status']}]", axis=1)
        sel_claim  = st.selectbox("Select Claim", claims_df['label'].tolist())
        claim_row  = claims_df[claims_df['label'] == sel_claim].iloc[0]
        new_status = st.selectbox("New Status", ["Pending","Completed","Cancelled"],
                                  index=["Pending","Completed","Cancelled"].index(claim_row['status']))

        if st.button("✅ Update Claim Status", type="primary"):
            try:
                with engine.connect() as conn:
                    conn.execute(text(
                        "UPDATE claims SET status = :s WHERE claim_id = :id"
                    ), {"s": new_status, "id": int(claim_row['claim_id'])})
                    conn.commit()
                st.success(f"✅ Claim {int(claim_row['claim_id'])} updated to '{new_status}'!")
            except Exception as e:
                st.error(f"Error: {e}")

    with tab_delete:
        st.markdown('<p class="section-title">Delete a Food Listing</p>', unsafe_allow_html=True)
        del_id = st.number_input("Enter Food ID to delete", min_value=1, value=1)
        check  = run_query(f"SELECT * FROM food_listings WHERE food_id = {int(del_id)}")

        if not check.empty:
            row = check.iloc[0]
            st.warning(f"⚠️ You are about to delete: **{row['food_name']}** | Qty: {row['quantity']} | City: {row['location']}")
        else:
            st.info("No food listing found with that ID.")

        if st.button("🗑️ Delete Listing", type="primary") and not check.empty:
            try:
                with engine.connect() as conn:
                    conn.execute(text("DELETE FROM food_listings WHERE food_id = :id"), {"id": int(del_id)})
                    conn.commit()
                st.success(f"✅ Food ID {int(del_id)} deleted successfully!")
                load_food_data.clear()
            except Exception as e:
                st.error(f"Error: {e}")

    # ── VIEW ─────────────────────────────────────────
    with tab_view:
        st.markdown('<p class="section-title">Live food_listings table (latest 50)</p>', unsafe_allow_html=True)
        live = run_query("SELECT * FROM food_listings ORDER BY food_id DESC LIMIT 50")
        st.dataframe(live, use_container_width=True)

elif page == "📈 EDA & Charts":
    st.title("📈 Exploratory Data Analysis")

    tab1, tab2, tab3, tab4 = st.tabs(["🍱 Food","🏪 Providers","🤝 Receivers","📦 Claims"])

    with tab1:
        c1, c2 = st.columns(2)

        ft = run_query("SELECT food_type, COUNT(*) AS count FROM food_listings GROUP BY food_type")
        fig = px.pie(ft, values='count', names='food_type', hole=0.4,
                     title="Food Type Mix",
                     color_discrete_sequence=["#52b788","#95d5b2","#b7e4c7"])
        c1.plotly_chart(fig, use_container_width=True)

        mt = run_query("SELECT meal_type, COUNT(*) AS count FROM food_listings GROUP BY meal_type ORDER BY count DESC")
        fig2 = px.bar(mt, x='meal_type', y='count', title="Meal Type Count",
                      color='meal_type', color_discrete_sequence=px.colors.qualitative.Pastel)
        c2.plotly_chart(fig2, use_container_width=True)

        qty_hist = run_query("SELECT quantity FROM food_listings")
        fig3 = px.histogram(qty_hist, x='quantity', nbins=30,
                            title="Quantity Distribution", color_discrete_sequence=["#40916c"])
        st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)

        pt = run_query("SELECT type, COUNT(*) AS count FROM providers GROUP BY type")
        fig = px.pie(pt, values='count', names='type', hole=0.4,
                     title="Provider Types", color_discrete_sequence=px.colors.qualitative.Safe)
        c1.plotly_chart(fig, use_container_width=True)

        pc = run_query("""SELECT city, COUNT(*) AS count FROM providers
                          GROUP BY city ORDER BY count DESC LIMIT 10""")
        fig2 = px.bar(pc, x='city', y='count', title="Top 10 Provider Cities",
                      color_discrete_sequence=["#e07b2a"])
        c2.plotly_chart(fig2, use_container_width=True)

    with tab3:
        c1, c2 = st.columns(2)

        rt = run_query("SELECT type, COUNT(*) AS count FROM receivers GROUP BY type")
        fig = px.pie(rt, values='count', names='type', hole=0.4,
                     title="Receiver Types", color_discrete_sequence=px.colors.qualitative.Antique)
        c1.plotly_chart(fig, use_container_width=True)

        rc = run_query("""SELECT city, COUNT(*) AS count FROM receivers
                          GROUP BY city ORDER BY count DESC LIMIT 10""")
        fig2 = px.bar(rc, x='city', y='count', title="Top 10 Receiver Cities",
                      color_discrete_sequence=["#2196f3"])
        c2.plotly_chart(fig2, use_container_width=True)

    with tab4:
        c1, c2 = st.columns(2)

        cs = run_query("SELECT status, COUNT(*) AS count FROM claims GROUP BY status")
        fig = px.pie(cs, values='count', names='status', hole=0.4,
                     title="Claim Status",
                     color_discrete_map={"Completed":"#52b788","Pending":"#f4a261","Cancelled":"#e76f51"})
        c1.plotly_chart(fig, use_container_width=True)

        monthly = run_query("""
            SELECT strftime('%Y-%m', timestamp) AS month,
            COUNT(*) AS claims
            FROM claims
            GROUP BY month
            ORDER BY month
        """)
        fig2 = px.line(monthly, x='month', y='claims', markers=True,
                       title="Claims Over Time", color_discrete_sequence=["#40916c"])
        c2.plotly_chart(fig2, use_container_width=True)

        # Summary stats
        st.divider()
        total  = run_query("SELECT COUNT(*) AS n FROM claims").iloc[0,0]
        done   = run_query("SELECT COUNT(*) AS n FROM claims WHERE status='Completed'").iloc[0,0]
        pend   = run_query("SELECT COUNT(*) AS n FROM claims WHERE status='Pending'").iloc[0,0]
        canc   = run_query("SELECT COUNT(*) AS n FROM claims WHERE status='Cancelled'").iloc[0,0]

        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Total Claims",   f"{total:,}")
        c2.metric("✅ Completed",   f"{done:,}",  f"{done/total*100:.1f}%")
        c3.metric("⏳ Pending",     f"{pend:,}",  f"{pend/total*100:.1f}%")
        c4.metric("❌ Cancelled",   f"{canc:,}",  f"{canc/total*100:.1f}%")