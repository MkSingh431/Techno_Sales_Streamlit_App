import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import base64
import os
import folium
from streamlit_folium import st_folium


st.set_page_config(page_title='Techno Sales!!!', page_icon=':bar_chart', layout='wide')
st.title('Techno Sales Analysis!!!')
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
                data = f.read()
        return base64.b64encode(data).decode()

def set_background_image(image_path):
        base64_str = get_base64_of_bin_file(image_path)
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{base64_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

def set_background_color(color):
        css = f"""
        <style>
        .stApp {{
            background: {color};
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

# import the data
data=pd.read_csv('Complete_Techno_Sales_Data.csv')
data['Order_Date'] = pd.to_datetime(data['Order_Date'], errors='coerce')
data = data.dropna(subset=['Order_Date']).copy()
data['Year'] = data['Order_Date'].dt.year

# Apply white background
set_background_color('white')

if "status_filter" not in st.session_state:
    st.session_state["status_filter"] = []
if "supervisor_filter" not in st.session_state:
    st.session_state["supervisor_filter"] = []
if "year_filter" not in st.session_state:
    st.session_state["year_filter"] = []
if "brand_filter" not in st.session_state:
    st.session_state["brand_filter"] = []

def clear_all_filters():
    st.session_state["status_filter"] = []
    st.session_state["supervisor_filter"] = []
    st.session_state["year_filter"] = []
    st.session_state["brand_filter"] = []

def select_supervisor(supervisor_name):
    st.session_state["supervisor_filter"] = [supervisor_name]

# Initial Sidebar setup
with st.sidebar:
    logo_path = "techno logo.jpg"
    if os.path.exists(logo_path):
        st.image(logo_path, width=100)
    st.title('Choose your Filters')

    st.subheader('Select Status')
    status_options = sorted(data['Status'].dropna().unique())
    status = st.multiselect('Status', status_options, key="status_filter")

    st.subheader('Select Supervisor')
    supervisor_options = sorted(data['Assigned Supervisor'].dropna().unique())
    supervisor = st.multiselect('Supervisor', supervisor_options, key="supervisor_filter")

    st.subheader("Select Years")
    years = sorted(data['Year'].dropna().astype(int).unique().tolist())
    selected_years = st.multiselect("Pick your Year(s)", years, key="year_filter")

    st.subheader("Select Brands")
    brand_options = sorted(data['Brand'].dropna().unique())
    brand = st.multiselect('Brand', brand_options, key="brand_filter")

    st.button("Clear All Filters", use_container_width=True, on_click=clear_all_filters)

filtered_data = data.copy()
if status:
    filtered_data = filtered_data[filtered_data['Status'].isin(status)]
if supervisor:
    filtered_data = filtered_data[filtered_data['Assigned Supervisor'].isin(supervisor)]
if selected_years:
    filtered_data = filtered_data[filtered_data['Year'].isin(selected_years)]
if brand:
    filtered_data = filtered_data[filtered_data['Brand'].isin(brand)]
    
    
    

    
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    with st.container(border=True):
        total_sales=filtered_data['Total_Sales'].sum()
        label_color="#F18C10"
        value_color="#0047AB"
        html_metrics = f"""
        <div>
        <p style="color: {label_color}; font-size: 25px; margin: 0;">Total Sales</p>
        <h style="color: {value_color}; font-size: 20px; margin: 0;">${total_sales:,.2f}</h>
        </div>
        """
        st.markdown(html_metrics, unsafe_allow_html=True)
        
with col2:
    with st.container(border=True):
     total_profit=filtered_data['Total_Profit'].sum()
     label_color="#F18C10"
     value_color="#0047AB"
     html_metrics=f"""
     <div>
     <p style="color: {label_color}; font-size: 25px; margin: 0;">Total Profit</p>
     <h style="color: {value_color}; font-size: 20px; margin: 0;">${total_profit:,.2f}</h>
     </div>
     """
     st.markdown(html_metrics, unsafe_allow_html=True)
     

with col3:
    with st.container(border=True):
     total_cost=filtered_data['Total_Cost'].sum()
     label_color="#F18C10"
     value_color="#0047AB"
     html_metrics=f"""
     <div>
     <p style="color: {label_color}; font-size: 25px; margin: 0;">Total Cost</p>
     <h style="color: {value_color}; font-size: 20px; margin: 0;">${total_cost:,.2f}</h>
     </div>
     """
     st.markdown(html_metrics, unsafe_allow_html=True)
     
with col4:
    with st.container(border=True):
     total_quantity=filtered_data['Quantity'].sum()
     label_color="#F18C10"
     value_color="#0047AB"
     html_metrics=f"""
     <div>
     <p style="color: {label_color}; font-size: 25px; margin: 0;">Total Quantity</p>
     <h style="color: {value_color}; font-size: 20px; margin: 0;">{total_quantity:,.2f}</h>
     </div>
     """
     st.markdown(html_metrics, unsafe_allow_html=True)
     
with col5:
    with st.container(border=True): 
     total_customer=filtered_data['Customer_Name'].count()
     label_color="#F18C10"
     value_color="#0047AB"
     html_metrics=f""" 
     <div>
     <p style="color: {label_color}; font-size: 25px; margin: 0;">Total Customer</p>
     <h style="color: {value_color}; font-size: 20px; margin: 0;">{total_customer:,.2f}</h>
     </div>
     """
     st.markdown(html_metrics, unsafe_allow_html=True)
     
st.divider()
     
col1, col2,col3,col4,col5,col6 = st.columns(6)
supervisor_cards = [
    {"name": "Aarvi Gupta", "image": "aarvi.jpg"},
    {"name": "Aadil Khan", "image": "adil_khan.png"},
    {"name": "Advika Joshi", "image": "advika.png"},
    {"name": "Ajay Sharma", "image": "ajay.png"},
    {"name": "Roshan Kumar", "image": "roshan.jpg"},
    {"name": "Vijay Singh", "image": "vijay.jpg"},
]

for col, card in zip([col1, col2, col3, col4, col5, col6], supervisor_cards):
    with col:
        with st.container(border=True):
            if os.path.exists(card["image"]):
                st.image(card["image"], use_container_width=True)
            else:
                st.write("Image not found")

            button_key = f"supervisor_btn_{card['name'].replace(' ', '_')}"
            st.button(
                card["name"],
                key=button_key,
                use_container_width=True,
                on_click=select_supervisor,
                args=(card["name"],),
            )

            if card["name"] in st.session_state.get("supervisor_filter", []):
                st.caption("Selected")
  
st.divider()

    
     
chart1, chart2 = st.columns(2)

with chart1:
    # Grammar fix: "Category wise" -> "by Category"
    st.markdown("### Total Sales by Category")
    
    # FIX 1: Sort the values descending so the best performers are first
    sales_by_category = filtered_data.groupby('Category')['Total_Sales'].sum().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # FIX 2: Safe color mapping. It repeats the palette if you have more categories than colors.
    base_colors = ['#FEC125', '#0047AB', '#FF5733', '#33FF57', '#8A2BE2', '#FFD700', 
                   '#00FFFF', '#FF69B4', '#A52A2A', '#5F9EA0', '#D2691E', '#FF7F54']
    safe_colors = [base_colors[i % len(base_colors)] for i in range(len(sales_by_category))]
    
    bars = ax.bar(
        sales_by_category.index,
        sales_by_category.values,
        color=safe_colors,
        width=0.6
    )
    
    plt.xticks(fontsize=12, color="#2AA3EF", rotation=45, ha='right')
    plt.yticks(fontsize=12, color="#318DF7")
    
    # Removed plt.yticks() because the y-axis is hidden anyway
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.yaxis.set_visible(False)
    
    fig.patch.set_alpha(0)
    ax.set_facecolor('none')
    plt.tight_layout()
    
    st.pyplot(fig)  

with chart2:
    st.markdown("### Total Profit by Category")
    
    sale_by_Brand=filtered_data.groupby('Brand')['Total_Profit'].sum().sort_values(ascending=False)
    
    fig ,ax = plt.subplots(figsize=(6,4))
    
    bars=ax.bar(
     sale_by_Brand.index,
     sale_by_Brand.values,
     color=['#F18C10','#0047AB','#FF5733','#33FF51','#8A2BE2','#FFD700','#00FFFF','#FF69B4','#A52A2A','#5F9EA0']
    )
    
    plt.xticks(fontsize=12,color="#2982EE",rotation=45,ha='right')
    plt.yticks(fontsize=12,color="#318DF7")
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_visible(False)
    
    fig.patch.set_alpha(0)
    ax.set_facecolor('none')
    plt.tight_layout()
    
    st.pyplot(fig)
    
view1, view2 = st.columns(2)

with view1:
    with st.expander("Sales by Category"):
     sales_cat=filtered_data.groupby('Category')['Total_Sales'].sum().reset_index()  
     
     style_df=sales_cat.style.background_gradient(cmap='YlOrRd',subset=['Total_Sales']).format({'Total_Sales':'${:,.2f}'})
     
     st.dataframe(style_df,use_container_width=True)
     
with view2:
 with st.expander("Profit by Category"):
     profit_cat=filtered_data.groupby('Category')['Total_Profit'].sum().reset_index()
     
     style_df=profit_cat.style.background_gradient(cmap='Blues',subset=['Total_Profit']).format({'Total_Profit':'${:,.2f}'})
     
     st.dataframe(style_df,use_container_width=True )
    
st.divider()

chart3, chart4 = st.columns(2)

with chart3:
    st.markdown("### Total Sale by Brand")
    
    sales_brand=filtered_data.groupby('Brand')['Total_Sales'].sum().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    
    bars=ax.bar(
     
     sales_brand.index,
     sales_brand.values,
     color=['#F18C10','#0047AB','#FF5733','#33FF53','#8A2BE2','#FFD878','#00FFFF','#FF69B4','#A52A2A','#5F9EA0'],
     width=0.6
    
    )
    
    plt.xticks(fontsize=12,color="#2982EE",rotation=45,ha='right')
    plt.yticks(fontsize=12,color="#318DF7")
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_visible(False)
    
    fig.patch.set_alpha(0)
    ax.set_facecolor('none')
    plt.tight_layout()
    
    st.pyplot(fig)


with chart4:
    st.markdown("### Total Profit by Brand")
    
    profit_brand=filtered_data.groupby('Brand')['Total_Profit'].sum().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    
    bars=ax.bar(
     
     profit_brand.index,
     profit_brand.values,
     color=['#F18C10','#0047AB','#FF5733','#33FF55','#8A2BE2','#FFD700','#00FFFF','#FF69B8','#A52A2A','#5F9EA9'],
     width=0.6
    )
    
    
    plt.xticks(fontsize=12,color="#2982EE",rotation=45,ha='right')
    plt.yticks(fontsize=12,color="#318DF7")
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_visible(False)
    
    fig.patch.set_alpha(0)
    ax.set_facecolor('none')
    plt.tight_layout()
    
    st.pyplot(fig)


view3, view4 = st.columns(2)

with view3:
    with st.expander("Sales by Brand"):
     sales_brand=filtered_data.groupby('Brand')['Total_Sales'].sum().reset_index()  
     
     style_df=sales_brand.style.background_gradient(cmap='Greens',subset=['Total_Sales']).format({'Total_Sales':'${:,.2f}'})
     
     st.dataframe(style_df,use_container_width=True)
     
with view4:
 with st.expander("Profit by Brand"):
     profit_brand=filtered_data.groupby('Brand')['Total_Profit'].sum().reset_index()
     
     style_df=profit_brand.style.background_gradient(cmap='Greens',subset=['Total_Profit']).format({'Total_Profit':'${:,.2f}'})
     
     st.dataframe(style_df,use_container_width=True )
     
st.divider()     

chart5, chart6 = st.columns(2)

with chart5:
    st.markdown("### Total Sales by Status")
    
    # 1. Aggregation
    status_by_sales = filtered_data.groupby('Status')['Total_Sales'].sum()
    
    # 2. Creating the figure
    fig, ax = plt.subplots(figsize=(6, 6)) # Square aspect ratio is better for circles
    
    # 3. Plotting the Pie Chart
    # We include 'autopct' to show percentages—the only way to make a pie chart "truthful"
    colors = ['#F18C10', '#0047AB', '#FF5733', '#33FF46']
    
    wedges, texts, autotexts = ax.pie(
        status_by_sales.values, 
        labels=status_by_sales.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        pctdistance=0.85, # Moves percentages inside the wedges
        textprops={'color':"w", 'weight':'bold'}
    )

    # 4. Optional: Turn it into a Donut Chart for a modern look
    # This provides a "center of gravity" for the visual
    centre_circle = plt.Circle((0,0), 0.70, fc='none', edgecolor='none')
    fig.gca().add_artist(centre_circle)

    # 5. UI Cleanup for Dark Theme
    fig.patch.set_alpha(0)
    ax.set_facecolor('none')
    plt.tight_layout()
    
    st.pyplot(fig)
 

with chart6:
    st.markdown("### Total Profit by Status")
    
    status_by_profit=filtered_data.groupby('Status')['Total_Profit'].sum()
    
    fig, ax = plt.subplots(figsize=(6, 6))
    
    colors = ['#F18C10', '#004745', "#33A3FF", '#33FF46']
    
    wedges, texts, autotexts = ax.pie(
        status_by_profit.values, 
        labels=status_by_profit.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        pctdistance=0.85,
        textprops={'color':"w", 'weight':'bold'}
    )
    
    centre_circle=plt.Circle((0,0),0.70,fc='none',edgecolor='none')
    fig.gca().add_artist(centre_circle)
    
    fig.patch.set_alpha(0)
    ax.set_facecolor('none')
    plt.tight_layout()
    
    st.pyplot(fig)

 
view5, view6 = st.columns(2)

with view5:
    with st.expander("Sales by Status"):
     sales_status=filtered_data.groupby('Status')['Total_Sales'].sum().reset_index()
     
     style_df=sales_status.style.background_gradient(cmap='BuGn_r',subset=['Total_Sales']).format({'Total_Sales':'${:,.2f}'})
     
     st.dataframe(style_df,use_container_width=True)
     
with view6:
 with st.expander("Profit by Status"):
     profit_status=filtered_data.groupby('Status')['Total_Profit'].sum().reset_index()
     
     style_df=profit_status.style.background_gradient(cmap='BuGn_r',subset=['Total_Profit']).format({'Total_Profit':'${:,.2f}'})
     
     st.dataframe(style_df,use_container_width=True )
     
st.divider()

chart7, chart8=st.columns(2)

with chart7:
    total_cost=filtered_data.groupby('Category')['Total_Cost'].sum().sort_values(ascending=False)
    st.markdown("### Total Cost by Category")
    
    fig, ax = plt.subplots(figsize=(6, 4))
    
    bars=ax.bar(
     total_cost.index,
     total_cost.values,
     color=['#F18C10','#0047AB','#FF5733','#33FF57','#8A2BE2','#FFD856','#00FFFF','#FF69B4','#A52A2A','#5F9EA0','#D2691E','#FF7F55'],
     width=0.6
    )
    plt.xticks(fontsize=12,color="#2982EE",rotation=45,ha='right')
    
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_visible(False)
    
    fig.patch.set_alpha(0)
    ax.set_facecolor('none')
    plt.tight_layout()
    
    st.pyplot(fig)

with chart8:
    total_cost=filtered_data.groupby('Brand')['Total_Cost'].sum().sort_values(ascending=False)
    st.markdown("### Total Cost by Brand")
    
    fig, ax = plt.subplots(figsize=(6, 4))
    
    bars=ax.bar(
     total_cost.index,
     total_cost.values,
     color=['#F18C10','#0047AB','#FF5733','#33FF58','#8A2BE2','#FFD700','#00FFFF','#FF69B4','#A52A2A','#5F9EA0','#D2691E','#FF7F54'],
     width=0.6
    
    )
    
    plt.xticks(fontsize=12,color="#2982EE",rotation=45,ha='right')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_visible(False)
    
    fig.patch.set_alpha(0)
    ax.set_facecolor('none')
    plt.tight_layout()
    
    st.pyplot(fig)
    
view7, view8 = st.columns(2)

with view7:
    with st.expander("Total Cost by Category"):
     total_cost=filtered_data.groupby('Category')['Total_Cost'].sum().reset_index()
     
     style_df=total_cost.style.background_gradient(cmap='BuGn_r',subset=['Total_Cost']).format({'Total_Cost':'${:,.2f}'})
     
     st.dataframe(style_df,use_container_width=True)
     
with view8:
   with st.expander("Total Cost by Brand"):
    total_cost=filtered_data.groupby('Brand')['Total_Cost'].sum().reset_index()
    
    style_df=total_cost.style.background_gradient(cmap='BuGn_r',subset=['Total_Cost']).format({'Total_Cost':'${:,.2f}'})
    
    st.dataframe(style_df,use_container_width=True)


                  
# 1. Define the complete mapping dictionary
state_mapping = {
    'AP': 'Andhra Pradesh',        'AR': 'Arunachal Pradesh',  'AS': 'Assam',
    'BR': 'Bihar',                 'CG': 'Chhattisgarh',       'JK': 'Jammu and Kashmir',
    'JH': 'Jharkhand',             'KA': 'Karnataka',          'KL': 'Kerala',
    'MN': 'Manipur',               'ML': 'Meghalaya',          'MZ': 'Mizoram',
    'NL': 'Nagaland',              'OR': 'Odisha',             'PB': 'Punjab',
    'RJ': 'Rajasthan',             'SK': 'Sikkim',             'TN': 'Tamil Nadu',
    'TR': 'Tripura',               'UK': 'Uttarakhand',        'UP': 'Uttar Pradesh',
    'WB': 'West Bengal',           'AN': 'Andaman and Nicobar Islands',
    'CH': 'Chandigarh',            'GA': 'Goa',                'GJ': 'Gujarat',
    'MP': 'Madhya Pradesh',        'MH': 'Maharashtra',        'DH': 'Dadra and Nagar Haveli',
    'DD': 'Daman and Diu',         'DL': 'Delhi',              'LD': 'Lakshadweep',
    'PY': 'Puducherry',            'HR': 'Haryana',            'HP': 'Himachal Pradesh'
}

# 2. Apply the replacement to your DataFrame
# This creates a new 'State_Name' column while preserving the original codes
data['State_Name'] = data['State_Code'].map(state_mapping)

# 3. Check for any unmapped codes (Truth Check)
if data['State_Name'].isnull().any():
    unmapped = data[data['State_Name'].isnull()]['State_Code'].unique()
    st.warning(f"Warning: These codes were not found in the map: {unmapped}")

state_coordinates = {
    "AN": (11.7401, 92.6586),
    "AP": (15.9129, 79.7400),
    "AR": (28.2180, 94.7278),
    "AS": (26.2006, 92.9376),
    "BR": (25.0961, 85.3131),
    "CG": (21.2787, 81.8661),
    "CH": (30.7333, 76.7794),
    "DD": (20.4283, 72.8397),
    "DH": (20.1809, 73.0169),
    "DL": (28.7041, 77.1025),
    "GA": (15.2993, 74.1240),
    "GJ": (22.2587, 71.1924),
    "HP": (31.1048, 77.1734),
    "HR": (29.0588, 76.0856),
    "JH": (23.6102, 85.2799),
    "JK": (33.7782, 76.5762),
    "KA": (15.3173, 75.7139),
    "KL": (10.8505, 76.2711),
    "LD": (10.5667, 72.6417),
    "MH": (19.7515, 75.7139),
    "ML": (25.4670, 91.3662),
    "MN": (24.6637, 93.9063),
    "MP": (22.9734, 78.6569),
    "MZ": (23.1645, 92.9376),
    "NL": (26.1584, 94.5624),
    "OR": (20.9517, 85.0985),
    "PB": (31.1471, 75.3412),
    "PY": (11.9416, 79.8083),
    "RJ": (27.0238, 74.2179),
    "SK": (27.5330, 88.5122),
    "TN": (11.1271, 78.6569),
    "TR": (23.9408, 91.9882),
    "UK": (30.0668, 79.0193),
    "UP": (26.8467, 80.9462),
    "WB": (22.9868, 87.8550),
}

st.divider()
st.markdown("### Total Sales Map by State Name")

# 1. Concise Data Prep: Group and Map in one flow
state_sales_map = filtered_data.groupby("State_Code", as_index=False)["Total_Sales"].sum()
max_sales = state_sales_map["Total_Sales"].max() or 1

# 2. Functional Mapping for Names and Coordinates
state_sales_map["Name"] = state_sales_map["State_Code"].map(state_mapping)
state_sales_map["Coords"] = state_sales_map["State_Code"].map(state_coordinates)
state_sales_map = state_sales_map.dropna(subset=["Coords"])

# 3. Layout & Render
m_col, t_col = st.columns([2, 1])

with m_col:
    m = folium.Map(location=[22.97, 78.65], zoom_start=4, tiles='cartodbpositron ')
    
    for _, r in state_sales_map.iterrows():
        # Clean scaling logic: (Value / Max * Scale) + Min
        rad = (r["Total_Sales"] / max_sales * 25) + 5
        folium.CircleMarker(
            location=r["Coords"], radius=rad, color='#DAA520', fill=True, fill_opacity=0.6,
            popup=f"<b>{r['Name']}</b>: ${r['Total_Sales']:,.0f}", tooltip=r['Name']
        ).add_to(m)
    
    st_folium(m, width=700, height=400, returned_objects=[])

with t_col:
    st.markdown("### Top States")
    st.dataframe(state_sales_map.nlargest(15, 'Total_Sales')[["Name", "Total_Sales"]], 
                 column_config={"Total_Sales": st.column_config.NumberColumn(format="$%1.0f")},
                 hide_index=True)
    
st.divider()

