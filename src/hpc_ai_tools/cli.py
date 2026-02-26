#!/usr/bin/env python3
"""
HPC/AI Tools Command Line Interface
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional

from .content_generator import ContentGenerator
from .x_poster import XPoster


def setup_parser() -> argparse.ArgumentParser:
    """Setup command line argument parser."""
    parser = argparse.ArgumentParser(
        description="HPC/AI Content Generation and Publishing Tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s generate                    # Generate HPC/AI content
  %(prog)s generate --output content.txt  # Save to file
  %(prog)s post --mock                 # Test publishing (dry run)
  %(prog)s post --real                 # Real publishing (requires API keys)
  %(prog)s setup                       # Setup configuration
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate HPC/AI content")
    gen_parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output file path (default: prints to stdout)",
    )
    gen_parser.add_argument(
        "--time",
        "-t",
        choices=["morning", "afternoon", "both"],
        default="both",
        help="Time of day for content (default: both)",
    )
    gen_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )

    # Post command
    post_parser = subparsers.add_parser("post", help="Post content to X/Twitter")
    post_parser.add_argument(
        "--mode",
        "-m",
        choices=["mock", "real"],
        default="mock",
        help="Publishing mode (default: mock)",
    )
    post_parser.add_argument(
        "--content",
        "-c",
        type=str,
        help="Content file to post (default: generates new content)",
    )
    post_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )

    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Setup configuration")
    setup_parser.add_argument(
        "--force", "-f", action="store_true", help="Force overwrite existing config"
    )
    setup_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )

    # Test command
    test_parser = subparsers.add_parser("test", help="Test system functionality")
    test_parser.add_argument(
        "--component",
        "-c",
        choices=["all", "generator", "poster", "config"],
        default="all",
        help="Component to test (default: all)",
    )
    test_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )

    return parser


def command_generate(args) -> int:
    """Handle generate command."""
    try:
        generator = ContentGenerator()
        
        if args.time == "both":
            morning_content = generator.generate_morning_content()
            afternoon_content = generator.generate_afternoon_content()
            
            if args.output:
                output_dir = Path(args.output).parent
                output_dir.mkdir(parents=True, exist_ok=True)
                
                morning_file = Path(args.output).with_stem(
                    Path(args.output).stem + "_morning"
                )
                afternoon_file = Path(args.output).with_stem(
                    Path(args.output).stem + "_afternoon"
                )
                
                morning_file.write_text(morning_content, encoding="utf-8")
                afternoon_file.write_text(afternoon_content, encoding="utf-8")
                
                if args.verbose:
                    print(f"✅ Morning content saved to: {morning_file}")
                    print(f"✅ Afternoon content saved to: {afternoon_file}")
                else:
                    print(f"✅ Content saved to: {morning_file}, {afternoon_file}")
            else:
                print("🌅 Morning Content:")
                print("=" * 50)
                print(morning_content)
                print("\n🌇 Afternoon Content:")
                print("=" * 50)
                print(afternoon_content)
                
        else:
            if args.time == "morning":
                content = generator.generate_morning_content()
                time_label = "Morning"
            else:  # afternoon
                content = generator.generate_afternoon_content()
                time_label = "Afternoon"
            
            if args.output:
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(content, encoding="utf-8")
                
                if args.verbose:
                    print(f"✅ {time_label} content saved to: {output_path}")
                else:
                    print(f"✅ Content saved to: {output_path}")
            else:
                print(f"{time_label} Content:")
                print("=" * 50)
                print(content)
        
        return 0
        
    except Exception as e:
        print(f"❌ Error generating content: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def command_post(args) -> int:
    """Handle post command."""
    try:
        poster = XPoster()
        
        if args.content:
            content_path = Path(args.content)
            if not content_path.exists():
                print(f"❌ Content file not found: {content_path}", file=sys.stderr)
                return 1
            content = content_path.read_text(encoding="utf-8")
        else:
            # Generate new content
            generator = ContentGenerator()
            content = generator.generate_morning_content()
            if args.verbose:
                print("📝 Generated content for posting:")
                print(content)
        
        if args.mode == "real":
            if args.verbose:
                print("🚀 Posting to X (real mode)...")
            success, message = poster.post_to_x(content, mock=False)
        else:
            if args.verbose:
                print("🧪 Testing X posting (mock mode)...")
            success, message = poster.post_to_x(content, mock=True)
        
        if success:
            print(f"✅ {message}")
            return 0
        else:
            print(f"❌ {message}", file=sys.stderr)
            return 1
            
    except Exception as e:
        print(f"❌ Error posting content: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def command_setup(args) -> int:
    """Handle setup command."""
    try:
        env_example = Path(".env.example")
        env_file = Path(".env")
        
        if env_file.exists() and not args.force:
            print("⚠️  .env file already exists. Use --force to overwrite.")
            return 0
        
        if not env_example.exists():
            print("❌ .env.example file not found.", file=sys.stderr)
            return 1
        
        # Copy .env.example to .env
        env_content = env_example.read_text(encoding="utf-8")
        env_file.write_text(env_content, encoding="utf-8")
        
        print("✅ Configuration file created: .env")
        print("\n📋 Next steps:")
        print("1. Edit .env file with your API credentials")
        print("2. For X/Twitter API, visit: https://developer.twitter.com/")
        print("3. Test with: hpc-ai-tools post --mock")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error setting up configuration: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def command_test(args) -> int:
    """Handle test command."""
    try:
        print("🧪 Testing HPC/AI Tools System...")
        print("=" * 50)
        
        tests_passed = 0
        tests_failed = 0
        
        # Test content generator
        if args.component in ["all", "generator"]:
            print("\n1. Testing Content Generator...")
            try:
                generator = ContentGenerator()
                morning = generator.generate_morning_content()
                afternoon = generator.generate_afternoon_content()
                
                if morning and afternoon:
                    print("   ✅ Content generator working")
                    print(f"   📝 Morning content length: {len(morning)} chars")
                    print(f"   📝 Afternoon content length: {len(afternoon)} chars")
                    tests_passed += 1
                else:
                    print("   ❌ Content generator failed")
                    tests_failed += 1
            except Exception as e:
                print(f"   ❌ Content generator error: {e}")
                tests_failed += 1
        
        # Test X poster
        if args.component in ["all", "poster"]:
            print("\n2. Testing X Poster...")
            try:
                poster = XPoster()
                test_content = "Test content from HPC/AI Tools"
                success, message = poster.post_to_x(test_content, mock=True)
                
                if success:
                    print(f"   ✅ X poster working: {message}")
                    tests_passed += 1
                else:
                    print(f"   ❌ X poster failed: {message}")
                    tests_failed += 1
            except Exception as e:
                print(f"   ❌ X poster error: {e}")
                tests_failed += 1
        
        # Test configuration
        if args.component in ["all", "config"]:
            print("\n3. Testing Configuration...")
            try:
                from dotenv import load_dotenv
                load_dotenv()
                
                # Check for required environment variables
                required_vars = ["X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET"]
                missing_vars = [var for var in required_vars if not os.getenv(var)]
                
                if missing_vars:
                    print(f"   ⚠️  Missing environment variables: {', '.join(missing_vars)}")
                    print("   ℹ️  Run 'hpc-ai-tools setup' to create configuration")
                    tests_passed += 1  # Not a failure, just a warning
                else:
                    print("   ✅ All required environment variables found")
                    tests_passed += 1
            except Exception as e:
                print(f"   ❌ Configuration error: {e}")
                tests_failed += 1
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Test Summary:")
        print(f"   ✅ Passed: {tests_passed}")
        print(f"   ❌ Failed: {tests_failed}")
        
        if tests_failed == 0:
            print("\n🎉 All tests passed!")
            return 0
        else:
            print(f"\n⚠️  {tests_failed} test(s) failed")
            return 1
            
    except Exception as e:
        print(f"❌ Error running tests: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def main() -> int:
    """Main entry point for CLI."""
    parser = setup_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    # Dispatch to appropriate command handler
    command_handlers = {
        "generate": command_generate,
        "post": command_post,
        "setup": command_setup,
        "test": command_test,
    }
    
    handler = command_handlers.get(args.command)
    if handler:
        return handler(args)
    else:
        print(f"❌ Unknown command: {args.command}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())