"""
Automated Actions Module - Enhanced Email Reports
Beautiful, professional email reports with enhanced formatting
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os

logger = logging.getLogger(__name__)


class EnhancedEmailReporter:
    """
    Creates and sends beautiful, professional AI update emails
    """
    
    def __init__(self, email_config: Dict[str, str]):
        """
        Initialize email reporter
        
        Args:
            email_config: Dict with smtp_server, smtp_port, username, password, from_email, to_email
        """
        self.config = email_config
        logger.info("✓ Enhanced email reporter initialized")
    
    async def send_daily_report(
        self,
        analysis: Dict[str, Any],
        all_data: Dict[str, List],
        stats: Dict[str, Any]
    ) -> bool:
        """
        Send comprehensive daily AI update email
        """
        logger.info("="*70)
        logger.info("Generating and sending daily AI update email")
        logger.info("="*70)
        
        try:
            # Create email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = self._create_subject_line(analysis)
            msg['From'] = self.config['from_email']
            msg['To'] = self.config['to_email']
            msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
            
            # Create both HTML and plain text versions
            html_body = self._create_html_email(analysis, all_data, stats)
            text_body = self._create_text_email(analysis, all_data, stats)
            
            # Attach both versions
            part1 = MIMEText(text_body, 'plain', 'utf-8')
            part2 = MIMEText(html_body, 'html', 'utf-8')
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            logger.info("Sending email...")
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls()
                server.login(self.config['username'], self.config['password'])
                server.send_message(msg)
            
            logger.info(f"✓ Email sent successfully to {self.config['to_email']}")
            logger.info("="*70)
            return True
            
        except Exception as e:
            logger.error(f"✗ Email sending failed: {e}")
            logger.info("="*70)
            return False
    
    def _create_subject_line(self, analysis: Dict) -> str:
        """Create engaging subject line"""
        date_str = datetime.now().strftime('%B %d, %Y')
        
        # Try to extract key topic from summary
        summary = analysis.get('executive_summary', '')
        
        # Simple but engaging subject
        return f"🤖 Daily AI Update - {date_str} | Latest Breakthroughs & Trends"
    
    def _create_html_email(
        self,
        analysis: Dict,
        all_data: Dict,
        stats: Dict
    ) -> str:
        """Create beautiful HTML email"""
        
        # Header section
        header = self._create_email_header(stats)
        
        # Executive summary section
        exec_summary = self._create_executive_summary_section(analysis)
        
        # Key developments section
        key_devs = self._create_key_developments_section(analysis)
        
        # Trends section
        trends = self._create_trends_section(analysis)
        
        # Breakthrough technologies section
        breakthroughs = self._create_breakthroughs_section(analysis)
        
        # Industry impact section
        industry = self._create_industry_impact_section(analysis)
        
        # Actionable insights section
        insights = self._create_actionable_insights_section(analysis)
        
        # Future predictions section
        future = self._create_future_predictions_section(analysis)
        
        # Source articles section
        sources = self._create_sources_section(all_data, analysis)
        
        # Footer
        footer = self._create_email_footer()
        
        # Complete HTML
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily AI Update</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: #f5f7fa;
            color: #2d3748;
            line-height: 1.6;
        }}
        .container {{
            max-width: 700px;
            margin: 0 auto;
            background-color: #ffffff;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 32px;
            font-weight: 700;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header .subtitle {{
            margin: 10px 0 0 0;
            font-size: 16px;
            opacity: 0.95;
        }}
        .stats-bar {{
            background: rgba(255,255,255,0.15);
            padding: 20px;
            margin-top: 20px;
            border-radius: 8px;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }}
        .stat-item {{
            text-align: center;
            padding: 10px;
        }}
        .stat-number {{
            font-size: 28px;
            font-weight: 700;
            display: block;
        }}
        .stat-label {{
            font-size: 12px;
            text-transform: uppercase;
            opacity: 0.9;
            letter-spacing: 0.5px;
        }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .section-title {{
            font-size: 24px;
            font-weight: 700;
            color: #1a202c;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        .section-title .emoji {{
            margin-right: 10px;
        }}
        .card {{
            background: #f7fafc;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .card-title {{
            font-size: 18px;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 10px;
        }}
        .card-content {{
            color: #4a5568;
            margin-bottom: 10px;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-right: 8px;
            margin-bottom: 8px;
        }}
        .badge-critical {{ background: #fee; color: #c53030; }}
        .badge-high {{ background: #fef5e7; color: #d97706; }}
        .badge-medium {{ background: #e6f7ff; color: #2563eb; }}
        .badge-low {{ background: #f0f0f0; color: #64748b; }}
        .badge-research {{ background: #f0fdf4; color: #059669; }}
        .badge-tool {{ background: #fef3c7; color: #d97706; }}
        .numbered-list {{
            counter-reset: item;
            list-style: none;
            padding-left: 0;
        }}
        .numbered-list li {{
            counter-increment: item;
            margin-bottom: 20px;
            padding-left: 40px;
            position: relative;
        }}
        .numbered-list li::before {{
            content: counter(item);
            position: absolute;
            left: 0;
            top: 0;
            background: #667eea;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
        }}
        .trend-item {{
            padding: 15px;
            background: white;
            border-radius: 8px;
            margin-bottom: 15px;
            border: 1px solid #e2e8f0;
        }}
        .trend-title {{
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 8px;
        }}
        .trend-strength {{
            display: inline-block;
            padding: 2px 8px;
            background: #10b981;
            color: white;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .insights-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
        }}
        .insight-box {{
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .insight-title {{
            font-weight: 700;
            color: #667eea;
            margin-bottom: 10px;
            font-size: 16px;
        }}
        .insight-list {{
            list-style: none;
            padding-left: 0;
        }}
        .insight-list li {{
            padding-left: 20px;
            margin-bottom: 8px;
            position: relative;
        }}
        .insight-list li::before {{
            content: "→";
            position: absolute;
            left: 0;
            color: #667eea;
            font-weight: 700;
        }}
        .source-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
        }}
        .source-card {{
            background: white;
            border: 1px solid #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            transition: box-shadow 0.3s;
        }}
        .source-card:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .source-title {{
            font-size: 16px;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 10px;
        }}
        .source-meta {{
            font-size: 13px;
            color: #718096;
            margin-bottom: 10px;
        }}
        .source-link {{
            display: inline-block;
            margin-top: 10px;
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
        }}
        .source-link:hover {{
            text-decoration: underline;
        }}
        .footer {{
            background: #2d3748;
            color: #cbd5e0;
            padding: 30px;
            text-align: center;
            font-size: 14px;
        }}
        .footer-links {{
            margin-top: 15px;
        }}
        .footer-link {{
            color: #90cdf4;
            text-decoration: none;
            margin: 0 10px;
        }}
        @media only screen and (max-width: 600px) {{
            .header {{
                padding: 30px 20px;
            }}
            .header h1 {{
                font-size: 24px;
            }}
            .content {{
                padding: 20px;
            }}
            .section-title {{
                font-size: 20px;
            }}
            .stats-bar {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {header}
        <div class="content">
            {exec_summary}
            {key_devs}
            {trends}
            {breakthroughs}
            {industry}
            {insights}
            {future}
            {sources}
        </div>
        {footer}
    </div>
</body>
</html>
"""
        
        return html
    
    def _create_email_header(self, stats: Dict) -> str:
        """Create email header with stats"""
        date_str = datetime.now().strftime('%B %d, %Y')
        time_str = datetime.now().strftime('%I:%M %p')
        
        total_items = stats.get('total_items', 0)
        sources_count = stats.get('sources_count', 0)
        
        # Count by category
        categories = stats.get('by_category', {})
        research_count = categories.get('Research Paper', 0) + categories.get('Research with Code', 0)
        models_count = categories.get('Model Release', 0)
        tools_count = categories.get('Open Source Tool', 0) + categories.get('Tool Update', 0)
        
        return f"""
        <div class="header">
            <h1>🤖 Daily AI Update</h1>
            <p class="subtitle">{date_str} • {time_str}</p>
            <div class="stats-bar">
                <div class="stat-item">
                    <span class="stat-number">{total_items}</span>
                    <span class="stat-label">Total Updates</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{sources_count}</span>
                    <span class="stat-label">Sources</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{research_count}</span>
                    <span class="stat-label">Papers</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{models_count}</span>
                    <span class="stat-label">Models</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{tools_count}</span>
                    <span class="stat-label">Tools</span>
                </div>
            </div>
        </div>
        """
    
    def _create_executive_summary_section(self, analysis: Dict) -> str:
        """Create executive summary section"""
        summary = analysis.get('executive_summary', 'No summary available')
        
        return f"""
        <div class="section">
            <h2 class="section-title"><span class="emoji">📊</span>Executive Summary</h2>
            <div class="card">
                <div class="card-content" style="white-space: pre-wrap;">{summary}</div>
            </div>
        </div>
        """
    
    def _create_key_developments_section(self, analysis: Dict) -> str:
        """Create key developments section"""
        developments = analysis.get('key_developments', [])
        
        if not developments:
            return ""
        
        items_html = ""
        for dev in developments[:10]:
            importance = dev.get('importance', 'Medium')
            badge_class = {
                'Critical': 'badge-critical',
                'High': 'badge-high',
                'Medium': 'badge-medium'
            }.get(importance, 'badge-medium')
            
            category = dev.get('category', 'Unknown')
            category_badge_class = {
                'Model Release': 'badge-high',
                'Research': 'badge-research',
                'Tool': 'badge-tool',
                'News': 'badge-medium'
            }.get(category, 'badge-medium')
            
            items_html += f"""
            <li>
                <div style="margin-bottom: 5px;">
                    <span class="badge {badge_class}">{importance}</span>
                    <span class="badge {category_badge_class}">{category}</span>
                </div>
                <div class="card-title">{dev.get('title', 'Unknown')}</div>
                <div class="card-content">
                    <strong>Impact:</strong> {dev.get('impact', 'N/A')}<br>
                    <strong>Timeframe:</strong> {dev.get('timeframe', 'N/A')}<br>
                    <strong>Key Takeaway:</strong> {dev.get('key_takeaway', 'N/A')}
                </div>
            </li>
            """
        
        return f"""
        <div class="section">
            <h2 class="section-title"><span class="emoji">🔥</span>Top 10 Key Developments</h2>
            <ol class="numbered-list">
                {items_html}
            </ol>
        </div>
        """
    
    def _create_trends_section(self, analysis: Dict) -> str:
        """Create trends and patterns section"""
        trends_data = analysis.get('trends_and_patterns', {})
        
        if not trends_data:
            return ""
        
        emerging_trends = trends_data.get('emerging_trends', [])
        dominant_themes = trends_data.get('dominant_themes', [])
        
        trends_html = ""
        for trend in emerging_trends[:5]:
            trends_html += f"""
            <div class="trend-item">
                <div class="trend-title">{trend.get('trend', 'Unknown')}</div>
                <span class="trend-strength">{trend.get('strength', 'Medium')} Strength</span>
                <p style="margin-top: 10px; color: #4a5568;">{trend.get('description', 'No description')}</p>
            </div>
            """
        
        themes_html = ""
        for theme in dominant_themes[:3]:
            themes_html += f"""
            <div class="card">
                <div class="card-title">{theme.get('theme', 'Unknown')}</div>
                <div class="card-content">
                    <strong>Prevalence:</strong> {theme.get('prevalence', 'N/A')}<br>
                    <strong>Significance:</strong> {theme.get('significance', 'N/A')}
                </div>
            </div>
            """
        
        return f"""
        <div class="section">
            <h2 class="section-title"><span class="emoji">📈</span>Trends & Patterns</h2>
            <h3 style="margin-bottom: 15px; color: #4a5568;">Emerging Trends</h3>
            {trends_html}
            <h3 style="margin: 30px 0 15px 0; color: #4a5568;">Dominant Themes</h3>
            {themes_html}
        </div>
        """
    
    def _create_breakthroughs_section(self, analysis: Dict) -> str:
        """Create breakthrough technologies section"""
        breakthroughs = analysis.get('breakthrough_technologies', [])
        
        if not breakthroughs:
            return ""
        
        items_html = ""
        for bt in breakthroughs[:5]:
            items_html += f"""
            <div class="card">
                <div class="card-title">🚀 {bt.get('technology', 'Unknown')}</div>
                <div class="card-content">
                    <strong>Innovation:</strong> {bt.get('innovation', 'N/A')}<br>
                    <strong>Capability:</strong> {bt.get('capability', 'N/A')}<br>
                    <strong>Adoption Timeline:</strong> {bt.get('adoption_timeline', 'N/A')}
                </div>
            </div>
            """
        
        return f"""
        <div class="section">
            <h2 class="section-title"><span class="emoji">💡</span>Breakthrough Technologies</h2>
            {items_html}
        </div>
        """
    
    def _create_industry_impact_section(self, analysis: Dict) -> str:
        """Create industry impact section"""
        impact = analysis.get('industry_impact', {})
        
        if not impact:
            return ""
        
        # Show top affected industries
        impact_html = ""
        for industry, details in list(impact.items())[:5]:
            if isinstance(details, dict):
                impact_html += f"""
                <div class="card">
                    <div class="card-title">{industry}</div>
                    <div class="card-content">
                        {details.get('direct_impact', 'No impact details available')}
                    </div>
                </div>
                """
        
        return f"""
        <div class="section">
            <h2 class="section-title"><span class="emoji">🏭</span>Industry Impact</h2>
            {impact_html}
        </div>
        """
    
    def _create_actionable_insights_section(self, analysis: Dict) -> str:
        """Create actionable insights section"""
        insights = analysis.get('actionable_insights', {})
        
        if not insights:
            return ""
        
        insights_html = ""
        
        insight_emojis = {
            'ai_practitioners': '👨‍💻',
            'business_leaders': '💼',
            'researchers': '🔬',
            'investors': '💰',
            'general_public': '👥'
        }
        
        for key, items in insights.items():
            if isinstance(items, list) and items:
                title = key.replace('_', ' ').title()
                emoji = insight_emojis.get(key, '•')
                
                items_list = "".join([f"<li>{item}</li>" for item in items[:5]])
                
                insights_html += f"""
                <div class="insight-box">
                    <div class="insight-title">{emoji} {title}</div>
                    <ul class="insight-list">
                        {items_list}
                    </ul>
                </div>
                """
        
        return f"""
        <div class="section">
            <h2 class="section-title"><span class="emoji">💡</span>Actionable Insights</h2>
            <div class="insights-grid">
                {insights_html}
            </div>
        </div>
        """
    
    def _create_future_predictions_section(self, analysis: Dict) -> str:
        """Create future predictions section"""
        predictions = analysis.get('future_predictions', {})
        
        if not predictions:
            return ""
        
        timeframes = ['next_week', 'next_month', 'next_quarter']
        pred_html = ""
        
        for tf in timeframes:
            data = predictions.get(tf, [])
            if data:
                title = tf.replace('_', ' ').title()
                if isinstance(data, list):
                    items = "".join([f"<li>{item}</li>" for item in data[:5]])
                    pred_html += f"""
                    <div class="card">
                        <div class="card-title">{title}</div>
                        <ul class="insight-list">
                            {items}
                        </ul>
                    </div>
                    """
        
        return f"""
        <div class="section">
            <h2 class="section-title"><span class="emoji">🔮</span>Future Outlook</h2>
            {pred_html}
        </div>
        """
    
    def _create_sources_section(self, all_data: Dict, analysis: Dict) -> str:
        """Create sources section with all articles"""
        prioritization = analysis.get('prioritization', {})
        critical_items = prioritization.get('critical', [])
        
        sources_html = ""
        
        # Show critical items first
        for item in critical_items[:15]:
            sources_html += self._format_source_card(item)
        
        return f"""
        <div class="section">
            <h2 class="section-title"><span class="emoji">📚</span>Source Articles ({len(critical_items)} Priority Items)</h2>
            <div class="source-grid">
                {sources_html}
            </div>
        </div>
        """
    
    def _format_source_card(self, item: Dict) -> str:
        """Format a single source card"""
        title = item.get('title', 'Unknown')
        source = item.get('source', 'Unknown')
        category = item.get('category', 'Unknown')
        url = item.get('url', '#')
        summary = item.get('summary', item.get('description', 'No summary available'))[:200]
        
        return f"""
        <div class="source-card">
            <div class="source-title">{title}</div>
            <div class="source-meta">
                <span class="badge badge-medium">{category}</span>
                <span style="color: #718096;">• {source}</span>
            </div>
            <p style="color: #4a5568; font-size: 14px;">{summary}...</p>
            <a href="{url}" class="source-link" target="_blank">Read Full Article →</a>
        </div>
        """
    
    def _create_email_footer(self) -> str:
        """Create email footer"""
        return f"""
        <div class="footer">
            <p style="margin: 0 0 10px 0; font-size: 16px; font-weight: 600;">Daily AI Updates</p>
            <p style="margin: 0 0 15px 0;">Powered by Gemini AI • Delivered with ❤️</p>
            <p style="margin: 0; font-size: 12px; color: #a0aec0;">
                Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
            <div class="footer-links">
                <a href="#" class="footer-link">Preferences</a>
                <a href="#" class="footer-link">Unsubscribe</a>
            </div>
        </div>
        """
    
    def _create_text_email(self, analysis: Dict, all_data: Dict, stats: Dict) -> str:
        """Create plain text version of email"""
        date_str = datetime.now().strftime('%B %d, %Y')
        
        text = f"""
{'='*70}
DAILY AI UPDATE - {date_str}
{'='*70}

STATISTICS
----------
Total Updates: {stats.get('total_items', 0)}
Sources: {stats.get('sources_count', 0)}

EXECUTIVE SUMMARY
-----------------
{analysis.get('executive_summary', 'No summary available')}

{'='*70}

[View full report with formatting in HTML version]

Generated by Daily AI Updates System
Powered by Gemini AI
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        return text


# Demo
async def demo():
    """Demo email reporter"""
    print("Email reporter demo - check implementation")


if __name__ == "__main__":
    asyncio.run(demo())
