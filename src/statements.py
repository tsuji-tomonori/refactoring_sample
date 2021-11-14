import json
import locale


def statement(invoice: dict, plays: dict) -> str:
    total_amount = 0
    volume_credits = 0
    result = f"Statement for {invoice['customer']}\n"
    locale.setlocale(locale.LC_ALL, "en-US")
    # 以降formatを呼べば動くように
    def format(x): return locale.currency(x, grouping=True)

    for perf in invoice["performances"]:
        play = plays[perf["playID"]]
        this_amount = 0

        if(play["type"] == "tragedy"):
            this_amount = 40000
            if (perf["audience"] > 30):
                this_amount += 1000 * (perf["audience"] - 30)
        elif(play["type"] == "comedy"):
            this_amount = 30000
            if (perf["audience"] > 20):
                this_amount += 10000 + 500 * (perf["audience"] - 20)
            this_amount += 300 * perf["audience"]
        else:
            raise Exception(f"unknown type {play['type']}")

        # ボリューム得点のポイントを加算
        volume_credits += max((perf["audience"] - 30, 0))
        # 喜劇のときは5人につきさらにポイントを加算
        if("comedy" == play["type"]):
            volume_credits += perf["audience"] // 5
        # 注文の内訳を出力
        result += f"  {play['name']}: {format(this_amount/100)} ({perf['audience']} seats)\n"
        total_amount += this_amount

    result += f"Amount owed is {format(total_amount/100)}\n"
    result += f"You earned {volume_credits} credits\n"
    return result


def read_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        result = json.load(f)
    return result


if __name__ == "__main__":
    invoices = read_json("invoices.json")
    plays = read_json("plays.json")
    print(statement(invoices[0], plays))
