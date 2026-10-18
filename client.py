"""
Agentic Commerce Retroactive Price Drop Refund Claimer (Pure Stdlib)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
from typing import Dict, Any, List

class AgenticPriceDropRefundClaimer:
    MERCHANT_POLICY_DAYS = {
        "bestbuy": 14,
        "target": 14,
        "amazon": 7,
        "nordstrom": 14,
        "walmart": 30
    }

    def __init__(self, claimer_name: str = "GenPark-PriceDrop-Claimer"):
        self.claimer_name = claimer_name

    def evaluate_price_drop_claims(self, purchase_orders: List[Dict[str, Any]]) -> Dict[str, Any]:
        eligible_claims = []
        total_reclaimable_usd = 0.0
        
        for order in purchase_orders:
            oid = order.get("order_id", "ORD-000")
            merchant = order.get("merchant", "retailer").lower()
            product = order.get("product_name", "Item")
            paid = float(order.get("paid_price", 0.0))
            live_price = float(order.get("live_current_price", paid))
            days = int(order.get("days_since_purchase", 5))
            
            max_days = self.MERCHANT_POLICY_DAYS.get(merchant, 14)
            price_delta = paid - live_price
            
            # Eligible if price dropped >= $3.00 within the policy window
            if price_delta >= 3.0 and days <= max_days:
                total_reclaimable_usd += price_delta
                claim_packet = (
                    f"Merchant: {merchant.title()} | Order: {oid} | Item: {product}\n"
                    f"Purchased Price: ${paid:.2f} | Current Live Price: ${live_price:.2f}\n"
                    f"Requested Refund Adjustment: ${price_delta:.2f} (Within {max_days}-day price match guarantee policy window)."
                )
                eligible_claims.append({
                    "order_id": oid,
                    "merchant": merchant,
                    "product_name": product,
                    "price_difference_usd": round(price_delta, 2),
                    "days_since_purchase": days,
                    "policy_window_days": max_days,
                    "claim_submission_text": claim_packet
                })
                
        return {
            "claimer": self.claimer_name,
            "orders_reviewed": len(purchase_orders),
            "eligible_claims_count": len(eligible_claims),
            "total_reclaimable_refund_usd": round(total_reclaimable_usd, 2),
            "claims": eligible_claims,
            "verdict": "PRICE_DROP_REFUNDS_CLAIMED" if eligible_claims else "NO_PRICE_DROPS_ELIGIBLE"
        }
