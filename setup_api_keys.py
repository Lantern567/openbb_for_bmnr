"""
Setup API Keys for OpenBB Platform
This script helps you configure API credentials for data providers

IMPORTANT: Do NOT commit your actual API keys to Git!
Set them as environment variables instead.
"""
from openbb import obb
import os

def setup_api_keys():
    """
    Configure API keys for OpenBB Platform data providers

    You need to obtain API keys from:
    1. Financial Modeling Prep (FMP): https://site.financialmodelingprep.com/developer/docs
    2. Polygon.io: https://polygon.io/
    3. Alpha Vantage: https://www.alphavantage.co/support/#api-key
    """

    print("=" * 60)
    print("OpenBB Platform API Key Configuration")
    print("=" * 60)

    # Check if keys are already set in environment
    fmp_key = os.environ.get('OPENBB_FMP_API_KEY', '')
    polygon_key = os.environ.get('OPENBB_POLYGON_API_KEY', '')
    av_key = os.environ.get('OPENBB_ALPHA_VANTAGE_API_KEY', '')

    if not fmp_key:
        print("\n[!] FMP API Key not found in environment")
        print("    Get your free key at: https://site.financialmodelingprep.com/developer/docs")
        fmp_key = input("    Enter your FMP API key (or press Enter to skip): ").strip()

    if not polygon_key:
        print("\n[!] Polygon API Key not found in environment")
        print("    Get your free key at: https://polygon.io/")
        polygon_key = input("    Enter your Polygon API key (or press Enter to skip): ").strip()

    if not av_key:
        print("\n[!] Alpha Vantage API Key not found in environment")
        print("    Get your free key at: https://www.alphavantage.co/support/#api-key")
        av_key = input("    Enter your Alpha Vantage API key (or press Enter to skip): ").strip()

    # Set credentials
    configured = []
    try:
        if fmp_key:
            obb.user.credentials.fmp_api_key = fmp_key
            os.environ['OPENBB_FMP_API_KEY'] = fmp_key
            configured.append("FMP")

        if polygon_key:
            obb.user.credentials.polygon_api_key = polygon_key
            os.environ['OPENBB_POLYGON_API_KEY'] = polygon_key
            configured.append("Polygon")

        if av_key:
            obb.user.credentials.alpha_vantage_api_key = av_key
            os.environ['OPENBB_ALPHA_VANTAGE_API_KEY'] = av_key
            configured.append("Alpha Vantage")

        if configured:
            print("\n" + "=" * 60)
            print(f"[OK] Configured: {', '.join(configured)}")
            print("=" * 60)

            print("\nTo make these keys permanent, add them to your environment variables:")
            print("\nWindows (Command Prompt):")
            if fmp_key:
                print(f'  SET OPENBB_FMP_API_KEY={fmp_key}')
            if polygon_key:
                print(f'  SET OPENBB_POLYGON_API_KEY={polygon_key}')
            if av_key:
                print(f'  SET OPENBB_ALPHA_VANTAGE_API_KEY={av_key}')

            print("\nOr add them to start_backend_with_keys.bat")
        else:
            print("\n[WARNING] No API keys configured")
            print("The system will use sample data for demonstration")

    except Exception as e:
        print(f"\n[ERROR] Configuration failed: {e}")

if __name__ == "__main__":
    print("\n")
    setup_api_keys()
    print("\n")
