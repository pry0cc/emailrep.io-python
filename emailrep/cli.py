import sys
import json
from dateutil import parser

from emailrep.utils import parse_args, setup, load_config
from emailrep import EmailRep

def main():
    action, args = parse_args()
    config = load_config()

    emailrep = EmailRep(config.get('emailrep', 'key'))
    try:
        if action == EmailRep.QUERY:
            result = emailrep.query(args.email)

            if result.get("status") and result["status"] == "fail":
                print("Failed: %s" % result["reason"])
                sys.exit()

            if args.format:
                if args.format == "json":
                    print(json.dumps(result, indent=4, sort_keys=True))
                else:
                    print("Format not supported")
            else:
                emailrep.format_query_output(result)

        elif action == EmailRep.REPORT:
            email = args.report
            tags = args.tags.split(",")

            if args.timestamp:
                try:
                    timestamp = parser.parse(args.timestamp)
                    timestamp = int(timestamp.timestamp())
                except Exception as e:
                    print("invalid timestamp: %s" % str(e))
                    sys.exit()
            else:
                timestamp = None

            result = emailrep.report(email, tags, args.description, timestamp, args.expires)
            if result.get("status") and result["status"] == "success":
                print("Successfully reported %s" % email)
            else:
                print("Failed to report %s. Reason: %s" % (email, result["reason"]))

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
