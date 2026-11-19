%dw 2.0
output application/json
var orders = payload groupBy $.order_id
---
{
  sheetName: "Orders",
  rows: flatten(
    orders pluck ((rows, orderId) -> do {
      var first = rows[0]
      var lineTotal = (row) -> (row.quantity as Number) * (row.unit_price as Number)
      ---
      rows map (row, index) -> {
        order_id: orderId as Number,
        customer: first.customer,
        order_date: first.order_date,
        status: first.status,
        line_no: index + 1,
        sku: row.sku,
        description: row.description,
        quantity: row.quantity,
        unit_price: row.unit_price,
        line_total: lineTotal(row)
      }
    })
  )
}
