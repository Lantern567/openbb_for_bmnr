"""
Setup API Keys for OpenBB Platform
This script configures all API credentials for data providers
"""
from openbb import obb
import os

def setup_api_keys():
    """Configure API keys for all data providers"""

    print("=" * 60)
    print("OpenBB Platform API Key Configuration")
    print("=" * 60)

    # API Keys
    api_keys = {
        'fmp_api_key': 'aMygwSPUSv1KUf1OxlVPvk12JrJnIGpi',
        'polygon_api_key': 'hzQYA0NSR15nlAT3Bym3nFCsTuF05inq',
        'alpha_vantage_api_key': 'OmM1MWM2NWU5Yjg2NzEzNGI1ZTQ2NzFlOGFiMzQ3M2Ji'
    }

    print("\nConfiguring API keys...")

    try:
        # Set credentials using OpenBB user settings
        for key_name, key_value in api_keys.items():
            provider = key_name.replace('_api_key', '')
            print(f"  Setting {provider} API key...")

            # Set the credential
            obb.user.credentials.__setattr__(key_name, key_value)

        # Save the configuration
        print("\nSaving configuration...")
        obb.user.save()

        print("\n" + "=" * 60)
        print("[OK] All API keys configured successfully!")
        print("=" * 60)

        print("\nConfigured providers:")
        print("  - Financial Modeling Prep (FMP)")
        print("  - Polygon.io")
        print("  - Alpha Vantage")

        print("\nYou can now fetch real market data from these providers!")

    except Exception as e:
        print(f"\n[ERROR] Failed to configure API keys: {e}")
        print("\nTrying alternative method (environment variables)...")

        # Fallback: Set as environment variables
        os.environ['OPENBB_FMP_API_KEY'] = api_keys['fmp_api_key']
        os.environ['OPENBB_POLYGON_API_KEY'] = api_keys['polygon_api_key']
        os.environ['OPENBB_ALPHA_VANTAGE_API_KEY'] = api_keys['alpha_vantage_api_key']

        print("\n[OK] API keys set as environment variables for this session")
        print("Note: These will need to be reconfigured each time you restart")

def verify_configuration():
    """Verify that API keys are properly configured"""

    print("\n" + "=" * 60)
    print("Verifying Configuration")
    print("=" * 60)

    # Check credentials
    try:
        fmp_key = obb.user.credentials.fmp_api_key
        polygon_key = obb.user.credentials.polygon_api_key
        av_key = obb.user.credentials.alpha_vantage_api_key

        print("\nCredentials Status:")
        print(f"  FMP: {'[OK] Configured' if fmp_key else '[X] Not configured'}")
        print(f"  Polygon: {'[OK] Configured' if polygon_key else '[X] Not configured'}")
        print(f"  Alpha Vantage: {'[OK] Configured' if av_key else '[X] Not configured'}")

        if all([fmp_key, polygon_key, av_key]):
            print("\n[OK] All API keys are configured!")
            return True
        else:
            print("\n[WARNING] Some API keys are missing")
            return False

    except Exception as e:
        print(f"\n[ERROR] Could not verify configuration: {e}")
        return False

if __name__ == "__main__":
    print("\n")
    setup_api_keys()
    verify_configuration()

    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print("1. Run test_symbol.py to test data fetching")
    print("2. Restart your backend server (if running)")
    print("3. Test OpenBB Workspace connection")
    print("\n")
