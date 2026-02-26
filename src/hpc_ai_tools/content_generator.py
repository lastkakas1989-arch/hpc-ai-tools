"""
HPC/AI Content Generator
"""

import random
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class ContentGenerator:
    """HPC/AI Content Generator"""
    
    def __init__(self, language: str = "en"):
        """
        Initialize content generator.
        
        Args:
            language: Content language ('en' for English, 'zh' for Chinese)
        """
        self.language = language or os.getenv("LANGUAGE", "en")
        self.max_length = int(os.getenv("MAX_TWEET_LENGTH", "280"))
        
        # Initialize content databases
        self._init_hpc_topics()
        self._init_ai_topics()
        self._init_organizations()
        self._init_emojis()
        self._init_templates()
        
        logger.info(f"ContentGenerator initialized with language: {self.language}")
    
    def _init_hpc_topics(self) -> None:
        """Initialize HPC topics database."""
        self.hpc_topics = [
            "Exascale Computing",
            "Quantum-HPC Integration", 
            "AI for Science",
            "High Performance Data Analytics",
            "Green Computing",
            "HPC Cloud",
            "GPU Computing",
            "Storage Technologies",
            "Interconnect Networks",
            "Scientific Visualization",
            "Edge Computing",
            "Hybrid Computing",
            "Memory Technologies",
            "Parallel Algorithms",
            "Workflow Management"
        ]
    
    def _init_ai_topics(self) -> None:
        """Initialize AI topics database."""
        self.ai_topics = [
            "Large Language Models",
            "Computer Vision",
            "Reinforcement Learning",
            "Generative AI",
            "Federated Learning",
            "Explainable AI",
            "AI Ethics",
            "Edge AI",
            "AI Hardware",
            "Multimodal AI",
            "Transfer Learning",
            "Self-Supervised Learning",
            "Neuro-Symbolic AI",
            "AI Safety",
            "AI Governance"
        ]
    
    def _init_organizations(self) -> None:
        """Initialize organizations database."""
        self.organizations = [
            "DOE (Department of Energy)",
            "NSF (National Science Foundation)",
            "CERN",
            "NASA",
            "Oak Ridge National Laboratory",
            "Lawrence Livermore National Laboratory",
            "Argonne National Laboratory",
            "European HPC Centers",
            "Chinese Supercomputing Centers",
            "Japanese Research Institutions",
            "MIT",
            "Stanford University",
            "Google Research",
            "Microsoft Research",
            "OpenAI"
        ]
    
    def _init_emojis(self) -> None:
        """Initialize emojis database."""
        self.emojis = ["🚀", "🔬", "💻", "⚡", "🌍", "📈", "🔍", "🎯", "🤖", "🧠", "💡", "⚛️", "🔋", "📊", "🌐"]
    
    def _init_templates(self) -> None:
        """Initialize content templates based on language."""
        if self.language == "zh":
            self._init_chinese_templates()
        else:
            self._init_english_templates()
    
    def _init_english_templates(self) -> None:
        """Initialize English content templates."""
        self.hpc_templates = [
            "{emoji} {topic} breakthrough: {organization} reports significant performance improvements, accelerating scientific discovery.\n\n#HighPerformanceComputing #ScientificComputing",
            "{emoji} {topic} technology analysis: New architecture shows excellent performance in {organization} tests, with improved energy efficiency.\n\nFollow cutting-edge computing infrastructure development!",
            "{emoji} {topic} application case: {organization} uses this technology to solve complex scientific problems, dramatically reducing computation time.\n\n#HPC #ResearchInnovation",
            "{emoji} Latest developments in {topic}: {organization} study reveals groundbreaking advances in computational capabilities.\n\n#Supercomputing #TechInnovation",
            "{emoji} {topic} infrastructure update: {organization} deploys new system achieving record-breaking performance metrics.\n\n#HPCNews #Computing"
        ]
        
        self.ai_templates = [
            "{emoji} {topic} breakthrough: {organization} research team publishes latest results, achieving new performance heights.\n\n#ArtificialIntelligence #MachineLearning",
            "{emoji} {topic} applications: Demonstrates powerful capabilities in real-world scenarios, validated by {organization}.\n\n#AI #TechnologyInnovation",
            "{emoji} {topic} trend analysis: {organization} report indicates rapid development in this field with widespread industry applications.\n\nFollow AI frontier developments!",
            "{emoji} Advancements in {topic}: {organization} researchers achieve state-of-the-art results in benchmark tests.\n\n#AIResearch #DeepLearning",
            "{emoji} {topic} implementation: Successful deployment at {organization} shows promising results for future applications.\n\n#AITechnology #Innovation"
        ]
    
    def _init_chinese_templates(self) -> None:
        """Initialize Chinese content templates."""
        self.hpc_templates = [
            "{emoji} {topic}最新进展：{organization}报告显示性能提升显著，推动科学发现加速。\n\n#高性能计算 #科学计算",
            "{emoji} {topic}技术解析：新型架构在{organization}测试中表现优异，能效比改善明显。\n\n关注前沿计算基础设施发展！",
            "{emoji} {topic}应用案例：{organization}利用该技术解决复杂科学问题，计算时间大幅缩短。\n\n#HPC #科研创新",
            "{emoji} {topic}基础设施更新：{organization}部署新系统，实现突破性性能指标。\n\n#超算 #技术创新",
            "{emoji} {topic}研究动态：{organization}最新研究揭示计算能力重大进展。\n\n#高性能计算 #科技前沿"
        ]
        
        self.ai_templates = [
            "{emoji} {topic}突破：{organization}研究团队发布最新成果，模型性能达到新高度。\n\n#人工智能 #机器学习",
            "{emoji} {topic}应用：在实际场景中展现强大能力，{organization}验证其有效性。\n\n#AI #技术创新",
            "{emoji} {topic}趋势分析：{organization}报告指出该领域发展迅速，产业应用广泛。\n\n关注AI前沿动态！",
            "{emoji} {topic}进展：{organization}研究人员在基准测试中取得最先进成果。\n\n#AI研究 #深度学习",
            "{emoji} {topic}实施：在{organization}的成功部署显示未来应用前景广阔。\n\n#AI技术 #创新"
        ]
    
    def generate_morning_content(self) -> str:
        """
        Generate morning content (HPC focus).
        
        Returns:
            Generated content string
        """
        return self._generate_content(focus="hpc")
    
    def generate_afternoon_content(self) -> str:
        """
        Generate afternoon content (AI focus).
        
        Returns:
            Generated content string
        """
        return self._generate_content(focus="ai")
    
    def _generate_content(self, focus: str = "hpc") -> str:
        """
        Generate content with specified focus.
        
        Args:
            focus: Content focus ('hpc' or 'ai')
            
        Returns:
            Generated content string
        """
        if focus == "hpc":
            topic = random.choice(self.hpc_topics)
            template = random.choice(self.hpc_templates)
        else:
            topic = random.choice(self.ai_topics)
            template = random.choice(self.ai_templates)
        
        organization = random.choice(self.organizations)
        emoji = random.choice(self.emojis)
        
        # Fill template
        content = template.format(
            emoji=emoji,
            topic=topic,
            organization=organization,
            date=datetime.now().strftime("%Y-%m-%d")
        )
        
        # Add hashtags
        hashtags = self._generate_hashtags(topic, focus)
        content += f"\n\n{hashtags}"
        
        # Validate length
        content = self._validate_content_length(content)
        
        logger.info(f"Generated {focus} content: {content[:50]}...")
        return content
    
    def _generate_hashtags(self, topic: str, focus: str) -> str:
        """
        Generate relevant hashtags.
        
        Args:
            topic: Content topic
            focus: Content focus
            
        Returns:
            Hashtag string
        """
        base_tags = ["#Tech", "#Innovation"]
        
        if focus == "hpc":
            focus_tags = ["#HPC", "#Supercomputing", "#HighPerformanceComputing"]
        else:
            focus_tags = ["#AI", "#ArtificialIntelligence", "#MachineLearning"]
        
        # Add topic-related tags
        topic_words = topic.lower().split()
        topic_tags = [f"#{word.capitalize()}" for word in topic_words[:2]]
        
        # Combine and limit number of tags
        all_tags = base_tags + focus_tags + topic_tags
        return " ".join(all_tags[:6])  # Limit to 6 tags
    
    def _validate_content_length(self, content: str) -> str:
        """
        Validate and adjust content length if necessary.
        
        Args:
            content: Original content
            
        Returns:
            Validated content
        """
        if len(content) <= self.max_length:
            return content
        
        logger.warning(f"Content too long ({len(content)} chars), truncating...")
        
        # Remove some hashtags if needed
        lines = content.split('\n')
        if len(lines) >= 3:
            # Try to shorten hashtag line
            hashtag_line = lines[-1]
            hashtags = hashtag_line.split()
            if len(hashtags) > 3:
                lines[-1] = ' '.join(hashtags[:3])
                content = '\n'.join(lines)
        
        # Final truncation if still too long
        if len(content) > self.max_length:
            content = content[:self.max_length-3] + "..."
        
        return content
    
    def generate_daily_content(self) -> Dict[str, str]:
        """
        Generate daily content (morning and afternoon).
        
        Returns:
            Dictionary with morning and afternoon content
        """
        return {
            "morning": self.generate_morning_content(),
            "afternoon": self.generate_afternoon_content()
        }
    
    def get_content_stats(self, content: str) -> Dict[str, int]:
        """
        Get statistics about content.
        
        Args:
            content: Content to analyze
            
        Returns:
            Dictionary with statistics
        """
        return {
            "length": len(content),
            "lines": len(content.split('\n')),
            "hashtags": content.count('#'),
            "mentions": content.count('@'),
            "emojis": sum(1 for char in content if char in self.emojis)
        }


if __name__ == "__main__":
    # Test code
    import sys
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Test English generator
    print("=== Testing English Content Generator ===")
    en_generator = ContentGenerator(language="en")
    
    print("\n🌅 Morning Content (HPC Focus):")
    morning_content = en_generator.generate_morning_content()
    print(morning_content)
    print(f"\n📊 Stats: {en_generator.get_content_stats(morning_content)}")
    
    print("\n🌇 Afternoon Content (AI Focus):")
    afternoon_content = en_generator.generate_afternoon_content()
    print(afternoon_content)
    print(f"\n📊 Stats: {en_generator.get_content_stats(afternoon_content)}")
    
    # Test Chinese generator
    print("\n\n=== Testing Chinese Content Generator ===")
    zh_generator = ContentGenerator(language="zh")
    
    print("\n🌅 上午内容（HPC焦点）:")
    zh_morning = zh_generator.generate_morning_content()
    print(zh_morning)
    
    print("\n🌇 下午内容（AI焦点）:")
    zh_afternoon = zh_generator.generate_afternoon_content()
    print(zh_afternoon)
