"""
UI Components for MSME Copilot
Premium, animated Streamlit components for data display
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any


# Dark theme for Plotly charts - Gold palette
PLOTLY_THEME = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {'color': '#e0e0e0', 'family': 'Inter'},
    'xaxis': {
        'gridcolor': 'rgba(201,162,39,0.1)',
        'zerolinecolor': 'rgba(201,162,39,0.2)'
    },
    'yaxis': {
        'gridcolor': 'rgba(201,162,39,0.1)',
        'zerolinecolor': 'rgba(201,162,39,0.2)'
    }
}


def render_agent_progress(agent_name: str, progress: float, status: str):
    """Render agent progress indicator"""
    agents = [
        ("📊", "Data Analyst"),
        ("📋", "Planner"),
        ("🔍", "Web Researcher"),
        ("🔎", "Critic"),
        ("📝", "Consultant")
    ]
    
    cols = st.columns(5)
    
    for i, (emoji, name) in enumerate(agents):
        with cols[i]:
            agent_progress = (i + 1) / 5
            if progress >= agent_progress:
                status_color = "🟢"
            elif progress >= (i / 5):
                status_color = "🔄"
            else:
                status_color = "⚪"
            
            st.markdown(f"""
            <div style="text-align: center; padding: 10px;">
                <div style="font-size: 24px;">{emoji}</div>
                <div style="font-size: 12px; color: #a0a0a0;">{name}</div>
                <div>{status_color}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.progress(progress)
    st.caption(status)


def render_analysis_results(analysis: Dict[str, Any]):
    """Render data analysis results with beautiful charts"""
    summary = analysis.get('summary', {})
    
    # Summary metrics with animation
    st.markdown("""
    <h3 style="color: #f5d061; margin-bottom: 1.5rem;">
        📊 Business Performance Summary
    </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Revenue",
            f"₹{summary.get('total_revenue', 0):,.0f}",
            delta=None
        )
    
    with col2:
        st.metric(
            "Total Profit",
            f"₹{summary.get('total_profit', 0):,.0f}",
            delta=f"{summary.get('avg_profit_margin', 0):.1f}% margin"
        )
    
    with col3:
        st.metric(
            "Rising Products",
            summary.get('rising_products', 0),
            delta="📈 Growing"
        )
    
    with col4:
        st.metric(
            "Declining Products",
            summary.get('declining_products', 0),
            delta="📉 Attention"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Profit by product chart
    st.markdown("""
    <h3 style="color: #f5d061; margin-bottom: 1rem;">
        🏆 Profit by Product
    </h3>
    """, unsafe_allow_html=True)
    
    profit_data = analysis.get('profit_by_product', [])
    if profit_data:
        df = pd.DataFrame(profit_data)
        
        fig = px.bar(
            df.head(10), 
            x='product_name', 
            y='total_profit',
            color='avg_profit_margin',
            color_continuous_scale=['#8B4513', '#c9a227', '#f5d061'],
        )
        fig.update_layout(
            **PLOTLY_THEME,
            xaxis_title="Product",
            yaxis_title="Total Profit (₹)",
            xaxis_tickangle=-45,
            coloraxis_colorbar_title="Margin %",
            height=400,
            margin=dict(l=20, r=20, t=30, b=80)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Demand trends
    st.markdown("""
    <h3 style="color: #f5d061; margin-top: 1.5rem; margin-bottom: 1rem;">
        📈 Demand Trends
    </h3>
    """, unsafe_allow_html=True)
    
    trends = analysis.get('demand_trends', {})
    if trends:
        trend_data = []
        for product, data in trends.items():
            trend_data.append({
                'Product': product,
                'Trend': data['trend'],
                'Change %': data['change_pct'],
                'Avg Weekly Sales': data['avg_weekly_sales']
            })
        
        trend_df = pd.DataFrame(trend_data)
        trend_df = trend_df.sort_values('Change %', ascending=False)
        
        fig = px.bar(
            trend_df,
            x='Product',
            y='Change %',
            color='Change %',
            color_continuous_scale=['#8B4513', '#b8860b', '#c9a227', '#daa520', '#f5d061'],
            color_continuous_midpoint=0
        )
        fig.update_layout(
            **PLOTLY_THEME,
            xaxis_tickangle=-45,
            height=400,
            margin=dict(l=20, r=20, t=30, b=80),
            coloraxis_colorbar_title="Change %"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Weak products alert
    weak_products = analysis.get('weak_products', [])
    if weak_products:
        st.markdown("""
        <h3 style="color: #f5d061; margin-top: 1.5rem; margin-bottom: 1rem;">
            ⚠️ Products Requiring Attention
        </h3>
        """, unsafe_allow_html=True)
        
        for wp in weak_products[:5]:
            severity_color = "🔴" if wp['severity'] >= 4 else "🟡" if wp['severity'] >= 2 else "🟢"
            with st.expander(f"{severity_color} {wp['product']} - Severity: {wp['severity']}/5"):
                for issue in wp['issues']:
                    st.markdown(f"• {issue}")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Profit Margin", f"{wp['profit_margin']:.1f}%")
                with col2:
                    st.metric("Total Profit", f"₹{wp['total_profit']:,.0f}")
    
    # Restock suggestions
    restock = analysis.get('restock_suggestions', [])
    if restock:
        st.markdown("""
        <h3 style="color: #f5d061; margin-top: 1.5rem; margin-bottom: 1rem;">
            📦 Restock Alerts
        </h3>
        """, unsafe_allow_html=True)
        
        restock_df = pd.DataFrame(restock)
        st.dataframe(
            restock_df[['product', 'urgency', 'current_stock', 'weeks_of_stock', 'action']],
            use_container_width=True,
            hide_index=True
        )


def render_sources_sidebar(sources: List[Dict[str, str]]):
    """Render sources investigated in sidebar with beautiful styling"""
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <h4 style="color: #f5d061; margin-bottom: 0.5rem;">
        📚 Sources Investigated
    </h4>
    """, unsafe_allow_html=True)
    st.sidebar.caption(f"✓ {len(sources)} verified sources")
    
    for i, source in enumerate(sources[:12], 1):
        title = source.get('title', 'Unknown')[:35]
        url = source.get('url', '#')
        
        st.sidebar.markdown(f"""
        <div style="
            background: rgba(201, 162, 39, 0.1);
            padding: 0.6rem 0.8rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            border-left: 3px solid #c9a227;
            font-size: 0.8rem;
        ">
            <a href="{url}" target="_blank" style="color: #f5d061; text-decoration: none;">
                {i}. {title}...
            </a>
        </div>
        """, unsafe_allow_html=True)


def render_strategy_report(markdown_report: str):
    """Render the final strategy report with styling"""
    st.markdown(markdown_report)


def render_weekly_plan(strategy: Dict[str, Any]):
    """Render the weekly action plan as an interactive checklist with fragment optimization"""
    
    # Get weekly plan from the correct location
    weekly_plan = strategy.get('strategy', {}).get('weekly_plan', [])
    
    # If not found there, try direct access
    if not weekly_plan:
        weekly_plan = strategy.get('weekly_plan', [])
    
    if not weekly_plan:
        st.info("No weekly plan generated yet. Please run the analysis first.")
        return
    
    st.markdown("""
    <h3 style="color: #f5d061; margin-bottom: 1.5rem;">
        📅 4-Week Action Plan
    </h3>
    """, unsafe_allow_html=True)
    
    # Create tabs for each week
    week_labels = [f"Week {w.get('week', i+1)}" for i, w in enumerate(weekly_plan)]
    tabs = st.tabs(week_labels)
    
    # Use fragments for each week to prevent full page reruns
    for tab_idx, (tab, week) in enumerate(zip(tabs, weekly_plan)):
        with tab:
            # Fragment makes this week's checkboxes independent
            # IMPORTANT: Use default parameter to capture week data (fixes closure issue)
            @st.fragment
            def render_week_content(week_data=week):
                focus = week_data.get('focus_area', 'General')
                
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(201, 162, 39, 0.15) 0%, rgba(180, 140, 30, 0.15) 100%);
                    padding: 1.5rem;
                    border-radius: 16px;
                    border: 1px solid rgba(201, 162, 39, 0.3);
                    margin-bottom: 1rem;">
                    <h4 style="color: #f5d061; margin: 0;">🎯 Focus: {focus}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("**Tasks to Complete:**")
                
                tasks = week_data.get('tasks', [])
                for j, task in enumerate(tasks):
                    # Use unique key for each checkbox
                    key = f"week_{week_data.get('week', 0)}_{j}_{task[:15]}"
                    st.checkbox(task, key=key)
                
                success_metric = week_data.get('success_metrics', 'Not specified')
                st.markdown(f"""
                <div style="
                    background: rgba(100, 140, 60, 0.1);
                    padding: 1rem;
                    border-radius: 12px;
                    border-left: 4px solid #9acd32;
                    margin-top: 1rem;">
                    <strong style="color: #9acd32;">📊 Success Metric:</strong>
                    <p style="color: #b0a090; margin: 0.5rem 0 0 0;">{success_metric}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Render this week's content as a fragment
            render_week_content()



def render_verification_badge(verification: Dict[str, Any]):
    """Render verification status badge with beautiful styling"""
    
    confidence = verification.get('overall_confidence', 'medium')
    score = verification.get('data_quality_score', 5)
    verified = verification.get('verified_count', 0)
    
    confidence_config = {
        'high': ('🟢', '#22c55e', 'High Confidence'),
        'medium': ('🟡', '#eab308', 'Medium Confidence'),
        'low': ('🔴', '#ef4444', 'Low Confidence')
    }
    
    emoji, color, label = confidence_config.get(confidence, ('⚪', '#a0a0a0', 'Unknown'))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="custom-tooltip">
            <div style="
                background: linear-gradient(145deg, rgba(25, 25, 25, 0.9) 0%, rgba(15, 15, 15, 0.9) 100%);
                padding: 1.5rem;
                border-radius: 16px;
                text-align: center;
                border: 1px solid {color}40;
                cursor: help;
            ">
                <div style="font-size: 2rem;">{emoji}</div>
                <div style="color: #b0a090; font-size: 0.85rem; margin-top: 0.5rem;">Confidence Level ℹ️</div>
                <div style="color: {color}; font-size: 1.2rem; font-weight: 600;">{label}</div>
            </div>
            <span class="tooltip-text">How much you should trust the overall analysis based on data consistency and research quality.</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="custom-tooltip">
            <div style="
                background: linear-gradient(145deg, rgba(25, 25, 25, 0.9) 0%, rgba(15, 15, 15, 0.9) 100%);
                padding: 1.5rem;
                border-radius: 16px;
                text-align: center;
                border: 1px solid rgba(201, 162, 39, 0.3);
                cursor: help;
            ">
                <div style="font-size: 2rem;">📊</div>
                <div style="color: #b0a090; font-size: 0.85rem; margin-top: 0.5rem;">Data Quality ℹ️</div>
                <div style="color: #f5d061; font-size: 1.5rem; font-weight: 700;">{score}/10</div>
            </div>
            <span class="tooltip-text">Score of your input data's completeness and reliability (1-10). Higher is better.</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="custom-tooltip">
            <div style="
                background: linear-gradient(145deg, rgba(25, 25, 25, 0.9) 0%, rgba(15, 15, 15, 0.9) 100%);
                padding: 1.5rem;
                border-radius: 16px;
                text-align: center;
                border: 1px solid rgba(100, 140, 60, 0.3);
                cursor: help;
            ">
                <div style="font-size: 2rem;">✅</div>
                <div style="color: #b0a090; font-size: 0.85rem; margin-top: 0.5rem;">Verified Items ℹ️</div>
                <div style="color: #9acd32; font-size: 1.5rem; font-weight: 700;">{verified}</div>
            </div>
            <span class="tooltip-text">Number of recommendations backed by both your data and external market research.</span>
        </div>
        """, unsafe_allow_html=True)


def render_category_analysis(analysis: Dict[str, Any]):
    """Render category-level performance analysis with donut chart"""
    
    categories = analysis.get('category_analysis', [])
    
    if not categories:
        return
    
    st.markdown("""
    <h3 style="color: #f5d061; margin-top: 2rem; margin-bottom: 1rem;">
        🏅 Performance by Category
    </h3>
    """, unsafe_allow_html=True)
    
    df = pd.DataFrame(categories)
    
    # Beautiful donut chart - Gold palette
    fig = px.pie(
        df, 
        values='total_profit', 
        names='category',
        hole=0.5,
        color_discrete_sequence=['#f5d061', '#c9a227', '#d4a574', '#b8860b', '#daa520', '#8b7355']
    )
    fig.update_layout(
        **PLOTLY_THEME,
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(
            font=dict(color='#e0e0e0'),
            bgcolor='rgba(0,0,0,0)'
        ),
        annotations=[dict(
            text='Profit',
            x=0.5, y=0.5,
            font_size=16,
            font_color='#c9a227',
            showarrow=False
        )]
    )
    fig.update_traces(
        textposition='outside',
        textinfo='percent+label',
        textfont=dict(color='#e0e0e0')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Category table
    st.dataframe(
        df[['category', 'num_products', 'total_qty_sold', 'total_revenue', 'total_profit']].rename(columns={
            'category': 'Category',
            'num_products': 'Products',
            'total_qty_sold': 'Units Sold',
            'total_revenue': 'Revenue (₹)',
            'total_profit': 'Profit (₹)'
        }),
        use_container_width=True,
        hide_index=True
    )
