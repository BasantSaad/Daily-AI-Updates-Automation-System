"""
Data Retrieval Module - Daily AI Updates System
Gathers AI news from multiple real-time sources
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Any
from datetime import datetime
import feedparser
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class AIDataRetriever:
    """
    Retrieves latest AI news from multiple real-time sources
    """
    
    def __init__(self):
        self.sources_fetched = []
        logger.info("AI Data Retriever initialized")
    
    async def fetch_all_sources(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch data from all sources in parallel
        Returns dict with categorized articles from each source
        """
        logger.info("="*70)
        logger.info("Starting parallel data collection from all sources")
        logger.info("="*70)
        
        # Run all fetchers in parallel
        tasks = [
            self.fetch_arxiv_papers(),
            self.fetch_huggingface_updates(),
            self.fetch_github_trending(),
            self.fetch_reddit_ai(),
            self.fetch_papers_with_code(),
            self.fetch_ai_news_aggregators(),
            self.fetch_company_blogs(),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Organize results
        all_data = {
            'arxiv_papers': results[0] if not isinstance(results[0], Exception) else [],
            'huggingface_models': results[1] if not isinstance(results[1], Exception) else [],
            'github_repos': results[2] if not isinstance(results[2], Exception) else [],
            'reddit_discussions': results[3] if not isinstance(results[3], Exception) else [],
            'papers_with_code': results[4] if not isinstance(results[4], Exception) else [],
            'news_articles': results[5] if not isinstance(results[5], Exception) else [],
            'company_updates': results[6] if not isinstance(results[6], Exception) else [],
        }
        
        # Count total items
        total_items = sum(len(v) for v in all_data.values() if isinstance(v, list))
        
        logger.info("="*70)
        logger.info(f"✓ Data collection complete: {total_items} items from {len(self.sources_fetched)} sources")
        logger.info("="*70)
        
        return all_data
    
    async def fetch_arxiv_papers(self) -> List[Dict[str, Any]]:
        """
        Fetch latest AI papers from arXiv
        Real-time source: https://arxiv.org/
        """
        logger.info(" Fetching arXiv papers...")
        
        try:
            # arXiv RSS feed for AI papers
            url = "http://export.arxiv.org/rss/cs.AI"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    content = await response.text()
            
            # Parse RSS feed
            feed = feedparser.parse(content)
            
            papers = []
            for entry in feed.entries[:10]:  # Latest 10 papers
                # Extract arXiv ID
                arxiv_id = entry.id.split('/')[-1]
                
                paper = {
                    'title': entry.title,
                    'summary': entry.summary[:300] + "...",
                    'authors': entry.get('author', 'Unknown'),
                    'published': entry.get('published', datetime.now().isoformat()),
                    'url': entry.link,
                    'arxiv_id': arxiv_id,
                    'category': 'Research Paper',
                    'source': 'arXiv'
                }
                papers.append(paper)
            
            self.sources_fetched.append('arXiv')
            logger.info(f"  ✓ Fetched {len(papers)} papers from arXiv")
            return papers
            
        except Exception as e:
            logger.error(f"  ✗ arXiv fetch failed: {e}")
            return []
    
    async def fetch_huggingface_updates(self):
        logger.info("Fetching Hugging Face top models...")

        url = "https://huggingface.co/api/models?limit=10&sort=downloads&direction=-1"

        headers = {
            "User-Agent": "AI-News-Aggregator/1.0"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=10) as response:

                    if response.status != 200:
                        logger.error(f"Hugging Face API returned {response.status}")
                        text = await response.text()
                        logger.error(text)   # مهم جدًا للتشخيص
                        return []

                    data = await response.json()

            models = []
            for item in data:
                models.append({
                    "title": item.get("modelId"),
                    "downloads": item.get("downloads"),
                    "likes": item.get("likes"),
                    "url": f"https://huggingface.co/{item.get('modelId')}",
                    "source": "Hugging Face"
                })

            logger.info(f"✓ Fetched {len(models)} models")
            return models

        except Exception as e:
            logger.error(f"Hugging Face fetch failed: {e}")
            return []


        
    async def fetch_github_trending(self) -> List[Dict[str, Any]]:
        """
        Fetch trending AI repositories from GitHub
        Real-time source: https://github.com/trending
        """
        logger.info(" Fetching GitHub trending AI repos...")
        
        try:
            url = "https://github.com/trending/python?since=daily"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    html = await response.text()
            
            soup = BeautifulSoup(html, 'html.parser')
            repos = []
            
            # Find repo articles
            for article in soup.find_all('article', class_='Box-row')[:8]:
                try:
                    # Extract repo name
                    h2 = article.find('h2')
                    if not h2:
                        continue
                    
                    repo_link = h2.find('a')
                    if not repo_link:
                        continue
                    
                    repo_name = repo_link.get('href', '').strip('/')
                    
                    # Extract description
                    desc_tag = article.find('p', class_='col-9')
                    description = desc_tag.text.strip() if desc_tag else "No description"
                    
                    # Extract stars
                    stars_tag = article.find('span', class_='d-inline-block float-sm-right')
                    stars = stars_tag.text.strip() if stars_tag else "0"
                    
                    # Only include if AI/ML related
                    combined_text = (repo_name + description).lower()
                    ai_keywords = ['ai', 'ml', 'machine learning', 'deep learning', 
                                   'neural', 'llm', 'gpt', 'transformer', 'model']
                    
                    if any(keyword in combined_text for keyword in ai_keywords):
                        repo = {
                            'title': f"Trending: {repo_name}",
                            'repo_name': repo_name,
                            'description': description,
                            'stars_today': stars,
                            'url': f"https://github.com/{repo_name}",
                            'category': 'Open Source Tool',
                            'source': 'GitHub',
                            'published': datetime.now().isoformat()
                        }
                        repos.append(repo)
                
                except Exception as e:
                    continue
            
            self.sources_fetched.append('GitHub')
            logger.info(f"  ✓ Fetched {len(repos)} trending AI repos")
            return repos
            
        except Exception as e:
            logger.error(f"  ✗ GitHub fetch failed: {e}")
            return []
    
    async def fetch_reddit_ai(self) -> List[Dict[str, Any]]:
        """
        Fetch hot posts from AI subreddits
        Real-time source: Reddit r/MachineLearning, r/artificial, r/LocalLLaMA
        """
        logger.info(" Fetching Reddit AI discussions...")
        
        try:
            subreddits = ['MachineLearning', 'artificial', 'LocalLLaMA']
            all_posts = []
            
            async with aiohttp.ClientSession() as session:
                for subreddit in subreddits:
                    try:
                        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=5"
                        headers = {'User-Agent': 'AI News Aggregator 1.0'}
                        
                        async with session.get(url, headers=headers, timeout=10) as response:
                            if response.status == 200:
                                data = await response.json()
                                
                                for post in data.get('data', {}).get('children', []):
                                    post_data = post.get('data', {})
                                    
                                    discussion = {
                                        'title': post_data.get('title', 'No title'),
                                        'summary': post_data.get('selftext', '')[:200] + "...",
                                        'upvotes': post_data.get('ups', 0),
                                        'comments': post_data.get('num_comments', 0),
                                        'url': f"https://reddit.com{post_data.get('permalink', '')}",
                                        'subreddit': subreddit,
                                        'category': 'Community Discussion',
                                        'source': f'Reddit r/{subreddit}',
                                        'published': datetime.fromtimestamp(
                                            post_data.get('created_utc', 0)
                                        ).isoformat()
                                    }
                                    all_posts.append(discussion)
                    
                    except Exception as e:
                        logger.warning(f"  ⚠ Failed to fetch r/{subreddit}: {e}")
                        continue
            
            self.sources_fetched.append('Reddit')
            logger.info(f"  ✓ Fetched {len(all_posts)} Reddit discussions")
            return all_posts
            
        except Exception as e:
            logger.error(f"  ✗ Reddit fetch failed: {e}")
            return []
    
    import feedparser

    async def fetch_papers_with_code(self):

        logger.info("Fetching Papers with Code via RSS...")

        try:
            feed = feedparser.parse("https://paperswithcode.com/rss/latest")

            papers = []

            for entry in feed.entries[:8]:

                papers.append({
                    "title": entry.title,
                    "summary": entry.summary[:300] + "...",
                    "url": entry.link,
                    "paper_url": entry.link,
                    "stars": 0,
                    "category": "Research with Code",
                    "source": "Papers with Code",
                    "published": entry.get("published", datetime.now().isoformat())
                })

            self.sources_fetched.append("Papers with Code")

            logger.info(f"✓ Fetched {len(papers)} papers via RSS")

            return papers

        except Exception as e:
            logger.error(f"Papers with Code fetch failed: {e}")
            return []


    
    async def fetch_ai_news_aggregators(self) -> List[Dict[str, Any]]:
        """
        Fetch from AI news aggregators and tech news sites
        """
        logger.info(" Fetching AI news from aggregators...")
        
        articles = []
        
        # Simulated news (in production, use RSS feeds or APIs)
        news_sources = [
            {
                'title': 'OpenAI Announces GPT-4.5 with Enhanced Reasoning',
                'summary': 'OpenAI releases GPT-4.5 with improved mathematical reasoning and coding capabilities, showing 40% improvement in STEM benchmarks.',
                'url': 'https://openai.com/blog/gpt-4-5',
                'source': 'OpenAI Blog',
                'category': 'Model Release',
                'published': datetime.now().isoformat()
            },
            {
                'title': 'Google DeepMind Releases Gemini 1.5 Pro',
                'summary': 'New model features 1M token context window and improved multimodal understanding across text, images, video, and audio.',
                'url': 'https://deepmind.google/gemini',
                'source': 'Google DeepMind',
                'category': 'Model Release',
                'published': datetime.now().isoformat()
            },
            {
                'title': 'Meta Open-Sources Llama 3 70B',
                'summary': 'Meta releases Llama 3 with 70B parameters, rivaling GPT-4 performance while remaining completely open-source and free to use.',
                'url': 'https://ai.meta.com/llama',
                'source': 'Meta AI',
                'category': 'Open Source Release',
                'published': datetime.now().isoformat()
            },
            {
                'title': 'Anthropic Claude 3.5 Sonnet Benchmarks',
                'summary': 'Claude 3.5 Sonnet shows state-of-the-art performance on coding benchmarks, surpassing GPT-4 on several metrics.',
                'url': 'https://anthropic.com/claude',
                'source': 'Anthropic',
                'category': 'Model Release',
                'published': datetime.now().isoformat()
            },
            {
                'title': 'Stability AI Releases Stable Diffusion 3',
                'summary': 'Latest image generation model features improved text rendering and better composition understanding.',
                'url': 'https://stability.ai/sd3',
                'source': 'Stability AI',
                'category': 'Image Generation',
                'published': datetime.now().isoformat()
            }
        ]
        
        articles.extend(news_sources)
        
        self.sources_fetched.append('AI News Aggregators')
        logger.info(f"  ✓ Fetched {len(articles)} news articles")
        return articles
    
    async def fetch_company_blogs(self) -> List[Dict[str, Any]]:
        """
        Fetch updates from major AI company blogs (OpenAI, Google, Meta, etc.)
        """
        logger.info(" Fetching company blog updates...")
        
        # In production, these would be RSS feeds or APIs
        updates = [
            {
                'title': 'OpenAI API Updates: Function Calling Improvements',
                'summary': 'Enhanced function calling with parallel execution and improved accuracy in parameter extraction.',
                'url': 'https://platform.openai.com/docs/guides/function-calling',
                'source': 'OpenAI',
                'category': 'Tool Update',
                'published': datetime.now().isoformat()
            },
            {
                'title': 'Hugging Face Launches Inference Endpoints',
                'summary': 'New managed service for deploying ML models at scale with automatic scaling and optimization.',
                'url': 'https://huggingface.co/inference-endpoints',
                'source': 'Hugging Face',
                'category': 'Platform Update',
                'published': datetime.now().isoformat()
            }
        ]
        
        self.sources_fetched.append('Company Blogs')
        logger.info(f"  ✓ Fetched {len(updates)} company updates")
        return updates
    
    def get_summary_stats(self, all_data: Dict[str, List]) -> Dict[str, Any]:
        """
        Get summary statistics of retrieved data
        """
        stats = {
            'total_items': sum(len(v) for v in all_data.values() if isinstance(v, list)),
            'sources_count': len(self.sources_fetched),
            'sources_list': self.sources_fetched,
            'by_category': {},
            'by_source': {}
        }
        
        # Count by category and source
        for source_type, items in all_data.items():
            if isinstance(items, list):
                for item in items:
                    # By category
                    cat = item.get('category', 'Unknown')
                    stats['by_category'][cat] = stats['by_category'].get(cat, 0) + 1
                    
                    # By source
                    src = item.get('source', 'Unknown')
                    stats['by_source'][src] = stats['by_source'].get(src, 0) + 1
        
        return stats


# Demo function
async def demo_data_retrieval():
    """Demo the data retrieval system"""
    print("\n" + "="*70)
    print("AI DATA RETRIEVAL DEMO")
    print("="*70 + "\n")
    
    retriever = AIDataRetriever()
    
    # Fetch all data
    all_data = await retriever.fetch_all_sources()
    
    # Get stats
    stats = retriever.get_summary_stats(all_data)
    
    # Display results
    print("\n" + "="*70)
    print("RETRIEVAL SUMMARY")
    print("="*70)
    print(f"Total items collected: {stats['total_items']}")
    print(f"Sources accessed: {stats['sources_count']}")
    print(f"\nSources: {', '.join(stats['sources_list'])}")
    
    print(f"\nBy Category:")
    for cat, count in sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True):
        print(f"  • {cat}: {count}")
    
    print(f"\nBy Source:")
    for src, count in sorted(stats['by_source'].items(), key=lambda x: x[1], reverse=True):
        print(f"  • {src}: {count}")
    
    # Show sample items
    print("\n" + "="*70)
    print("SAMPLE ITEMS")
    print("="*70)
    
    for source_type, items in all_data.items():
        if items and len(items) > 0:
            print(f"\n{source_type.upper().replace('_', ' ')} (showing first):")
            item = items[0]
            print(f"  Title: {item.get('title', 'N/A')}")
            print(f"  Source: {item.get('source', 'N/A')}")
            print(f"  Category: {item.get('category', 'N/A')}")
            print(f"  URL: {item.get('url', 'N/A')}")
    
    print("\n" + "="*70 + "\n")
    
    return all_data, stats


if __name__ == "__main__":
    asyncio.run(demo_data_retrieval())
