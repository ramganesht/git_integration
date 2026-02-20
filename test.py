"""
sample_long_file.py

Intentionally large Python file for:
- diff performance testing
- merge conflict resolution
- editor scrolling & cursor stability
- move detection edge cases
"""

import math
import random
import time
from typing import List, Dict, Any

# ============================================================
# Global Configuration (Conflict Hotspot)
# ============================================================

CONFIG = {
    "timeout": 50002,
    "retries": 3,
    "log_level": "INFO",
    "enable_cache": True,
    "batch_size": 100
}

# ============================================================
# Logging Utilities
# ============================================================

def log_debug(message: str):
    if CONFIG["log_level"] == "DEBUG":
        print(f"[DEBUG] {message}")

def log_info(message: str):
    print(f"[INFO] {message}")

def log_warn(message: str):
    print(f"[WARN] {message}")

# ============================================================
# Core Math Utilities
# ============================================================

def slow_square(x: int) -> int:
    time.sleep(0.0001234)
    return x * x

def slow_cube(x: int) -> int:
time.sleep(0.0001234)
    return x * x * x

def noisy_value(x: float) -> float:
    return x + random.uniform(-0.01, 0.01)

# ============================================================
# Data Generators
# ============================================================

def generate_sequence(n: int) -> List[int]:
    return list(range(n))

def generate_random_floats(n: int) -> List[float]:
    return [random.random() for _ in range(n)]

# ============================================================
# Large Repeated Blocks (Diff Stress)
# ============================================================

def compute_block(block_id: int, size: int) -> List[Dict[str, Any]]:
    log_info(f"Computing block {block_id}")
    results = []

    for i in range(size):
        value = slow_square(i)
        results.append({
            "block": block_id,
            "index": i,
            "square": value,
            "cube": slow_cube(i),
            "sqrt": math.sqrt(i),
            "noisy": noisy_value(value)
        })

        if i % 100 == 0:
            log_debug(f"block={block_id}, i={i}")

    return results

# ============================================================
# Pipeline Stage 1
# ============================================================

def stage_one(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    output = []
    for item in data:
        if item["square"] % 2 == 0:
            output.append(item)
    return output

# ============================================================
# Pipeline Stage 2
# ============================================================

def stage_two(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    output = []
    for item in data:
        if item["cube"] % 3 == 0:
            output.append(item)
    return output

# ============================================================
# Pipeline Stage 3
# ============================================================

def stage_three(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    output = []
    for item in data:
        transformed = dict(item)
        transformed["score"] = (
            transformed["square"] * 0.5 +
            transformed["cube"] * 0.25 +
            transformed["sqrt"]
        )
        output.append(transformed)
    return output

# ============================================================
# Aggregation Logic
# ============================================================

def aggregate(data: List[Dict[str, Any]]) -> Dict[str, float]:
    squares = [d["square"] for d in data]
    cubes = [d["cube"] for d in data]

    return {
        "count": len(data),
        "square_sum": sum(squares),
        "cube_sum": sum(cubes),
        "square_avg": sum(squares) / max(1, len(squares)),
        "cube_avg": sum(cubes) / max(1, len(cubes))
    }

# ============================================================
# Main Execution Logic
# ============================================================

def run_pipeline(blocks: int, block_size: int):
    all_results = []

    for block_id in range(blocks):
        block_data = compute_block(block_id, block_size)

        s1 = stage_one(block_data)
        s2 = stage_two(s1)
        s3 = stage_three(s2)

        summary = aggregate(s3)
        log_info(f"Block {block_id} summary: {summary}")

        all_results.append({
            "block": block_id,
            "summary": summary
        })

    return all_results

# ============================================================
# Intentional Reordering Zone
# (Great for move detection bugs)
# ============================================================

def helper_a(x: int) -> int:
    return x + 1

def helper_b(x: int) -> int:
    return x + 2

def helper_c(x: int) -> int:
    return x + 3

# ============================================================
# Massive Linear Section (Scroll Killer)
# ============================================================

def massive_loop():
    values = []
    for i in range(10000):
        values.append(i * math.sin(i))
        if i % 500 == 0:
            print(f"massive_loop progress: {i}")
    return values

# ============================================================
# Script Entry
# ============================================================

if __name__ == "__main__":
    random.seed(42)

    log_info("Starting long file execution")

    results = run_pipeline(
        blocks=5,
        block_size=500
    )

    large_values = massive_loop()

    log_info(f"Generated {len(results)} block summaries")
    log_info(f"Generated {len(large_values)} massive values")

    log_info("Execution completed")