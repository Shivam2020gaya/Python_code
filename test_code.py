rom trading_framework import ExecutionClient

class LimitOrderAgent:
    def __init__(self, execution_client: ExecutionClient):
        self.execution_client = execution_client
        self.orders = []

    def add_order(self, buy_flag: bool, product_id: str, amount: int, limit_price: float):
        order = {'buy_flag': buy_flag, 'product_id': product_id, 'amount': amount, 'limit_price': limit_price}
        self.orders.append(order)

    def price_tick(self, product_id: str, price: float):
        remaining_orders = []
        for order in self.orders:
            if order['product_id'] == product_id:
                if (order['buy_flag'] and price <= order['limit_price']) or (not order['buy_flag'] and price >= order['limit_price']):
                    self.execute_order(order)
                else:
                    remaining_orders.append(order)
            else:
                remaining_orders.append(order)
        self.orders = remaining_orders

    def execute_order(self, order):
        action = 'buy' if order['buy_flag'] else 'sell'
        getattr(self.execution_client, action)(order['product_id'], order['amount'], order['limit_price'])

# Test cases
if __name__ == "__main__":
    class MockExecutionClient(ExecutionClient):
        def buy(self, product_id: str, amount: int, price: float):
            print(f"Executed buy order: {amount} shares of {product_id} at ${price}")

        def sell(self, product_id: str, amount: int, price: float):
            print(f"Executed sell order: {amount} shares of {product_id} at ${price}")

    execution_client = MockExecutionClient()
    agent = LimitOrderAgent(execution_client)
    agent.add_order(True, 'IBM', 1000, 100)
    agent.price_tick('IBM', 99)
    agent.price_tick('IBM', 101)
    agent.add_order(False, 'AAPL', 500, 150)
    agent.price_tick('AAPL', 151)
    agent.price_tick('AAPL', 149)

