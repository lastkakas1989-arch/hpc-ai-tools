"""
X/Twitter Publishing Tool
"""

import os
import sys
import logging
from datetime import datetime
from typing import Optional, Dict, Tuple
from pathlib import Path
from dotenv import load_dotenv

# Try to import tweepy, provide fallback if not installed
try:
    import tweepy
    TWEEPY_AVAILABLE = True
except ImportError:
    TWEEPY_AVAILABLE = False

logger = logging.getLogger(__name__)


class XPoster:
    """X/Twitter Publisher"""
    
    def __init__(self, mock_mode: Optional[bool] = None):
        """
        Initialize X/Twitter publisher.
        
        Args:
            mock_mode: If True, run in mock mode (no actual posting).
                       If None, auto-detect based on environment.
        """
        load_dotenv()
        
        # Determine mode
        if mock_mode is None:
            env_mock = os.getenv("MOCK_MODE", "true").lower()
            self.mock_mode = (env_mock == "true") or not TWEEPY_AVAILABLE
        else:
            self.mock_mode = mock_mode
        
        # Initialize client
        self.client = None
        if not self.mock_mode:
            self._init_tweepy_client()
        
        # Setup logging
        self._setup_logging()
        
        mode_str = "mock" if self.mock_mode else "real"
        logger.info(f"XPoster initialized in {mode_str} mode")
    
    def _setup_logging(self) -> None:
        """Setup logging directory and file."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / "x_poster.log"
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    def _init_tweepy_client(self) -> None:
        """Initialize Tweepy client."""
        try:
            api_key = os.getenv("X_API_KEY")
            api_secret = os.getenv("X_API_SECRET")
            access_token = os.getenv("X_ACCESS_TOKEN")
            access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
            
            # Check for required credentials
            missing_creds = []
            if not api_key:
                missing_creds.append("X_API_KEY")
            if not api_secret:
                missing_creds.append("X_API_SECRET")
            if not access_token:
                missing_creds.append("X_ACCESS_TOKEN")
            if not access_token_secret:
                missing_creds.append("X_ACCESS_TOKEN_SECRET")
            
            if missing_creds:
                logger.warning(f"Missing X API credentials: {', '.join(missing_creds)}")
                logger.warning("Switching to mock mode")
                self.mock_mode = True
                return
            
            # Initialize client
            self.client = tweepy.Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
            )
            
            # Test connection
            try:
                user = self.client.get_me()
                logger.info(f"Tweepy client initialized successfully. User: @{user.data.username}")
            except Exception as e:
                logger.error(f"Failed to verify X API credentials: {e}")
                logger.warning("Switching to mock mode")
                self.mock_mode = True
                self.client = None
            
        except Exception as e:
            logger.error(f"Failed to initialize Tweepy client: {e}")
            self.mock_mode = True
            self.client = None
    
    def post_to_x(self, content: str, mock: Optional[bool] = None) -> Tuple[bool, str]:
        """
        Post content to X/Twitter.
        
        Args:
            content: Content to post
            mock: Override mock mode for this call
            
        Returns:
            Tuple of (success, message)
        """
        use_mock = mock if mock is not None else self.mock_mode
        
        # Validate content
        validation_result = self._validate_content(content)
        if not validation_result[0]:
            return validation_result
        
        logger.info(f"Posting to X: {content[:50]}...")
        
        if use_mock:
            return self._mock_post(content)
        else:
            return self._real_post(content)
    
    def _validate_content(self, content: str) -> Tuple[bool, str]:
        """
        Validate content before posting.
        
        Args:
            content: Content to validate
            
        Returns:
            Tuple of (is_valid, message)
        """
        # Check length
        max_length = int(os.getenv("MAX_TWEET_LENGTH", "280"))
        if len(content) > max_length:
            return False, f"Content too long ({len(content)} > {max_length} characters)"
        
        # Check for empty content
        if not content.strip():
            return False, "Content is empty"
        
        # Check for minimum length
        if len(content.strip()) < 10:
            return False, "Content is too short (minimum 10 characters)"
        
        return True, "Content validation passed"
    
    def _mock_post(self, content: str) -> Tuple[bool, str]:
        """Mock posting (logs but doesn't actually post)."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log to file
        log_file = Path("logs") / "tweet_log.txt"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] MOCK POST\n")
            f.write(f"{content}\n")
            f.write("=" * 50 + "\n")
        
        # Log to console
        logger.info(f"[MOCK] Would post: {content[:100]}...")
        
        # Also save to output directory
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"mock_post_{timestamp_str}.txt"
        output_file.write_text(content, encoding="utf-8")
        
        return True, f"Mock post successful (saved to {output_file})"
    
    def _real_post(self, content: str) -> Tuple[bool, str]:
        """Real posting to X/Twitter."""
        if not self.client:
            return False, "X/Twitter client not initialized"
        
        try:
            # Post tweet
            response = self.client.create_tweet(text=content)
            
            # Extract tweet ID
            tweet_id = response.data['id']
            tweet_url = f"https://twitter.com/user/status/{tweet_id}"
            
            # Log success
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file = Path("logs") / "tweet_log.txt"
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] REAL POST - ID: {tweet_id}\n")
                f.write(f"{content}\n")
                f.write(f"URL: {tweet_url}\n")
                f.write("=" * 50 + "\n")
            
            logger.info(f"Posted successfully! Tweet ID: {tweet_id}")
            logger.info(f"Tweet URL: {tweet_url}")
            
            return True, f"Posted successfully! Tweet ID: {tweet_id}"
            
        except tweepy.TweepyException as e:
            error_msg = str(e)
            logger.error(f"Failed to post to X: {error_msg}")
            
            # Log error
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_log = Path("logs") / "post_errors.log"
            with open(error_log, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] ERROR\n")
                f.write(f"Content: {content}\n")
                f.write(f"Error: {error_msg}\n")
                f.write("=" * 50 + "\n")
            
            return False, f"Failed to post: {error_msg}"
        
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Unexpected error posting to X: {error_msg}")
            return False, f"Unexpected error: {error_msg}"
    
    def post_with_image(self, content: str, image_path: str) -> Tuple[bool, str]:
        """
        Post content with image to X/Twitter.
        
        Args:
            content: Text content
            image_path: Path to image file
            
        Returns:
            Tuple of (success, message)
        """
        if self.mock_mode:
            logger.info(f"[MOCK] Would post with image: {image_path}")
            return self._mock_post(f"{content}\n[Image: {image_path}]")
        
        if not self.client:
            return False, "X/Twitter client not initialized"
        
        # Check if image exists
        image_path_obj = Path(image_path)
        if not image_path_obj.exists():
            return False, f"Image file not found: {image_path}"
        
        # Check file size (X limit is 5MB for images)
        if image_path_obj.stat().st_size > 5 * 1024 * 1024:
            return False, "Image file too large (max 5MB)"
        
        try:
            # Upload media
            media = self.client.media_upload(filename=str(image_path_obj))
            
            # Post tweet with media
            response = self.client.create_tweet(
                text=content,
                media_ids=[media.media_id]
            )
            
            tweet_id = response.data['id']
            logger.info(f"Posted with image successfully! Tweet ID: {tweet_id}")
            
            return True, f"Posted with image successfully! Tweet ID: {tweet_id}"
            
        except tweepy.TweepyException as e:
            logger.error(f"Failed to post with image: {e}")
            return False, f"Failed to post with image: {e}"
    
    def get_posting_stats(self) -> Dict[str, any]:
        """
        Get posting statistics.
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            "mode": "mock" if self.mock_mode else "real",
            "tweepy_available": TWEEPY_AVAILABLE,
            "client_initialized": self.client is not None,
        }
        
        # Count posts from log file
        log_file = Path("logs") / "tweet_log.txt"
        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                content = f.read()
                stats["total_posts"] = content.count("REAL POST") + content.count("MOCK POST")
                stats["real_posts"] = content.count("REAL POST")
                stats["mock_posts"] = content.count("MOCK POST")
        
        return stats


def main():
    """Command-line interface for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test X/Twitter posting")
    parser.add_argument("--content", "-c", type=str, help="Content to post")
    parser.add_argument("--mock", "-m", action="store_true", help="Use mock mode")
    parser.add_argument("--image", "-i", type=str, help="Image file path")
    parser.add_argument("--stats", "-s", action="store_true", help="Show posting statistics")
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create poster
    poster = XPoster(mock_mode=args.mock)
    
    if args.stats:
        stats = poster.get_posting_stats()
        print("📊 Posting Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        return
    
    # Get content
    if args.content:
        content = args.content
    else:
        # Default test content
        content = "🚀 Test tweet from HPC/AI Tools - Automated content generation system working! #HPC #AI #Automation #Testing"
    
    # Post content
    if args.image:
        success, message = poster.post_with_image(content, args.image)
    else:
        success, message = poster.post_to_x(content)
    
    # Print result
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
