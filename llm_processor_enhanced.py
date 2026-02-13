"""
LLM Processing Module - Enhanced with Gemini
Comprehensive AI analysis and summarization
"""

import asyncio
import logging
from typing import Dict, List, Any
from datetime import datetime
import json
from dotenv import load_dotenv
import os

#load_dotenv(".env.gemini")
load_dotenv() 

logger = logging.getLogger(__name__)


class GeminiProcessor:
    """
    Advanced LLM processor using Gemini for comprehensive AI analysis
    """
    
    def __init__(self, api_key: str):
        """
        Initialize Gemini processor
        
        Args:
            api_key: Gemini API key
        """
        self.api_key = api_key
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-3-flash-preview")

            '''from google import genai
            client = genai.Client(api_key=self.api_key)
            self.model = client.models.generate_content(model="gemini-3-flash-preview")'''

            logger.info("✓ Gemini processor initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            raise
    
    async def process_all_data(self, all_data: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """
        Comprehensive processing of all collected AI data
        """
        logger.info("="*70)
        logger.info("Starting comprehensive AI analysis with Gemini")
        logger.info("="*70)

        ###################################################################################################################
                                            # Process different aspects in parallel
        ###################################################################################################################
        tasks = [
            self.generate_executive_summary(all_data),
            self.extract_key_developments(all_data),
            self.analyze_trends_and_patterns(all_data),
            self.identify_breakthrough_technologies(all_data),
            self.assess_industry_impact(all_data),
            self.generate_actionable_insights(all_data),
            self.predict_future_directions(all_data),
            self.categorize_by_importance(all_data),
        ]
        
        results = await asyncio.gather(*tasks)
        
        analysis_result = {
            'timestamp': datetime.now().isoformat(),
            'executive_summary': results[0],
            'key_developments': results[1],
            'trends_and_patterns': results[2],
            'breakthrough_technologies': results[3],
            'industry_impact': results[4],
            'actionable_insights': results[5],
            'future_predictions': results[6],
            'prioritization': results[7],
            'metadata': {
                'total_sources': sum(len(v) for v in all_data.values() if isinstance(v, list)),
                'analysis_model': 'Gemini Pro',
                'processing_time': datetime.now().isoformat()
            }
        }
        
        logger.info("="*70)
        logger.info("✓ Comprehensive analysis complete")
        logger.info("="*70)
        
        return analysis_result
    ####################################### Generate executive summary using Gemini and prompt [MadeUP ->data_summary #####################################
    ######################################################## First TAsk #######################################################

    async def generate_executive_summary(self, all_data: Dict) -> str:
        """
        Generate executive summary of all AI developments
        """
        logger.info(" Generating executive summary...")
        
        # Prepare data for Gemini
        data_summary = self._prepare_data_summary(all_data)
        
        prompt = f"""
        You are an AI industry analyst. Analyze today's AI developments and create a compelling executive summary.
        
        DATA COLLECTED TODAY:
        {data_summary}
        
        Create a 3-paragraph executive summary covering:
        
        1. OVERVIEW: What's happening in AI today? Big picture view.
        2. SIGNIFICANCE: Why do these developments matter? What changed?
        3. OUTLOOK: What does this mean for the near future?
        
        Write in a professional, engaging tone. Focus on impact and implications.
        Be specific with numbers and names when available.
        """
        
        try:
            response = self.model.generate_content(prompt)
            summary = response.text
            logger.info("  ✓ Executive summary generated")
            return summary
        except Exception as e:
            logger.error(f"  ✗ Summary generation failed: {e}")
            return "Executive summary generation failed. Please check API configuration."
    ####################################### extract_key_developments using Gemini and prompt ->data_summary#####################################
    ######################################################## 2 -> TAsk #######################################################

    async def extract_key_developments(self, all_data: Dict) -> List[Dict[str, Any]]:
        """
        Extract and rank the most important developments
        """
        logger.info(" Extracting key developments...")
        
        data_summary = self._prepare_data_summary(all_data)
        
        prompt = f"""
        Analyze these AI developments and identify the TOP 10 MOST IMPORTANT items.
        
        DATA:
        {data_summary}
        
        For each of the top 10, provide:
        - Title: Clear, specific title
        - Category: (Model Release / Research / Tool / News / Policy)
        - Importance: (Critical / High / Medium) with reasoning
        - Impact: Who/what is affected and how
        - Timeframe: When will impact be felt (Immediate / Short-term / Long-term)
        - Key Takeaway: One sentence on why this matters
        
        Return as JSON array with exactly these fields:
        [
          {{
            "rank": 1,
            "title": "...",
            "category": "...",
            "importance": "...",
            "importance_reason": "...",
            "impact": "...",
            "timeframe": "...",
            "key_takeaway": "...",
            "source": "..."
          }},
          ...
        ]
        
        Return ONLY the JSON array, no other text.
        """
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Extract JSON from response
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]
            
            developments = json.loads(result_text)
            logger.info(f"  ✓ Extracted {len(developments)} key developments")
            return developments
        except Exception as e:
            logger.error(f"  ✗ Development extraction failed: {e}")
            return []
    ####################################### analyze_trends_and_patterns using Gemini and prompt ->data_summary #####################################
    ######################################################## 3 -> TAsk #######################################################
    async def analyze_trends_and_patterns(self, all_data: Dict) -> Dict[str, Any]:
        """
        Identify emerging trends and patterns in AI
        """
        logger.info(" Analyzing trends and patterns...")
        
        data_summary = self._prepare_data_summary(all_data)
        
        prompt = f"""
        Analyze these AI developments for TRENDS and PATTERNS.
        
        DATA:
        {data_summary}
        
        Identify:
        
        1. EMERGING TRENDS (3-5 trends)
           - What patterns do you see?
           - What's gaining momentum?
           - What's new or accelerating?
        
        2. DOMINANT THEMES (top 3)
           - What topics appear most?
           - What's the current focus?
        
        3. TECHNOLOGICAL SHIFTS
           - What's changing in the technology landscape?
           - Old vs new approaches
        
        4. MARKET MOVEMENTS
           - Who's making moves? (companies, researchers)
           - What sectors are active?
        
        Return as structured JSON:
        {{
          "emerging_trends": [
            {{"trend": "...", "description": "...", "strength": "...", "examples": ["..."]}},
            ...
          ],
          "dominant_themes": [
            {{"theme": "...", "prevalence": "...", "significance": "..."}},
            ...
          ],
          "technological_shifts": {{
            "description": "...",
            "old_approach": "...",
            "new_approach": "...",
            "implications": "..."
          }},
          "market_movements": {{
            "active_companies": ["..."],
            "hot_sectors": ["..."],
            "investment_areas": ["..."]
          }}
        }}
        
        Return ONLY JSON.
        """
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]
            
            trends = json.loads(result_text)
            logger.info("  ✓ Trend analysis complete")
            return trends
        except Exception as e:
            logger.error(f"  ✗ Trend analysis failed: {e}")
            return {}
    ####################################### identify_breakthrough_technologies using Gemini and prompt ->data_summary #####################################
    ######################################################## 4 -> TAsk #######################################################
    async def identify_breakthrough_technologies(self, all_data: Dict) -> List[Dict[str, Any]]:
        """
        Identify breakthrough technologies and innovations
        """
        logger.info(" Identifying breakthrough technologies...")
        
        data_summary = self._prepare_data_summary(all_data)
        
        prompt = f"""
        Identify BREAKTHROUGH TECHNOLOGIES from today's AI developments.
        
        DATA:
        {data_summary}
        
        Find the top 5 most significant technical breakthroughs or innovations.
        
        For each, provide:
        - Technology: Name/description
        - Innovation: What's new or improved?
        - Capability: What can it do now that wasn't possible before?
        - Technical Advancement: Specific metrics or improvements
        - Potential Applications: Real-world use cases
        - Adoption Timeline: When might this be widely available?
        - Limitations: What are the current constraints?
        
        Return as JSON array, ranked by significance.
        """
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            
            breakthroughs = json.loads(result_text)
            logger.info(f"  ✓ Identified {len(breakthroughs)} breakthroughs")
            return breakthroughs
        except Exception as e:
            logger.error(f"  ✗ Breakthrough identification failed: {e}")
            return []
    ####################################### assess_industry_impact using Gemini and prompt ->data_summary #####################################
    ######################################################## 4 -> TAsk #######################################################
    async def assess_industry_impact(self, all_data: Dict) -> Dict[str, Any]:
        """
        Assess impact on different industries and sectors
        """
        logger.info(" Assessing industry impact...")
        
        data_summary = self._prepare_data_summary(all_data)
        
        prompt = f"""
        Assess how today's AI developments impact different industries.
        
        DATA:
        {data_summary}
        
        Analyze impact on these sectors:
        - Healthcare & Biotech
        - Finance & Banking
        - Technology & Software
        - Manufacturing & Robotics
        - Education & Research
        - Creative Industries
        - Legal & Compliance
        - Retail & E-commerce
        
        For each relevant sector, provide:
        - Direct Impact: Immediate effects
        - Opportunities: New possibilities
        - Challenges: Potential disruptions or problems
        - Timeline: Short-term vs long-term impact
        
        Return as JSON with sector-specific analysis.
        """
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            
            impact = json.loads(result_text)
            logger.info("  ✓ Industry impact assessed")
            return impact
        except Exception as e:
            logger.error(f"  ✗ Industry impact assessment failed: {e}")
            return {}
    ####################################### generate_actionable_insights using Gemini and prompt ->data_summary #####################################
    ######################################################## 5 -> TAsk #######################################################
    async def generate_actionable_insights(self, all_data: Dict) -> Dict[str, List[str]]:
        """
        Generate actionable insights for different stakeholders
        """
        logger.info(" Generating actionable insights...")
        
        data_summary = self._prepare_data_summary(all_data)
        
        prompt = f"""
        Based on today's AI developments, provide ACTIONABLE INSIGHTS for different stakeholders.
        
        DATA:
        {data_summary}
        
        Provide specific, actionable recommendations for:
        
        1. AI PRACTITIONERS & DEVELOPERS
           - What tools/models should they try?
           - What skills to develop?
           - What to watch next?
        
        2. BUSINESS LEADERS & EXECUTIVES
           - Strategic decisions to consider
           - Investment opportunities
           - Competitive threats
        
        3. RESEARCHERS & ACADEMICS
           - Research directions
           - Collaboration opportunities
           - Emerging questions
        
        4. INVESTORS
           - Market signals
           - Growth areas
           - Risk factors
        
        5. GENERAL PUBLIC
           - What these changes mean for everyday life
           - How to prepare
           - Opportunities to learn
        
        Return as JSON with clear, specific action items for each group.
        """
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            
            insights = json.loads(result_text)
            logger.info("  ✓ Actionable insights generated")
            return insights
        except Exception as e:
            logger.error(f"  ✗ Insight generation failed: {e}")
            return {}
    ####################################### predict_future_directions using Gemini and prompt ->data_summary #####################################
    ######################################################## 4 -> TAsk #######################################################
    async def predict_future_directions(self, all_data: Dict) -> Dict[str, Any]:
        """
        Predict future directions based on current developments
        """
        logger.info(" Predicting future directions...")
        
        data_summary = self._prepare_data_summary(all_data)
        
        prompt = f"""
        Based on today's developments, predict FUTURE DIRECTIONS for AI.
        
        DATA:
        {data_summary}
        
        Provide predictions for:
        
        1. NEXT WEEK
           - Expected announcements
           - Likely developments
        
        2. NEXT MONTH
           - Probable trends
           - Anticipated releases
        
        3. NEXT QUARTER
           - Strategic shifts
           - Market changes
        
        4. WILD CARDS
           - Unexpected possibilities
           - Potential surprises
        
        Be specific with companies, technologies, and timelines when possible.
        Return as JSON.
        """
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            
            predictions = json.loads(result_text)
            logger.info("  ✓ Future predictions generated")
            return predictions
        except Exception as e:
            logger.error(f"  ✗ Prediction generation failed: {e}")
            return {}
    ####################################### categorize_by_importance using Gemini and prompt ->data_summary #####################################
    ######################################################## 3 -> TAsk #######################################################
    async def categorize_by_importance(self, all_data: Dict) -> Dict[str, List]:
        """
        Categorize all items by importance level
        """
        logger.info(" Categorizing by importance...")
        
        # Simple categorization based on source and content
        categorized = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }
        
        # Keywords for importance classification
        critical_keywords = ['breakthrough', 'release', 'launches', 'announces', 'gpt', 'gemini']
        high_keywords = ['improves', 'enhances', 'new model', 'open source']
        
        for source_type, items in all_data.items():
            if not isinstance(items, list):
                continue
            
            for item in items:
                title_lower = item.get('title', '').lower()
                
                if any(kw in title_lower for kw in critical_keywords):
                    categorized['critical'].append(item)
                elif any(kw in title_lower for kw in high_keywords):
                    categorized['high'].append(item)
                elif 'research' in source_type.lower() or 'paper' in source_type.lower():
                    categorized['medium'].append(item)
                else:
                    categorized['low'].append(item)
        
        logger.info(f"  ✓ Items categorized: {len(categorized['critical'])} critical, "
                   f"{len(categorized['high'])} high, {len(categorized['medium'])} medium")
        
        return categorized
    
    def _prepare_data_summary(self, all_data: Dict) -> str:
        """
        Prepare concise data summary for Gemini prompts
        """
        summary_parts = []
        
        for source_type, items in all_data.items():
            if not isinstance(items, list) or not items:
                continue
            
            summary_parts.append(f"\n{source_type.upper().replace('_', ' ')}:")
            for i, item in enumerate(items[:15], 1):  # Limit to 15 per source
                title = item.get('title', 'Unknown')
                source = item.get('source', 'Unknown')
                summary = item.get('summary', item.get('description', ''))[:150]
                summary_parts.append(f"{i}. {title} [{source}]")
                if summary:
                    summary_parts.append(f"   {summary}...")
        
        return "\n".join(summary_parts)


# Demo function
async def demo_gemini_processing():
    """Demo the Gemini processing"""
    print("\n" + "="*70)
    print("GEMINI PROCESSING DEMO")
    print("="*70 + "\n")
    
    # Sample data
    sample_data = {
        'news_articles': [
            {
                'title': 'OpenAI Releases GPT-5',
                'summary': 'Major breakthrough in reasoning capabilities',
                'source': 'OpenAI',
                'category': 'Model Release'
            }
        ]
    }
    
    api_key = os.getenv('GEMINI_API_KEY', 'your-key')
    
    if api_key == 'your-key':
        print("⚠️  Set GEMINI_API_KEY environment variable to test\n")
        return
    
    processor = GeminiProcessor(api_key=api_key)
    results = await processor.process_all_data(sample_data)
    
    print("Results:")
    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(demo_gemini_processing())
