import json
import locale


def statement(invoice: dict, plays: dict) -> str:

    def play_for(a_performance):
        return plays[a_performance["playID"]]

    def amount_for(a_performance):
        result = 0
        match play_for(a_performance)["type"]:
            case "tragedy":
                result = 40000
                if (a_performance["audience"] > 30):
                    result += 1000 * (a_performance["audience"] - 30)
            case "comedy":
                result = 30000
                if (a_performance["audience"] > 20):
                    result += 10000 + 500 * (a_performance["audience"] - 20)
                result += 300 * a_performance["audience"]
            case _:
                raise Exception(
                    f"unknown type {play_for(a_performance)['type']}")
        return result

    def volume_credits_for(a_performance):
        result = 0
        result += max((a_performance["audience"] - 30, 0))
        if("comedy" == play_for(a_performance)["type"]):
            result += a_performance["audience"] // 5
        return result

    def format(a_number):
        locale.setlocale(locale.LC_ALL, "en-US")
        return locale.currency(a_number, grouping=True)

    total_amount = 0
    volume_credits = 0
    result = f"Statement for {invoice['customer']}\n"

    for perf in invoice["performances"]:

        volume_credits += volume_credits_for(perf)

        # 注文の内訳を出力
        result += f"  {play_for(perf)['name']}: {format(amount_for(perf)/100)} ({perf['audience']} seats)\n"
        total_amount += amount_for(perf)

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
