# 💰 LBO Financial Modeling & Valuation Tool

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Private Equity](https://img.shields.io/badge/Use%20Case-Private%20Equity-gold.svg)]()

**Comprehensive leveraged buyout analysis and valuation tool for private equity transactions**

Built based on experience structuring **€500M+ LBO transactions** at **BNP Paribas Corporate & Investment Banking** across Western Europe.

![LBO Dashboard](https://via.placeholder.com/800x400/1B263B/E1E5E9?text=LBO+Financial+Model+Dashboard)

## 🎯 Key Features

### Transaction Structuring
- **Multi-Tranche Debt Modeling** - Term Loan A/B, revolvers, subordinated debt
- **Debt Capacity Analysis** - Leverage ratios and covenant compliance
- **Sources & Uses** - Complete transaction financing structure
- **Purchase Price Allocation** - Asset allocation and goodwill calculation

### Financial Projections
- **5-Year Operating Model** - Revenue, EBITDA, and cash flow projections
- **Debt Schedule Modeling** - Amortization and optional prepayments
- **Working Capital Analysis** - Cash conversion cycle optimization
- **Tax Optimization** - Interest deductibility and tax shield benefits

### Exit Analysis & Returns
- **Multiple Exit Scenarios** - Strategic vs. financial buyer analysis
- **IRR & MOIC Calculations** - Money-on-money and internal rate of return
- **Dividend Recapitalization** - Interim cash distributions to sponsors
- **Management Equity** - Rollover and incentive plan modeling

## 💼 Real-World Application

This tool addresses key challenges from my experience in **Corporate & Investment Banking**:

### At BNP Paribas Paris (2023)
- **LBO Transaction Analysis** - Built cash-flow models for acquisition financing
- **Credit Risk Assessment** - Analyzed financial statements and industry dynamics  
- **Syndicated Financing** - Structured RCFs and term loan facilities
- **Due Diligence Support** - Collaborated with coverage teams on deal execution

### Technical Capabilities
- **Leverage Analysis** - Debt/EBITDA multiple optimization
- **Sensitivity Testing** - Revenue growth and margin compression scenarios  
- **Covenant Modeling** - Financial maintenance and incurrence covenants
- **Credit Committee Materials** - Investment memoranda and risk assessment

## 🏗️ Model Architecture

### Core Components
```
lbo_model/
├── src/
│   ├── transaction_structure.py    # Sources & uses, debt structure
│   ├── operating_model.py          # P&L, cash flow projections  
│   ├── debt_schedule.py            # Amortization and paydown
│   ├── exit_analysis.py            # Returns and sensitivity analysis
│   └── risk_assessment.py          # Credit metrics and covenants
├── templates/
│   └── lbo_template.xlsx           # Excel template for comparison
├── examples/
│   └── sample_transaction.py       # Worked example
└── requirements.txt
```

### Financial Model Flow
1. **Transaction Setup** → Purchase price, debt structure, sponsor equity
2. **Operating Projections** → 5-year revenue, EBITDA, cash flow forecasts
3. **Debt Modeling** → Amortization schedule and cash sweep mechanics
4. **Exit Analysis** → Multiple scenarios with IRR/MOIC calculations
5. **Sensitivity Analysis** → Key variable stress testing

## 📊 Sample Transaction Metrics

**Target Company:** TechCorp Industries  
**Enterprise Value:** €500M  
**Total Debt:** €350M (5.8x EBITDA)  
**Sponsor Equity:** €150M  

| Debt Tranche | Amount (€M) | Rate | Term | LTV |
|--------------|-------------|------|------|-----|
| **Term Loan A** | €100M | L+400bps | 7yr | 20% |
| **Term Loan B** | €200M | L+650bps | 8yr | 40% |
| **Revolver** | €25M | L+350bps | 5yr | 5% |
| **Sub Debt** | €25M | 8.5% | 10yr | 5% |

### Base Case Returns (10.0x Exit Multiple)
| Metric | Value |
|--------|-------|
| **Money Multiple** | 2.8x |
| **IRR** | 22.4% |
| **5-Year Revenue CAGR** | 8.2% |
| **Exit EBITDA** | €75M |

## 🚀 Quick Start

### Installation
```bash
# Clone repository
git clone https://github.com/LiamHirsch/lbo-modeling-tool.git
cd lbo-modeling-tool

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage
```python
from src.lbo_model import LBOAnalysis

# Initialize transaction
lbo = LBOAnalysis(
    company_name="TechCorp Industries",
    purchase_price=500,  # €500M
    sponsor_equity=150   # €150M
)

# Set debt structure  
lbo.structure_debt(
    term_loan_a=100,
    term_loan_b=200, 
    revolver=25,
    subordinated=25
)

# Build projections
lbo.build_model(
    base_revenue=200,
    revenue_growth=[0.08, 0.07, 0.06, 0.05],
    ebitda_margin=0.25
)

# Analyze returns
returns = lbo.exit_analysis(
    exit_multiples=[8.0, 9.0, 10.0, 11.0, 12.0]
)

print(f"Base Case IRR: {returns['10.0x']['irr']:.1%}")
print(f"Base Case MOIC: {returns['10.0x']['moic']:.1f}x")
```

## 📈 Visualizations & Analysis

### Transaction Overview
![Sources and Uses](https://via.placeholder.com/600x300/2E3440/88C0D0?text=Sources+and+Uses+Waterfall)

### Debt Paydown Schedule
![Debt Schedule](https://via.placeholder.com/600x300/2E3440/A3BE8C?text=Debt+Amortization+Schedule)

### Returns Analysis
![Returns Heatmap](https://via.placeholder.com/600x300/2E3440/EBCB8B?text=IRR+Returns+Heatmap)

### Sensitivity Analysis
![Tornado Chart](https://via.placeholder.com/600x300/2E3440/BF616A?text=Sensitivity+Tornado+Chart)

## 🎯 Use Cases

### Private Equity Funds
- **Deal Sourcing** - Quick transaction feasibility analysis
- **Investment Committee** - Comprehensive deal evaluation materials
- **Portfolio Management** - Ongoing performance monitoring
- **Exit Planning** - Strategic vs. financial buyer analysis

### Investment Banks
- **Pitch Books** - LBO transaction structuring proposals
- **Fairness Opinions** - Valuation analysis for board opinions
- **Syndication** - Debt capacity and structure optimization
- **Due Diligence** - Financial model validation

### Corporate Development
- **Acquisition Analysis** - Buy-side financial modeling
- **Strategic Planning** - Capital structure optimization
- **Board Reporting** - Transaction economics analysis

## 📊 Advanced Features

### Covenant Analysis
- Financial maintenance covenants (Net Leverage, FCCR)
- Incurrence covenants for additional debt/dividends  
- Covenant step-downs and pricing grids
- Cure mechanisms and equity contribution rights

### Management Equity
- Rollover percentage and vesting schedules
- Option pool sizing and strike price determination  
- Accelerated vesting upon exit scenarios
- Tax optimization strategies

### Dividend Policy
- Recurring dividend capacity modeling
- Special dividend recapitalization analysis
- Available amount basket calculations
- Debt/EBITDA ratio maintenance

## 🔬 Technical Methodology

### Valuation Approach
- **DCF Analysis** - Unlevered free cash flow projections
- **Comparable Company** - Trading and transaction multiples
- **Precedent Transactions** - Industry-specific benchmarking
- **Sum-of-the-Parts** - Division-level valuation analysis

### Risk Assessment
- **Business Risk** - Industry dynamics and competitive position
- **Financial Risk** - Leverage, liquidity, and covenant compliance  
- **Execution Risk** - Management team and operational improvements
- **Market Risk** - Economic sensitivity and cyclical exposure

## 📚 Documentation

- [**Installation Guide**](docs/installation.md) - Setup and configuration
- [**Model Methodology**](docs/methodology.md) - Financial modeling approach
- [**API Reference**](docs/api_reference.md) - Function documentation  
- [**Case Studies**](docs/case_studies.md) - Worked transaction examples

## 🤝 Contributing

Professional development practices following PE industry standards:

1. **Fork** the repository
2. **Create feature branch** (`git checkout -b feature/DebtScheduleUpdate`)
3. **Commit changes** (`git commit -m 'Add covenant analysis'`)
4. **Push to branch** (`git push origin feature/DebtScheduleUpdate`)  
5. **Open Pull Request** with detailed description

## 📧 Contact

**Liam Hirsch** - Finance & Technology Professional  
📧 [hirschliam17@gmail.com](mailto:hirschliam17@gmail.com)  
🔗 [LinkedIn](https://linkedin.com/in/liam-hirsch1709)  
📍 Frankfurt am Main, Germany

---

## ⚠️ Disclaimer

This tool is for educational and analytical purposes. LBO models should be validated by qualified financial professionals. Past performance does not guarantee future results.

**Built with Corporate Banking experience from BNP Paribas Paris**
