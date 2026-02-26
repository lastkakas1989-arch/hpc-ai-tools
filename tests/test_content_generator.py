"""
测试内容生成器
"""

import pytest
from hpc_ai_tools.content_generator import HPCContentGenerator


class TestHPCContentGenerator:
    """测试HPCContentGenerator类"""
    
    def setup_method(self):
        """测试前设置"""
        self.generator = HPCContentGenerator()
    
    def test_initialization(self):
        """测试初始化"""
        assert hasattr(self.generator, 'hpc_topics')
        assert hasattr(self.generator, 'ai_topics')
        assert hasattr(self.generator, 'organizations')
        assert hasattr(self.generator, 'emojis')
        
        assert len(self.generator.hpc_topics) > 0
        assert len(self.generator.ai_topics) > 0
        assert len(self.generator.organizations) > 0
        assert len(self.generator.emojis) > 0
    
    def test_generate_tweet_hpc(self):
        """测试生成HPC推文"""
        tweet = self.generator.generate_tweet("hpc")
        
        assert isinstance(tweet, str)
        assert len(tweet) > 0
        assert "#" in tweet  # 应该包含话题标签
    
    def test_generate_tweet_ai(self):
        """测试生成AI推文"""
        tweet = self.generator.generate_tweet("ai")
        
        assert isinstance(tweet, str)
        assert len(tweet) > 0
        assert "#" in tweet  # 应该包含话题标签
    
    def test_generate_daily_content(self):
        """测试生成每日内容"""
        content = self.generator.generate_daily_content()
        
        assert isinstance(content, dict)
        assert "morning" in content
        assert "afternoon" in content
        
        assert isinstance(content["morning"], str)
        assert isinstance(content["afternoon"], str)
        
        assert len(content["morning"]) > 0
        assert len(content["afternoon"]) > 0
    
    def test_tweet_length(self):
        """测试推文长度"""
        tweet = self.generator.generate_tweet("hpc")
        # X推文最大长度280字符，确保不超过
        assert len(tweet) <= 280
    
    def test_emoji_in_tweet(self):
        """测试推文包含emoji"""
        tweet = self.generator.generate_tweet("hpc")
        # 检查是否包含常见emoji字符
        has_emoji = any(ord(char) > 0xFFFF for char in tweet[:100])
        assert has_emoji or "🚀" in tweet or "🔬" in tweet


if __name__ == "__main__":
    # 运行测试
    import sys
    sys.exit(pytest.main([__file__, "-v"]))