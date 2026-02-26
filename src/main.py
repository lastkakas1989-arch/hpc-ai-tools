#!/usr/bin/env python3
"""
HPC/AI Tools - Main Entry Point

This module provides backward compatibility with the old CLI.
For new development, use the hpc_ai_tools.cli module instead.
"""

import sys
import warnings

warnings.warn(
    "The main.py entry point is deprecated. Use 'hpc-ai-tools' command instead.",
    DeprecationWarning,
    stacklevel=2
)

if __name__ == "__main__":
    # Redirect to new CLI
    from hpc_ai_tools.cli import main
    sys.exit(main())