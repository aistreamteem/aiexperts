# Payment-status export

**Pointer only. No passwords. Starter / guess until they teach.**

The payment-status export is their software dump of paid-through, last payment, autopay enrolled or failed, and NSF flags. You list codes as written. You never copy PAN, CVV, or full ACH numbers; if those columns exist, stop and ask for a stripped file. You do not retry a card and you do not send money. Late fees still come from the fee file, not this export alone. No processor login is stored here. Checks look for unit and status or paid_through when the workflow asks. This tool feeds the late-list pack.
