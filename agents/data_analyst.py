"""
Agent 1: Data Analyst Agent
Analyzes sales CSV data to extract insights on profit, demand, and inventory
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional


class DataAnalystAgent:
    """
    Analyzes business sales data to provide insights on:
    - Profit by product
    - Demand trends
    - Weak/declining products
    - Restock suggestions
    """
    
    def __init__(self):
        self.analysis_results = {}
        
    def parse_csv(self, file_or_path) -> pd.DataFrame:
        """Parse and validate CSV sales data"""
        try:
            if isinstance(file_or_path, str):
                df = pd.read_csv(file_or_path)
            else:
                df = pd.read_csv(file_or_path)
            
            # Convert date column if exists
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date')
            
            return df
        except Exception as e:
            raise ValueError(f"Error parsing CSV: {str(e)}")
    
    def calculate_profit_by_product(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate profit metrics for each product"""
        # Calculate profit per unit
        df['profit_per_unit'] = df['unit_price'] - df['unit_cost']
        df['total_profit'] = df['profit_per_unit'] * df['quantity_sold']
        df['total_revenue'] = df['unit_price'] * df['quantity_sold']
        df['profit_margin'] = (df['profit_per_unit'] / df['unit_price'] * 100).round(2)
        
        # Aggregate by product
        profit_summary = df.groupby('product_name').agg({
            'quantity_sold': 'sum',
            'total_revenue': 'sum',
            'total_profit': 'sum',
            'profit_margin': 'mean',
            'unit_price': 'first',
            'unit_cost': 'first'
        }).reset_index()
        
        profit_summary = profit_summary.rename(columns={
            'quantity_sold': 'total_qty_sold',
            'profit_margin': 'avg_profit_margin'
        })
        
        profit_summary = profit_summary.sort_values('total_profit', ascending=False)
        
        return profit_summary
    
    def detect_demand_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze demand trends over time for each product"""
        if 'date' not in df.columns:
            return {"error": "Date column required for trend analysis"}
        
        trends = {}
        
        for product in df['product_name'].unique():
            product_df = df[df['product_name'] == product].sort_values('date')
            
            if len(product_df) >= 2:
                # Calculate week-over-week change
                quantities = product_df['quantity_sold'].values
                first_half = quantities[:len(quantities)//2].mean()
                second_half = quantities[len(quantities)//2:].mean()
                
                if first_half > 0:
                    trend_pct = ((second_half - first_half) / first_half) * 100
                else:
                    trend_pct = 0
                
                if trend_pct > 10:
                    trend = "📈 Rising"
                elif trend_pct < -10:
                    trend = "📉 Declining"
                else:
                    trend = "➡️ Stable"
                
                trends[product] = {
                    'trend': trend,
                    'change_pct': round(trend_pct, 1),
                    'avg_weekly_sales': round(quantities.mean(), 1),
                    'latest_sales': int(quantities[-1])
                }
        
        return trends
    
    def identify_weak_products(self, df: pd.DataFrame, trends: Dict) -> List[Dict]:
        """Identify products with declining sales or low profit margins"""
        profit_summary = self.calculate_profit_by_product(df)
        weak_products = []
        
        for _, row in profit_summary.iterrows():
            product = row['product_name']
            issues = []
            severity = 0
            
            # Check profit margin
            if row['avg_profit_margin'] < 15:
                issues.append(f"Low profit margin ({row['avg_profit_margin']:.1f}%)")
                severity += 2
            
            # Check demand trend
            if product in trends:
                if trends[product]['change_pct'] < -15:
                    issues.append(f"Declining demand ({trends[product]['change_pct']:.1f}%)")
                    severity += 3
                elif trends[product]['change_pct'] < -5:
                    issues.append(f"Slightly declining ({trends[product]['change_pct']:.1f}%)")
                    severity += 1
            
            # Check total profit contribution
            total_profit = profit_summary['total_profit'].sum()
            if total_profit > 0:
                contribution = (row['total_profit'] / total_profit) * 100
                if contribution < 2:
                    issues.append(f"Low profit contribution ({contribution:.1f}%)")
                    severity += 1
            
            if issues:
                weak_products.append({
                    'product': product,
                    'issues': issues,
                    'severity': severity,
                    'total_profit': row['total_profit'],
                    'profit_margin': row['avg_profit_margin']
                })
        
        # Sort by severity
        weak_products.sort(key=lambda x: x['severity'], reverse=True)
        
        return weak_products
    
    def generate_restock_suggestions(self, df: pd.DataFrame, trends: Dict) -> List[Dict]:
        """Generate inventory restocking recommendations"""
        suggestions = []
        
        # Get latest stock levels
        latest_data = df.sort_values('date').groupby('product_name').last().reset_index()
        
        for _, row in latest_data.iterrows():
            product = row['product_name']
            stock = row.get('stock_remaining', 0)
            
            if product in trends:
                avg_sales = trends[product]['avg_weekly_sales']
                weeks_of_stock = stock / avg_sales if avg_sales > 0 else float('inf')
                
                urgency = "normal"
                action = ""
                
                if weeks_of_stock < 1:
                    urgency = "🔴 CRITICAL"
                    action = f"Restock immediately! Only {stock} units left (~{weeks_of_stock:.1f} weeks)"
                elif weeks_of_stock < 2:
                    urgency = "🟠 HIGH"
                    action = f"Restock soon. ~{weeks_of_stock:.1f} weeks of stock remaining"
                elif weeks_of_stock < 4:
                    urgency = "🟡 MEDIUM"
                    action = f"Plan restock. ~{weeks_of_stock:.1f} weeks of stock"
                
                # Consider demand trend
                if trends[product]['trend'] == "📈 Rising" and weeks_of_stock < 3:
                    urgency = "🟠 HIGH" if urgency == "🟡 MEDIUM" else urgency
                    action += " (Demand is rising!)"
                
                if urgency != "normal":
                    suggestions.append({
                        'product': product,
                        'urgency': urgency,
                        'current_stock': int(stock),
                        'avg_weekly_sales': avg_sales,
                        'weeks_of_stock': round(weeks_of_stock, 1),
                        'action': action,
                        'trend': trends[product]['trend']
                    })
        
        # Sort by urgency
        urgency_order = {"🔴 CRITICAL": 0, "🟠 HIGH": 1, "🟡 MEDIUM": 2}
        suggestions.sort(key=lambda x: urgency_order.get(x['urgency'], 3))
        
        return suggestions
    
    def get_category_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyze performance by product category"""
        if 'category' not in df.columns:
            return pd.DataFrame()
        
        df['total_profit'] = (df['unit_price'] - df['unit_cost']) * df['quantity_sold']
        df['total_revenue'] = df['unit_price'] * df['quantity_sold']
        
        category_summary = df.groupby('category').agg({
            'quantity_sold': 'sum',
            'total_revenue': 'sum',
            'total_profit': 'sum',
            'product_name': 'nunique'
        }).reset_index()
        
        category_summary = category_summary.rename(columns={
            'product_name': 'num_products',
            'quantity_sold': 'total_qty_sold'
        })
        
        category_summary['avg_profit_per_item'] = (
            category_summary['total_profit'] / category_summary['total_qty_sold']
        ).round(2)
        
        return category_summary.sort_values('total_profit', ascending=False)
    
    def run(self, file_or_path) -> Dict[str, Any]:
        """Run complete analysis and return all insights"""
        # Parse data
        df = self.parse_csv(file_or_path)
        
        # Run all analyses
        profit_analysis = self.calculate_profit_by_product(df)
        demand_trends = self.detect_demand_trends(df)
        weak_products = self.identify_weak_products(df, demand_trends)
        restock_suggestions = self.generate_restock_suggestions(df, demand_trends)
        category_analysis = self.get_category_analysis(df)
        
        # Calculate summary stats
        total_revenue = profit_analysis['total_revenue'].sum()
        total_profit = profit_analysis['total_profit'].sum()
        avg_margin = profit_analysis['avg_profit_margin'].mean()
        
        self.analysis_results = {
            'summary': {
                'total_revenue': total_revenue,
                'total_profit': total_profit,
                'avg_profit_margin': round(avg_margin, 1),
                'total_products': len(profit_analysis),
                'rising_products': sum(1 for t in demand_trends.values() if t['trend'] == "📈 Rising"),
                'declining_products': sum(1 for t in demand_trends.values() if t['trend'] == "📉 Declining"),
                'products_needing_restock': len(restock_suggestions)
            },
            'profit_by_product': profit_analysis.to_dict('records'),
            'demand_trends': demand_trends,
            'weak_products': weak_products,
            'restock_suggestions': restock_suggestions,
            'category_analysis': category_analysis.to_dict('records') if len(category_analysis) > 0 else [],
            'raw_data': df
        }
        
        return self.analysis_results
    
    def get_analysis_summary_text(self) -> str:
        """Get a text summary of the analysis for LLM consumption"""
        if not self.analysis_results:
            return "No analysis has been run yet."
        
        summary = self.analysis_results['summary']
        trends = self.analysis_results['demand_trends']
        weak = self.analysis_results['weak_products']
        restock = self.analysis_results['restock_suggestions']
        
        text = f"""
=== BUSINESS ANALYSIS SUMMARY ===

📊 OVERALL PERFORMANCE:
- Total Revenue: ₹{summary['total_revenue']:,.0f}
- Total Profit: ₹{summary['total_profit']:,.0f}
- Average Profit Margin: {summary['avg_profit_margin']}%
- Total Products: {summary['total_products']}

📈 DEMAND TRENDS:
- Rising Demand: {summary['rising_products']} products
- Declining Demand: {summary['declining_products']} products

🔴 WEAK PRODUCTS REQUIRING ATTENTION:
"""
        for wp in weak[:5]:
            text += f"- {wp['product']}: {', '.join(wp['issues'])}\n"
        
        text += f"\n📦 RESTOCK ALERTS ({len(restock)} items):\n"
        for rs in restock[:5]:
            text += f"- {rs['product']}: {rs['urgency']} - {rs['action']}\n"
        
        text += "\n🏆 TOP PERFORMERS BY TREND:\n"
        rising = [(p, t) for p, t in trends.items() if t['trend'] == "📈 Rising"]
        for product, trend in sorted(rising, key=lambda x: x[1]['change_pct'], reverse=True)[:3]:
            text += f"- {product}: +{trend['change_pct']}% growth\n"
        
        return text
