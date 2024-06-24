import datetime
import random
import uuid
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Generate plausible log files with opaque IDs")
    parser.add_argument("--num-lines", default=100, type=int)
    parser.add_argument("--num-users", default=10, type=int)
    parser.add_argument("--num-items", default=20, type=int)

    args = parser.parse_args()

    now = datetime.datetime.now()
    users = [uuid.uuid4().hex[: -random.randint(1, 3)] for _ in range(args.num_users)]
    items = [f"{uuid.uuid4().hex[:10].upper()}" for _ in range(args.num_items)]
    actions = [
        "{user_0} levelled up",
        "{user_0} sending message to {user_1}",
        "Receiving message (to {user_0}, from {user_1})",
        "Monitoring connection between {user_0} and {user_1}",
        "Contact: user {user_0} vs {user_1}",
        "Sending {item_0} from {user_0} to {user_1}",
        "{user_0} found {item_0}",
        "{user_0} found {item_0}, {item_1}, {item_2}",
    ]

    for _ in range(args.num_lines):
        now += datetime.timedelta(seconds=random.random() * 2)

        format_args = {
            "user_0": random.choice(users),
            "user_1": random.choice(users),
            "item_0": random.choice(items),
            "item_1": random.choice(items),
            "item_2": random.choice(items),
        }
        action = random.choice(actions)
        formatted = action.format(**format_args)
        print(f"{now.isoformat()} | {formatted}")
