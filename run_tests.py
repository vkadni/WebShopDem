"""
run_tests.py – Main Suite Runner
Outputs:
   reports/TestReport_<timestamp>.html   – HTML with screenshots per step
   reports/TestResult_<timestamp>.xlsx   – Excel with screenshots per step
   data/DemoWebShop_Smoke_Tests_JIRA_Import.xlsx – NOT touched

Usage:
  python run_tests.py                         # run all 36 TCs
  python run_tests.py --tc TC-001 TC-002      # run specific TCs
  python run_tests.py --module "Shopping Cart"# run by module
  python run_tests.py --headless              # CI/Jenkins mode
"""

from __future__ import annotations
import argparse
import importlib
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from config.config import HEADLESS, BROWSER
from utils.report_generator    import generate_html_report
from utils.excel_result_writer import write_excel_results

#  Full TC Registry 
TC_REGISTRY: dict[str, tuple[str, str, str]] = {
    # (module_path, class_name, module_name)
    "TC-001": ("tests.tc001_home_page",              "TC001_HomePageLoads",          "Home Page & Navigation"),
    "TC-002": ("tests.tc002_navigation",             "TC002_NavigationLinks",         "Home Page & Navigation"),
    "TC-003": ("tests.tc003_search_bar",             "TC003_SearchBarVisibility",     "Home Page & Navigation"),
    "TC-004": ("tests.tc004_search_valid",           "TC004_SearchValid",             "Search Functionality"),
    "TC-005": ("tests.tc005_search_invalid",         "TC005_SearchInvalid",           "Search Functionality"),
    "TC-006": ("tests.tc006_search_empty",           "TC006_SearchEmpty",             "Search Functionality"),
    "TC-007": ("tests.tc007_register_valid",         "TC007_RegisterValid",           "User Registration"),
    "TC-008": ("tests.tc008_register_existing_email","TC008_RegisterExistingEmail",   "User Registration"),
    "TC-009": ("tests.tc009_register_blank",         "TC009_RegisterBlank",           "User Registration"),
    "TC-010": ("tests.tc010_register_invalid_email", "TC010_RegisterInvalidEmail",    "User Registration"),
    "TC-011": ("tests.tc011_login_valid",            "TC011_LoginValid",              "User Login & Logout"),
    "TC-012": ("tests.tc012_login_invalid_password", "TC012_LoginInvalidPassword",    "User Login & Logout"),
    "TC-013": ("tests.tc013_login_blank",            "TC013_LoginBlank",              "User Login & Logout"),
    "TC-014": ("tests.tc014_logout",                 "TC014_Logout",                  "User Login & Logout"),
    "TC-015": ("tests.tc015_browse_category",        "TC015_BrowseCategory",          "Product Browsing & Details"),
    "TC-016": ("tests.tc016_product_detail",         "TC016_ProductDetail",           "Product Browsing & Details"),
    "TC-017": ("tests.tc017_product_price",          "TC017_ProductPrice",            "Product Browsing & Details"),
    "TC-018": ("tests.tc018_sort_products",          "TC018_SortProducts",            "Product Browsing & Details"),
    "TC-019": ("tests.tc019_add_to_cart",            "TC019_AddToCart",               "Shopping Cart"),
    "TC-020": ("tests.tc020_view_cart",              "TC020_ViewCart",                "Shopping Cart"),
    "TC-021": ("tests.tc021_update_cart",            "TC021_UpdateCart",              "Shopping Cart"),
    "TC-022": ("tests.tc022_remove_cart",            "TC022_RemoveCart",              "Shopping Cart"),
    "TC-023": ("tests.tc023_continue_shopping",      "TC023_ContinueShopping",        "Shopping Cart"),
    "TC-024": ("tests.tc024_add_wishlist",           "TC024_AddWishlist",             "Wishlist"),
    "TC-025": ("tests.tc025_view_wishlist",          "TC025_ViewWishlist",            "Wishlist"),
    "TC-026": ("tests.tc026_checkout_guest",         "TC026_CheckoutGuest",           "Checkout Process"),
    "TC-027": ("tests.tc027_checkout_registered",    "TC027_CheckoutRegistered",      "Checkout Process"),
    "TC-028": ("tests.tc028_payment_methods",        "TC028_PaymentMethods",          "Checkout Process"),
    "TC-029": ("tests.tc029_place_order",            "TC029_PlaceOrder",              "Checkout Process"),
    "TC-030": ("tests.tc030_my_account",             "TC030_MyAccount",               "My Account"),
    "TC-031": ("tests.tc031_edit_account",           "TC031_EditAccount",             "My Account"),
    "TC-032": ("tests.tc032_change_password",        "TC032_ChangePassword",          "My Account"),
    "TC-033": ("tests.tc033_order_history",          "TC033_OrderHistory",            "My Account"),
    "TC-034": ("tests.tc034_add_compare",            "TC034_AddCompare",              "Product Compare & Reviews"),
    "TC-035": ("tests.tc035_view_compare",           "TC035_ViewCompare",             "Product Compare & Reviews"),
    "TC-036": ("tests.tc036_write_review",           "TC036_WriteReview",             "Product Compare & Reviews"),
}


def _run_tc(tc_id: str) -> dict:
    if tc_id not in TC_REGISTRY:
        print(f"  ️  {tc_id} not in TC_REGISTRY – skipping.")
        return {
            "tc_id": tc_id, "summary": "Not implemented", "module": "",
            "priority": "", "status": "Not Run", "actual_result": "TC not registered",
            "exec_date": "", "exec_time": "", "tester": "",
            "defect_id": "", "comments": "", "steps": [],
        }
    mod_path, cls_name, _ = TC_REGISTRY[tc_id]
    mod   = importlib.import_module(mod_path)
    klass = getattr(mod, cls_name)
    return klass().run()


def main():
    parser = argparse.ArgumentParser(description="DemoWebShop Smoke Test Runner")
    parser.add_argument("--tc",       nargs="+", help="TC IDs (e.g. TC-001 TC-002)")
    parser.add_argument("--module",   help="Run TCs by module name")
    parser.add_argument("--headless", action="store_true", help="Run headless (CI mode)")
    parser.add_argument("--browser",  default=None, help="chromium|firefox|webkit")
    args = parser.parse_args()

    if args.headless:
        import config.config as cfg; cfg.HEADLESS = True
    if args.browser:
        import config.config as cfg; cfg.BROWSER = args.browser

    # Determine TCs to run
    if args.tc:
        tc_ids = args.tc
    elif args.module:
        tc_ids = [k for k, v in TC_REGISTRY.items() if args.module.lower() in v[2].lower()]
        if not tc_ids:
            print(f"  ️  No TCs found for module: '{args.module}'")
            raise SystemExit(1)
    else:
        tc_ids = list(TC_REGISTRY.keys())

    print(f"\n{'='*65}")
    print(f"    DemoWebShop Smoke Test Suite  |  {len(tc_ids)} TC(s)")
    print(f"  Browser : {BROWSER}  |  Headless : {HEADLESS}")
    print(f"  TCs     : {', '.join(tc_ids)}")
    print(f"    JIRA import sheet will NOT be modified")
    print(f"{'='*65}")

    start   = time.time()
    results = [_run_tc(tc_id) for tc_id in tc_ids]
    elapsed = time.time() - start

    passed  = sum(1 for r in results if r["status"] == "Pass")
    failed  = sum(1 for r in results if r["status"] == "Fail")

    print(f"\n{'='*65}")
    print(f"  SUITE DONE  |  Total={len(results)}  Pass={passed}  Fail={failed}"
          f"  |  {int(elapsed//60):02d}:{int(elapsed%60):02d}")
    print(f"{'='*65}\n")

    generate_html_report(results)
    write_excel_results(results)

    raise SystemExit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
