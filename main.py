import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json

# Configure the page
st.set_page_config(page_title="Acolyte Lead Management", layout="wide")

# Initialize session state for data persistence
if 'leads' not in st.session_state:
    st.session_state.leads = pd.DataFrame({
        # Basic Institution Information
        'institution_name': [],
        'institution_type': [],  # Medical College/Dental College/Other
        'ownership': [],  # Private/Government/Society
        'establishment_year': [],
        'accreditation_status': [],  # NMC Approved, etc.
        
        # Contact Information
        'primary_contact_name': [],
        'primary_contact_role': [],
        'primary_contact_email': [],
        'primary_contact_phone': [],
        'secondary_contact_name': [],
        'secondary_contact_role': [],
        
        # Location Information
        'territory': [],
        'city': [],
        'address': [],
        
        # Institution Details
        'category': [],  # Premium/Mid-tier/Budget
        'current_student_count': [],
        'max_student_capacity': [],
        'current_lms_provider': [],
        'contract_renewal_date': [],
        
        # Lead Details
        'lead_source': [],  # Conference/Referral/Direct/Digital
        'lead_owner': [],   # Sales rep name
        'first_contact_date': [],
        'last_contact_date': [],
        'next_follow_up_date': [],
        'stage': [],        # New/Contacted/Qualified/Demo/Proposal/Negotiation/Closed
        'stage_change_date': [],
        'probability': [],  # Success probability percentage
        
        # Product Interest
        'interested_modules': [],  # Student/Faculty/Institution
        'feature_requirements': [],
        'technical_requirements': [],
        
        # Financial Information
        'proposed_pricing_tier': [],
        'student_price_monthly': [],
        'total_deal_value_annual': [],
        'payment_preference': [],  # Monthly/Quarterly/Annual
        'budget_confirmed': [],    # Yes/No
        
        # Timeline
        'demo_scheduled_date': [],
        'proposal_sent_date': [],
        'expected_close_date': [],
        'actual_close_date': [],
        
        # Notes and Activities
        'last_activity': [],
        'next_steps': [],
        'decision_makers': [],
        'competitors_involved': [],
        'pain_points': [],
                'notes': [],
                #Price
                'monthly_price': [],
                'total_deal_value_annual': []
    })

def calculate_deal_metrics(student_count, category, payment_preference):
    """Calculate deal metrics based on Acolyte's pricing structure"""
    # Base monthly price calculation
    if student_count >= 1000:
        monthly_price = 300
    elif student_count >= 500:
        monthly_price = 450
    else:
        monthly_price = 750
        
    # Apply payment preference adjustments
    if payment_preference == "Quarterly":
        monthly_price *= 0.9  # 10% discount
    elif payment_preference == "Annual":
        monthly_price *= 0.8  # 20% discount
        
    annual_value = monthly_price * 12 * student_count
    return monthly_price, annual_value
def calculate_deal_value(student_count, payment_preference):
    """Calculate monthly price and annual deal value based on Acolyte's pricing structure"""
    # Base monthly price calculation
    if student_count >= 1000:
        monthly_price = 300
    elif student_count >= 500:
        monthly_price = 450
    else:
        monthly_price = 750
        
    # Apply payment preference adjustments
    if payment_preference == "Quarterly":
        monthly_price *= 0.9  # 10% discount
    elif payment_preference == "Annual":
        monthly_price *= 0.8  # 20% discount
        
    annual_value = monthly_price * 12 * student_count
    return monthly_price, annual_value
def create_lead_form():
    """Create a detailed lead entry form"""
    with st.form("new_lead_form"):
        st.subheader("New Lead Entry Form")
        
        # Create tabs for organized data entry
        tab1, tab2, tab3, tab4 = st.tabs([
            "Basic Information",
            "Contact Details",
            "Product & Pricing",
            "Timeline & Notes"
        ])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                institution_name = st.text_input("Institution Name")
                institution_type = st.selectbox(
                    "Institution Type",
                    ["Medical College", "Dental College", "Other"]
                )
                ownership = st.selectbox(
                    "Ownership",
                    ["Private", "Government", "Society"]
                )
                establishment_year = st.number_input(
                    "Establishment Year",
                    min_value=1900,
                    max_value=datetime.now().year
                )
                
            with col2:
                territory = st.selectbox(
                    "Territory",
                    ["Bangalore Urban", "Bangalore Rural & Mysore",
                     "Mangalore & Coastal", "North Karnataka"]
                )
                city = st.text_input("City")
                category = st.selectbox(
                    "Category",
                    ["Premium Private", "Mid-tier Private", "Budget Private", "Government"]
                )
                accreditation_status = st.text_input("Accreditation Status")
                
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                primary_contact_name = st.text_input("Primary Contact Name")
                primary_contact_role = st.text_input("Primary Contact Role")
                primary_contact_email = st.text_input("Primary Contact Email")
                primary_contact_phone = st.text_input("Primary Contact Phone")
                
            with col2:
                secondary_contact_name = st.text_input("Secondary Contact Name")
                secondary_contact_role = st.text_input("Secondary Contact Role")
                decision_makers = st.text_area("Key Decision Makers")
                
        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                current_student_count = st.number_input("Current Student Count", min_value=0)
                max_student_capacity = st.number_input("Maximum Student Capacity", min_value=0)
                current_lms = st.text_input("Current LMS Provider (if any)")
                interested_modules = st.multiselect(
                    "Interested Modules",
                    ["Student Module", "Faculty Module", "Institution Module"]
                )
                
            with col2:
                payment_preference = st.selectbox(
                    "Payment Preference",
                    ["Monthly", "Quarterly", "Annual"]
                )
                budget_confirmed = st.selectbox("Budget Confirmed", ["Yes", "No"])
                competitors = st.text_area("Competitors Involved")
                
        with tab4:
            col1, col2 = st.columns(2)
            with col1:
                lead_source = st.selectbox(
                    "Lead Source",
                    ["Conference", "Referral", "Direct Outreach", "Digital Marketing", "Other"]
                )
                lead_owner = st.text_input("Lead Owner")
                stage = st.selectbox(
                    "Stage",
                    ["New", "Contacted", "Qualified", "Demo", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]
                )
                probability = st.slider("Success Probability (%)", 0, 100, 50)
                
            with col2:
                demo_date = st.date_input("Demo Scheduled Date")
                expected_close = st.date_input("Expected Close Date")
                next_follow_up = st.date_input("Next Follow-up Date")
                
            notes = st.text_area("Additional Notes")
            pain_points = st.text_area("Pain Points")
            next_steps = st.text_area("Next Steps")
            
        submitted = st.form_submit_button("Save Lead")
        
        if submitted:
            # Calculate pricing
            monthly_price, annual_value = calculate_deal_value(
            current_student_count, 
            payment_preference
        )
            
            # Create new lead entry
            new_lead = pd.DataFrame({
                'institution_name': [institution_name],
                'institution_type': [institution_type],
                'ownership': [ownership],
                'establishment_year': [establishment_year],
                'accreditation_status': [accreditation_status],
                'primary_contact_name': [primary_contact_name],
                'primary_contact_role': [primary_contact_role],
                'primary_contact_email': [primary_contact_email],
                'primary_contact_phone': [primary_contact_phone],
                'secondary_contact_name': [secondary_contact_name],
                'secondary_contact_role': [secondary_contact_role],
                'territory': [territory],
                'city': [city],
                'category': [category],
                'current_student_count': [current_student_count],
                'max_student_capacity': [max_student_capacity],
                'current_lms_provider': [current_lms],
                'lead_source': [lead_source],
                'lead_owner': [lead_owner],
                'first_contact_date': [datetime.now().date()],
                'last_contact_date': [datetime.now().date()],
                'next_follow_up_date': [next_follow_up],
                'stage': [stage],
                'stage_change_date': [datetime.now().date()],
                'probability': [probability],
                'interested_modules': [json.dumps(interested_modules)],
                'student_price_monthly': [monthly_price],
                'total_deal_value_annual': [annual_value],
                'payment_preference': [payment_preference],
                'budget_confirmed': [budget_confirmed],
                'demo_scheduled_date': [demo_date],
                'expected_close_date': [expected_close],
                'decision_makers': [decision_makers],
                'competitors_involved': [competitors],
                'pain_points': [pain_points],
                'notes': [notes],
                'next_steps': [next_steps],
                'monthly_price': [monthly_price],
                'total_deal_value_annual': [annual_value]
            })
            
            st.session_state.leads = pd.concat([st.session_state.leads, new_lead], ignore_index=True)
            st.success("Lead added successfully!")
            
def view_lead_dashboard():
    """Create a comprehensive lead viewing dashboard"""
    st.subheader("Lead Dashboard")
    
    if st.session_state.leads.empty:
        st.warning("No leads in the database yet.")
        return
        
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        territory_filter = st.multiselect(
            "Filter by Territory",
            options=st.session_state.leads['territory'].unique()
        )
    with col2:
        stage_filter = st.multiselect(
            "Filter by Stage",
            options=st.session_state.leads['stage'].unique()
        )
    with col3:
        category_filter = st.multiselect(
            "Filter by Category",
            options=st.session_state.leads['category'].unique()
        )
        
    # Apply filters
    filtered_leads = st.session_state.leads.copy()
    if territory_filter:
        filtered_leads = filtered_leads[filtered_leads['territory'].isin(territory_filter)]
    if stage_filter:
        filtered_leads = filtered_leads[filtered_leads['stage'].isin(stage_filter)]
    if category_filter:
        filtered_leads = filtered_leads[filtered_leads['category'].isin(category_filter)]
        
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Leads", len(filtered_leads))
    with col2:
        st.metric("Total Pipeline Value", f"₹{filtered_leads['total_deal_value_annual'].sum():,.2f}")
    with col3:
        st.metric("Avg Deal Size", 
                 f"₹{filtered_leads['total_deal_value_annual'].mean():,.2f}")
    with col4:
        weighted_pipeline = (filtered_leads['total_deal_value_annual'] * 
                           filtered_leads['probability'] / 100).sum()
        st.metric("Weighted Pipeline", f"₹{weighted_pipeline:,.2f}")
        
    # Pipeline visualization
    fig = go.Figure()
    stages = filtered_leads['stage'].unique()
    for stage in stages:
        stage_data = filtered_leads[filtered_leads['stage'] == stage]
        fig.add_trace(go.Bar(
            name=stage,
            y=[stage_data['total_deal_value_annual'].sum()],
            text=[f"₹{stage_data['total_deal_value_annual'].sum():,.0f}"],
            textposition='auto',
        ))
    fig.update_layout(
        title="Pipeline by Stage",
        yaxis_title="Total Value (₹)",
        barmode='group'
    )
    st.plotly_chart(fig)
    
    # Leads table with detailed view
    st.subheader("Lead Details")
    lead_view = filtered_leads[[
        'institution_name', 'territory', 'category', 'stage',
        'current_student_count', 'total_deal_value_annual',
        'probability', 'expected_close_date'
    ]].copy()
    
    # Add view details button
    if not lead_view.empty:
        selected_lead = st.selectbox(
            "Select Lead to View Details",
            lead_view['institution_name'].tolist()
        )
        
        if selected_lead:
            lead_details = filtered_leads[
                filtered_leads['institution_name'] == selected_lead
            ].iloc[0]
            
            with st.expander("Lead Details", expanded=True):
                tab1, tab2, tab3 = st.tabs([
                    "Institution Information",
                    "Contact Information",
                    "Pipeline Information"
                ])
                
                with tab1:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("Institution Type:", lead_details['institution_type'])
                        st.write("Ownership:", lead_details['ownership'])
                        st.write("Territory:", lead_details['territory'])
                        st.write("Category:", lead_details['category'])
                    with col2:
                        st.write("Current Students:", lead_details['current_student_count'])
                        st.write("Max Capacity:", lead_details['max_student_capacity'])
                        st.write("Current LMS:", lead_details['current_lms_provider'])
                        
                with tab2:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("Primary Contact:", lead_details['primary_contact_name'])
                        st.write("Role:", lead_details['primary_contact_role'])
                        st.write("Email:", lead_details['primary_contact_email'])
                        st.write("Phone:", lead_details['primary_contact_phone'])
                    with col2:
                        st.write("Secondary Contact:", lead_details['secondary_contact_name'])
                        st.write("Role:", lead_details['secondary_contact_role'])
                        st.write("Decision Makers:", lead_details['decision_makers'])
                        
                with tab3:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("Stage:", lead_details['stage'])
                        st.write("Probability:", f"{lead_details['probability']}%")
                        st.write("Monthly Price:", f"₹{lead_details['student_price_monthly']:,.2f}")
                        st.write("Annual Value:", f"₹{lead_details['total_deal_value_annual']:,.2f}")
                    with col2:
                        st.write("Demo Date:", lead_details['demo_scheduled_date'])
                        st.write("Expected Close:", lead_details['expected_close_date'])
                        st.write("Next Follow-up:", lead_details['next_follow_up_date'])
                        st.write("Payment Preference:", lead_details['payment_preference'])
                        
                # Additional sections for notes and updates
                with st.expander("Notes & Activities"):
                    st.write("Pain Points:", lead_details['pain_points'])
                    st.write("Competitors:", lead_details['competitors_involved'])
                    st.write("Next Steps:", lead_details['next_steps'])
                    st.write("Notes:", lead_details['notes'])
                    
                    # Add new activity log
                    st.subheader("Add Activity Log")
                    with st.form(f"activity_log_{selected_lead}"):
                        activity_type = st.selectbox(
                            "Activity Type",
                            ["Call", "Email", "Meeting", "Demo", "Proposal", "Other"]
                        )
                        activity_date = st.date_input("Activity Date", datetime.now())
                        activity_notes = st.text_area("Activity Notes")
                        next_follow_up = st.date_input("Next Follow-up Date")
                        new_stage = st.selectbox(
                            "Update Stage",
                            ["No Change"] + [
                                "New", "Contacted", "Qualified", "Demo", 
                                "Proposal", "Negotiation", "Closed Won", "Closed Lost"
                            ]
                        )
                        new_probability = st.slider(
                            "Update Success Probability (%)", 
                            0, 100, 
                            int(lead_details['probability'])
                        )
                        
                        update_submitted = st.form_submit_button("Update Lead")
                        
                        if update_submitted:
                            # Update lead information
                            idx = filtered_leads[
                                filtered_leads['institution_name'] == selected_lead
                            ].index[0]
                            
                            # Update notes with new activity
                            new_note = f"""
                            {datetime.now().strftime('%Y-%m-%d %H:%M')}
                            Activity: {activity_type}
                            Notes: {activity_notes}
                            """
                            current_notes = st.session_state.leads.at[idx, 'notes']
                            updated_notes = f"{new_note}\n---\n{current_notes}" if current_notes else new_note
                            
                            # Update lead information
                            st.session_state.leads.at[idx, 'notes'] = updated_notes
                            st.session_state.leads.at[idx, 'last_contact_date'] = activity_date
                            st.session_state.leads.at[idx, 'next_follow_up_date'] = next_follow_up
                            st.session_state.leads.at[idx, 'probability'] = new_probability
                            
                            if new_stage != "No Change":
                                st.session_state.leads.at[idx, 'stage'] = new_stage
                                st.session_state.leads.at[idx, 'stage_change_date'] = datetime.now().date()
                            
                            st.success("Lead updated successfully!")
                            st.rerun()
    if not lead_view.empty:
        col1, col2 = st.columns([3, 1])
        with col1:
            selected_lead = st.selectbox(
                "Select Lead to View Details",
                lead_view['institution_name'].tolist()
            )
        with col2:
            if st.button("Edit Selected Lead"):
                lead_data = filtered_leads[
                    filtered_leads['institution_name'] == selected_lead
                ].iloc[0]
                edit_lead_form(lead_data)
def show_lead_analytics():
    """Display detailed analytics about the lead pipeline"""
    st.subheader("Lead Analytics")
    
    if st.session_state.leads.empty:
        st.warning("No leads data available for analysis.")
        return
        
    # Time period filter
    col1, col2 = st.columns(2)
    with col1:
        date_range = st.selectbox(
            "Time Period",
            ["Last 30 Days", "Last Quarter", "Last 6 Months", "Year to Date", "All Time"]
        )
    
    # Filter data based on time period
    filtered_leads = st.session_state.leads.copy()
    today = datetime.now().date()
    
    if date_range == "Last 30 Days":
        filtered_leads = filtered_leads[
            pd.to_datetime(filtered_leads['first_contact_date']).dt.date >= 
            (today - timedelta(days=30))
        ]
    elif date_range == "Last Quarter":
        filtered_leads = filtered_leads[
            pd.to_datetime(filtered_leads['first_contact_date']).dt.date >= 
            (today - timedelta(days=90))
        ]
    elif date_range == "Last 6 Months":
        filtered_leads = filtered_leads[
            pd.to_datetime(filtered_leads['first_contact_date']).dt.date >= 
            (today - timedelta(days=180))
        ]
    elif date_range == "Year to Date":
        filtered_leads = filtered_leads[
            pd.to_datetime(filtered_leads['first_contact_date']).dt.date >= 
            datetime(today.year, 1, 1).date()
        ]
    
    # Summary metrics in cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_leads = len(filtered_leads)
        new_leads = len(filtered_leads[
            pd.to_datetime(filtered_leads['first_contact_date']).dt.date >= 
            (today - timedelta(days=30))
        ])
        st.metric("Total Leads", total_leads, f"+{new_leads} new")
        
    with col2:
        total_pipeline = filtered_leads['total_deal_value_annual'].sum()
        st.metric("Total Pipeline Value", f"₹{total_pipeline:,.2f}")
        
    with col3:
        avg_deal_size = filtered_leads['total_deal_value_annual'].mean()
        st.metric("Average Deal Size", f"₹{avg_deal_size:,.2f}")
        
    with col4:
        conversion_rate = (
            len(filtered_leads[filtered_leads['stage'] == 'Closed Won']) /
            len(filtered_leads) * 100
        ) if len(filtered_leads) > 0 else 0
        st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
    
    # Pipeline by stage
    st.subheader("Pipeline Stage Analysis")
    stage_data = filtered_leads.groupby('stage').agg({
        'total_deal_value_annual': 'sum',
        'institution_name': 'count'
    }).reset_index()
    
    fig = px.bar(stage_data, x='stage', y='total_deal_value_annual',
                title="Pipeline Value by Stage",
                labels={'total_deal_value_annual': 'Value (₹)', 'stage': 'Stage'})
    st.plotly_chart(fig)
    
    # Territory performance
    st.subheader("Territory Performance")
    territory_data = filtered_leads.groupby('territory').agg({
        'total_deal_value_annual': 'sum',
        'institution_name': 'count'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(territory_data, values='total_deal_value_annual', names='territory',
                    title="Pipeline Distribution by Territory")
        st.plotly_chart(fig)
        
    with col2:
        st.dataframe(territory_data.rename(columns={
            'territory': 'Territory',
            'total_deal_value_annual': 'Pipeline Value',
            'institution_name': 'Number of Leads'
        }))
    
    # Lead source analysis
    st.subheader("Lead Source Analysis")
    source_data = filtered_leads.groupby('lead_source').agg({
        'total_deal_value_annual': 'sum',
        'institution_name': 'count'
    }).reset_index()
    
    fig = px.bar(source_data, x='lead_source', y=['total_deal_value_annual'],
                title="Pipeline Value by Lead Source",
                labels={'value': 'Value (₹)', 'lead_source': 'Source'})
    st.plotly_chart(fig)
    
    # Monthly trending
    st.subheader("Monthly Trends")
    filtered_leads['month'] = pd.to_datetime(
        filtered_leads['first_contact_date']
    ).dt.to_period('M')
    
    monthly_data = filtered_leads.groupby('month').agg({
        'total_deal_value_annual': 'sum',
        'institution_name': 'count'
    }).reset_index()
    
    monthly_data['month'] = monthly_data['month'].astype(str)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_data['month'],
        y=monthly_data['total_deal_value_annual'],
        name='Pipeline Value',
        line=dict(color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=monthly_data['month'],
        y=monthly_data['institution_name']*100000,  # Scale for visibility
        name='Number of Leads',
        line=dict(color='red', dash='dash'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title='Monthly Pipeline and Lead Trends',
        yaxis=dict(title='Pipeline Value (₹)'),
        yaxis2=dict(
            title='Number of Leads',
            overlaying='y',
            side='right',
            showgrid=False
        )
    )
    st.plotly_chart(fig)
def edit_lead_form(lead_data):
    """Create a form pre-filled with lead data for editing"""
    with st.form("edit_lead_form"):
        st.subheader(f"Edit Lead: {lead_data['institution_name']}")
        
        # Create tabs for organized data editing
        tab1, tab2, tab3, tab4 = st.tabs([
            "Basic Information",
            "Contact Details",
            "Product & Pricing",
            "Timeline & Notes"
        ])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                institution_name = st.text_input(
                    "Institution Name",
                    value=lead_data['institution_name']
                )
                institution_type = st.selectbox(
                    "Institution Type",
                    ["Medical College", "Dental College", "Other"],
                    index=["Medical College", "Dental College", "Other"].index(
                        lead_data['institution_type']
                    )
                )
                ownership = st.selectbox(
                    "Ownership",
                    ["Private", "Government", "Society"],
                    index=["Private", "Government", "Society"].index(
                        lead_data['ownership']
                    )
                )
                establishment_year = st.number_input(
                    "Establishment Year",
                    min_value=1900,
                    max_value=datetime.now().year,
                    value=int(lead_data['establishment_year'])
                )
                
            with col2:
                territory = st.selectbox(
                    "Territory",
                    ["Bangalore Urban", "Bangalore Rural & Mysore",
                     "Mangalore & Coastal", "North Karnataka"],
                    index=["Bangalore Urban", "Bangalore Rural & Mysore",
                          "Mangalore & Coastal", "North Karnataka"].index(
                        lead_data['territory']
                    )
                )
                city = st.text_input("City", value=lead_data['city'])
                category = st.selectbox(
                    "Category",
                    ["Premium Private", "Mid-tier Private", 
                     "Budget Private", "Government"],
                    index=["Premium Private", "Mid-tier Private",
                          "Budget Private", "Government"].index(
                        lead_data['category']
                    )
                )
                
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                primary_contact_name = st.text_input(
                    "Primary Contact Name",
                    value=lead_data['primary_contact_name']
                )
                primary_contact_role = st.text_input(
                    "Primary Contact Role",
                    value=lead_data['primary_contact_role']
                )
                primary_contact_email = st.text_input(
                    "Primary Contact Email",
                    value=lead_data['primary_contact_email']
                )
                primary_contact_phone = st.text_input(
                    "Primary Contact Phone",
                    value=lead_data['primary_contact_phone']
                )
                
            with col2:
                secondary_contact_name = st.text_input(
                    "Secondary Contact Name",
                    value=lead_data['secondary_contact_name']
                )
                secondary_contact_role = st.text_input(
                    "Secondary Contact Role",
                    value=lead_data['secondary_contact_role']
                )
                decision_makers = st.text_area(
                    "Key Decision Makers",
                    value=lead_data['decision_makers']
                )
                
        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                current_student_count = st.number_input(
                    "Current Student Count",
                    min_value=0,
                    value=int(lead_data['current_student_count'])
                )
                max_student_capacity = st.number_input(
                    "Maximum Student Capacity",
                    min_value=0,
                    value=int(lead_data['max_student_capacity'])
                )
                current_lms = st.text_input(
                    "Current LMS Provider",
                    value=lead_data['current_lms_provider']
                )
                interested_modules = st.multiselect(
                    "Interested Modules",
                    ["Student Module", "Faculty Module", "Institution Module"],
                    default=json.loads(lead_data['interested_modules'])
                )
                
            with col2:
                payment_preference = st.selectbox(
                    "Payment Preference",
                    ["Monthly", "Quarterly", "Annual"],
                    index=["Monthly", "Quarterly", "Annual"].index(
                        lead_data['payment_preference']
                    )
                )
                budget_confirmed = st.selectbox(
                    "Budget Confirmed",
                    ["Yes", "No"],
                    index=["Yes", "No"].index(lead_data['budget_confirmed'])
                )
                competitors = st.text_area(
                    "Competitors Involved",
                    value=lead_data['competitors_involved']
                )
                
        with tab4:
            col1, col2 = st.columns(2)
            with col1:
                stage = st.selectbox(
                    "Stage",
                    ["New", "Contacted", "Qualified", "Demo",
                     "Proposal", "Negotiation", "Closed Won", "Closed Lost"],
                    index=["New", "Contacted", "Qualified", "Demo",
                          "Proposal", "Negotiation", "Closed Won",
                          "Closed Lost"].index(lead_data['stage'])
                )
                probability = st.slider(
                    "Success Probability (%)",
                    0, 100,
                    value=int(lead_data['probability'])
                )
                
            with col2:
                demo_date = st.date_input(
                    "Demo Scheduled Date",
                    value=pd.to_datetime(lead_data['demo_scheduled_date']).date()
                )
                expected_close = st.date_input(
                    "Expected Close Date",
                    value=pd.to_datetime(lead_data['expected_close_date']).date()
                )
                next_follow_up = st.date_input(
                    "Next Follow-up Date",
                    value=pd.to_datetime(lead_data['next_follow_up_date']).date()
                )
                
            notes = st.text_area(
                "Additional Notes",
                value=lead_data['notes']
            )
            pain_points = st.text_area(
                "Pain Points",
                value=lead_data['pain_points']
            )
            next_steps = st.text_area(
                "Next Steps",
                value=lead_data['next_steps']
            )
            
        submitted = st.form_submit_button("Update Lead")
        
        if submitted:
            # Calculate updated pricing
            monthly_price, annual_value = calculate_deal_metrics(
                current_student_count, category, payment_preference
            )
            
            # Create updated lead data
            updated_lead = {
                'institution_name': institution_name,
                'institution_type': institution_type,
                'ownership': ownership,
                'establishment_year': establishment_year,
                'territory': territory,
                'city': city,
                'category': category,
                'primary_contact_name': primary_contact_name,
                'primary_contact_role': primary_contact_role,
                'primary_contact_email': primary_contact_email,
                'primary_contact_phone': primary_contact_phone,
                'secondary_contact_name': secondary_contact_name,
                'secondary_contact_role': secondary_contact_role,
                'decision_makers': decision_makers,
                'current_student_count': current_student_count,
                'max_student_capacity': max_student_capacity,
                'current_lms_provider': current_lms,
                'interested_modules': json.dumps(interested_modules),
                'payment_preference': payment_preference,
                'budget_confirmed': budget_confirmed,
                'competitors_involved': competitors,
                'stage': stage,
                'probability': probability,
                'demo_scheduled_date': demo_date,
                'expected_close_date': expected_close,
                'next_follow_up_date': next_follow_up,
                'notes': notes,
                'pain_points': pain_points,
                'next_steps': next_steps,
                'student_price_monthly': monthly_price,
                'total_deal_value_annual': annual_value,
                'last_contact_date': datetime.now().date()
            }
            
            # Add change log entry
            change_log = f"""
            {datetime.now().strftime('%Y-%m-%d %H:%M')}
            Lead Updated
            Stage: {lead_data['stage']} → {stage}
            Probability: {lead_data['probability']}% → {probability}%
            """
            updated_lead['notes'] = f"{change_log}\n---\n{notes}"
            
            # Update lead in database
            idx = st.session_state.leads[
                st.session_state.leads['institution_name'] == lead_data['institution_name']
            ].index[0]
            
            for key, value in updated_lead.items():
                st.session_state.leads.at[idx, key] = value
                
            st.success("Lead updated successfully!")
            st.rerun()
def analyze_pipeline():
    """Comprehensive pipeline analysis dashboard for Acolyte's sales team"""
    st.title("Pipeline Analysis Dashboard")
    
    if st.session_state.leads.empty:
        st.warning("No pipeline data available for analysis.")
        return
        
    # Date range selector for analysis
    col1, col2 = st.columns([2, 2])
    with col1:
        date_range = st.selectbox(
            "Analysis Period",
            ["Current Quarter", "Last Quarter", "Year to Date", "Custom Range"]
        )
    
    # Handle custom date range selection
    if date_range == "Custom Range":
        with col2:
            start_date, end_date = st.date_input(
                "Select Date Range",
                value=(datetime.now().date() - timedelta(days=90), datetime.now().date()),
                max_value=datetime.now().date()
            )
    else:
        # Calculate date range based on selection
        end_date = datetime.now().date()
        if date_range == "Current Quarter":
            start_date = datetime(end_date.year, ((end_date.month-1)//3)*3+1, 1).date()
        elif date_range == "Last Quarter":
            last_quarter_end = datetime(end_date.year, ((end_date.month-1)//3)*3+1, 1).date() - timedelta(days=1)
            start_date = datetime(last_quarter_end.year, ((last_quarter_end.month-1)//3)*3+1, 1).date()
            end_date = last_quarter_end
        else:  # Year to Date
            start_date = datetime(end_date.year, 1, 1).date()

    # Filter leads based on date range
    filtered_leads = st.session_state.leads[
        (pd.to_datetime(st.session_state.leads['first_contact_date']).dt.date >= start_date) &
        (pd.to_datetime(st.session_state.leads['first_contact_date']).dt.date <= end_date)
    ].copy()

    # Key Pipeline Metrics
    st.header("Key Pipeline Metrics")
    
    # Calculate key metrics
    total_pipeline = filtered_leads['total_deal_value_annual'].sum()
    weighted_pipeline = (filtered_leads['total_deal_value_annual'] * 
                        filtered_leads['probability'] / 100).sum()
    avg_deal_size = filtered_leads['total_deal_value_annual'].mean()
    total_leads = len(filtered_leads)
    conversion_rate = (len(filtered_leads[filtered_leads['stage'] == 'Closed Won']) / 
                      total_leads * 100) if total_leads > 0 else 0
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Pipeline Value",
            f"₹{total_pipeline:,.0f}",
            help="Total value of all opportunities in the pipeline"
        )
        
    with col2:
        st.metric(
            "Weighted Pipeline",
            f"₹{weighted_pipeline:,.0f}",
            help="Pipeline value adjusted by probability of closing"
        )
        
    with col3:
        st.metric(
            "Average Deal Size",
            f"₹{avg_deal_size:,.0f}",
            help="Average value of opportunities in pipeline"
        )
        
    with col4:
        st.metric(
            "Conversion Rate",
            f"{conversion_rate:.1f}%",
            help="Percentage of leads that convert to closed won"
        )

    # Pipeline Stage Analysis
    st.header("Pipeline Stage Analysis")
    
    # Create tabs for different pipeline views
    tab1, tab2 = st.tabs(["Stage Distribution", "Stage Movement"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Pipeline by stage visualization
            stage_pipeline = filtered_leads.groupby('stage').agg({
                'total_deal_value_annual': 'sum',
                'institution_name': 'count'
            }).reset_index()
            
            # Calculate probability-weighted values
            stage_pipeline['weighted_value'] = filtered_leads.groupby('stage').apply(
                lambda x: (x['total_deal_value_annual'] * x['probability'] / 100).sum()
            ).values
            
            # Create funnel chart
            fig = go.Figure()
            
            # Add total value bars
            fig.add_trace(go.Bar(
                name='Total Value',
                x=stage_pipeline['stage'],
                y=stage_pipeline['total_deal_value_annual'],
                marker_color='lightblue'
            ))
            
            # Add weighted value bars
            fig.add_trace(go.Bar(
                name='Weighted Value',
                x=stage_pipeline['stage'],
                y=stage_pipeline['weighted_value'],
                marker_color='darkblue'
            ))
            
            fig.update_layout(
                title="Pipeline Value by Stage",
                barmode='overlay',
                yaxis_title="Value (₹)",
                xaxis_title="Stage",
                legend_title="Value Type",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Stage metrics table
            stage_metrics = pd.DataFrame({
                'Stage': stage_pipeline['stage'],
                'Count': stage_pipeline['institution_name'],
                'Value (₹)': stage_pipeline['total_deal_value_annual'].map('{:,.0f}'.format),
                'Weighted (₹)': stage_pipeline['weighted_value'].map('{:,.0f}'.format)
            })
            
            st.dataframe(
                stage_metrics,
                hide_index=True,
                use_container_width=True
            )
    
    with tab2:
        # Stage movement analysis
        st.subheader("Stage Movement Analysis")
        
        # Calculate average days in each stage
        filtered_leads['stage_duration'] = (
            pd.to_datetime(filtered_leads['last_contact_date']) - 
            pd.to_datetime(filtered_leads['stage_change_date'])
        ).dt.days
        
        avg_stage_duration = filtered_leads.groupby('stage')['stage_duration'].mean()
        
        # Create stage duration chart
        fig = go.Figure(go.Bar(
            x=avg_stage_duration.index,
            y=avg_stage_duration.values,
            text=avg_stage_duration.values.round(1),
            textposition='auto',
        ))
        
        fig.update_layout(
            title="Average Days in Each Stage",
            xaxis_title="Stage",
            yaxis_title="Days",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

    # Territory Analysis
    st.header("Territory Performance")
    
    # Calculate territory metrics
    territory_metrics = filtered_leads.groupby('territory').agg({
        'total_deal_value_annual': ['sum', 'mean'],
        'institution_name': 'count',
        'probability': 'mean'
    }).round(2)
    
    territory_metrics.columns = ['Total Value', 'Avg Deal Size', 'Lead Count', 'Avg Probability']
    
    # Territory visualization
    col1, col2 = st.columns(2)
    
    with col1:
        # Territory map (using a treemap as placeholder)
        fig = px.treemap(
            filtered_leads,
            path=[px.Constant("Karnataka"), 'territory'],
            values='total_deal_value_annual',
            title="Territory Pipeline Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        # Territory metrics table
        st.dataframe(
            territory_metrics.style.format({
                'Total Value': '₹{:,.0f}',
                'Avg Deal Size': '₹{:,.0f}',
                'Avg Probability': '{:.1f}%'
            }),
            use_container_width=True
        )

    # Time-based Analysis
    st.header("Pipeline Trends")
    
    # Create monthly trend analysis
    filtered_leads['month'] = pd.to_datetime(
        filtered_leads['first_contact_date']
    ).dt.to_period('M')
    
    monthly_trends = filtered_leads.groupby('month').agg({
        'total_deal_value_annual': 'sum',
        'institution_name': 'count',
        'probability': 'mean'
    }).reset_index()
    
    monthly_trends['month'] = monthly_trends['month'].astype(str)
    
    # Create trend visualization
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add pipeline value line
    fig.add_trace(
        go.Scatter(
            x=monthly_trends['month'],
            y=monthly_trends['total_deal_value_annual'],
            name="Pipeline Value",
            line=dict(color='blue')
        ),
        secondary_y=False
    )
    
    # Add lead count line
    fig.add_trace(
        go.Scatter(
            x=monthly_trends['month'],
            y=monthly_trends['institution_name'],
            name="Lead Count",
            line=dict(color='red', dash='dash')
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title="Monthly Pipeline Trends",
        xaxis_title="Month",
        height=400
    )
    
    fig.update_yaxes(
        title_text="Pipeline Value (₹)", 
        secondary_y=False
    )
    fig.update_yaxes(
        title_text="Number of Leads", 
        secondary_y=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Pipeline Health Indicators
    st.header("Pipeline Health Indicators")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Deal size distribution
        fig = px.box(
            filtered_leads,
            y='total_deal_value_annual',
            title="Deal Size Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        # Probability distribution
        fig = px.histogram(
            filtered_leads,
            x='probability',
            title="Probability Distribution",
            nbins=20
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col3:
        # Lead source distribution
        lead_source_dist = filtered_leads.groupby('lead_source').agg({
            'total_deal_value_annual': 'sum'
        }).reset_index()
        
        fig = px.pie(
            lead_source_dist,
            values='total_deal_value_annual',
            names='lead_source',
            title="Pipeline by Lead Source"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Risk Analysis
    st.header("Risk Analysis")
    
    # Calculate risk metrics
    aging_threshold = 30  # days
    probability_threshold = 40  # percent
    size_threshold = avg_deal_size * 1.5  # 50% above average
    
    at_risk_deals = filtered_leads[
        ((datetime.now().date() - pd.to_datetime(filtered_leads['last_contact_date']).dt.date).dt.days > aging_threshold) |
        (filtered_leads['probability'] < probability_threshold) |
        (filtered_leads['total_deal_value_annual'] > size_threshold)
    ]
    
    if not at_risk_deals.empty:
        st.warning(f"Found {len(at_risk_deals)} opportunities that need attention")
        
        # Create risk table
        risk_table = at_risk_deals[[
            'institution_name', 'territory', 'stage', 'total_deal_value_annual',
            'probability', 'last_contact_date'
        ]].copy()
        
        # Add risk indicators
        risk_table['Risk Factors'] = risk_table.apply(
            lambda x: ' | '.join([
                'Aging' if (datetime.now().date() - pd.to_datetime(x['last_contact_date']).dt.date).days > aging_threshold else '',
                'Low Probability' if x['probability'] < probability_threshold else '',
                'Large Deal' if x['total_deal_value_annual'] > size_threshold else ''
            ]).strip(' |'),
            axis=1
        )
        
        st.dataframe(
            risk_table.style.format({
                'total_deal_value_annual': '₹{:,.0f}',
                'probability': '{:.1f}%'
            }),
            hide_index=True,
            use_container_width=True
        )
    else:
        st.success("No high-risk opportunities identified")
def analyze_revenue_forecast():
    """Comprehensive revenue forecasting dashboard for Acolyte"""
    st.title("Revenue Forecasting Dashboard")

    # Check if we have the necessary columns
    if 'total_deal_value_annual' not in st.session_state.leads.columns:
        st.warning("Please add some leads first to generate revenue forecasts.")
        return
    
    if len(st.session_state.leads) == 0:
        st.warning("No leads available for forecasting. Please add some leads first.")
        return

    # Create tabs for different forecasting views
    tab1, tab2, tab3 = st.tabs([
        "Pipeline-Based Forecast", 
        "Territory-Based Projections",
        "Scenario Analysis"
    ])

    with tab1:
        st.header("Pipeline-Based Revenue Forecast")
        
        # Date filters for forecasting period
        col1, col2 = st.columns(2)
        with col1:
            forecast_period = st.selectbox(
                "Forecast Period",
                ["Next Quarter", "Next 6 Months", "Next Year"]
            )
        
        # Calculate forecast dates
        current_date = datetime.now().date()
        if forecast_period == "Next Quarter":
            forecast_end = current_date + timedelta(days=90)
        elif forecast_period == "Next 6 Months":
            forecast_end = current_date + timedelta(days=180)
        else:
            forecast_end = current_date + timedelta(days=365)

        # Filter leads based on expected close dates
        forecast_leads = st.session_state.leads[
            (pd.to_datetime(st.session_state.leads['expected_close_date']).dt.date <= forecast_end)
        ].copy()

        # Calculate weighted pipeline values
        forecast_leads['weighted_value'] = (
            forecast_leads['total_deal_value_annual'] * 
            forecast_leads['probability'] / 100
        )

        # Calculate forecast scenarios
        total_pipeline = forecast_leads['total_deal_value_annual'].sum()
        weighted_pipeline = forecast_leads['weighted_value'].sum()
        
        # Display forecast metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Conservative Forecast",
                f"₹{weighted_pipeline * 0.8:,.0f}",
                help="80% of weighted pipeline value"
            )
        with col2:
            st.metric(
                "Base Forecast",
                f"₹{weighted_pipeline:,.0f}",
                help="100% of weighted pipeline value"
            )
        with col3:
            st.metric(
                "Optimistic Forecast",
                f"₹{weighted_pipeline * 1.2:,.0f}",
                help="120% of weighted pipeline value"
            )

        # Monthly forecast breakdown
        forecast_leads['month'] = pd.to_datetime(
            forecast_leads['expected_close_date']
        ).dt.to_period('M')

        monthly_forecast = forecast_leads.groupby('month').agg({
            'total_deal_value_annual': 'sum',
            'weighted_value': 'sum'
        }).reset_index()

        monthly_forecast['month'] = monthly_forecast['month'].astype(str)

        # Create monthly forecast visualization
        fig = go.Figure()
        
        # Add total potential revenue
        fig.add_trace(go.Bar(
            name='Potential Revenue',
            x=monthly_forecast['month'],
            y=monthly_forecast['total_deal_value_annual'],
            marker_color='lightblue'
        ))
        
        # Add weighted forecast
        fig.add_trace(go.Bar(
            name='Weighted Forecast',
            x=monthly_forecast['month'],
            y=monthly_forecast['weighted_value'],
            marker_color='darkblue'
        ))

        fig.update_layout(
            title="Monthly Revenue Forecast",
            barmode='overlay',
            xaxis_title="Month",
            yaxis_title="Revenue (₹)",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.header("Territory-Based Revenue Projections")

        # Territory-wise forecast
        territory_forecast = forecast_leads.groupby('territory').agg({
            'total_deal_value_annual': 'sum',
            'weighted_value': 'sum',
            'institution_name': 'count'
        }).reset_index()

        # Calculate territory growth projections
        territory_forecast['growth_projection'] = territory_forecast['weighted_value'] * 1.1

        # Territory forecast visualization
        fig = go.Figure()
        
        for measure in ['weighted_value', 'growth_projection']:
            fig.add_trace(go.Bar(
                name='Current Forecast' if measure == 'weighted_value' else 'Growth Projection',
                x=territory_forecast['territory'],
                y=territory_forecast[measure],
                text=territory_forecast[measure].map('₹{:,.0f}'.format),
                textposition='auto',
            ))

        fig.update_layout(
            title="Territory Revenue Projections",
            barmode='group',
            xaxis_title="Territory",
            yaxis_title="Revenue (₹)",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        # Territory metrics table
        st.dataframe(
            territory_forecast.style.format({
                'total_deal_value_annual': '₹{:,.0f}',
                'weighted_value': '₹{:,.0f}',
                'growth_projection': '₹{:,.0f}'
            }),
            hide_index=True
        )

    with tab3:
        st.header("Scenario Analysis")

        # Allow user to adjust scenario parameters
        st.subheader("Adjust Scenario Parameters")
        
        col1, col2 = st.columns(2)
        with col1:
            conversion_rate_adj = st.slider(
                "Conversion Rate Adjustment",
                min_value=-50,
                max_value=50,
                value=0,
                help="Adjust expected conversion rates"
            )
        
        with col2:
            deal_size_adj = st.slider(
                "Average Deal Size Adjustment",
                min_value=-50,
                max_value=50,
                value=0,
                help="Adjust expected deal sizes"
            )

        # Calculate adjusted forecasts
        base_conversion = len(forecast_leads[forecast_leads['stage'] == 'Closed Won']) / len(forecast_leads)
        adjusted_conversion = base_conversion * (1 + conversion_rate_adj/100)
        
        base_deal_size = forecast_leads['total_deal_value_annual'].mean()
        adjusted_deal_size = base_deal_size * (1 + deal_size_adj/100)

        # Create scenario comparison
        scenarios = pd.DataFrame({
            'Scenario': ['Conservative', 'Base', 'Optimistic'],
            'Conversion Rate': [
                adjusted_conversion * 0.8,
                adjusted_conversion,
                adjusted_conversion * 1.2
            ],
            'Deal Size': [
                adjusted_deal_size * 0.8,
                adjusted_deal_size,
                adjusted_deal_size * 1.2
            ]
        })

        scenarios['Forecast'] = (
            scenarios['Conversion Rate'] * 
            scenarios['Deal Size'] * 
            len(forecast_leads)
        )

        # Display scenario comparison
        st.dataframe(
            scenarios.style.format({
                'Conversion Rate': '{:.1%}',
                'Deal Size': '₹{:,.0f}',
                'Forecast': '₹{:,.0f}'
            }),
            hide_index=True
        )

        # Create scenario visualization
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=scenarios['Scenario'],
            y=scenarios['Forecast'],
            text=scenarios['Forecast'].map('₹{:,.0f}'.format),
            textposition='auto',
        ))

        fig.update_layout(
            title="Revenue Forecast Scenarios",
            xaxis_title="Scenario",
            yaxis_title="Revenue (₹)",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        # Additional insights
        st.subheader("Key Insights")

        # Calculate and display key metrics
        expected_growth = (scenarios.iloc[1]['Forecast'] / 
                         weighted_pipeline - 1) * 100
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Expected Growth",
                f"{expected_growth:.1f}%",
                help="Expected growth based on scenario adjustments"
            )
        
        with col2:
            confidence_score = min(100, 
                                 (adjusted_conversion / base_conversion) * 100)
            st.metric(
                "Forecast Confidence",
                f"{confidence_score:.1f}%",
                help="Confidence score based on historical performance"
            )
def analyze_territories():
    """Comprehensive territory analytics dashboard for Acolyte's Karnataka expansion"""
    st.title("Territory Analytics Dashboard")

    if 'leads' not in st.session_state or len(st.session_state.leads) == 0:
        st.warning("No lead data available for territory analysis. Please add some leads first.")
        return

    # Create tabs for different territory views
    tab1, tab2, tab3, tab4 = st.tabs([
        "Territory Overview",
        "Institution Analysis",
        "Performance Metrics",
        "Expansion Tracking"
    ])

    with tab1:
        st.header("Territory Overview")

        # Time period filter for analysis
        col1, col2 = st.columns([2, 2])
        with col1:
            analysis_period = st.selectbox(
                "Analysis Period",
                ["Last Quarter", "Last 6 Months", "Year to Date", "All Time"]
            )

        # Filter data based on selected period
        current_date = datetime.now().date()
        if analysis_period == "Last Quarter":
            start_date = current_date - timedelta(days=90)
        elif analysis_period == "Last 6 Months":
            start_date = current_date - timedelta(days=180)
        elif analysis_period == "Year to Date":
            start_date = datetime(current_date.year, 1, 1).date()
        else:
            start_date = datetime(2000, 1, 1).date()

        filtered_leads = st.session_state.leads[
            pd.to_datetime(st.session_state.leads['first_contact_date']).dt.date >= start_date
        ].copy()

        # Calculate territory metrics
        territory_metrics = filtered_leads.groupby('territory').agg({
            'total_deal_value_annual': ['sum', 'mean'],
            'institution_name': 'count',
            'probability': 'mean',
            'monthly_price': 'mean'
        }).round(2)

        territory_metrics.columns = [
            'Total Pipeline', 'Avg Deal Size', 
            'Number of Leads', 'Avg Probability',
            'Avg Monthly Price'
        ]

        # Create territory map visualization
        st.subheader("Karnataka Territory Performance Map")
        
        # Calculate territory performance score (0-100)
        territory_metrics['Performance Score'] = (
            (territory_metrics['Total Pipeline'] / territory_metrics['Total Pipeline'].max() * 0.4) +
            (territory_metrics['Number of Leads'] / territory_metrics['Number of Leads'].max() * 0.3) +
            (territory_metrics['Avg Probability'] / 100 * 0.3)
        ) * 100

        # Create a treemap visualization for territory performance
        fig = px.treemap(
            territory_metrics.reset_index(),
            path=['territory'],
            values='Total Pipeline',
            color='Performance Score',
            color_continuous_scale='RdYlBu',
            title="Territory Performance Overview"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Display territory metrics table
        st.subheader("Territory Performance Metrics")
        st.dataframe(
            territory_metrics.style.format({
                'Total Pipeline': '₹{:,.0f}',
                'Avg Deal Size': '₹{:,.0f}',
                'Avg Probability': '{:.1f}%',
                'Avg Monthly Price': '₹{:.0f}',
                'Performance Score': '{:.1f}'
            }),
            hide_index=False
        )

    with tab2:
        st.header("Institution Analysis")

        # Territory selection for detailed analysis
        selected_territory = st.selectbox(
            "Select Territory for Analysis",
            filtered_leads['territory'].unique()
        )

        territory_leads = filtered_leads[
            filtered_leads['territory'] == selected_territory
        ]

        # Institution category distribution
        category_dist = territory_leads.groupby('category').agg({
            'institution_name': 'count',
            'total_deal_value_annual': 'sum'
        }).reset_index()

        # Create category distribution visualization
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                category_dist,
                values='institution_name',
                names='category',
                title=f"Institution Distribution in {selected_territory}"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.pie(
                category_dist,
                values='total_deal_value_annual',
                names='category',
                title=f"Pipeline Distribution by Category in {selected_territory}"
            )
            st.plotly_chart(fig, use_container_width=True)

        # Institution size analysis
        st.subheader("Institution Size Analysis")
        
        fig = px.histogram(
            territory_leads,
            x='current_student_count',
            nbins=20,
            title=f"Institution Size Distribution in {selected_territory}"
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("Performance Metrics")

        # Calculate key performance indicators by territory
        territory_kpis = filtered_leads.groupby('territory').apply(
            lambda x: pd.Series({
                'Total Pipeline': x['total_deal_value_annual'].sum(),
                'Lead Conversion Rate': (
                    len(x[x['stage'] == 'Closed Won']) / len(x) * 100 
                    if len(x) > 0 else 0
                ),
                'Avg Sales Cycle': (
                    (pd.to_datetime(x[x['stage'] == 'Closed Won']['actual_close_date']) -
                     pd.to_datetime(x[x['stage'] == 'Closed Won']['first_contact_date']))
                    .mean().days if len(x[x['stage'] == 'Closed Won']) > 0 else 0
                ),
                'Active Opportunities': len(x[x['stage'].isin(['Qualified', 'Demo', 'Proposal', 'Negotiation'])]),
                'Win Rate': (
                    len(x[x['stage'] == 'Closed Won']) / 
                    (len(x[x['stage'].isin(['Closed Won', 'Closed Lost'])]))
                    * 100 if len(x[x['stage'].isin(['Closed Won', 'Closed Lost'])]) > 0 else 0
                )
            })
        ).round(2)

        # Create KPI visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure(data=[
                go.Bar(
                    x=territory_kpis.index,
                    y=territory_kpis['Lead Conversion Rate'],
                    name='Conversion Rate'
                )
            ])
            fig.update_layout(title="Lead Conversion Rate by Territory")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = go.Figure(data=[
                go.Bar(
                    x=territory_kpis.index,
                    y=territory_kpis['Win Rate'],
                    name='Win Rate'
                )
            ])
            fig.update_layout(title="Win Rate by Territory")
            st.plotly_chart(fig, use_container_width=True)

        # Display KPI table
        st.subheader("Territory KPIs")
        st.dataframe(
            territory_kpis.style.format({
                'Total Pipeline': '₹{:,.0f}',
                'Lead Conversion Rate': '{:.1f}%',
                'Avg Sales Cycle': '{:.0f} days',
                'Win Rate': '{:.1f}%'
            }),
            hide_index=False
        )

    with tab4:
        st.header("Expansion Tracking")

        # Calculate territory penetration rates
        territory_targets = {
            'Bangalore Urban': {'target_institutions': 15, 'potential_students': 4500},
            'Bangalore Rural & Mysore': {'target_institutions': 8, 'potential_students': 2400},
            'Mangalore & Coastal': {'target_institutions': 6, 'potential_students': 1800},
            'North Karnataka': {'target_institutions': 5, 'potential_students': 1500}
        }

        expansion_metrics = []
        for territory in territory_targets:
            territory_data = filtered_leads[filtered_leads['territory'] == territory]
            
            metrics = {
                'Territory': territory,
                'Current Institutions': len(territory_data['institution_name'].unique()),
                'Target Institutions': territory_targets[territory]['target_institutions'],
                'Current Students': territory_data['current_student_count'].sum(),
                'Target Students': territory_targets[territory]['potential_students']
            }
            
            metrics['Institution Coverage'] = (
                metrics['Current Institutions'] / metrics['Target Institutions'] * 100
            )
            metrics['Student Coverage'] = (
                metrics['Current Students'] / metrics['Target Students'] * 100
            )
            
            expansion_metrics.append(metrics)

        expansion_df = pd.DataFrame(expansion_metrics)

        # Create expansion progress visualization
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Institution Coverage',
            x=expansion_df['Territory'],
            y=expansion_df['Institution Coverage'],
            yaxis='y',
            offsetgroup=1
        ))
        
        fig.add_trace(go.Bar(
            name='Student Coverage',
            x=expansion_df['Territory'],
            y=expansion_df['Student Coverage'],
            yaxis='y2',
            offsetgroup=2
        ))

        fig.update_layout(
            yaxis=dict(title='Institution Coverage %', side='left', range=[0, 100]),
            yaxis2=dict(title='Student Coverage %', side='right', range=[0, 100], overlaying='y'),
            title='Territory Expansion Progress',
            barmode='group'
        )

        st.plotly_chart(fig, use_container_width=True)

        # Display expansion metrics table
        st.subheader("Territory Expansion Metrics")
        st.dataframe(
            expansion_df.style.format({
                'Institution Coverage': '{:.1f}%',
                'Student Coverage': '{:.1f}%',
                'Current Students': '{:,.0f}',
                'Target Students': '{:,.0f}'
            }),
            hide_index=True
        )

        # Provide expansion recommendations
        st.subheader("Expansion Recommendations")
        
        for _, row in expansion_df.iterrows():
            territory = row['Territory']
            institution_coverage = row['Institution Coverage']
            student_coverage = row['Student Coverage']
            
            st.write(f"**{territory}**")
            
            if institution_coverage < 30:
                st.write("🔴 Priority: High - Need to accelerate institution acquisition")
            elif institution_coverage < 60:
                st.write("🟡 Priority: Medium - Continue steady expansion")
            else:
                st.write("🟢 Priority: Low - Focus on optimizing existing partnerships")
                
            recommendations = []
            if institution_coverage < student_coverage:
                recommendations.append(
                    "Focus on acquiring smaller institutions to increase institutional presence"
                )
            elif student_coverage < institution_coverage:
                recommendations.append(
                    "Target larger institutions to increase student coverage"
                )
                
            if recommendations:
                for rec in recommendations:
                    st.write(f"- {rec}")
            
            st.write("")
def calculate_pricing():
    """Interactive pricing calculator for Acolyte's sales team"""
    st.title("Acolyte Pricing Calculator")

    # Create tabs for different pricing scenarios
    tab1, tab2, tab3 = st.tabs(["Quick Calculator", "Custom Pricing","Detailed Analysis"])

    with tab1:
        st.header("Quick Pricing Calculator")

        # Basic inputs
        col1, col2 = st.columns(2)
        
        with col1:
            # Institution details
            student_count_std = st.number_input(
                "Number of Students",
                min_value=1,
                value=100,
                help="Total number of students in the institution",
                key="standard_tab_student_count"  # Added unique key
            )
            institution_category = st.selectbox(
                "Institution Category",
                ["Higher Capacity", "Limited Capacity"],
                help="Select the institution's capacity category",
                key="standard_tab_category"
            )

        with col2:
            # Payment preferences
            payment_cycle_std = st.selectbox(
                "Payment Cycle",
                ["Monthly", "Quarterly", "Annual"],
                help="Select the preferred payment cycle",
                key="standard_tab_payment_cycle"
            )
            
            commitment_years_std = st.slider(
                "Commitment Period (Years)",
                min_value=1,
                max_value=5,
                value=1,
                help="Select the number of years of commitment",
                key="standard_tab_commitment_years"
            )

        # Calculate base price per student
        def get_base_monthly_price(student_count_std, category):
            if category == "Higher Capacity":
                if student_count_std >= 1000:
                    return 300
                elif student_count_std >= 500:
                    return 450
                else:
                    return 750
            else:  # Limited Capacity
                if student_count_std >= 501:
                    return 350
                elif student_count_std >= 301:
                    return 450
                else:
                    return 750

        # Calculate all discounts
        def calculate_total_discount(payment_cycle_std, commitment_years_std):
            # Base payment cycle discount
            if payment_cycle_std == "Annual":
                cycle_discount = 0.20  # 20% for annual
            elif payment_cycle_std == "Quarterly":
                cycle_discount = 0.10  # 10% for quarterly
            else:
                cycle_discount = 0.00  # No discount for monthly
            
            # Multi-year commitment discount (only for annual payment)
            if payment_cycle_std == "Annual" and commitment_years_std > 1:
                commitment_discount = (commitment_years_std - 1) * 0.05  # 5% per additional year
            else:
                commitment_discount = 0.00
            
            # Total discount (capped at 40%)
            total_discount = min(cycle_discount + commitment_discount, 0.40)
            return total_discount

        # Calculate with inflation for multi-year
        def calculate_with_inflation(base_price, years):
            inflation_rate = 0.05  # 5% annual inflation
            yearly_prices = []
            
            for year in range(years):
                inflated_price = base_price * (1 + inflation_rate) ** year
                yearly_prices.append(inflated_price)
            
            return yearly_prices

        # Perform calculations
        base_monthly_price = get_base_monthly_price(student_count_std, institution_category)
        total_discount = calculate_total_discount(payment_cycle_std, commitment_years_std)
        discounted_monthly_price = base_monthly_price * (1 - total_discount)
        
        # Calculate yearly prices with inflation
        yearly_prices = calculate_with_inflation(
            discounted_monthly_price * 12 * student_count_std, 
            commitment_years_std
        )

        # Display pricing summary
        st.subheader("Pricing Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Base Monthly Price per Student",
                f"₹{base_monthly_price:,.2f}"
            )
            
        with col2:
            st.metric(
                "Total Discount",
                f"{total_discount*100:.1f}%"
            )
            
        with col3:
            st.metric(
                "Final Monthly Price per Student",
                f"₹{discounted_monthly_price:,.2f}"
            )

        # Display yearly breakdown
        st.subheader("Year-by-Year Breakdown")
        
        breakdown_data = []
        for year, yearly_price in enumerate(yearly_prices, 1):
            monthly_equivalent = yearly_price / 12
            if payment_cycle_std == "Quarterly":
                quarterly_payment = yearly_price / 4
                breakdown_data.append({
                    "Year": year,
                    "Annual Total": f"₹{yearly_price:,.2f}",
                    "Payment Amount": f"₹{quarterly_payment:,.2f} per quarter",
                    "Monthly Equivalent": f"₹{monthly_equivalent:,.2f}"
                })
            elif payment_cycle_std == "Annual":
                breakdown_data.append({
                    "Year": year,
                    "Annual Total": f"₹{yearly_price:,.2f}",
                    "Payment Amount": f"₹{yearly_price:,.2f} per year",
                    "Monthly Equivalent": f"₹{monthly_equivalent:,.2f}"
                })
            else:  # Monthly
                breakdown_data.append({
                    "Year": year,
                    "Annual Total": f"₹{yearly_price:,.2f}",
                    "Payment Amount": f"₹{monthly_equivalent:,.2f} per month",
                    "Monthly Equivalent": f"₹{monthly_equivalent:,.2f}"
                })

        st.table(pd.DataFrame(breakdown_data))
    with tab2:
        st.header("Custom Pricing Calculator")
        
        # Create columns for main inputs
        col1, col2 = st.columns(2)
        
        with col1:
            pricing_mode = st.radio(
                "Pricing Mode",
                ["Use Standard Price as Reference", "Start with Custom Price"],
                help="Choose whether to start from standard pricing or enter a completely custom price",
                key="custom_tab_pricing_mode"
            )
            
            student_count_custom = st.number_input(
                "Number of Students",
                min_value=1,
                value=100,
                help="Total number of students in the institution",
                key="custom_tab_student_count"  # Added unique key
            )

        with col2:
            payment_cycle_custom = st.selectbox(
                "Payment Cycle",
                ["Monthly", "Quarterly", "Annual"],
                help="Select the preferred payment cycle",
                key="tab2_payment_cycle"
            )
            
            commitment_years_custom = st.slider(
                "Commitment Period (Years)",
                min_value=1,
                max_value=5,
                value=1,
                help="Select the number of years of commitment",
                key="tab2_commitment_years"
            )

        # Calculate standard price for reference
        def get_standard_price(student_count_custom):
            if student_count_custom >= 1000:
                return 300
            elif student_count_custom >= 500:
                return 450
            else:
                return 750

        standard_price = get_standard_price(student_count_custom)

        # Custom pricing section
        st.subheader("Custom Price Setting")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if pricing_mode == "Use Standard Price as Reference":
                # Show standard price and allow percentage adjustment
                st.info(f"Standard Monthly Price: ₹{standard_price} per student")
                
                price_adjustment = st.slider(
                    "Price Adjustment (%)",
                    min_value=-50,
                    max_value=50,
                    value=0,
                    help="Adjust price as a percentage of standard price",
                    key="tab2_price_adjustment"
                )
                
                custom_price = standard_price * (1 + price_adjustment/100)
                
                # Show comparison metrics
                difference_from_standard = ((custom_price - standard_price) / 
                                         standard_price * 100)
                
                st.metric(
                    "Custom Monthly Price per Student",
                    f"₹{custom_price:.2f}",
                    f"{difference_from_standard:+.1f}% vs Standard"
                )
                
            else:
                # Direct custom price input
                custom_price = st.number_input(
                    "Enter Custom Monthly Price per Student",
                    min_value=0.0,
                    value=float(standard_price),
                    step=50.0,
                    help="Enter your custom price",
                    key="custom_price_input",
                )
                
                # Show comparison to standard
                difference_from_standard = ((custom_price - standard_price) / 
                                         standard_price * 100)
                
                st.metric(
                    "Difference from Standard",
                    f"{difference_from_standard:+.1f}%",
                    help="Percentage difference from standard pricing"
                )

        with col2:
            # Additional negotiation terms
            additional_terms = st.multiselect(
                "Additional Terms",
                [
                    "Extended Payment Terms",
                    "Free Implementation",
                    "Premium Support Included",
                    "Early Renewal Option",
                    "Price Lock Guarantee"
                ],
                help="Select additional terms to include in the offer"
            )
            
            special_notes = st.text_area(
                "Special Terms & Conditions",
                help="Enter any special terms or conditions for this custom price"
            )

        # Calculate total costs with custom pricing
        st.subheader("Cost Analysis")
        
        # Apply payment cycle discounts
        if payment_cycle_custom == "Annual":
            cycle_discount = 0.20
        elif payment_cycle_custom == "Quarterly":
            cycle_discount = 0.10
        else:
            cycle_discount = 0.00

        # Apply multi-year commitment discount
        commitment_discount = (commitment_years_custom - 1) * 0.05 if payment_cycle_custom == "Annual" else 0
        total_discount = min(cycle_discount + commitment_discount, 0.40)
        
        # Calculate final price
        final_monthly_price = custom_price * (1 - total_discount)
        
        # Create annual breakdown with inflation
        inflation_rate = 0.05  # 5% annual inflation
        yearly_breakdown = []
        
        for year in range(commitment_years_custom):
            yearly_price = (final_monthly_price * 12 * student_count_custom * 
                          (1 + inflation_rate) ** year)
            
            if payment_cycle_custom == "Annual":
                payment_amount = yearly_price
                payment_text = "per year"
            elif payment_cycle_custom == "Quarterly":
                payment_amount = yearly_price / 4
                payment_text = "per quarter"
            else:
                payment_amount = yearly_price / 12
                payment_text = "per month"
                
            yearly_breakdown.append({
                "Year": year + 1,
                "Total Annual Cost": f"₹{yearly_price:,.2f}",
                f"Payment Amount ({payment_cycle_custom})": f"₹{payment_amount:,.2f} {payment_text}",
                "Monthly Equivalent": f"₹{yearly_price/12:,.2f}"
            })

        st.table(pd.DataFrame(yearly_breakdown))

        # Financial Impact Analysis
        st.subheader("Financial Impact Analysis")
        
        total_standard_cost = (standard_price * (1 - total_discount) * 
                             12 * student_count_custom * commitment_years_custom)
        total_custom_cost = (final_monthly_price * 12 * student_count_custom * 
                           commitment_years_custom)
        
        cost_difference = total_custom_cost - total_standard_cost
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Contract Value",
                f"₹{total_custom_cost:,.2f}",
                f"₹{cost_difference:,.2f} vs Standard"
            )
            
        with col2:
            monthly_difference = cost_difference / (12 * commitment_years_custom)
            st.metric(
                "Monthly Impact",
                f"₹{monthly_difference:,.2f}",
                "vs Standard Pricing"
            )
            
        with col3:
            per_student_impact = monthly_difference / student_count_custom
            st.metric(
                "Per Student Impact",
                f"₹{per_student_impact:,.2f}",
                "Monthly per Student"
            )

        # Approval Requirements
        st.subheader("Approval Requirements")
        
        if difference_from_standard <= -10:
            st.warning("⚠️ Requires Director Approval - Price more than 10% below standard")
        elif difference_from_standard <= -5:
            st.warning("⚠️ Requires Sales Manager Approval - Price 5-10% below standard")
        else:
            st.success("✓ Within standard approval limits")

        # Generate custom proposal
        if st.button("Generate Custom Proposal"):
            proposal_text = f"""
            # Acolyte Custom Pricing Proposal

            ## Institution Details
            - Number of Students: {student_count_custom}
            - Payment Cycle: {payment_cycle_custom}
            - Commitment Period: {commitment_years_custom} years

            ## Custom Pricing Structure
            - Standard Monthly Price per Student: ₹{standard_price:,.2f}
            - Custom Monthly Price per Student: ₹{custom_price:,.2f}
            - Price Adjustment: {difference_from_standard:+.1f}%
            - Applied Discounts: {total_discount*100:.1f}%
            - Final Monthly Price per Student: ₹{final_monthly_price:,.2f}

            ## Total Investment
            - Total Contract Value: ₹{total_custom_cost:,.2f}
            - Difference from Standard: ₹{cost_difference:,.2f}
            - Monthly Impact: ₹{monthly_difference:,.2f}

            ## Additional Terms
            {chr(10).join([f"- {term}" for term in additional_terms])}

            ## Special Terms & Conditions
            {special_notes if special_notes else "Standard terms and conditions apply"}

            ## Approval Requirements
            {("Requires Director Approval" if difference_from_standard <= -10 else "Requires Sales Manager Approval" if difference_from_standard <= -5 else "Within standard approval limits")}
            """
            
            st.download_button(
                "Download Custom Proposal",
                proposal_text,
                file_name="acolyte_custom_pricing_proposal.md",
                mime="text/markdown"
            )
    with tab3:
        st.header("Detailed Pricing Analysis")

        # Additional inputs for detailed analysis
        col1, col2 = st.columns(2)
        
        with col1:
            include_implementation = st.checkbox(
                "Include Implementation Services",
                help="Add one-time implementation cost"
            )
            
            custom_discount = st.number_input(
                "Additional Custom Discount (%)",
                min_value=0,
                max_value=20,
                value=0,
                help="Enter any additional approved discount"
            )
            student_count_analysis = st.number_input(
                "Number of Students",
                min_value=1,
                value=100,
                help="Total number of students in the institution",
                key="analysis_tab_student_count"
            )
            
            hourly_value = st.number_input(
                "Value of Student Hour (₹)",
                min_value=100,
                value=500,
                key="analysis_tab_hourly_value"
            )

        with col2:
            add_support_package = st.checkbox(
                "Add Premium Support Package",
                help="Include premium support services"
            )
            
            custom_terms = st.text_area(
                "Custom Terms",
                help="Enter any special terms or conditions"
            )

        # Calculate additional costs
        implementation_cost = 50000 if include_implementation else 0
        support_cost = yearly_prices[0] * 0.10 if add_support_package else 0
        
        # Apply custom discount
        final_yearly_prices = [
            price * (1 - custom_discount/100) 
            for price in yearly_prices
        ]

        # Display comprehensive pricing analysis
        st.subheader("Comprehensive Pricing Breakdown")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Total Contract Value",
                f"₹{sum(final_yearly_prices) + implementation_cost + support_cost:,.2f}"
            )
            
        with col2:
            avg_monthly_cost = (
                sum(final_yearly_prices) + implementation_cost + support_cost
            ) / (commitment_years_custom * 12)
            
            st.metric(
                "Average Monthly Cost",
                f"₹{avg_monthly_cost:,.2f}"
            )

        # Create detailed cost breakdown
        st.subheader("Detailed Cost Structure")
        
        detailed_costs = pd.DataFrame({
            "Component": [
                "Base License Cost",
                "Implementation Services",
                "Premium Support",
                "Custom Discount",
                "Total"
            ],
            "Cost": [
                f"₹{sum(yearly_prices):,.2f}",
                f"₹{implementation_cost:,.2f}",
                f"₹{support_cost:,.2f}",
                f"-₹{sum(yearly_prices) * (custom_discount/100):,.2f}",
                f"₹{sum(final_yearly_prices) + implementation_cost + support_cost:,.2f}"
            ]
        })
        
        st.table(detailed_costs)

        # ROI Calculator
        st.subheader("ROI Calculator")
        
        avg_student_hours_saved = st.slider(
            "Average Hours Saved per Student per Month",
            min_value=1,
            max_value=20,
            value=5
        )
        
        hourly_value = st.number_input(
            "Value of Student Hour (₹)",
            min_value=100,
            value=500,
            key="hourly_value_input"
        )
        
        monthly_savings = (
            student_count_analysis * avg_student_hours_saved * hourly_value
        )
        
        annual_savings = monthly_savings * 12
        total_investment = sum(final_yearly_prices) + implementation_cost + support_cost
        roi = (annual_savings - total_investment) / total_investment * 100
        payback_months = total_investment / monthly_savings
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Annual Cost Savings",
                f"₹{annual_savings:,.2f}"
            )
            
        with col2:
            st.metric(
                "ROI (%)",
                f"{roi:.1f}%"
            )
            
        with col3:
            st.metric(
                "Payback Period",
                f"{payback_months:.1f} months"
            )

        # Generate proposal
        if st.button("Generate Proposal"):
            proposal_text = f"""
            # Acolyte Pricing Proposal

            ## Institution Details
            - Number of Students: {student_count_analysis}
            - Category: {institution_category}
            - Payment Cycle: {payment_cycle_custom}
            - Commitment Period: {commitment_years_custom} years

            ## Pricing Structure
            - Base Monthly Price per Student: ₹{base_monthly_price:,.2f}
            - Applied Discounts: {total_discount*100:.1f}%
            - Final Monthly Price per Student: ₹{discounted_monthly_price:,.2f}

            ## Total Investment
            - Total Contract Value: ₹{sum(final_yearly_prices) + implementation_cost + support_cost:,.2f}
            - Average Monthly Cost: ₹{avg_monthly_cost:,.2f}

            ## Return on Investment
            - Annual Cost Savings: ₹{annual_savings:,.2f}
            - ROI: {roi:.1f}%
            - Payback Period: {payback_months:.1f} months

            ## Terms and Conditions
            {custom_terms if custom_terms else "Standard terms and conditions apply"}
            """
            
            st.download_button(
                "Download Proposal",
                proposal_text,
                file_name="acolyte_pricing_proposal.md",
                mime="text/markdown"
            )
def main():
    st.title("Acolyte Sales Tool")
    
    menu = st.sidebar.selectbox(
        "Select Function",
        ["Add New Lead", "View Lead Dashboard", "Pipeline Analysis", 
         "Revenue Forecasting", "Territory Analytics", "Pricing Calculator",
         "Lead Analytics"]
    )
    
    if menu == "Add New Lead":
        create_lead_form()
    elif menu == "View Lead Dashboard":
        view_lead_dashboard()
    elif menu == "Pipeline Analysis":
        analyze_pipeline()
    elif menu == "Revenue Forecasting":
        analyze_revenue_forecast()
    elif menu == "Territory Analytics":
        analyze_territories()
    elif menu == "Pricing Calculator":
        calculate_pricing()
    else:
        show_lead_analytics()

if __name__ == "__main__":
    main()