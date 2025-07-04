import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import random

# Set page config
st.set_page_config(
    page_title="AI Dev Marketplace",
    page_icon="🚀",
    layout="wide"
)

# Mock database of developers
@st.cache_data
def load_developers():
    developers = []
    names = [
        "Sarah Chen", "Michael Rodriguez", "Priya Patel", "David Kim", 
        "Emma Johnson", "Ahmed Hassan", "Lisa Wang", "Carlos Silva",
        "Anna Kowalski", "Raj Sharma", "Maria Garcia", "James Liu",
        "Fatima Al-Zahra", "Robert Taylor", "Nina Andersson", "Kevin O'Brien"
    ]
    
    languages = ["English", "Spanish", "Chinese", "Hindi", "Arabic", "French", "German", "Japanese"]
    specializations = [
        "Healthcare AI", "Finance AI", "Frontend Development", 
        "Backend Development", "Embedded Systems", "DevOps", 
        "Security", "Testing", "Full Stack"
    ]
    
    for i, name in enumerate(names):
        # Generate random skills
        skills = {
            "C": random.randint(20, 95),
            "C++": random.randint(30, 90),
            "C#": random.randint(25, 85),
            "JavaScript": random.randint(40, 95),
            "Python": random.randint(50, 98),
            "DevOps": random.randint(30, 90),
            "Security": random.randint(25, 85),
            "Development": random.randint(60, 95),
            "Testing": random.randint(40, 90),
            "Code Maintenance": random.randint(35, 80),
            "Production Release": random.randint(30, 85)
        }
        
        developer = {
            "id": i + 1,
            "name": name,
            "experience": random.randint(2, 12),
            "hourly_rate": random.randint(25, 150),
            "daily_rate": random.randint(200, 1200),
            "weekly_rate": random.randint(1000, 6000),
            "languages": random.sample(languages, random.randint(1, 3)),
            "specialization": random.choice(specializations),
            "skills": skills,
            "rating": round(random.uniform(3.5, 5.0), 1),
            "completed_projects": random.randint(5, 100),
            "availability": random.choice(["Available", "Busy", "Partially Available"])
        }
        developers.append(developer)
    
    return developers

# Initialize session state
if 'selected_jobs' not in st.session_state:
    st.session_state.selected_jobs = []

if 'quote_items' not in st.session_state:
    st.session_state.quote_items = []

# Load data
developers = load_developers()

# Header
st.title("🚀 AI Developer Marketplace")
st.markdown("Find the perfect AI application developer for your healthcare, finance, and tech projects")

# Sidebar filters
st.sidebar.header("🔍 Filter Developers")

# Experience filter
exp_range = st.sidebar.slider("Years of Experience", 0, 15, (2, 12))

# Specialization filter
specializations = list(set([dev["specialization"] for dev in developers]))
selected_specializations = st.sidebar.multiselect("Specializations", specializations, default=specializations)

# Skills filter
skills_list = ["C", "C++", "C#", "JavaScript", "Python", "DevOps", "Security", "Development", "Testing", "Code Maintenance", "Production Release"]
selected_skills = st.sidebar.multiselect("Required Skills", skills_list)

# Minimum skill level
if selected_skills:
    min_skill_level = st.sidebar.slider("Minimum Skill Level (%)", 0, 100, 50)
else:
    min_skill_level = 0

# Language filter
all_languages = list(set([lang for dev in developers for lang in dev["languages"]]))
selected_languages = st.sidebar.multiselect("Languages", all_languages)

# Rate filter
rate_type = st.sidebar.selectbox("Rate Type", ["Hourly", "Daily", "Weekly"])
if rate_type == "Hourly":
    rate_range = st.sidebar.slider("Hourly Rate ($)", 0, 200, (25, 150))
elif rate_type == "Daily":
    rate_range = st.sidebar.slider("Daily Rate ($)", 0, 1500, (200, 1200))
else:
    rate_range = st.sidebar.slider("Weekly Rate ($)", 0, 8000, (1000, 6000))

# Availability filter
availability_options = ["Available", "Busy", "Partially Available"]
selected_availability = st.sidebar.multiselect("Availability", availability_options, default=["Available", "Partially Available"])

# Filter developers
filtered_developers = []
for dev in developers:
    # Experience filter
    if not (exp_range[0] <= dev["experience"] <= exp_range[1]):
        continue
    
    # Specialization filter
    if dev["specialization"] not in selected_specializations:
        continue
    
    # Skills filter
    if selected_skills:
        meets_skill_req = all(
            skill in dev["skills"] and dev["skills"][skill] >= min_skill_level
            for skill in selected_skills
        )
        if not meets_skill_req:
            continue
    
    # Language filter
    if selected_languages:
        if not any(lang in dev["languages"] for lang in selected_languages):
            continue
    
    # Rate filter
    if rate_type == "Hourly":
        if not (rate_range[0] <= dev["hourly_rate"] <= rate_range[1]):
            continue
    elif rate_type == "Daily":
        if not (rate_range[0] <= dev["daily_rate"] <= rate_range[1]):
            continue
    else:
        if not (rate_range[0] <= dev["weekly_rate"] <= rate_range[1]):
            continue
    
    # Availability filter
    if dev["availability"] not in selected_availability:
        continue
    
    filtered_developers.append(dev)

# Main content
st.header(f"🔍 Found {len(filtered_developers)} Developers")

if not filtered_developers:
    st.warning("No developers match your criteria. Try adjusting your filters.")
else:
    # Display developers
    for i, dev in enumerate(filtered_developers):
        with st.expander(f"👨‍💻 {dev['name']} - {dev['specialization']} (⭐ {dev['rating']})", expanded=i < 3):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.write(f"**Experience:** {dev['experience']} years")
                st.write(f"**Languages:** {', '.join(dev['languages'])}")
                st.write(f"**Completed Projects:** {dev['completed_projects']}")
                st.write(f"**Availability:** {dev['availability']}")
                
                # Display skills
                st.write("**Skills:**")
                skills_df = pd.DataFrame(list(dev['skills'].items()), columns=['Skill', 'Level'])
                st.dataframe(skills_df, use_container_width=True)
            
            with col2:
                st.write("**Rates:**")
                st.write(f"💰 Hourly: ${dev['hourly_rate']}")
                st.write(f"📅 Daily: ${dev['daily_rate']}")
                st.write(f"📆 Weekly: ${dev['weekly_rate']}")
                
                # Project duration
                duration_type = st.selectbox(
                    "Project Duration Type", 
                    ["Hours", "Days", "Weeks"], 
                    key=f"duration_type_{dev['id']}"
                )
                
                if duration_type == "Hours":
                    duration = st.number_input(
                        "Number of Hours", 
                        min_value=1, 
                        max_value=1000, 
                        value=40,
                        key=f"duration_{dev['id']}"
                    )
                    total_cost = duration * dev['hourly_rate']
                elif duration_type == "Days":
                    duration = st.number_input(
                        "Number of Days", 
                        min_value=1, 
                        max_value=365, 
                        value=5,
                        key=f"duration_{dev['id']}"
                    )
                    total_cost = duration * dev['daily_rate']
                else:
                    duration = st.number_input(
                        "Number of Weeks", 
                        min_value=1, 
                        max_value=52, 
                        value=2,
                        key=f"duration_{dev['id']}"
                    )
                    total_cost = duration * dev['weekly_rate']
                
                st.write(f"**Total Cost: ${total_cost:,.2f}**")
            
            with col3:
                project_description = st.text_area(
                    "Project Description",
                    placeholder="Describe your project...",
                    key=f"desc_{dev['id']}"
                )
                
                if st.button(f"Add to Project", key=f"add_{dev['id']}"):
                    if project_description:
                        job_item = {
                            "developer_name": dev['name'],
                            "specialization": dev['specialization'],
                            "duration": duration,
                            "duration_type": duration_type,
                            "rate": dev[f"{duration_type.lower()[:-1]}_rate"],
                            "total_cost": total_cost,
                            "project_description": project_description,
                            "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.session_state.selected_jobs.append(job_item)
                        st.success(f"Added {dev['name']} to your project!")
                    else:
                        st.error("Please provide a project description.")

# Selected Jobs Section
if st.session_state.selected_jobs:
    st.header("📋 Selected Jobs")
    
    jobs_df = pd.DataFrame(st.session_state.selected_jobs)
    st.dataframe(jobs_df, use_container_width=True)
    
    total_project_cost = sum(job["total_cost"] for job in st.session_state.selected_jobs)
    st.metric("Total Project Cost", f"${total_project_cost:,.2f}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Download Excel Report"):
            # Create Excel file
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                jobs_df.to_excel(writer, sheet_name='Selected Jobs', index=False)
                
                # Add summary sheet
                summary_data = {
                    "Total Jobs": [len(st.session_state.selected_jobs)],
                    "Total Cost": [f"${total_project_cost:,.2f}"],
                    "Report Generated": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            output.seek(0)
            st.download_button(
                label="Download Excel Report",
                data=output.getvalue(),
                file_name=f"ai_dev_project_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col2:
        if st.button("📄 Generate Quote"):
            # Generate quote
            quote_number = f"Q{datetime.now().strftime('%Y%m%d%H%M%S')}"
            quote_date = datetime.now().strftime("%Y-%m-%d")
            valid_until = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            
            st.session_state.quote_items = st.session_state.selected_jobs.copy()
            st.session_state.quote_number = quote_number
            st.session_state.quote_date = quote_date
            st.session_state.valid_until = valid_until
            
            st.success(f"Quote {quote_number} generated successfully!")
    
    with col3:
        if st.button("🗑️ Clear All Jobs"):
            st.session_state.selected_jobs = []
            st.session_state.quote_items = []
            st.rerun()

# Quote Section
if 'quote_items' in st.session_state and st.session_state.quote_items:
    st.header("💰 Generated Quote")
    
    quote_col1, quote_col2 = st.columns([2, 1])
    
    with quote_col1:
        st.subheader(f"Quote Number: {st.session_state.quote_number}")
        st.write(f"**Date:** {st.session_state.quote_date}")
        st.write(f"**Valid Until:** {st.session_state.valid_until}")
        
        # Quote items
        quote_df = pd.DataFrame(st.session_state.quote_items)
        st.dataframe(quote_df, use_container_width=True)
        
        quote_total = sum(item["total_cost"] for item in st.session_state.quote_items)
        st.metric("Quote Total", f"${quote_total:,.2f}")
        
        # Terms and conditions
        st.subheader("Terms & Conditions")
        st.write("""
        - Quote valid for 7 days from date of issue
        - 50% payment required to start project
        - All rates are in USD
        - Project timeline may vary based on complexity
        - Additional charges may apply for scope changes
        """)
    
    with quote_col2:
        if st.button("📧 Email Quote"):
            st.info("Quote emailing feature would be implemented with email service integration")
        
        if st.button("📱 Share Quote"):
            st.info("Quote sharing feature would be implemented with sharing APIs")

# Footer
st.markdown("---")
st.markdown("🚀 **AI Developer Marketplace** - Connecting businesses with top AI talent")
st.markdown("Need help? Contact us at support@aidevmarketplace.com")