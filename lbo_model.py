"""
LBO Financial Modeling & Valuation Tool
Comprehensive leveraged buyout analysis for private equity transactions

Author: Liam Hirsch
Based on experience at BNP Paribas Corporate & Investment Banking
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class LBOAnalysis:
    """
    Comprehensive LBO financial model for private equity transactions
    
    Features:
    - Multi-tranche debt structure modeling
    - 5-year operating projections
    - Debt amortization schedules
    - Exit scenario analysis with IRR/MOIC calculations
    - Sensitivity analysis and risk assessment
    """
    
    def __init__(self, company_name, purchase_price, sponsor_equity):
        """
        Initialize LBO analysis
        
        Parameters:
        company_name (str): Target company name
        purchase_price (float): Total enterprise value (€M)
        sponsor_equity (float): PE sponsor equity contribution (€M)
        """
        self.company_name = company_name
        self.purchase_price = purchase_price
        self.sponsor_equity = sponsor_equity
        self.total_debt = purchase_price - sponsor_equity
        
        # Initialize data structures
        self.debt_structure = {}
        self.operating_model = {}
        self.debt_schedule = {}
        self.returns_analysis = {}
        
        print(f"Initialized LBO Analysis for {company_name}")
        print(f"Purchase Price: €{purchase_price:,.0f}M")
        print(f"Sponsor Equity: €{sponsor_equity:,.0f}M") 
        print(f"Total Debt: €{self.total_debt:,.0f}M")
    
    def structure_debt(self, term_loan_a=0, term_loan_b=0, revolver=0, subordinated=0):
        """
        Structure multi-tranche debt facility
        
        Parameters represent debt amounts in €M
        """
        self.debt_structure = {
            'Term Loan A': {
                'amount': term_loan_a,
                'rate': 0.045,  # L+400bps (assuming 4.5% all-in)
                'term': 7,
                'amortization': 0.15,  # 15% annual mandatory amortization
                'seniority': 1
            },
            'Term Loan B': {
                'amount': term_loan_b, 
                'rate': 0.065,  # L+650bps (assuming 6.5% all-in)
                'term': 8,
                'amortization': 0.01,  # 1% annual mandatory amortization
                'seniority': 2
            },
            'Revolver': {
                'amount': revolver,
                'rate': 0.035,  # L+350bps (assuming 3.5% all-in) 
                'term': 5,
                'amortization': 0.0,   # Revolving facility
                'seniority': 1
            },
            'Subordinated Debt': {
                'amount': subordinated,
                'rate': 0.085,  # 8.5% fixed rate
                'term': 10,
                'amortization': 0.0,   # Bullet maturity
                'seniority': 3
            }
        }
        
        total_debt_check = sum([tranche['amount'] for tranche in self.debt_structure.values()])
        print(f"\nDebt Structure (€M):")
        print("-" * 40)
        for tranche_name, details in self.debt_structure.items():
            if details['amount'] > 0:
                print(f"{tranche_name}: €{details['amount']:,.0f}M at {details['rate']:.1%}")
        print(f"Total Debt: €{total_debt_check:,.0f}M")
        
        return self.debt_structure
    
    def build_operating_model(self, base_revenue, revenue_growth, ebitda_margin, 
                            capex_rate=0.03, nwc_rate=0.02, tax_rate=0.25):
        """
        Build 5-year operating projections
        
        Parameters:
        base_revenue (float): Year 1 revenue (€M)
        revenue_growth (list): Annual revenue growth rates [Y2, Y3, Y4, Y5]
        ebitda_margin (float): EBITDA as % of revenue
        capex_rate (float): CapEx as % of revenue
        nwc_rate (float): NWC increase as % of revenue growth
        tax_rate (float): Tax rate on EBT
        """
        years = [1, 2, 3, 4, 5]
        model = {}
        
        for i, year in enumerate(years):
            # Revenue projections
            if year == 1:
                revenue = base_revenue
            else:
                growth_rate = revenue_growth[i-1] if i-1 < len(revenue_growth) else revenue_growth[-1]
                revenue = model[year-1]['revenue'] * (1 + growth_rate)
            
            # P&L calculations
            ebitda = revenue * ebitda_margin
            depreciation = revenue * 0.03  # Assume 3% depreciation rate
            ebit = ebitda - depreciation
            
            # Interest expense (simplified - based on average debt outstanding)
            if self.debt_structure:
                total_debt_amount = sum([debt['amount'] for debt in self.debt_structure.values()])
                weighted_avg_rate = sum([
                    debt['amount'] * debt['rate'] 
                    for debt in self.debt_structure.values()
                ]) / total_debt_amount if total_debt_amount > 0 else 0
                
                # Assume debt paydown reduces interest expense over time
                debt_reduction_factor = 0.9 ** (year - 1)  # Simplified debt reduction
                interest_expense = total_debt_amount * weighted_avg_rate * debt_reduction_factor
            else:
                interest_expense = 0
            
            # Tax calculations
            ebt = ebit - interest_expense
            taxes = max(0, ebt * tax_rate)
            net_income = ebt - taxes
            
            # Cash flow calculations
            operating_cash_flow = net_income + depreciation
            capex = revenue * capex_rate
            
            # Working capital change
            if year == 1:
                nwc_change = 0
            else:
                revenue_change = revenue - model[year-1]['revenue']
                nwc_change = revenue_change * nwc_rate
            
            free_cash_flow = operating_cash_flow - capex - nwc_change
            
            # Store results
            model[year] = {
                'revenue': revenue,
                'ebitda': ebitda,
                'ebit': ebit,
                'depreciation': depreciation,
                'interest_expense': interest_expense,
                'ebt': ebt,
                'taxes': taxes,
                'net_income': net_income,
                'operating_cash_flow': operating_cash_flow,
                'capex': capex,
                'nwc_change': nwc_change,
                'free_cash_flow': free_cash_flow
            }
        
        self.operating_model = model
        
        # Display summary
        print(f"\nOperating Model Summary (€M):")
        print("-" * 50)
        print("Year\tRevenue\tEBITDA\tFree CF")
        for year, data in model.items():
            print(f"{year}\t€{data['revenue']:.0f}M\t€{data['ebitda']:.0f}M\t€{data['free_cash_flow']:.0f}M")
        
        return model
    
    def model_debt_schedule(self):
        """
        Model debt amortization and paydown schedule
        """
        if not self.debt_structure or not self.operating_model:
            print("Error: Need both debt structure and operating model")
            return None
        
        schedule = {}
        years = [1, 2, 3, 4, 5]
        
        # Initialize debt balances
        debt_balances = {}
        for tranche, terms in self.debt_structure.items():
            debt_balances[tranche] = terms['amount']
        
        for year in years:
            year_schedule = {}
            free_cash_flow = self.operating_model[year]['free_cash_flow']
            remaining_cash = free_cash_flow
            
            for tranche, terms in self.debt_structure.items():
                beginning_balance = debt_balances[tranche]
                
                # Mandatory amortization
                mandatory_payment = beginning_balance * terms['amortization']
                mandatory_payment = min(mandatory_payment, beginning_balance)
                
                # Optional prepayment from excess cash (prioritize by seniority)
                optional_payment = 0
                if remaining_cash > mandatory_payment and tranche == 'Term Loan B':
                    # Use excess cash for TLB prepayment
                    available_cash = remaining_cash - mandatory_payment
                    optional_payment = min(available_cash, beginning_balance - mandatory_payment)
                
                total_payment = mandatory_payment + optional_payment
                ending_balance = max(0, beginning_balance - total_payment)
                interest_payment = beginning_balance * terms['rate']
                
                year_schedule[tranche] = {
                    'beginning_balance': beginning_balance,
                    'mandatory_payment': mandatory_payment,
                    'optional_payment': optional_payment,
                    'total_payment': total_payment,
                    'interest_payment': interest_payment,
                    'ending_balance': ending_balance
                }
                
                # Update remaining cash and debt balance
                remaining_cash -= total_payment
                debt_balances[tranche] = ending_balance
            
            schedule[year] = year_schedule
        
        self.debt_schedule = schedule
        return schedule
    
    def exit_analysis(self, exit_multiples=None, exit_year=5):
        """
        Analyze exit scenarios and calculate returns
        
        Parameters:
        exit_multiples (list): EV/EBITDA exit multiples to analyze
        exit_year (int): Exit year for analysis
        """
        if exit_multiples is None:
            exit_multiples = [8.0, 9.0, 10.0, 11.0, 12.0]
        
        if not self.operating_model or not self.debt_schedule:
            print("Error: Need operating model and debt schedule")
            return None
        
        exit_ebitda = self.operating_model[exit_year]['ebitda']
        
        # Calculate remaining debt at exit
        total_remaining_debt = 0
        for tranche in self.debt_schedule[exit_year].values():
            total_remaining_debt += tranche['ending_balance']
        
        results = {}
        
        print(f"\nExit Analysis - Year {exit_year}")
        print(f"Exit EBITDA: €{exit_ebitda:.0f}M")
        print(f"Remaining Debt: €{total_remaining_debt:.0f}M")
        print("-" * 50)
        
        for multiple in exit_multiples:
            # Calculate enterprise and equity value
            enterprise_value = exit_ebitda * multiple
            equity_value = max(0, enterprise_value - total_remaining_debt)
            
            # Calculate returns
            moic = equity_value / self.sponsor_equity if self.sponsor_equity > 0 else 0
            irr = (moic ** (1/exit_year)) - 1 if moic > 0 else -1
            
            results[f"{multiple:.1f}x"] = {
                'exit_multiple': multiple,
                'enterprise_value': enterprise_value,
                'remaining_debt': total_remaining_debt,
                'equity_value': equity_value,
                'moic': moic,
                'irr': irr
            }
            
            print(f"{multiple:.1f}x Multiple: €{equity_value:.0f}M equity, {moic:.1f}x MOIC, {irr:.1%} IRR")
        
        self.returns_analysis = results
        return results
    
    def sensitivity_analysis(self, revenue_sensitivity=[-0.1, 0, 0.1], 
                           ebitda_sensitivity=[-0.02, 0, 0.02]):
        """
        Perform sensitivity analysis on key variables
        """
        if not self.returns_analysis:
            print("Error: Need to run exit analysis first")
            return None
        
        base_case = self.returns_analysis['10.0x']  # Use 10x multiple as base
        sensitivity_grid = []
        
        for rev_adj in revenue_sensitivity:
            for ebitda_adj in ebitda_sensitivity:
                # Adjust base case EBITDA
                adjusted_ebitda = self.operating_model[5]['ebitda'] * (1 + rev_adj) * (1 + ebitda_adj)
                
                # Recalculate returns
                enterprise_value = adjusted_ebitda * 10.0
                remaining_debt = base_case['remaining_debt']
                equity_value = max(0, enterprise_value - remaining_debt)
                moic = equity_value / self.sponsor_equity
                irr = (moic ** (1/5)) - 1 if moic > 0 else -1
                
                sensitivity_grid.append({
                    'revenue_adj': rev_adj,
                    'ebitda_adj': ebitda_adj, 
                    'irr': irr,
                    'moic': moic
                })
        
        return pd.DataFrame(sensitivity_grid)
    
    def create_visualizations(self):
        """
        Create professional charts for LBO analysis
        """
        if not self.debt_schedule or not self.operating_model:
            print("Error: Need complete financial model")
            return None
        
        # 1. Debt Paydown Waterfall
        fig_debt = go.Figure()
        
        years = list(range(1, 6))
        for tranche in ['Term Loan A', 'Term Loan B', 'Revolver', 'Subordinated Debt']:
            if self.debt_structure[tranche]['amount'] > 0:
                balances = [self.debt_schedule[year][tranche]['ending_balance'] for year in years]
                fig_debt.add_trace(go.Scatter(
                    x=years,
                    y=balances,
                    mode='lines+markers',
                    name=tranche,
                    line=dict(width=3)
                ))
        
        fig_debt.update_layout(
            title=f"{self.company_name} - Debt Amortization Schedule",
            xaxis_title="Year",
            yaxis_title="Outstanding Debt (€M)",
            hovermode='x unified'
        )
        
        # 2. Returns Heatmap
        if self.returns_analysis:
            multiples = list(range(8, 13))
            years = list(range(3, 8))
            irr_matrix = []
            
            for year in years:
                row = []
                for multiple in multiples:
                    # Simplified IRR calculation for different scenarios
                    exit_ebitda = self.operating_model[min(year, 5)]['ebitda']
                    enterprise_value = exit_ebitda * multiple
                    remaining_debt = sum([
                        self.debt_schedule[min(year, 5)][tranche]['ending_balance'] 
                        for tranche in self.debt_structure.keys()
                        if self.debt_structure[tranche]['amount'] > 0
                    ])
                    equity_value = max(0, enterprise_value - remaining_debt)
                    moic = equity_value / self.sponsor_equity
                    irr = (moic ** (1/year)) - 1 if moic > 0 else -1
                    row.append(irr)
                irr_matrix.append(row)
            
            fig_heatmap = px.imshow(
                irr_matrix,
                x=[f"{m}x" for m in multiples],
                y=[f"Year {y}" for y in years],
                color_continuous_scale='RdYlGn',
                title=f"{self.company_name} - IRR Sensitivity Analysis",
                labels=dict(x="Exit Multiple", y="Exit Year", color="IRR")
            )
        
        return fig_debt, fig_heatmap
    
    def export_to_excel(self, filename=None):
        """
        Export complete LBO model to Excel
        """
        if filename is None:
            filename = f"{self.company_name.replace(' ', '_')}_LBO_Model.xlsx"
        
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            # Transaction summary
            summary_data = {
                'Metric': ['Purchase Price', 'Sponsor Equity', 'Total Debt', 'Debt/Equity'],
                'Value (€M)': [self.purchase_price, self.sponsor_equity, 
                              self.total_debt, self.total_debt/self.sponsor_equity]
            }
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='Transaction Summary', index=False)
            
            # Operating model
            if self.operating_model:
                operating_df = pd.DataFrame(self.operating_model).T
                operating_df.to_excel(writer, sheet_name='Operating Model')
            
            # Debt schedule
            if self.debt_schedule:
                for year in [1, 2, 3, 4, 5]:
                    debt_df = pd.DataFrame(self.debt_schedule[year]).T
                    debt_df.to_excel(writer, sheet_name=f'Debt Schedule Y{year}')
            
            # Returns analysis
            if self.returns_analysis:
                returns_df = pd.DataFrame(self.returns_analysis).T
                returns_df.to_excel(writer, sheet_name='Returns Analysis')
        
        print(f"Model exported to {filename}")

# Example usage and demonstration
if __name__ == "__main__":
    # Initialize sample LBO transaction
    print("=== LBO FINANCIAL MODELING TOOL ===")
    print("Author: Liam Hirsch")
    print("Based on BNP Paribas Corporate Banking experience\n")
    
    # Create sample transaction
    lbo = LBOAnalysis(
        company_name="TechCorp Industries",
        purchase_price=500,  # €500M
        sponsor_equity=150   # €150M
    )
    
    # Structure debt tranches
    lbo.structure_debt(
        term_loan_a=100,     # €100M
        term_loan_b=200,     # €200M  
        revolver=25,         # €25M
        subordinated=25      # €25M
    )
    
    # Build 5-year operating model
    lbo.build_operating_model(
        base_revenue=200,    # €200M Year 1 revenue
        revenue_growth=[0.08, 0.07, 0.06, 0.05],  # Declining growth
        ebitda_margin=0.25   # 25% EBITDA margin
    )
    
    # Model debt amortization
    debt_schedule = lbo.model_debt_schedule()
    
    # Perform exit analysis
    returns = lbo.exit_analysis()
    
    # Sensitivity analysis
    sensitivity = lbo.sensitivity_analysis()
    print(f"\nSensitivity Analysis:")
    print(sensitivity.head())
    
    # Export to Excel
    lbo.export_to_excel()
    
    print(f"\n=== ANALYSIS COMPLETE ===")
    print(f"Base Case (10x Multiple): {returns['10.0x']['moic']:.1f}x MOIC, {returns['10.0x']['irr']:.1%} IRR")
