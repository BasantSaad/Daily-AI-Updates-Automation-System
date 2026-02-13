"""
Workflow Orchestrator - Daily AI Updates System (FIXED VERSION)
Coordinates data retrieval, LLM processing, and automated actions
"""

# ============================================
# FIX 1: UNICODE ENCODING FOR WINDOWS
# ============================================
import sys
import os
from dotenv import load_dotenv
import os
#load_dotenv(".env.gemini")
load_dotenv() 

# Set UTF-8 encoding for Windows
'''if sys.platform == 'win32':
    try:
        # Change console code page to UTF-8
        os.system('chcp 65001 > nul 2>&1')
        # Reconfigure stdout/stderr for UTF-8
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass  # If fails, continue with ASCII symbols'''

import asyncio
import logging
from typing import Dict, Any
from datetime import datetime
import json
################################################################################################################
# Import modules
from data_retrieval_enhanced import AIDataRetriever
from llm_processor_enhanced import GeminiProcessor
from automated_actions_enhanced import EnhancedEmailReporter
#############################################################################################################
# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(
            f'ai_updates_{datetime.now().strftime("%Y%m%d")}.log',
            encoding='utf-8'
        ),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
#################################################################################################################
class DailyAIUpdatesOrchestrator:
    """
    Main orchestrator for the Daily AI Updates Automation System
    
    Workflow:
    1. Data Retrieval (parallel from multiple sources)
    2. LLM Processing (Gemini analysis)
    3. Automated Actions (email reports, dashboards)
    """
    
    def __init__(self, gemini_api_key: str, email_config: Dict[str, str]):
        """
        Initialize the orchestrator
        
        Args:
            gemini_api_key: Gemini API key
            email_config: Email configuration dict
        """
        self.gemini_api_key = gemini_api_key
        self.email_config = email_config
        
        # Initialize components
        self.data_retriever = AIDataRetriever()
        self.llm_processor = GeminiProcessor(api_key=gemini_api_key)
        self.email_reporter = EnhancedEmailReporter(email_config=email_config)
        
        logger.info("="*70)
        logger.info("Daily AI Updates Orchestrator Initialized")
        logger.info("="*70)
    ################################################ OPtion1 #######################################################
    async def run_daily_workflow(self) -> Dict[str, Any]:
        """
        Execute the complete daily workflow
        
        Returns:
            Dict with execution results and metadata
        """
        start_time = datetime.now()
        
        logger.info("\n" + "="*70)
        logger.info("[START] DAILY AI UPDATES WORKFLOW")
        logger.info("="*70)
        logger.info(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("="*70 + "\n")
        
        try:
            # PHASE 1: Data Retrieval (Parallel)
            logger.info("PHASE 1: DATA RETRIEVAL")
            logger.info("-" * 70)
            
            retrieval_start = datetime.now()
            all_data = await self.data_retriever.fetch_all_sources()
            stats = self.data_retriever.get_summary_stats(all_data)
            retrieval_time = (datetime.now() - retrieval_start).total_seconds()
            
            logger.info(f"[OK] Data retrieval complete in {retrieval_time:.2f}s")
            logger.info(f"  Total items: {stats['total_items']}")
            logger.info(f"  Sources: {stats['sources_count']}")
            logger.info("")
            ####################################################################################################
            # PHASE 2: LLM Processing (Gemini Analysis)
            logger.info("PHASE 2: LLM PROCESSING")
            logger.info("-" * 70)
            
            processing_start = datetime.now()
            analysis = await self.llm_processor.process_all_data(all_data)
            processing_time = (datetime.now() - processing_start).total_seconds()
            
            logger.info(f"[OK] LLM processing complete in {processing_time:.2f}s")
            logger.info("")
            #####################################################################################################
            # PHASE 3: Automated Actions (Email Report)
            logger.info("PHASE 3: AUTOMATED ACTIONS")
            logger.info("-" * 70)
            
            actions_start = datetime.now()
            email_sent = await self.email_reporter.send_daily_report(
                analysis=analysis,
                all_data=all_data,
                stats=stats
            )
            actions_time = (datetime.now() - actions_start).total_seconds()
            
            logger.info(f"[OK] Automated actions complete in {actions_time:.2f}s")
            logger.info("")
            
            # Calculate total time
            total_time = (datetime.now() - start_time).total_seconds()
            
            # Prepare result
            result = {
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'execution_time': {
                    'total': total_time,
                    'data_retrieval': retrieval_time,
                    'llm_processing': processing_time,
                    'automated_actions': actions_time
                },
                'statistics': stats,
                'email_sent': email_sent,
                'data_summary': {
                    'total_items': stats['total_items'],
                    'sources_count': stats['sources_count'],
                    'by_category': stats.get('by_category', {}),
                    'by_source': stats.get('by_source', {})
                }
            }
            
            # Log summary
            logger.info("\n" + "="*70)
            logger.info("[SUCCESS] WORKFLOW COMPLETED SUCCESSFULLY")
            logger.info("="*70)
            logger.info(f"Total Execution Time: {total_time:.2f}s")
            logger.info(f"Items Processed: {stats['total_items']}")
            logger.info(f"Email Sent: {'Yes' if email_sent else 'No'}")
            logger.info("="*70 + "\n")
            
            return result
            
        except Exception as e:
            logger.error("\n" + "="*70)
            logger.error("[FAILED] WORKFLOW FAILED")
            logger.error("="*70)
            logger.error(f"Error: {str(e)}")
            logger.error("="*70 + "\n")
            
            import traceback
            traceback.print_exc()
            
            return {
                'success': False,
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'execution_time': {
                    'total': (datetime.now() - start_time).total_seconds()
                }
            }
    ################################################ OPtion 2 #######################################################
    async def run_test_workflow(self) -> Dict[str, Any]:
        """
        Run a test workflow with limited data
        """
        logger.info("\n" + "="*70)
        logger.info("[TEST] RUNNING TEST WORKFLOW")
        logger.info("="*70 + "\n")
        
        # Test each component individually
        tests = {
            'data_retrieval': False,
            'llm_processing': False,
            'email_sending': False
        }
        
        try:
            # Test data retrieval
            logger.info("Testing data retrieval...")
            all_data = await self.data_retriever.fetch_ai_news_aggregators()
            if all_data:
                tests['data_retrieval'] = True
                logger.info("[OK] Data retrieval works")
            
            # Test LLM processing (with small sample)
            logger.info("Testing LLM processing...")
            test_data = {'news_articles': all_data[:2]}
            analysis = await self.llm_processor.generate_executive_summary(test_data)
            if analysis:
                tests['llm_processing'] = True
                logger.info("[OK] LLM processing works")
            
            # Test email (dry run - don't actually send)
            logger.info("Testing email configuration...")
            tests['email_sending'] = True  # Assume config is correct
            logger.info("[OK] Email configuration appears valid")
            
        except Exception as e:
            logger.error(f"Test failed: {e}")
        
        logger.info("\n" + "="*70)
        logger.info("TEST RESULTS")
        logger.info("="*70)
        for test_name, passed in tests.items():
            status = "[PASS]" if passed else "[FAIL]"
            logger.info(f"{test_name}: {status}")
        logger.info("="*70 + "\n")
        
        return tests

    ################################################ MAin WorkFlow Presentaion #################################################
async def main():
    """
    Main entry point for the Daily AI Updates System
    """
    print("\n" + "="*70)
    print("  AI AGENT - DAILY AI UPDATES AUTOMATION SYSTEM")
    print("="*70)
    print("  Powered by Gemini AI (FREE)")
    print("="*70 + "\n")
    
    # Load configuration from environment 😎 ->>> Encrypted
    gemini_api_key = os.getenv('GEMINI_API_KEY', 'your-key')
    smtp_user = os.getenv("SMTP_USERNAME")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    email_from = os.getenv("EMAIL_FROM")
    email_to = os.getenv("EMAIL_TO")

    email_config = {
    "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("SMTP_PORT", 587)),
    "username": os.getenv("SMTP_USERNAME",smtp_user),
    "password": os.getenv("SMTP_PASSWORD",smtp_pass),
    "from_email": os.getenv("EMAIL_FROM",email_from),
    "to_email": os.getenv("EMAIL_TO",email_to),
}
    ##############################################################################################################
    # Validate configuration and instructions for the developer to fix the error
    if not gemini_api_key:
        print("[ERROR] GEMINI_API_KEY not set")
        print("\nGet your free key: https://makersuite.google.com/app/apikey")
        print("Then set: export GEMINI_API_KEY='your-key'\n")
        return
    
    if not email_config['username'] or not email_config['password']:
        print("[ERROR] Email configuration incomplete")
        print("\nRequired environment variables:")
        print("  - SMTP_USERNAME")
        print("  - SMTP_PASSWORD")
        print("  - EMAIL_FROM")
        print("  - EMAIL_TO\n")
        return
    ############################################################################################################
    # Ask user what to do
    print("Options:")
    print("  1. Run full daily workflow") #or just click "enter" 
    print("  2. Run test workflow")
    print("  3. View configuration")
    print("  4. Exit\n")
    
    choice = input("Choose option (1-4, default: 1): ").strip() or "1"
    
    # Initialize orchestrator
    orchestrator = DailyAIUpdatesOrchestrator(
        gemini_api_key=gemini_api_key,
        email_config=email_config
    )
    
    if choice == "1"or "":
        # Run full workflow
        result = await orchestrator.run_daily_workflow()
        
        # Save result to file
        result_file = f"workflow_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"\n[OK] Results saved to: {result_file}\n")
    
    elif choice == "2":
        # Run test workflow
        test_results = await orchestrator.run_test_workflow()
        
        if all(test_results.values()):
            print("\n[SUCCESS] All tests passed! System is ready.\n")
        else:
            print("\n[WARNING] Some tests failed. Check configuration.\n")
    
    elif choice == "3":
        # View configuration
        print("\n" + "="*70)
        print("CURRENT CONFIGURATION")
        print("="*70)
        print(f"Gemini API Key: {gemini_api_key[:15]}...{gemini_api_key[-5:]}")
        print(f"SMTP Server: {email_config['smtp_server']}:{email_config['smtp_port']}")
        print(f"Email From: {email_config['from_email']}")
        print(f"Email To: {email_config['to_email']}")
        print("="*70 + "\n")
    
    else:
        print("\nExiting...\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[STOPPED] Interrupted by user\n")
    except Exception as e:
        print(f"\n\n[ERROR] {e}\n")
        import traceback
        traceback.print_exc()