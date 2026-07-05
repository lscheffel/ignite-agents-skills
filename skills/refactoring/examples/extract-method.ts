// Exemplo: Extract Method

// ❌ ANTES - método longo com múltiplas responsabilidades
function processOrder(order: Order) {
  // validação
  if (!order.items || order.items.length === 0) {
    throw new Error('Order must have items');
  }
  if (!order.customerId) {
    throw new Error('Order must have a customer');
  }

  // cálculo
  let subtotal = 0;
  for (const item of order.items) {
    subtotal += item.price * item.quantity;
  }
  const tax = subtotal * 0.1;
  const total = subtotal + tax;

  // persistência
  db.orders.insert({
    customerId: order.customerId,
    items: order.items,
    subtotal,
    tax,
    total,
    status: 'pending',
  });

  // notificação
  emailService.send(order.customerId, 'Order confirmed', `Total: ${total}`);

  return { subtotal, tax, total };
}

// ✅ DEPOIS - métodos extraídos com responsabilidade única
function processOrder(order: Order) {
  validateOrder(order);
  const { subtotal, tax, total } = calculateTotals(order.items);
  persistOrder(order, { subtotal, tax, total });
  notifyCustomer(order.customerId, total);
  return { subtotal, tax, total };
}

function validateOrder(order: Order) {
  if (!order.items || order.items.length === 0) {
    throw new Error('Order must have items');
  }
  if (!order.customerId) {
    throw new Error('Order must have a customer');
  }
}

function calculateTotals(items: OrderItem[]) {
  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const tax = subtotal * 0.1;
  const total = subtotal + tax;
  return { subtotal, tax, total };
}

function persistOrder(order: Order, totals: { subtotal: number; tax: number; total: number }) {
  db.orders.insert({
    customerId: order.customerId,
    items: order.items,
    ...totals,
    status: 'pending',
  });
}

function notifyCustomer(customerId: string, total: number) {
  emailService.send(customerId, 'Order confirmed', `Total: ${total}`);
}
