# cli.py
import argparse
import grpc
from decimal import Decimal
from generated import orderbook_pb2
from generated import orderbook_pb2_grpc

def connect():
    channel = grpc.insecure_channel('localhost:50051')
    return orderbook_pb2_grpc.OrderBookServiceStub(channel)

def place_order(stub, args):
    request = orderbook_pb2.OrderRequest(
        id=args.id,
        price=str(Decimal(args.price)),
        quantity=str(Decimal(args.quantity)),
        side=orderbook_pb2.Side.BID if args.side.upper() == "BID" else orderbook_pb2.Side.ASK,
        order_type=orderbook_pb2.OrderType.LIMIT if args.type.upper() == "LIMIT"
                  else orderbook_pb2.OrderType.MARKET
    )
    response = stub.PlaceOrder(request)
    print(f"Order placed: ID={response.id}, Status={response.status}")

def get_book(stub, args):
    request = orderbook_pb2.GetOrderBookRequest(depth=args.depth)
    response = stub.GetOrderBook(request)

    print("\nBids:")
    for level in response.bids:
        print(f"  {level.price}: {level.quantity}")

    print("\nAsks:")
    for level in response.asks:
        print(f"  {level.price}: {level.quantity}")

def main():
    parser = argparse.ArgumentParser(description='OrderBook CLI')
    subparsers = parser.add_subparsers(dest='command')

    place_parser = subparsers.add_parser('place')
    place_parser.add_argument('id', type=int)
    place_parser.add_argument('price', type=float)
    place_parser.add_argument('quantity', type=float)
    place_parser.add_argument('side', choices=['bid', 'ask'])
    place_parser.add_argument('type', choices=['limit', 'market'])

    book_parser = subparsers.add_parser('book')
    book_parser.add_argument('depth', type=int)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    try:
        stub = connect()
        if args.command == 'place':
            place_order(stub, args)
        elif args.command == 'book':
            get_book(stub, args)
    except grpc.RpcError as e:
        print(f"Error: {e.details()}")

if __name__ == '__main__':
    main()
