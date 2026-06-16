def _require_pandas(feature_name: str):
    try:
        import pandas as pd
    except ImportError as e:
        raise ImportError(
            f"{feature_name} requires pandas. Install it with: pip install partialstats[pandas]"
        ) from e
    return pd
