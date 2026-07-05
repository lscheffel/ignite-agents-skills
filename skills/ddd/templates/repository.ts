// Repository Interface Template
// Interface in domain, implementation in infrastructure

export interface OrderRepository {
  // Add aggregate
  add(order: Order): Promise<void>;
  
  // Remove aggregate
  remove(order: Order): Promise<void>;
  
  // Find by ID (returns aggregate root)
  findById(id: OrderId): Promise<Order | null>;
  
  // Find by user (domain-specific query)
  findByUserId(userId: UserId): Promise<Order[]>;
  
  // Find pending orders (domain-specific query)
  findPendingOrders(): Promise<Order[]>;
}

// Implementation in infrastructure layer
// src/infrastructure/repositories/prisma-order-repository.ts

export class PrismaOrderRepository implements OrderRepository {
  constructor(private readonly prisma: PrismaClient) {}
  
  async add(order: Order): Promise<void> {
    await this.prisma.order.create({
      data: OrderMapper.toPersistence(order)
    });
  }
  
  async findById(id: OrderId): Promise<Order | null> {
    const data = await this.prisma.order.findUnique({
      where: { id: id.value },
      include: { items: true }
    });
    return data ? OrderMapper.toDomain(data) : null;
  }
  
  async findByUserId(userId: UserId): Promise<Order[]> {
    const orders = await this.prisma.order.findMany({
      where: { userId: userId.value }
    });
    return orders.map(OrderMapper.toDomain);
  }
  
  async findPendingOrders(): Promise<Order[]> {
    const orders = await this.prisma.order.findMany({
      where: { status: "PENDING" }
    });
    return orders.map(OrderMapper.toDomain);
  }
  
  async remove(order: Order): Promise<void> {
    await this.prisma.order.delete({
      where: { id: order.orderId.value }
    });
  }
}