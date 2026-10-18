#!/usr/bin/env python3
import json
import sys
from client import AgenticPriceDropRefundClaimer

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        claimer = AgenticPriceDropRefundClaimer()
        orders = [
            {"order_id": "BB-1092", "merchant": "bestbuy", "product_name": "4K OLED TV", "paid_price": 1299.99, "live_current_price": 1149.99, "days_since_purchase": 8},
            {"order_id": "AMZ-991", "merchant": "amazon", "product_name": "USB-C Hub", "paid_price": 35.0, "live_current_price": 35.0, "days_since_purchase": 3}
        ]
        res = claimer.evaluate_price_drop_claims(orders)
        assert res["eligible_claims_count"] == 1
        assert res["total_reclaimable_refund_usd"] == 150.0
        print(f"[TEST PASS] Retroactive Refund Found: ${res['total_reclaimable_refund_usd']}")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-price-drop-claimer", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "evaluate_price_drop_claims", "description": "Scan past orders and claim retroactive price-drop refunds"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                claimer = AgenticPriceDropRefundClaimer()
                out = claimer.evaluate_price_drop_claims(args.get("purchase_orders", []))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
