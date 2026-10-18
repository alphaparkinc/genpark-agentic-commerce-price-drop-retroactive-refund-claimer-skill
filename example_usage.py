from client import AgenticPriceDropRefundClaimer

def main():
    claimer = AgenticPriceDropRefundClaimer()
    purchases = [
        {"order_id": "TGT-4481", "merchant": "target", "product_name": "Espresso Machine", "paid_price": 199.99, "live_current_price": 159.99, "days_since_purchase": 6},
        {"order_id": "WMT-7712", "merchant": "walmart", "product_name": "Cordless Vacuum", "paid_price": 249.00, "live_current_price": 209.00, "days_since_purchase": 18}
    ]
    res = claimer.evaluate_price_drop_claims(purchases)
    print("--- Price Drop Retroactive Claimer ---")
    print(f"Total Reclaimable: ${res['total_reclaimable_refund_usd']} across {res['eligible_claims_count']} claims")
    for c in res['claims']:
        print(f"* [{c['merchant'].upper()}] {c['product_name']}: Refund ${c['price_difference_usd']}")

if __name__ == "__main__":
    main()
