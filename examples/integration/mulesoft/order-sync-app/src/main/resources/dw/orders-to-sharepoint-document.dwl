%dw 2.0
output application/json
var orders = payload groupBy $.order_id
---
{
  fileName: "order-summary.html",
  title: "Order summary export",
  contentType: "text/html",
  content: "<html><body><h1>Order summary export</h1><p>Generated from SQLite via MuleSoft and DataWeave.</p><table><thead><tr><th>Order ID</th><th>Customer</th><th>Date</th><th>Status</th><th>SKU</th><th>Description</th><th>Qty</th><th>Unit price</th></tr></thead><tbody>"
    ++ (
      flatten(
        orders pluck ((rows, orderId) ->
          rows map (row) ->
            "<tr><td>" ++ (orderId as String) ++ "</td><td>" ++ row.customer ++ "</td><td>" ++ (row.order_date as String) ++ "</td><td>" ++ row.status ++ "</td><td>" ++ row.sku ++ "</td><td>" ++ row.description ++ "</td><td>" ++ (row.quantity as String) ++ "</td><td>" ++ (row.unit_price as String) ++ "</td></tr>"
        )
      ) joinBy ""
    )
    ++ "</tbody></table></body></html>"
}
