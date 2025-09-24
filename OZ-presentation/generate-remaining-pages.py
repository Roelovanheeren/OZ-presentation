#!/usr/bin/env python3

import os

# Common styles for all pages
common_styles = '''
<style>
    .content-page {
        height: 100%;
        width: 100%;
    }
    
    .content-page h2 {
        font-family: 'Playfair Display', serif;
        font-size: 28pt;
        font-weight: 700;
        color: #000;
        margin-bottom: 20px;
        border-left: 4px solid #000;
        padding-left: 20px;
    }
    
    .content-page h3 {
        font-family: 'Playfair Display', serif;
        font-size: 18pt;
        font-weight: 600;
        color: #000;
        margin: 20px 0 10px 0;
    }
    
    .content-page p {
        font-family: 'Inter', sans-serif;
        font-size: 13pt;
        line-height: 1.6;
        color: #000;
        margin-bottom: 15px;
    }
    
    .stat-box {
        background: #000;
        color: white;
        padding: 20px;
        border-radius: 8px;
        margin: 20px 0;
        text-align: center;
    }
    
    .stat-box .number {
        font-family: 'Playfair Display', serif;
        font-size: 32pt;
        font-weight: 700;
        display: block;
    }
    
    .stat-box .label {
        font-family: 'Inter', sans-serif;
        font-size: 14pt;
        margin-top: 5px;
    }
    
    .highlight-box {
        background: #f5f5f5;
        border: 2px solid #000;
        padding: 20px;
        margin: 20px 0;
        border-radius: 8px;
    }
    
    .highlight-box h3 {
        font-family: 'Playfair Display', serif;
        font-size: 18pt;
        font-weight: 700;
        color: #000;
        margin: 0 0 10px 0;
    }
    
    .callout-box {
        background: #e0e0e0;
        padding: 20px;
        margin: 20px 0;
        border-radius: 8px;
        text-align: center;
    }
    
    .callout-box h3 {
        font-family: 'Playfair Display', serif;
        font-size: 18pt;
        font-weight: 700;
        color: #000;
        margin: 0 0 10px 0;
    }
    
    .sidebar-box {
        background: #f0f0f0;
        padding: 20px;
        margin: 20px 0;
        border-radius: 8px;
        border-left: 4px solid #000;
    }
    
    .sidebar-box h3 {
        font-family: 'Playfair Display', serif;
        font-size: 16pt;
        font-weight: 700;
        color: #000;
        margin: 0 0 10px 0;
    }
    
    .chart-container {
        margin: 20px 0;
        text-align: center;
    }
    
    .chart-container img {
        width: 100%;
        height: 300px;
        object-fit: cover;
        border-radius: 8px;
    }
    
    .disclaimer {
        border-top: 2px solid #000;
        margin-top: 30px;
        padding-top: 20px;
        font-size: 10pt;
        color: #666;
    }
    
    @media (max-width: 768px) {
        .content-page h2 {
            font-size: 24pt;
        }
        
        .content-page h3 {
            font-size: 16pt;
        }
        
        .content-page p {
            font-size: 12pt;
        }
        
        .stat-box .number {
            font-size: 28pt;
        }
        
        .stat-box .label {
            font-size: 12pt;
        }
    }
</style>
'''

# Page content data
pages = {
    'page-04-what-are-oz.html': {
        'title': '2. What Opportunity Zones Are',
        'content': '''
        <p>Opportunity Zones are economically distressed communities where new investments may be eligible for preferential tax treatment. Created by the Tax Cuts and Jobs Act of 2017, these zones are designed to spur economic development and job creation in low-income communities across the United States.</p>
        
        <div class="chart-container">
            <img src="https://via.placeholder.com/600x400/f0f0f0/666666?text=US+Map+with+Opportunity+Zones" alt="US Map with Opportunity Zones">
        </div>
        
        <h3>Designation Process</h3>
        <p>Opportunity Zones are nominated by state governors and certified by the U.S. Treasury Department. Each state can nominate up to 25% of its low-income census tracts, with a minimum of 25 zones per state.</p>
        
        <div class="sidebar-box">
            <h3>Twin Benefits</h3>
            <p>Opportunity Zones provide dual advantages: significant tax benefits for investors and meaningful economic development for underserved communities.</p>
        </div>
        
        <h3>Geographic Distribution</h3>
        <p>Over 8,700 Opportunity Zones exist across all 50 states, the District of Columbia, and five U.S. territories. These zones represent diverse markets, from urban cores to rural communities.</p>
        '''
    },
    'page-05-tax-advantage.html': {
        'title': '3. The Tax Advantage Framework',
        'content': '''
        <p>The Opportunity Zone tax framework provides three distinct benefits that can significantly enhance after-tax returns for qualified investments.</p>
        
        <h3>Tax Deferral</h3>
        <p>Capital gains invested in Opportunity Zones are deferred until December 31, 2026, or until the investment is sold, whichever comes first. This deferral provides immediate liquidity benefits and allows for compound growth on the deferred tax liability.</p>
        
        <h3>Tax Reduction</h3>
        <p>5-Year Hold: 10% reduction in deferred gains<br>
        7-Year Hold: 15% reduction in deferred gains<br>
        Maximum Benefit: Achieved by holding until December 31, 2026</p>
        
        <div class="chart-container">
            <img src="https://via.placeholder.com/600x300/e8e8e8/333333?text=Tax+Deferral+Timeline+2027+to+2035" alt="Tax Deferral Timeline">
        </div>
        
        <h3>Tax-Free Appreciation</h3>
        <p>The most significant benefit is the complete elimination of capital gains tax on appreciation for investments held for 10 or more years.</p>
        
        <div class="callout-box">
            <h3>Illustrative Example: $2M → $5M Growth</h3>
            <p>Original gain: $2M (deferred until 2026)<br>
            Investment appreciation: $3M (tax-free after 10 years)<br>
            Total tax savings: $600K+ (assuming 20% capital gains rate)</p>
        </div>
        '''
    },
    'page-06-compliance.html': {
        'title': '4. Compliance Architecture',
        'content': '''
        <h3>90% Asset Test</h3>
        <p>Qualified Opportunity Funds must maintain at least 90% of their assets in Opportunity Zone property. This test is measured semi-annually and requires careful asset allocation management.</p>
        
        <div class="chart-container">
            <img src="https://via.placeholder.com/600x250/f5f5f5/333333?text=Compliance+Checklist+Graphic" alt="Compliance Checklist">
        </div>
        
        <h3>Safe Harbor Provisions</h3>
        <p>Safe harbor rules provide flexibility for working capital and development activities, allowing up to 31 months for property improvement and business development within Opportunity Zones.</p>
        
        <h3>Substantial Improvement Requirements</h3>
        <p>Existing property must be substantially improved, defined as doubling the adjusted basis of the property through improvements within 30 months of acquisition.</p>
        
        <h3>IRS Scrutiny and Documentation</h3>
        <p>Comprehensive documentation is essential for IRS compliance, including detailed records of asset allocation, improvement activities, and business operations within Opportunity Zones.</p>
        '''
    },
    'page-07-investment-structures.html': {
        'title': '5. Investment Structures & Costs',
        'content': '''
        <h3>Qualified Opportunity Fund Structures</h3>
        <p>QOFs can be structured as partnerships, corporations, or LLCs, each offering different advantages for tax treatment, management flexibility, and investor liquidity.</p>
        
        <h3>Institutional vs. Self-Managed</h3>
        <p>Institutional QOFs provide professional management and diversification, while self-managed QOFs offer greater control and potentially lower fees for sophisticated investors.</p>
        
        <h3>Fee Structures</h3>
        <p>Typical fee structures include management fees (1-2% annually), performance fees (10-20% of profits), and acquisition fees (1-3% of invested capital).</p>
        
        <h3>Minimum Investment Requirements</h3>
        <p>Minimum investments typically range from $25,000 to $1,000,000, depending on the fund structure and target investor base.</p>
        '''
    },
    'page-08-real-estate.html': {
        'title': '6. Why Real Estate Dominates',
        'content': '''
        <h3>Asset Class Advantages</h3>
        <p>Real estate represents approximately 75% of Opportunity Zone investments due to its tangible nature, predictable cash flows, and alignment with community development goals.</p>
        
        <div class="chart-container">
            <img src="https://via.placeholder.com/400x400/f8f9fa/333333?text=Pie+Chart+75%25+Real+Estate" alt="Real Estate Investment Distribution">
        </div>
        
        <h3>Development Opportunities</h3>
        <p>Opportunity Zones often contain underutilized or vacant properties suitable for redevelopment, creating value through improvement and repositioning.</p>
        
        <h3>Cash Flow Generation</h3>
        <p>Real estate investments can generate immediate cash flow through rental income, providing ongoing returns while benefiting from tax advantages.</p>
        
        <h3>Appreciation Potential</h3>
        <p>The combination of community development and economic growth in Opportunity Zones creates significant appreciation potential over the 10-year hold period.</p>
        '''
    },
    'page-09-phoenix-market.html': {
        'title': '7. Phoenix Market Deep Dive',
        'content': '''
        <p>Phoenix represents one of the most compelling Opportunity Zone markets in the United States, offering a unique combination of rapid population growth, economic diversification, and favorable regulatory environment.</p>
        
        <div class="chart-container">
            <img src="https://via.placeholder.com/600x400/e8f4f8/333333?text=Arizona+Map+with+Phoenix+Highlighted" alt="Arizona Map with Phoenix">
        </div>
        
        <div class="stat-box">
            <span class="number">+100k</span>
            <span class="label">Annual Migration to Phoenix</span>
        </div>
        
        <h3>Demographic Trends</h3>
        <p>Phoenix has experienced consistent population growth exceeding 100,000 new residents annually, driven by migration from high-tax states, retirees seeking favorable climate, and young professionals attracted by job opportunities.</p>
        
        <div class="sidebar-box">
            <h3>Key Market Drivers</h3>
            <p>• No state income tax<br>
            • Business-friendly regulatory environment<br>
            • Major corporate relocations (Intel, TSMC)<br>
            • Growing tech sector<br>
            • Affordable cost of living</p>
        </div>
        
        <h3>Economic Diversification</h3>
        <p>The Phoenix economy has evolved beyond traditional sectors like tourism and agriculture to include significant technology, healthcare, financial services, and advanced manufacturing.</p>
        '''
    },
    'page-10-hazen-road.html': {
        'title': '8. Hazen Road BTR Example',
        'content': '''
        <h3>Project Overview</h3>
        <p>The Hazen Road Build-to-Rent development represents a $52 million Opportunity Zone investment in Phoenix, demonstrating the potential for institutional-scale projects.</p>
        
        <div class="chart-container">
            <img src="https://via.placeholder.com/600x300/f0f8ff/333333?text=Investment+Flow+Diagram+$52M+Project" alt="Investment Flow Diagram">
        </div>
        
        <h3>Investment Structure</h3>
        <p>Investor gains are deployed through a Qualified Opportunity Fund into the $52M project, with planned refinancing in years 3-4 and a 10-year hold strategy.</p>
        
        <div class="callout-box">
            <h3>Community Impact: Attainable Housing</h3>
            <p>The project addresses Phoenix's housing shortage while providing institutional-quality returns and significant tax benefits.</p>
        </div>
        
        <h3>Financial Projections</h3>
        <p>Projected returns include 6-8% cash-on-cash yields, 12-15% IRR, and tax-free appreciation on the 10-year hold period.</p>
        '''
    },
    'page-11-risk-management.html': {
        'title': '9. Risk Management & Mitigation',
        'content': '''
        <h3>Liquidity Risk</h3>
        <p>Opportunity Zone investments require long-term commitments. Mitigation through diversification and professional management reduces concentration risk.</p>
        
        <h3>Execution Risk</h3>
        <p>Development and operational risks are managed through experienced sponsors, conservative underwriting, and comprehensive due diligence processes.</p>
        
        <h3>Compliance Risk</h3>
        <p>Regulatory compliance is maintained through professional legal and tax advisors, regular monitoring, and comprehensive documentation systems.</p>
        
        <h3>Regulatory Risk</h3>
        <p>Changes in Opportunity Zone regulations are monitored through industry associations and legal counsel, with contingency planning for potential modifications.</p>
        '''
    },
    'page-12-exit-strategy.html': {
        'title': '10. Exit Strategy Design',
        'content': '''
        <h3>Refinancing Strategy</h3>
        <p>Planned refinancing in years 3-4 allows for capital return while maintaining Opportunity Zone compliance and tax benefits.</p>
        
        <h3>10-Year Hold Period</h3>
        <p>The full 10-year hold maximizes tax benefits, including complete elimination of capital gains tax on appreciation.</p>
        
        <h3>Estate Planning Integration</h3>
        <p>Long-term holds align with estate planning strategies, allowing for tax-efficient wealth transfer to heirs.</p>
        
        <div class="callout-box">
            <h3>Tax-Free Appreciation</h3>
            <p>After 10 years, all appreciation above the original deferred gain amount is completely tax-free, providing significant value enhancement.</p>
        </div>
        '''
    },
    'page-13-legal-regulatory.html': {
        'title': '11. Legal & Regulatory Environment',
        'content': '''
        <h3>Federal Framework</h3>
        <p>The Opportunity Zone program is established under federal law, providing consistent tax benefits across all states and territories.</p>
        
        <h3>State Conformity</h3>
        <p>Most states conform to federal Opportunity Zone provisions, though California, Massachusetts, and North Carolina have exceptions that require careful planning.</p>
        
        <h3>Regulatory Updates</h3>
        <p>Ongoing regulatory guidance from the IRS and Treasury Department continues to clarify compliance requirements and investment structures.</p>
        
        <h3>Legal Considerations</h3>
        <p>Professional legal counsel is essential for structuring investments, ensuring compliance, and maximizing tax benefits within the regulatory framework.</p>
        '''
    },
    'page-14-eligibility.html': {
        'title': '12. Eligibility & Gain Source Rules',
        'content': '''
        <h3>Eligible Gain Sources</h3>
        <p>Capital gains from stocks, real estate, cryptocurrency, art, and other investments can be deferred through Opportunity Zone investments.</p>
        
        <h3>180-Day Rule</h3>
        <p>Investments must be made within 180 days of the gain recognition date, with different rules for individuals versus partnerships and corporations.</p>
        
        <h3>Partnership Considerations</h3>
        <p>Partnership gains create unique timing considerations, as the 180-day period begins when the partnership recognizes the gain, not when distributions are made.</p>
        
        <h3>Documentation Requirements</h3>
        <p>Comprehensive documentation of gain sources, timing, and investment amounts is essential for IRS compliance and audit protection.</p>
        '''
    },
    'page-15-reporting.html': {
        'title': '13. Reporting & Administrative Burden',
        'content': '''
        <h3>IRS Form 8996</h3>
        <p>Qualified Opportunity Funds must file Form 8996 annually to report compliance with the 90% asset test and other requirements.</p>
        
        <h3>IRS Form 8997</h3>
        <p>Investors must file Form 8997 to report their Opportunity Zone investments and calculate deferred gains and basis adjustments.</p>
        
        <h3>Record Keeping</h3>
        <p>Comprehensive record keeping is essential for compliance, including documentation of asset allocation, improvement activities, and business operations.</p>
        
        <h3>Professional Support</h3>
        <p>Professional tax and legal support is recommended to ensure compliance and maximize benefits within the complex regulatory framework.</p>
        '''
    },
    'page-16-community-impact.html': {
        'title': '14. Community Impact & ESG Narrative',
        'content': '''
        <h3>ESG Alignment</h3>
        <p>Opportunity Zone investments align with Environmental, Social, and Governance (ESG) principles through community development and economic inclusion.</p>
        
        <h3>Community Benefits</h3>
        <p>Investments create jobs, affordable housing, and infrastructure improvements in underserved communities, generating measurable social impact.</p>
        
        <h3>Impact Measurement</h3>
        <p>Professional impact measurement and reporting demonstrate the social and economic benefits of Opportunity Zone investments to stakeholders.</p>
        
        <h3>Stakeholder Engagement</h3>
        <p>Community engagement and stakeholder alignment enhance project success and create long-term value for both investors and communities.</p>
        '''
    },
    'page-17-case-studies.html': {
        'title': '15. Practical Case Studies',
        'content': '''
        <h3>Success Stories</h3>
        <p>Successful Opportunity Zone projects demonstrate strong returns, community impact, and effective risk management through professional execution.</p>
        
        <h3>Common Challenges</h3>
        <p>Failed projects often result from inadequate due diligence, poor location selection, or insufficient capital for development and operations.</p>
        
        <h3>Lessons Learned</h3>
        <p>Key success factors include experienced sponsors, strong market fundamentals, adequate capitalization, and comprehensive risk management.</p>
        
        <h3>Best Practices</h3>
        <p>Professional management, conservative underwriting, and community engagement are essential for successful Opportunity Zone investments.</p>
        '''
    },
    'page-18-comparative.html': {
        'title': '16. Comparative Landscape',
        'content': '''
        <h3>1031 Exchanges</h3>
        <p>Opportunity Zones offer advantages over 1031 exchanges, including broader asset eligibility, longer deferral periods, and potential tax-free appreciation.</p>
        
        <h3>DST/REIT Investments</h3>
        <p>Compared to DST and REIT investments, Opportunity Zones provide unique tax benefits but require longer hold periods and more complex compliance.</p>
        
        <h3>Traditional Real Estate</h3>
        <p>Opportunity Zone investments offer superior after-tax returns compared to traditional real estate investments, particularly for high-net-worth investors.</p>
        
        <h3>Alternative Investments</h3>
        <p>The combination of tax benefits, community impact, and real estate fundamentals makes Opportunity Zones attractive relative to other alternative investments.</p>
        '''
    },
    'page-19-investor-protections.html': {
        'title': '17. Investor Protections & Alignment',
        'content': '''
        <h3>Sponsor Alignment</h3>
        <p>Effective sponsors demonstrate alignment through co-investment, performance-based compensation, and transparent reporting to investors.</p>
        
        <h3>Waterfall Structures</h3>
        <p>Preferred return structures and profit-sharing arrangements ensure investor protection while incentivizing sponsor performance.</p>
        
        <h3>IRR Disclosure</h3>
        <p>Transparent IRR reporting and regular investor communications build trust and demonstrate sponsor commitment to investor success.</p>
        
        <div class="callout-box">
            <h3>Alignment is Transparency</h3>
            <p>True alignment between sponsors and investors is achieved through transparency, co-investment, and performance-based compensation structures.</p>
        </div>
        '''
    },
    'page-20-timeline.html': {
        'title': '18. Timeline & Deadlines',
        'content': '''
        <h3>Critical Deadlines</h3>
        <p>December 31, 2026 marks the deadline for tax reduction benefits, making early investment timing crucial for maximizing benefits.</p>
        
        <h3>Investment Timeline</h3>
        <p>2025-2026: Optimal investment period for maximum tax benefits<br>
        2027-2035: Tax deferral period<br>
        2035+: Tax-free appreciation period</p>
        
        <h3>Compliance Milestones</h3>
        <p>Regular compliance monitoring, annual reporting, and milestone tracking ensure continued qualification for tax benefits.</p>
        
        <h3>Exit Planning</h3>
        <p>Strategic exit planning considers tax implications, market conditions, and investor objectives within the regulatory framework.</p>
        '''
    },
    'page-21-action-plan.html': {
        'title': '19. Investor Action Plan',
        'content': '''
        <h3>Step 1: Identify Gains</h3>
        <p>Review investment portfolio for eligible capital gains that can be deferred through Opportunity Zone investments.</p>
        
        <h3>Step 2: Evaluate Timing</h3>
        <p>Assess timing considerations, including the 180-day rule and December 31, 2026 deadline for maximum tax benefits.</p>
        
        <h3>Step 3: Due Diligence</h3>
        <p>Conduct comprehensive due diligence on sponsors, markets, and investment opportunities to ensure alignment with objectives.</p>
        
        <h3>Step 4: Structure Investment</h3>
        <p>Work with legal and tax advisors to structure investments for maximum tax benefits and compliance with regulatory requirements.</p>
        
        <h3>Step 5: Deploy Capital</h3>
        <p>Execute investment strategy with professional management and ongoing monitoring to ensure success and compliance.</p>
        '''
    },
    'page-22-conclusion.html': {
        'title': '20. Conclusion & Disclaimer',
        'content': '''
        <h3>Investment Summary</h3>
        <p>Opportunity Zone investing offers sophisticated investors significant tax advantages, community impact opportunities, and potential for superior risk-adjusted returns through careful execution and professional management.</p>
        
        <h3>Key Success Factors</h3>
        <p>Success requires experienced sponsors, strong market fundamentals, adequate capitalization, comprehensive due diligence, and ongoing professional support.</p>
        
        <h3>Strategic Recommendations</h3>
        <p>Investors should prioritize early investment timing, professional management, and long-term commitment to maximize benefits within the regulatory framework.</p>
        
        <div class="disclaimer">
            <p><strong>Disclaimer:</strong> This document is for informational purposes only and does not constitute investment advice. Investors should consult with qualified tax, legal, and financial advisors before making investment decisions. Past performance does not guarantee future results. Opportunity Zone investments involve significant risks and may not be suitable for all investors.</p>
        </div>
        '''
    }
}

# Generate all pages
for filename, page_data in pages.items():
    content = f'''{common_styles}

<div class="content-page">
    <h2>{page_data['title']}</h2>
    {page_data['content']}
</div>'''
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Generated {filename}")

print("All remaining pages generated successfully!")
