# Facts — Operations (pre-seeded)


---

## 2026-11-08: Accounts payable
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/accounts-payable.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role accounts payable is the list of vendor bills not yet paid: who is owed, how much, and when. Accrual shops enter the bill when received. Cash shops may never put AP on the books and only code the bank when paid. The list exists so the owner can pay on purpose and so aging is not a pile of email. Next files are the AP aging export, the pay list, and the vendor-bills pack. They pay. You do not. Typical fields are vendor, bill date, due date, amount, account, status (open or paid), and bill number. Files are the software aging or a folder of unpaid PDFs. Cadence is weekly for a pay run, monthly for close. The bookkeeper enters and ages; the owner chooses what to pay. Shops vary. A cash shop with no AP register still has unpaid PDFs. List those as open bills for the owner, labeled not on the books if that is true. Ask whether they enter bills or only code the bank. A starter guess until they teach: enter bills if they already do; otherwise build a pay list from PDFs and label it. Common mistakes are paying from an estimate, entering every purchase order as AP, and coding a card charge as a bill and again as a card expense. Never invent a due date, never send payment, never invent terms, and never treat the pay list as filed with anyone.

---

## 2026-11-08: Accounts receivable
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/accounts-receivable.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role accounts receivable is unpaid customer invoices: who owes the shop, which invoice, and how old. It exists so collections, deposits, and the cash forecast are not guesswork. Next files are the AR aging export, cash-application questions, and the AR write-up. This Expert does not write off balances and does not email customers unless they asked and the list is theirs. Typical fields are customer, invoice number, invoice date, due date, original amount, open amount, and bucket. Files are the software export or a spreadsheet they keep. Cadence is weekly for collections, monthly for close. The bookkeeper ages and flags; the owner collects. Shops vary on aging by invoice date versus due date and on how payments apply (oldest open versus invoice number in the memo). Ask their cash-application rule. A starter guess until they teach: age with their export's buckets; do not apply a payment because the amount matches. Common mistakes are applying a payment to the wrong invoice, writing off to make aging pretty, and calling a credit in 90-plus uncollectible. Never invent a write-off, never decide bad-debt tax treatment, never store card numbers from a customer, and never threaten a customer as counsel.

---

## 2026-11-08: Accruals as optional
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/accruals-optional.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role an accrual is a month-end entry for a known cost or amount earned that is not yet on a bill or invoice: unpaid wages, unpaid commissions, or a vendor invoice that will arrive next month. It exists so an accrual-method profit and loss matches the period. Many small shops skip this. Next files are the close pack and any reversing journals they already use. Typical fields are date, account, amount, memo, and reverse date if they reverse next month. Files are a payroll cutoff note, a vendor email, or their close checklist. Cadence is month-end only if they use accruals. The bookkeeper drafts only after they say to; the CPA may require it at year end only. Shops vary. Cash shops usually do not accrue. Month-end "accrue then reverse" is a choice they or their CPA make. Ask. A starter guess until they teach: no accruals until their close list says so. Common mistakes are adding accruals to make a cash-basis profit and loss look like large-company books, accruing a guess with no vendor file, and leaving last month's accrual unreversed. Never invent amounts, never add surprise accruals, never present an accrual as a tax method change, and never hide a missing bill inside an accrual instead of asking.

---

## 2026-11-08: Aging buckets
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/aging-buckets.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role AR and AP aging is a snapshot of open invoices or bills grouped by age: current, 1–30, 31–60, 61–90, 90-plus. Some shops use invoice date, some due date. The buckets exist so the owner knows who to call and what to pay. Next files are the aged CSV and the AR or AP write-up. Typical fields are customer or vendor, document number, date used for aging, open amount, and bucket label. Files are the software aging export. Cadence is weekly or monthly. The bookkeeper produces the list; the owner acts. Shops vary on bucket labels and on whether they email statements. Ask. Credits sitting in 90-plus often mean a mis-applied payment. A starter guess until they teach: use their export's buckets and date basis. Common mistakes are calling 90-plus uncollectible, changing dates to move a row, and mixing invoice-date aging with due-date aging in one pack. Never write off, never invent buckets, never email customers unless they asked, and never treat aging as a legal demand.

---

## 2026-11-08: Balance-sheet families
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/assets-liabilities-equity.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role the balance-sheet families are assets (bank, receivables, inventory, prepaid, fixed assets), liabilities (payables, cards, loans, sales-tax payable, payroll liabilities), and equity (contributions, draws, retained earnings). Even a shop that only looks at a profit and loss has these under the hood. They exist so cash, debt, and owner activity are not dumped into income. Next files are the rec pack, loan split, and year-end trial balance. Typical fields are account name, family, and balance as of the period end. Files are a trial-balance or balance-sheet export. Cadence is monthly in a close, or whenever a new loan or account appears. The bookkeeper lists what the export shows; the owner confirms new accounts. Shops vary on which balance-sheet accounts they actually use. Many cash shops have little AR or AP on the books. Ask. A starter guess until they teach: bank, card liability, and owner equity at minimum; still wait for their chart. Common mistakes are creating a loan account for a named lender without their chart, calling a card a bank, and booking owner contributions as sales. Never invent loan or asset accounts for a named company, never decide depreciation, never give a solvency or legal opinion, and never treat a starter family list as their chart.

---

## 2026-11-08: Bank export
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/bank-feed.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role the bank export is the downloaded activity for one account and date range: a CSV, OFX, or QBO file, or a feed that already landed in their software. It exists so coding, the rec, and the "what is this line" list start from the bank's record, not from memory. Next files are the bank-flagged questions sheet and the reconcile pack. Typical fields are date, description or memo, amount (signed or separate debit and credit columns), and sometimes a running balance or check number. Column names vary by bank. Files are the download they provide. Cadence is weekly or at statement end. The bookkeeper reviews; they download. This Expert does not log in. Shops vary: operating, savings, payroll, and tax-reserve accounts are different files. Feeds can duplicate a manual entry. Ask which account and which date range before you treat a file as complete. A starter guess until they teach: one operating checking CSV for the period they named; still ask about other accounts. Common mistakes are treating "last 90 days" as a month, mixing two accounts in one sheet, and coding a transfer as income because the memo is vague. Never invent a payee from a processor name, never store a bank login or full account number, never originate a transfer, and never assume the feed replaced the statement for the rec.

---

## 2026-11-08: Bank fees and interest
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/bank-fees.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role the bank statement includes service charges, wire fees, NSF fees, and interest credited. Fees are expense. Interest earned is other income, not sales. The lines exist so the rec zeros and so small amounts are not "noise." Next files are the statement lines CSV and the rec pack. Typical fields are date, description, amount, and the expense or other-income account they use. Files are the statement PDF or CSV. Cadence is each statement. The bookkeeper codes; the bank charges. Shops vary on account names (Bank charges versus Office). Ask. A starter guess until they teach: fee lines to their bank-fee account if they have one, otherwise a labeled guess; interest to other income, not sales. Common mistakes are netting fees against sales, ignoring small fees so the rec does not zero, and coding interest as customer sales. Never invent a fee, never treat interest as taxable as an opinion, never call the bank as them, and never hide a rec difference inside "bank fees."

---

## 2026-11-08: Barter and trade-outs
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/barter-ask.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role some shops trade work for work: a plumber does a job for a web designer and no cash moves. Tax orientation often still treats barter as income. This role does not value the trade. If their file shows a trade, list both sides as they recorded them and ask. The topic exists so a silent trade is not missing from the questions list. Next files are their written trade note and a CPA question. Typical fields are date, what they gave, what they received, amounts only if they recorded them, and "ask CPA." Files are emails or invoices marked trade. Cadence is rare. The bookkeeper lists; they and their CPA value if required. Shops vary. Ask. A starter guess until they teach: do not invent a fair-market number. Common mistakes are inventing a market value, omitting the trade, and treating barter as nontaxable as an opinion. Never invent a fair-market number, never give a tax opinion, never record only one side, and never treat a starter value as theirs.

---

## 2026-11-08: Bill vs invoice
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/bill-vs-invoice.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role a bill is what the shop owes a vendor (accounts payable). An invoice is what a customer owes the shop (accounts receivable). The split exists so AP aging, the pay list, AR aging, and cash application do not land in the same pile. Next files are the vendor-bills pack, the AR questions pack, and the bank rec when payments clear. Typical fields on a bill are vendor, date, due date, amount, account or category, and bill number. Typical fields on an invoice are customer, date, due date, amount, items or a memo, and invoice number. Files are vendor PDFs, customer PDFs, and software exports. Cadence is daily or weekly as paper and email arrive. The bookkeeper enters; the owner approves payment and customer terms. Shops vary. Some owners say invoice for both. Some cash shops never enter bills and only code the bank when paid. Ask which words this shop uses and whether they enter AP at all. A starter guess until they teach: a PDF from a supplier is a bill; a PDF they send a customer is an invoice. Common mistakes are posting the same PDF as both a bill and an invoice, entering a customer estimate as an invoice, and paying from a quote. Do not post the same PDF as both unless their file shows a pass-through. Never invent a named customer's terms, never send payment, and never invent a tax treatment for a pass-through.

---

## 2026-11-08: Billable expenses
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/billable-expenses.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role a billable expense is a cost the shop paid (parts, permit, sub, travel) that they intend to put on a customer invoice. Software may mark a bill line billable. It exists so job cost and AR stay tied and so the owner does not forget to bill. Next files are the job-cost sheet, the customer invoice draft they asked for, and AP. Typical fields are job or customer, vendor, amount, billed-or-not, and the income or reimbursement item they use when billed. Files are the bill PDF and their invoice. Cadence is weekly as jobs run. The bookkeeper flags unbilled; they invoice. You do not send the customer invoice unless they said that is the job and the file is theirs. Shops vary. Some markup; some bill at cost. Ask their rule. Do not invent a markup. A starter guess until they teach: tag the cost to their job if they use jobs; leave markup as a question. Common mistakes are inventing a markup percent, forgetting to mark billed so it double-bills, and putting owner draws on a customer invoice. Never invent markup, never invent a job, never treat billable as a tax pass-through opinion, and never send an invoice from this folder unless they asked and the list is theirs.

---

## 2026-11-08: Repair vs improvement — ask
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/capital-vs-repair.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role a repair is routine fix-up they already expense; an improvement or restoration may be an asset. The line is a common CPA question. IRS Publication 535 is orientation, not a decision tree you apply as tax. This role lists the vendor, amount, and what the invoice describes. The distinction exists so a roof or a remodel does not silently sit in repairs. Next files are the invoice, the asset list, and a CPA question. Typical fields are date, vendor, amount, invoice description copied as written, and "ask CPA: capital vs repair." Files are the vendor PDF and photos if they have them. Cadence is when a large facilities or equipment invoice arrives, and at year-end review. The bookkeeper lists; the CPA decides tax treatment. Shops vary on dollar thresholds and on splitting a project across invoices. Ask. A starter guess until they teach: expense only if they already treat that vendor as repairs; otherwise list and ask. Common mistakes are deciding capital versus repair for tax, splitting a project across years to "help" them, and inventing a betterment test. Never decide for tax, never invent a split to change a year, never compute depreciation, and never treat Publication 535 as a filing position for this shop.

---

## 2026-11-08: Cash sales and undeposited cash
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/cash-on-hand.md
**Status:** active

**Starter / guess until they teach.**

On a typical US retail or cash-service role cash sales use a Z-tape or day sheet, a deposit, and a short or over. Books should explain the deposit. The trail exists so cash days are not skipped and so cash is not labeled owner just because it was cash. Next files are the day sheet, the deposit slip, and the bank rec. Typical fields are business date, Z-tape or day-sheet total, cash deposited, card batches, and short or over. Files are the POS close and the bank deposit. Cadence is daily close, weekly rec. The bookkeeper ties; a cashier or owner counts. Shops vary. Ask their day-close file. A starter guess until they teach: every cash day in their file needs a deposit story or a question. Common mistakes are income-coding a deposit as owner because it was cash, skipping cash days with no bank deposit, and parking unexplained cash in petty cash. Never invent a Z-tape, never take the deposit, never treat missing cash as a tax loss, and never store a safe code.

---

## 2026-11-08: Cash vs accrual
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/cash-vs-accrual.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role, cash versus accrual is the shop's books method: when income and expenses hit the registers, not a tax election this Expert may choose. Cash books record income when received and expenses when paid. Accrual books record income when earned and expenses when the bill is owed, even if unpaid. The method exists so the profit and loss, aging, bank rec, and year-end pack the owner hands their CPA tell one story. IRS Publication 334 orientation is that books should clearly show income and use the same method as the return. This Expert does not pick the method, say a change is allowed, or file anything. Typical files: a close-checklist note, the software company setting, or a CPA email. Cadence is always. The owner, bookkeeper, and CPA touch it; only they may change it. Shops vary. Mixed or modified-cash books are common. Inventory shops may treat purchases and sales differently from the rest of the P&L. Ask which this shop uses for the operating bank, cards, and any inventory. A starter guess until they teach: many small service shops run cash on the bank and still enter customer invoices. Do not assume that is this shop. Common mistakes: coding unpaid bills as expenses on cash books, or skipping receivables on accrual books because the customer has not paid. Never invent a method for a named company, never advise a method change as a tax position, and never treat a starter note as their filed return method.

---

## 2026-11-08: Chart of accounts
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/chart-of-accounts.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role the chart of accounts is the live list of income, cost of goods, operating expense, other income and expense, assets, liabilities, and equity names the software posts to. It exists so every coded bill, bank line, invoice, and journal lands in a bucket the owner and their CPA can read on a profit and loss or balance sheet. Next files are the coded bills pack, the trial balance, and the year-end handoff. Typical fields are account name, type or family, sometimes a number, and active or hidden. Files are a software export, PDF, or screenshot. Cadence is whenever they add a vendor type or the CPA asks for a new split. The bookkeeper proposes; the owner or CPA approves a new name. Shops vary. Software ships a generic list; shops rename, number, merge, and hide. Ask for this shop's export of the live chart. A starter sketch in this folder is only a guess until they teach. Never publish a numbered chart as if it already belonged to a named company. Common mistakes are merging two of their accounts because the labels look similar, inventing "Office expense" when they already use "Supplies," and posting owner draws to an expense family. Never invent a chart for a named company, never choose their numbering, never map books to Schedule C as a tax opinion, and never store a login to pull the list. Wait for their file.

---

## 2026-11-08: Check register and outstanding checks
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/check-register.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role the check register is handwritten or printed checks, plus voids, that may not look like a card swipe on the bank feed. The bank later shows the check number and amount. The register exists so outstanding checks can be listed on the rec and so a missing check is a question. Next files are the outstanding-checks list and the bank rec. Typical fields are check number, date, payee, amount, account, and cleared-or-outstanding. Files are a check-stub export, a written register photo, or the software check list. Cadence is whenever they write checks and at statement rec. The bookkeeper lists outstanding; they sign checks. You do not sign or mail. Shops vary. Many shops are ACH-only. Ask if they still write checks. A starter guess until they teach: if the statement shows check numbers, ask for the register; do not invent payees from amounts. Common mistakes are coding a cleared check as a new expense when the bill was already entered, leaving old outstanding checks forever, and treating a void as still outstanding. Never sign or mail a check, never invent a payee, never store a signature image, and never originate ACH because a check is late.

---

## 2026-11-08: Class, location, or department
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/class-or-location.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role class, location, or a tracking category is an extra tag on a line for stores, trucks, departments, or owners. QuickBooks and Xero style books use these so a profit and loss can split without a second company file. It exists only if they turned it on. Next files are coded bills and the class P&L they already run. Typical fields are the class or location name on each bill, invoice, or bank line they require. Files are their class list export. Cadence is every transaction if they require it, or only on some jobs. The bookkeeper tags from their list; they own the list. Shops vary. Many shops do not use classes. Ask if this shop requires a class on every line. A starter guess until they teach: leave class blank and ask if their export shows classes in use. Common mistakes are inventing a class list from a blog, guessing a location from a vendor city, and allocating a bill 50/50 across classes without their word. Never invent a class list, never treat a missing class as optional if they said it is required (ask instead), and never use class to hide a personal charge.

---

## 2026-11-08: Clearing and suspense
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/clearing-account.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role a clearing account holds in-transit money: processor, payroll, or money moving between their own accounts. Suspense or "ask my accountant" is a parking lot for lines nobody coded yet. Both should go toward zero. The accounts exist so in-transit cash is not dumped into income. Next files are the aged clearing list in the close pack and the matching bank or processor file. Typical fields are date, amount, source, age in days, and proposed match. Files are the account register export. Cadence is weekly if volume is high, monthly at close. The bookkeeper ages and matches; they explain leftovers. Shops vary on how old a leftover may sit. Ask their aging rule for leftover clearing. A starter guess until they teach: list anything still in clearing at period end as a question. Common mistakes are using suspense to hide a rec difference, income-coding clearing to zero it, and leaving payroll clearing to grow. Never hide a rec in suspense, never invent a match, never treat clearing as an owner draw without their word, and never store a login to "just clear it."

---

## 2026-11-08: Constructive receipt — ask, do not rule
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/constructive-receipt.md
**Status:** active

**Starter / guess until they teach.**

On a typical US cash-method role constructive receipt is the idea that income available without restriction can be income even if not deposited. IRS cash-method orientation includes that idea. This Expert does not rule on constructive receipt. If a check sat in a drawer over year-end, list the dates from their file and ask the CPA. The topic exists so you do not move income across years to "help." Next files are the undeposited checks list and a CPA question. Typical fields are check date, received date if they recorded it, deposit date, customer, and amount. Files are the check copy and the deposit. Cadence is year-end. The bookkeeper lists dates; the CPA rules. Shops vary. Ask. A starter guess until they teach: list drawer checks with dates; do not move them. Common mistakes are moving a December check to January to "help," income-coding a check they have not received, and treating undeposited funds as a tax election. Never rule on constructive receipt, never move income across years to help, never give a tax opinion, and never invent received dates.

---

## 2026-11-08: Contractor vs employee — ask only
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/contractor-vs-employee.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role people get paid either through payroll (employees) or as vendors (often contractors). The books follow how the shop already pays them. Worker classification is a legal and tax question. IRS pages on employee versus independent contractor are orientation only. This Expert does not decide status. The fact exists so 1099 tracking and payroll files stay in the right piles. Next files are the vendor-YTD sheet and the payroll register. Typical fields are payee label, how they are already paid (payroll versus vendor bill or check), and a note if unclear. Files are the payroll roster and the vendor list. Cadence is when a new payee appears and at year-end 1099 work. The bookkeeper lists; they or their CPA decide status. Shops vary. Ask how this shop already treats each payee. If unclear, list the payee and ask. A starter guess until they teach: follow the existing pile (payroll versus vendor); do not move anyone. Common mistakes are moving someone from payroll to 1099 to "save tax," inventing a contractor because they have no W-2, and putting a person in both piles. Never decide employee versus contractor, never give a tax-saving opinion, never file a W-2 or 1099, and never store a Social Security number.

---

## 2026-11-08: Business credit cards
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/credit-card-liability.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role a business credit card is a liability account, not a bank. Charges are expenses, job costs, or personal questions; the payment from the operating bank is a transfer that reduces the card, not a second expense. The card exists so the owner can float purchases and so the books can show what is still owed to the card issuer. Next files are the card-coding pack, the card rec, and the bank line for the payment. Typical fields are transaction date, payee, amount, category, statement ending date, statement ending balance, and payment date. Files are the statement PDF plus a CSV if they have it. Cadence is monthly per card, sometimes weekly. The bookkeeper codes and recs; they download. Ask every card they use, including store cards. Shops vary on personal charges (draw versus reimbursement versus "leave it"). Ask. A starter guess until they teach: code the statement period they named; treat the bank payment as a transfer; flag personal-looking lines as questions. Common mistakes are expensing the payment and the charges, treating the card as a checking account, and skipping store cards. Never invent a personal-versus-business call, never store a full card number, never pay the card, never log into the issuer, and never treat a starter "all business" guess as their policy.

---

## 2026-11-08: Customer deposits and retainers
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/customer-deposits.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role a customer deposit or retainer is money received before the work is done or before it is earned under their rule. Accrual books often sit it as a liability (unearned or customer deposit) and move it to income when earned. Cash shops may income it when received. The distinction exists so a busy deposit month is not fake sales. Next files are the invoice when they apply it and the AR or liability detail. Typical fields are date received, customer, amount, job if any, and the liability or income account they use. Files are the receipt, the estimate, and their rule. Cadence is when money arrives and when the invoice applies it. The bookkeeper asks; they decide earned. Shops vary. Ask this shop. A starter guess until they teach: do not call a deposit sales on accrual-looking books without their rule; list it as a question. Common mistakes are income-coding every deposit, spending-coding a deposit as the owner's, and applying a deposit to the wrong job. Never invent their earned rule, never give a constructive-receipt opinion, never move money, and never treat a retainer as a gift card unless they said so.

---

## 2026-11-08: Customer statements
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/customer-statements.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role a customer statement is a period list of open invoices, credits, and payments for one customer, used so the owner can collect. It is not a new invoice and not a legal demand this Expert issues as counsel. It exists so AR aging has a customer-facing attachment if they want one. Next files are the AR aged CSV and the statement export they produce from software. Typical fields are customer, statement date, invoice lines, credits, payments, and open total. Files are a software PDF or CSV export. Cadence is monthly or when they ask for a collections pack. The bookkeeper prepares the file; they send it. Shops vary on invoice-date versus due-date and on whether they send statements at all. Ask. A starter guess until they teach: produce a list from their AR export; do not email customers unless they asked and the list is theirs. Common mistakes are changing amounts to "help" the customer, adding late fees they did not teach, and treating the statement as a lawsuit. Never invent late fees, never email unless asked, never write off from a statement, and never store customer card numbers on the statement you write.

---

## 2026-11-08: Depreciation — ask, do not compute as tax
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/depreciation-ask.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role depreciation is the entry that expenses part of a fixed asset over time on the books. Book depreciation and tax depreciation (section 179, bonus) often differ. This role may list assets and ask the CPA for the entry. The fact exists so the close pack does not invent a pretty number. Next files are the asset list and a question in the year-end handoff. IRS Publication 946 is orientation for them and their CPA, not a worksheet you complete as tax. Typical fields you may list are asset, cost, date, and "depreciation entry: ask CPA." Files are the asset list and any prior-year entry they already posted. Cadence is year-end, sometimes monthly if they already have a book schedule. The bookkeeper asks; the CPA computes tax. Shops vary. Many small shops only book what the CPA sends after the return. Ask. A starter guess until they teach: no depreciation number until their CPA file or last-year entry is in the folder. Common mistakes are inventing a monthly amount so the P&L "looks right," mixing book and tax, and saying a write-off is allowed. Never compute tax depreciation, never say 179 or bonus is allowed, never invent a life, and never present a starter schedule as theirs.

---

## 2026-11-08: Double-entry sketch
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/double-entry.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role double-entry is how the software keeps score even when the owner never sees the words debit and credit: every bill, invoice, payment, and journal has a balancing side. It exists so the trial balance stays in balance and so a CSV import that lands only one side is caught before the CPA pack. Next files are the journal proposal (only if they allow it) and the trial-balance questions. Typical fields on a journal are date, accounts, debit amount, credit amount, memo, and period. Files are a journal CSV or a screenshot of a transaction. Cadence is as needed, plus month-end if they use standard journals. The bookkeeper proposes; they post in their software unless they asked you only to draft. Shops vary. Some shops allow proposed journals; others want bank lines coded only. Ask. A starter guess until they teach: code bank and bills; do not post a one-sided adjustment. Common mistakes are a one-sided "adjustment" to hide a mismatch, importing a register with no offset, and using miscellaneous expense as the silent other side. Never invent a balancing account to make a pack look clean, never give a tax opinion via a journal description, never plug a rec, and never store a software password to post it yourself.

---

## 2026-11-08: Estimates vs bills vs POs
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/estimates-vs-bills.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role an estimate or quote is not a bill. A purchase order is a commitment, not AP, until the vendor invoices. Accrual shops may accrue received-not-invoiced; many small shops do not. Customer estimates are not income. The distinction exists so AP and AR are real. Next files are the vendor invoice when it arrives and the customer invoice when they bill. Typical fields are document type (estimate, PO, bill, invoice), date, amount, and status. Files are PDFs in their quote or PO folder versus the bills folder. Cadence is as documents arrive. The bookkeeper enters bills and invoices; they issue POs and estimates. Shops vary. Ask. A starter guess until they teach: do not enter every PO as AP; do not income a customer estimate. Common mistakes are entering POs as bills, income-coding a customer estimate, and accruing received-not-invoiced without their rule. Never invent an accrual for unbilled POs, never treat an estimate as a contract opinion, never pay from a quote, and never file anything from an estimate.

---

## 2026-11-08: Fiscal year vs calendar
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/fiscal-year.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role the income-tax year is often the calendar year, but some shops use a fiscal year that ends in another month. Sales-tax years and payroll calendar years may differ from the income-tax year. The year-end date exists so YTD 1099 totals, close packs, and "this year versus last" mean the same thing. Next files are the close calendar and the 1099 tracker year they name. Typical fields are year-end month and day, and labels for sales-tax and payroll years if they differ. Files are a CPA email or the software company settings they export. Cadence is once, then confirmed before year-end work. The bookkeeper asks; they or the CPA set it. Shops vary. Do not assume December. Ask this shop's year-end before building a YTD 1099 or a close pack. A starter guess until they teach: calendar year until they say otherwise, labeled as a guess. Common mistakes are building 1099 YTD on a calendar year for a fiscal shop, mixing sales-tax quarters with the wrong income year, and closing "December" when they are fiscal. Never invent a year-end, never change their software year, never give a fiscal-year tax opinion, and never assume a starter calendar year is filed.

---

## 2026-11-08: Fixed assets and receipts for equipment
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/fixed-assets.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role a fixed-asset list is lasting equipment, vehicles, and build-outs: date placed, cost, vendor, and a short description. It exists so a truck is not lost in repairs expense and so the CPA has a list for depreciation. Next files are the receipt, the loan if any, and the depreciation ask. Whether a purchase is a repair expense or an asset is often a CPA call. Typical fields are asset label, date, cost, vendor, account they use, and notes. Files are a spreadsheet plus invoices. Cadence is when a large purchase arrives and at year-end. The bookkeeper lists; the CPA decides tax depreciation. Shops vary on a dollar threshold. Ask this shop's threshold if they have one. A starter guess until they teach: list the invoice and ask capital versus expense; do not invent a policy. Common mistakes are inventing a capitalization policy, inventing a useful life, and expensing a vehicle because the owner "wants the write-off." Never invent policy or life, never compute section 179 or bonus, never say a write-off is allowed, and never create asset accounts for a named company without their chart.

---

## 2026-11-08: 1099-K and processor reports
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/form1099-k-ask.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role processors and marketplaces issue Form 1099-K. Public thresholds have changed. Do not treat a blog number as this shop's rule. Typical books still need sales and fees from the processor report, not from the 1099-K alone. The form exists as a third-party report their CPA may ask about. Next files are the processor payout report and a question in the year-end pack. Typical fields are processor name, year, gross as the form or year-end report shows if they provided it, and fees from the payout file. Files are the 1099-K PDF they received plus payout CSVs. Cadence is year-end. The bookkeeper ties sales to processor reports; their CPA uses the form. Shops vary. Ask. A starter guess until they teach: do not double-count POS sales plus the 1099-K. Common mistakes are booking the 1099-K as extra income on top of already-recorded sales, using the form instead of monthly payouts, and quoting a threshold as law for this shop. Never invent a threshold as their rule, never file, never treat the form as the books, and never store a login to the processor.

---

## 2026-11-08: 1099 tracking as files
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/form1099-tracking.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role 1099 work is a year-end file: vendors, year-to-date service payments, whether a W-9 is on file, entity type as they recorded, and whether they think the payee is reportable. It exists so they or their CPA can file from a clean list, not from memory. Next files are the vendor-YTD CSV, the W-9 present-or-missing list, and the tracker write-up. Thresholds and form types change. Read the current IRS 1099-NEC and 1099-MISC instructions they care about. Do not quote a threshold as this shop's rule unless they taught it. Typical fields are payee label, YTD amount, W-9 path yes or no, form they think applies, and notes. No taxpayer ID numbers. Files are a spreadsheet they maintain or you build from their vendor payments. Cadence is quarterly for some shops, year-end for most. The bookkeeper tracks; they or their CPA file. Shops vary on who is exempt, who is product-only, and who uses a corporation. Ask. A starter guess until they teach: list service payees and W-9 gaps; leave reportable as a question. Common mistakes are pasting TINs into the sheet, treating a blog dollar amount as law for this shop, and e-filing from this folder. Never e-file, never decide who is exempt, never put TINs in docs/, never give a classification opinion, and never say forms are filed.

---

## 2026-11-08: Gift cards and stored value
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/gift-cards-ask.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role sold gift cards or stored value are often a liability until redeemed. Breakage and unused balances have tax and state unclaimed-property angles that are out of scope as an opinion. The topic exists only if they sell cards. Next files are their gift-card report and the liability account if they use one. Typical fields are sold date, amount, redeemed date, and outstanding if their POS tracks it. Files are a POS gift-card report. Cadence is monthly if they sell cards. The bookkeeper lists; they run the POS. Shops vary. Ask if this shop sells cards. If not, skip. If yes, ask their current method. A starter guess until they teach: do not invent breakage income. Common mistakes are income-coding sales of cards as if earned, inventing breakage, and ignoring unredeemed balances. Never invent breakage income, never give an unclaimed-property opinion, never invent a rate of unused cards, and never treat a blog method as theirs.

---

## 2026-11-08: Home office — ask, do not compute
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/home-office-ask.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role some sole proprietors track a home-office amount: a share of utilities or a square-footage note they already keep. The method and allowance are tax positions. This role may list utilities they already split. The topic exists so you do not compute a deduction. Next files are their utility bills and any existing split they taught. Typical fields are vendor, amount, and the split percent only if they gave it. Files are utility PDFs and their written split. Cadence is monthly bills or year-end. The bookkeeper lists; their CPA computes the deduction if any. Shops vary. Many LLCs and corporations do this differently or not at all. Ask. A starter guess until they teach: code the utility as they already do; do not compute a home-office deduction. Common mistakes are inventing a square-footage percentage, applying a simplified IRS method on the books, and treating rent as a corporation home office. Never compute a home-office deduction, never invent a percentage they did not give, never give a tax opinion, and never treat a starter split as filed.

---

## 2026-11-08: How this role files work items
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/how-we-file.md
**Status:** active

**Starter / guess until they teach.**

Day-to-day work does **not** go in one shared pile. Each **work item** gets its own folder under `work-items/<id>/` so Tuesday does not overwrite Monday, and one period does not mix with the next.

Typical name for *this* role (until they teach a different pattern):

- **What one folder is:** books period (and usually one account or one close pack)
- **How to name it:** `work-items/2026-08-operating-bank-rec/`
- **Pattern:** `work-items/YYYY-MM-account-or-pack/` or `work-items/WID-XXXXXXXX/`

Inside every item folder:

- `in/` — files they dropped for *this* item only
- `work/` — scratch while this item is in progress
- `out/` — the finished list or write-up for *this* item
- `evidence/` — check logs for this item only

Month-end is its own folder. A bank rec for operating is not mixed with the card rec. 1099 season is a year folder they name.

If they already file another way (their software’s id, a property code, a period name), **use their words**. Ask before starting if it is unclear which item this is. Never dump new files into yesterday’s folder. Never put two appointments, two tickets, or two periods in the same item folder unless they asked for a combined pack and named it that way (for example one day-list).

---

## 2026-11-08: Income vs COGS
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/income-vs-cogs.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role income is what customers were charged for the shop's work or goods (plus contra-revenue such as refunds). Cost of goods is the material, product, or subcontract cost that moves with a sale. The split exists so gross profit is readable and so the CPA is not handed a pile of "job stuff" mixed with rent. Next files are the coded-bills pack, job-cost sheet if they use one, and the P&L the owner reviews. Typical fields are account name, amount, customer or job if they tag it, and vendor. Files are invoices, bills, and the chart. Cadence is every sales and purchase batch. The bookkeeper codes; the owner says what is a job cost versus overhead. Shops vary. Job shops may use job costing instead of a formal cost-of-goods account. Retail may use inventory and a cost adjustment. Service shops may have no cost of goods. Ask this shop's split. A starter guess until they teach: customer invoices to income; vendor product or sub bills that they already treat as job cost to cost of goods; rent and owner draws elsewhere. Common mistakes are dumping all vendor bills into cost of goods because they "feel like jobs," putting owner draws in cost of goods, and netting refunds against a random expense. Never invent their cost-of-goods policy, never map to a tax form line as an opinion, and never recode their chart because a textbook used different names.

---

## 2026-11-08: Insurance and license bonds
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/insurance-and-bonds.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role insurance and license bonds are general liability, workers compensation, auto, and surety or license bonds. Auditable policies may true-up at year end. Premiums may be prepaid or financed monthly. The pile exists so a workers-comp deposit is not wages and so a finance-company draft is not a mystery expense. Next files are the invoice, the finance agreement if any, and prepaid if they use it. Typical fields are policy type, vendor or finance company, amount, coverage dates if on the bill, and account name. Files are binder or invoice PDFs and bank drafts. Cadence is when billed and at audit true-up. The bookkeeper codes; they bind coverage. Shops vary on finance companies (loan-like monthly payments) and on prepaid. Ask their account names. A starter guess until they teach: code to their insurance account; flag a workers-comp deposit as a question, not wages. Common mistakes are expensing a workers-comp deposit as wages, ignoring a year-end audit bill, and inventing a prepaid schedule. Never invent coverage, never file a claim, never treat premium as deductible as an opinion, and never pay the finance company.

---

## 2026-11-08: More than one entity
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/intercompany-ask.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role some owners run two LLCs or a corporation plus a side shop: one bank pays the other's bills, or one invoice is really the sister company. Clean books keep entities separate. Combined packs are labeled combined only if they asked. The topic exists so one P&L is not a blend by accident. Next files are each entity's bank export and a question list. Typical fields are entity name as they use it, bank last four they already wrote, payee, amount, and which books should hold it. Files are separate folders per entity if they have them. Cadence is whenever a mixed payment appears. The bookkeeper asks; they own entity structure. Shops vary. Ask. Do not invent an intercompany account name. A starter guess until they teach: one pack per entity; mixed payments are questions. Common mistakes are netting two companies on one P&L without a combined label, inventing due-to/due-from accounts, and treating a sister rent as owner draw without their word. Never invent intercompany accounts, never give an entity-tax opinion, never merge legal entities, and never move money between them.

---

## 2026-11-08: Inventory vs supplies
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/inventory-vs-supplies.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role inventory is goods held for sale or for jobs that will be billed; incidental shop supplies are often expensed when bought. The split exists so the balance sheet and cost of goods are not a junk drawer of rags and resale parts. Next files are their count sheet if they count, the parts-house statement, and the CPA's inventory questions. IRS Publication 334 discusses inventory and small-business exceptions. This Expert does not decide the tax method. Typical fields are item or a simple description, quantity if they count, unit cost if they store it, and the asset or expense account they use. Files are a count spreadsheet, a parts-house export, or "we expense everything" in their close notes. Cadence is year-end for many shops, monthly for some retailers. The bookkeeper lists; they count. Shops vary. Some expense everything. Some keep a perpetual parts list. Ask whether this shop counts stock, uses a parts house on account, or expenses everything. A starter guess until they teach: treat as supplies expense until their file shows an inventory asset. Common mistakes are inventing a count, inventing a unit cost, and building a fake inventory asset so the books "look accrual." Never invent quantities or costs, never choose a tax inventory method, never write off shrinkage as a tax opinion, and never create inventory accounts for a named company without their chart.

---

## 2026-11-08: Job costing (light)
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/job-costing-light.md
**Status:** active

**Starter / guess until they teach.**

On a typical US trade or remodel role job costing is a tag on the same books: bills, materials, and sometimes labor coded to a job number so the owner can see job profit. It is not a second set of books. It exists so the owner can decide what to bid next and so the close pack can show open-job cost. Next files are the job-cost sheet and the job write-up. Typical fields are job id as they already use it, customer, vendor, date, amount, category, and optionally hours if they track labor. Files are their job list, bills, and payroll or sub bills. Cadence is weekly as bills arrive and at job close. The bookkeeper tags; the owner owns the job list and any overhead rule. Shops vary. Owner time is often not costed. Overhead allocation may not exist. Ask their job list and whether labor is payroll, owner time, or sub bills. A starter guess until they teach: tag only when the bill already shows a job or they named it; leave untagged as a question. Common mistakes are inventing a job number, allocating overhead with a rate they did not give, and putting owner draws on a job as "labor." Never invent jobs, never invent an overhead rate, never treat job profit as a tax return, and never pay a sub from this folder.

---

## 2026-11-08: Loans and principal
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/loans-and-principal.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role a loan is a liability: truck, equipment, EIDL, line of credit, or a recorded note. Each payment usually splits interest (expense) and principal (reduces the loan). New proceeds are cash in and more liability, not sales. The split exists so the profit and loss is not overstated and so the loan does not sit forever at the original amount. Next files are the lender statement, the payment split worksheet, and the balance-sheet tie-out. Typical fields are payment date, total paid, interest, principal, fees if shown, and remaining balance as the lender states. Files are the amortization or monthly lender statement they provide. Cadence is each payment and at month-end for the rec of any loan account. The bookkeeper splits from their file; they get the statement. Shops vary on extra principal, interest-only periods, and whether a finance company for insurance is treated as a small loan. Ask. A starter guess until they teach: do not split until the lender file is in the folder; leave the full payment as a question. Common mistakes are expensing the full payment, booking proceeds as income, and guessing the split from a leftover liability. Never guess the split, never invent an interest rate, never give a debt-tax opinion, never contact the lender as them, and never pay the loan from this folder.

---

## 2026-11-08: Meals and entertainment — ask
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/meals-ask.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role meals sit in their own account because tax deductibility is often limited. The limit is a return issue, not a bookkeeper opinion. Entertainment is often separate or blocked. The account exists so the CPA can see the pile. Next files are the card-coding pack and receipts with who and why if they keep that. Typical fields are date, payee, amount, who attended if they wrote it, and the meals account name. Files are receipts and the card CSV. Cadence is monthly coding. The bookkeeper codes to meals if that is their account; the CPA applies any tax limit. Shops vary on whether meals are split from travel. Ask. A starter guess until they teach: use their meals account; do not apply a percentage write-down on the books "for the IRS." Common mistakes are applying a 50 percent write-down on the books, inventing per-diem amounts, and hiding owner personal meals in office. Never apply a tax percentage on the books, never invent per diem, never give a deductibility opinion, and never treat a starter "all meals 50 percent" as their books method.

---

## 2026-11-08: Processor fees and net deposits
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/merchant-fees.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role processor activity is Square, Stripe, PayPal, Clover, or a merchant account: customers pay, the processor takes fees, refunds, and chargebacks, and a net payout hits the bank. Books that only record the net deposit understate sales and miss fee expense, and they can miss sales tax on gross if the shop collects tax. The payout report exists so gross, fees, and net can be tied to the bank. Next files are the merchant-payout match and the sales-tax list if they collect. Typical fields are payout date, gross charges, refunds, fees, net, and payout id. Files are the processor payout CSV or PDF they export. Cadence is each payout and monthly. The bookkeeper ties net to the bank; they export. No dashboard login here. Shops vary. Some record gross sales plus fees; some live with net in income. Ask. Do not invent fee percentages. A starter guess until they teach: match net to bank and list fees as a question until they teach gross versus net. Common mistakes are coding the bank net as sales and stopping, double-counting POS sales plus the payout, and inventing a fee percent. Never invent fees, never file a 1099-K question as settled, never store processor passwords, and never treat a blog threshold as this shop's 1099-K rule.

---

## 2026-11-08: Mileage and vehicle logs
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/mileage-log.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role vehicle support is a mileage log or a written allowance policy: dates, miles, and business purpose, or odometer readings they already keep. It exists so vehicle costs on the books have a file behind them when the owner or CPA asks. Next files are the log export and the vehicle-cost questions. Cents-per-mile versus actual expenses is a tax method. Ask their CPA path. Do not pick. Typical fields are date, miles or start and end odometer, purpose as they wrote, and vehicle label. Files are a spreadsheet, app export, or paper scan. Cadence is monthly or at year-end. The bookkeeper lists what the log shows; they drive and write the log. Shops vary. Some use a flat reimbursement. Some put everything on a shop truck card and skip miles. Ask. A starter guess until they teach: list fuel and repairs from the card; do not invent miles. Common mistakes are inventing miles from a calendar, applying a standard mileage rate they did not teach as their book method, and putting a personal car loan on the business books. Never invent miles, never pick the tax method, never compute a deduction, and never store a driver's license number.

---

## 2026-11-08: Multi-state sales and payroll — ask
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/multi-state-ask.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role shops that sell or employ across states may have extra sales-tax and payroll files. This role lists where they already file. It does not register them in a state. The topic exists so a ship-to list is not treated as a nexus opinion. Next files are their invoice ship-to export only if they asked for that list, and their existing registration notes. Typical fields are state as already in their file, tax collected if marked, and "already file: yes/no/ask." Files are invoice exports and their CPA or tax-filer emails. Cadence is when they ask for a state list, or year-end. The bookkeeper lists from their file; they or their CPA register and file. Shops vary. Ask where they already file. A starter guess until they teach: do not invent economic-nexus math. Common mistakes are inventing nexus from a single invoice, registering them, and treating remote payroll as "just contractors." Never register them, never invent nexus math, never file a state return, and never give a multi-state tax opinion.

---

## 2026-11-08: Payment terms
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/net-terms.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role payment terms are the due-date rule printed on a vendor bill or a customer invoice: due on receipt, net 10, net 15, net 30, or an early-pay discount such as 2/10 net 30. Terms exist so aging buckets, the pay list, and cash-flow questions match what the paper actually says. Next files are AP and AR aging and the owner's "what do we pay this Friday" list. Typical fields are the terms label, invoice or bill date, due date, discount date if they use one, and discount amount if they take it. Files are the PDF header, the vendor or customer record in their software, and sometimes a rate card. Cadence is per document. The bookkeeper copies what is on the page; the owner decides whether to take a discount or pay late. Shops vary. Early-pay discounts and late fees are their policy, not a starter rule. Some shops ignore printed terms and pay on a fixed weekday. Ask this shop's rule and do not invent a named customer's terms. A starter guess until they teach: use the due date on the PDF, and flag if the software due date disagrees. Common mistakes are changing a due date to make aging look prettier, assuming everyone is net 30, and booking a discount they did not take. Never invent late-fee income, never decide they "should" take 2/10, and never treat a starter net-30 as this shop's contract.

---

## 2026-11-08: NSF, returned payments, chargebacks
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/nsf-and-chargebacks.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role a bounced customer check or returned ACH reverses the deposit and may add a bank fee. The invoice often reopens. A card chargeback is similar: the processor pulls money and the sale is disputed. These events exist so cash and AR stay honest. Next files are the bank line, the processor notice, and the AR questions pack. Typical fields are original payment date, return date, customer, amount, fee, and invoice number if known. Files are the bank statement, processor email, and the invoice. Cadence is when it happens and at month-end if AR looks odd. The bookkeeper flags and proposes the reverse; the owner collects again. Shops vary on whether they bill the NSF fee to the customer. Ask their steps. A starter guess until they teach: do not delete the original invoice; list the return as a question. Common mistakes are deleting the invoice to hide it, recoding a chargeback as a vendor bill, and expensing the whole sale. Never invent a fee billed to the customer, never decide the dispute as a lawyer, never write off without their word, and never treat a chargeback as cost of goods.

---

## 2026-11-08: Opening balances
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/opening-balance.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role opening balances are the start-date snapshot when books begin or convert: bank balances that match statements, plus AR, AP, loans, and opening equity someone already approved. They exist so the first month is not invented from a pile of old PDFs. Next files are the conversion trial balance and the first rec. Typical fields are account, amount, as-of date, and who approved. Files are the conversion workbook or CPA opening journal. Cadence is once at start, then only if they correct conversion. The bookkeeper ties banks to statements; they or the CPA own opening AR and AP. Shops vary. Do not invent opening AR. If the trial balance does not balance at conversion, ask. A starter guess until they teach: match bank statements at the start date; leave other openings as questions. Common mistakes are plugging to miscellaneous expense, inventing customer balances from memory, and changing opening equity to hide a miss. Never invent openings, never plug, never treat conversion as a filed return, and never create a named company's opening chart.

---

## 2026-11-08: Operating expense
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/operating-expense.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role operating expense is the overhead that keeps the shop running: rent, utilities, insurance, software, ads, office, professional fees, and repairs they already treat as expense. It exists so the profit and loss can show what it costs to operate apart from product or job cost and apart from owner draws. Next files are coded bills, card coding, and the close P&L questions. Typical fields are date, payee, amount, account name from their chart, class or location if they use it, and a receipt path. Files are bills, card lines, and the chart export. Cadence is weekly coding and monthly review. The bookkeeper proposes accounts; the owner corrects names. Shops vary on account names and on what they capitalize. Mapping to Schedule C lines is a CPA handoff, not this role's opinion. Ask their account names. A starter guess until they teach: use the closest name on their chart and label it a guess if you are not sure. Common mistakes are recoding a capitalized purchase as office expense because it is under a round number you invented, hiding owner personal charges in supplies, and creating new expense names instead of asking. Never invent a capitalization threshold, never apply a meals percentage "for the IRS," never give a deductibility opinion, and never pay a bill.

---

## 2026-11-08: Owner contributions
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/owner-contributions.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role an owner contribution is owner money into the operating account, or a transfer from a personal account they already treat as capital. It is equity, not sales. It exists so a large deposit is not booked as a miracle month of revenue. Next files are the bank-questions pack and the equity rollforward. Typical fields are date, amount, from-account if they said, and the equity account they use (Owner contribution, Capital, Member contribution). Files are the bank line and their word. Cadence is whenever a large unexplained deposit appears. The bookkeeper asks; the owner labels. Shops vary. Loan proceeds, customer deposits, and sales can look similar on a bank memo. Ask before coding a large unexplained deposit as income. A starter guess until they teach: large odd deposits are questions labeled contribution versus sales versus loan, not silent income. Common mistakes are coding "online transfer" as sales, mixing contributions with customer retainers, and treating a reimbursed personal expense as income. Never invent their entity's capital account name, never treat a contribution as taxable income as an opinion, never move money, and never assume a starter "must be capital" story is theirs.

---

## 2026-11-08: Owner draws
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/owner-draws.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role an owner draw is money the owner takes for personal use, or a personal charge on a business card that they treat as personal. It is an equity reduction (draw or distribution), not an operating expense and not cost of goods. It exists so the profit and loss stays about the shop and the balance sheet shows what the owner took. Next files are the bank or card coding pack, the equity rollforward, and the CPA's year-end questions about basis and distributions. This Expert does not compute basis or say a distribution is allowed. Typical fields are date, amount, the equity account they use, and a memo. Files are the bank line, card line, or check image. Cadence is whenever cash leaves for the owner. The bookkeeper codes; the owner confirms what was personal. Shops vary. Entity types use different equity labels. S-corp owner wages, if they run payroll, are a different file. Do not recode a draw as wages. Ask how this shop labels owner cash, personal card charges, and year-end distributions. A starter guess until they teach: personal-looking charges are questions, not silent draws. Common mistakes are dumping draws into meals, auto, or cost of goods to "make the P&L look right," and treating a distribution as wages without their payroll file. Never invent their entity type, never give a tax opinion on reasonable compensation, never pay the owner, and never store account passwords.

---

## 2026-11-08: Payroll as a file, not a filing
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/payroll-as-file.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role payroll arrives as a register file from a service or in-house software: gross wages, taxes withheld, employer taxes, net pay, and the cash leaving the bank. This role lists what the file shows and codes the bank drafts to match. It exists so wages and liabilities hit the right accounts and so the CPA has a trail. Next files are the payroll-export match and the payroll-liability tie-out. This role does not file 941 or 940, does not set up employees, and does not say wages are reasonable for an S corporation. Typical fields are pay period, pay date, gross, employee taxes, employer taxes, net, and the bank draft amounts and dates. Files are PDF or CSV from Gusto, ADP, QuickBooks Payroll, or similar. Cadence is each pay run and quarterly if they ask for a liability check. The bookkeeper codes; the service or they remit. Shops vary on liability account names and on whether contractor payments sit in the same service. Ask who runs payroll and which liability accounts they use. A starter guess until they teach: code the bank to the register totals; leave new liability names as questions. Common mistakes are expensing only net pay, ignoring employer tax drafts, and recoding a draw as wages. Never file a payroll form, never store employee Social Security numbers, never give a reasonable-compensation opinion, never decide worker status, and never log into the payroll product.

---

## 2026-11-08: Payroll liabilities as a file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/payroll-liability-file.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role payroll liabilities are federal and state withholding and employer taxes sitting in liability accounts until the payroll service or the shop remits. This role compares the register, the bank drafts, and the liability balances. It exists so leftover liabilities are questions, not silent expense. Next files are the register, the draft list, and a liability tie-out. It does not say a 941 is correct or filed. Typical fields are liability name, period, register amount, draft amount and date, and remaining balance. Files are the payroll export and the bank CSV. Cadence is each pay run and each remittance. The bookkeeper compares; they or the service remit. Shops vary on who remits and on what schedule. Ask. A starter guess until they teach: match drafts to the register; leftover balance is a question. Common mistakes are expensing remittances a second time, ignoring a leftover that grows, and saying a 941 is filed because a draft left the bank. Never file 941 or 940, never store employee SSNs, never give a deposit-schedule opinion, and never log into EFTPS or the service.

---

## 2026-11-08: Period and close
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/period.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role the books period is the slice of time a pack covers: usually a calendar month, sometimes a week for AP, sometimes a 4-4-5 or fiscal month. It exists so coded bills, bank recs, aging, and close notes can be compared to the same statement and the same profit and loss. Next files are every work CSV for that pack and the month-end write-up. Typical fields are period start, period end, and a label (March 2026, week ending date). Files are the close calendar they keep or a one-line instruction. Cadence is the close itself. The bookkeeper asks first; the owner or CPA sets lock dates. Shops vary. Some code AP weekly and close books monthly. Some use a fiscal year that is not December. Ask the period before coding a batch. Ask what locked means here: a software close date versus a CPA review. A starter guess until they teach: one calendar month matching the bank statement dates they handed you. Common mistakes are mixing two months in one work file, using a rolling 90-day bank download as "the month," and editing a locked period to hide a miss. Never invent their fiscal year, never unlock their software, never treat a starter calendar month as their year-end, and never call a period closed if they did not accept the rec.

---

## 2026-11-08: Personal vs business
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/personal-vs-business.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role personal versus business is the daily mess of a personal charge on the shop card, or a shop deposit into a personal account. SBA-style orientation is that a dedicated business account reduces mix-ups. Real shops still mix. The ask exists so draws and contributions are labeled and so the P&L is not a household register. Next files are the card-coding pack and the bank-questions list. Typical fields are date, payee, amount, and their label (business, draw, contribution, ask). Files are the card or bank line and their word. Cadence is every coding batch. The bookkeeper asks; the owner labels. Do not lecture. Shops vary. Ask; code draws or contributions when they say so. A starter guess until they teach: mixed-looking lines are questions, not silent office supplies. Common mistakes are hiding personal in supplies, treating a mixed account as fully business income, and scolding the owner in the write-up. Never invent the label, never treat a mixed account as all sales, never give a commingling legal opinion, never pay personal bills, and never store personal account passwords.

---

## 2026-11-08: Petty cash and cash on hand
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/petty-cash.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role petty cash is a small box or envelope with a log and occasional replenish from the operating account. A retail till or cash drawer is a different count tied to the day's sales. The account exists so small cash spends have a home and so unidentified cash is not parked there. Next files are the petty-cash log and the replenish check or withdrawal. Typical fields are date, amount, payee or purpose, and remaining cash if they count. Files are a log sheet and receipts. Cadence is when the box is low, or daily for a till. The bookkeeper recs the log if they use one; a cashier or owner handles cash. Shops vary. Many shops use no cash. Ask whether this shop uses cash at all. A starter guess until they teach: do not create a petty-cash account to park unidentified cash. Common mistakes are using petty cash as a suspense dump, income-coding a cash deposit as owner because it was cash, and skipping till shorts. Short or over goes to their account if they have one. Never invent a till count, never take or replenish cash, never store a safe combination, and never treat missing cash as a tax deduction.

---

## 2026-11-08: Prepaid and deposits paid
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/prepaid.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role a prepaid is a payment that covers future months (insurance, software, rent paid ahead) sitting on the balance sheet until it is expensed. A deposit paid to a landlord or vendor may sit as an asset until applied. It exists so a large cash outlay does not smash one month's profit and loss unless that is how they already book. Next files are their prepaid schedule and the month-end journals they already use. Typical fields are vendor, payment date, coverage start and end if on the invoice, monthly amount if they amortize, and the asset and expense accounts they named. Files are the invoice plus their schedule. Cadence is when the invoice arrives and then monthly if they amortize. The bookkeeper follows their schedule; the CPA may set the method. Shops vary. Cash shops often expense when paid and never use prepaid. Accrual shops may. Ask whether this shop uses prepaid at all. A starter guess until they teach: expense when paid unless their file already has a prepaid schedule. Common mistakes are inventing a twelve-month amortization for a modest annual app, forgetting to expense the last month, and calling a refundable deposit an expense. Never invent an amortization schedule, never treat prepaid as a tax election, never guess a useful life, and never build prepaid to make a cash-basis P&L look like a textbook.

---

## 2026-11-08: Source documents
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/receipts.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role source documents are the papers and files that back a books line: vendor PDFs, bank and card CSVs, processor payouts, payroll registers, and photos of paper receipts. They exist because IRS recordkeeping orientation is that supporting documents back the books, and because the owner and CPA will ask "what was this?" months later. Next files are the receipt-match pack, coded bills, and the close questions list. Typical index fields are date, vendor as printed, amount, tax if shown, last four of a card if already printed, and filename. Files live in a drop folder they name, email, or a capture-app export. Cadence is daily drop and weekly match. The bookkeeper matches; the owner supplies missing photos. Shops vary on what is "enough" support under a dollar threshold and where files land. Ask where this shop drops files and what they treat as enough for a small line. A starter guess until they teach: card lines they care about want a file; still ask before treating a chat recap as the source. Common mistakes are coding from memory, keeping only a chat summary, and photographing a full card number. IRS Publication 583 is orientation only. Never invent an amount or vendor when the file is missing, never store passwords, never copy a full card number into docs/, and never say a missing receipt is "fine for the IRS" as a tax opinion.

---

## 2026-11-08: Bank reconcile
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/reconcile.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role a bank or card reconcile is the proof that the statement ending balance and date match the books for that account, with outstanding checks and deposits-in-transit listed. It exists so the month-end pack and the CPA handoff can say the cash line is explained, not hoped. Next files are the outstanding-items CSV, the rec write-up, and the close status sheet. Typical fields are statement ending date, statement ending balance, book balance, outstanding checks, deposits in transit, and the difference. Files are the statement PDF they provided plus the worksheet. Cadence is monthly per account, sometimes weekly for a high-volume operating account. The bookkeeper prepares; the owner or CPA confirms matched. Vendor help pages for QuickBooks Online and Xero treat a zero difference as the software finish line. This shop must say what matched means here. Shops vary on cutoff for old uncleared items and whether they rec cards the same way as banks. Ask. A starter guess until they teach: one account, one statement period, difference left open if it is not zero. Common mistakes are plugging miscellaneous income or expense to force a zero, clearing old checks without asking, and calling the month closed while the rec is open. Never invent outstanding items, never force a plug journal, never log into their bank, and never say the rec is "IRS approved."

---

## 2026-11-08: How long files are kept — ask
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/record-retention.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role record retention is how long they keep bank statements, receipts, payroll files, and filed-return copies. IRS orientation pages describe general periods, often measured from when the return is filed, and longer holds for some items; employment-tax records are often kept longer. This is not legal advice and not a retention policy for this shop. The topic exists so you do not delete source PDFs. Next files are their existing archive location and a question if they ask you to purge. Typical fields you may note are file type, where they keep it, and what they already said they keep. Files are their drive or boxes. Cadence is rare; usually only when someone wants to throw things out. The bookkeeper keeps work files; they own retention. Shops vary. Ask what they already keep and where. A starter guess until they teach: do not delete source PDFs. Common mistakes are deleting because a blog said three years, pasting TINs into a "permanent" sheet, and treating IRS orientation as this shop's policy. Never delete their sources, never invent a retention policy as law, never give legal advice, and never say a year is "safe to shred."

---

## 2026-11-08: Recurring and memorized bills
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/recurring-bills.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role recurring or memorized bills are rent, software, loan payments, and retainers that look the same each period. Shops store them as memorized transactions, standing bills, or a checklist. They exist so monthly overhead is not re-invented from a blank page and so a missed rent shows up when the bank line has no match. Next files are the vendor-bills pack, the card or bank coding, and the close "expected but missing" list. Typical fields are vendor, usual amount, usual account, cadence (monthly on the first, weekly), and last date entered. Files are their memorized-bill export, a rent ledger, or a simple recurring list they keep. Cadence is each period before close. The bookkeeper proposes the list from last month; they confirm changes. Shops vary. Some enter a true AP bill each month; cash shops only code the bank. Amounts change (rent bumps, annual price changes). Ask this shop's list and whether a missing expected bill is a question. A starter guess until they teach: copy last period's recurring names as questions, not as posted amounts. Common mistakes are posting this month from last month's amount without looking at the new invoice, entering a memorized bill and also coding the bank as expense, and inventing a lease. Never invent rent or a lease term, never pay, never treat a starter recurring list as their contract, and never store a landlord portal login.

---

## 2026-11-08: Refunds and credit memos
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/refunds-and-credits.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role a credit memo reduces what a customer owes. A refund check or card credit reduces cash and either applies that credit or hits a contra-revenue account. Vendor credits work the other way on AP. The trail exists so returns do not disappear into supplies. Next files are the credit memo, the bank or processor line, and AR or AP aging. Typical fields are date, customer or vendor, original invoice or bill, credit amount, and whether cash was refunded. Files are the credit PDF and the processor or bank line. Cadence is when returns happen. The bookkeeper applies; the owner approves refunds. You do not send money. Shops vary. Some enter a negative invoice; some require credit memos. Ask their path. A starter guess until they teach: do not enter a negative invoice if their file shows credit memos. Common mistakes are expensing a customer refund as supplies, leaving credits unapplied in 90-plus aging, and refunding in the books without their payment. Never invent a credit, never pay a refund, never decide restocking as a legal term, and never treat a refund as a tax-free event as an opinion.

---

## 2026-11-08: Employee and owner reimbursements
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/reimbursements.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role a reimbursement is an employee or owner out-of-pocket spend that the shop will repay: an expense report with receipts, then an AP bill or a bank transfer. Owner out-of-pocket may be contribution plus expense or a draw reversal. Ask. The trail exists so the same lunch is not on the card and on a report. Next files are the expense report, receipts, and the pay list. You never pay. Typical fields are person, date, amount, account, receipt path, and paid-or-open. Files are the report PDF or sheet plus receipts. Cadence is whenever reports arrive. The bookkeeper codes; they pay. Shops vary. Ask owner treatment. A starter guess until they teach: employee reports become AP if they enter bills; do not expense a reimbursement that is already on the card. Common mistakes are double-counting card plus report, paying from this folder, and treating owner out-of-pocket as wages. Never pay, never invent a report, never store a full card image, and never treat a reimbursement as a tax-free plan opinion.

---

## 2026-11-08: Retainage (if they bill it)
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/retainage-ask.md
**Status:** active

**Starter / guess until they teach.**

On a typical US construction-adjacent role retainage is a portion of a billed job held until the job ends. Accrual shops may keep retainage receivable separate from current AR. Many small shops ignore the word and just have an unpaid invoice. The topic exists only if they bill it. Next files are the AIA-style invoice if they use one and the AR aging. Typical fields are job, invoice, retainage amount, and release date if they store one. Files are their invoice template and job list. Cadence is each progress bill and at job close. The bookkeeper lists what the invoice shows; they negotiate retainage. Shops vary. Ask. Do not invent retainage accounting for a shop that never used the word. A starter guess until they teach: if their invoice shows retainage, list it and ask how they book it; otherwise skip. Common mistakes are inventing a retainage receivable, income-coding unreleased retainage as if collected, and writing it off. Never invent the accounting, never give a contract-law opinion, never file a lien, and never treat retainage as a tax deferral opinion.

---

## 2026-11-08: Sales tax payable on the books
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/sales-tax-payable.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role sales-tax payable is the liability for tax collected (or accrued) until they remit. Typical accrual: tax on invoices increases the liability; the remittance reduces it. The account exists so the balance is explainable from the period's taxable sales, not a random leftover. Next files are their sales-tax report and the remittance bank line. You do not file the return. Typical fields are period, tax collected as their report shows, remittance date and amount, and remaining liability. Files are the software sales-tax report or their sheet plus the bank draft. Cadence is each filing period they already use. The bookkeeper ties; they or their CPA file. Shops vary on cash versus accrual for the liability and on marketplace-collected tax. Ask their report. A starter guess until they teach: list collected and remitted from their files; leftover after they say they paid is a question, not a write-off to income. Common mistakes are writing off leftover to income, inventing a remittance, and treating marketplace tax as theirs when their file says the platform remitted. Never invent a rate, never say a return is filed, never remit, and never give a nexus opinion.

---

## 2026-11-08: Sales tax — ask, do not invent
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/sales-tax.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role sales tax is the money invoiced or collected on taxable sales, plus the liability and remittance, as this shop already tracks it on a sheet or in software. It is state and local. It exists so the owner can see what was collected and what they still owe, and so their CPA or sales-tax filer has a list. Next files are the sales-tax questions pack and the payable tie-out. This Expert does not file a return. Typical fields are invoice date, customer or channel, taxable amount as they marked, tax collected, and jurisdiction only if their file already has it. Files are invoice or POS exports and their working sheet. Cadence follows their filing period, which you ask and never invent. The bookkeeper lists; they or their CPA file. Shops vary on nexus, item taxability, marketplace facilitator rules, and rates. Streamlined Sales Tax orientation does not give you a rate for this shop. Ask their nexus list, item taxability, and who files. A starter guess until they teach: list tax collected as marked on their invoices; leave rate and nexus as questions. Common mistakes are inventing a rate from a city name, treating marketplace payouts as if the shop collected tax, and writing off a leftover liability. Never invent a rate or nexus, never say a return is filed, never pick a jurisdiction because a customer address looks local, and never give a tax opinion.

---

## 2026-11-08: Sources (orientation only)
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/sources.md
**Status:** active

Public pages used to shape typical practice. Not copied. Not *this* shop.

- [IRS Publication 334, Tax Guide for Small Business (orientation)](https://www.irs.gov/publications/p334)
- [IRS Publication 583, Starting a Business and Keeping Records](https://www.irs.gov/publications/p583)
- [IRS Publication 535, Business Expenses (orientation)](https://www.irs.gov/publications/p535)
- [IRS recordkeeping overview for small businesses](https://www.irs.gov/businesses/small-businesses-self-employed/recordkeeping)
- [IRS: How long should I keep records?](https://www.irs.gov/businesses/small-businesses-self-employed/how-long-should-i-keep-records)
- [IRS Instructions for Forms 1099-MISC and 1099-NEC](https://www.irs.gov/instructions/i1099mec)
- [IRS Instructions for the Requester of Form W-9](https://www.irs.gov/instructions/iw9)
- [IRS About Form W-9](https://www.irs.gov/forms-pubs/about-form-w-9)
- [IRS independent contractor vs employee (orientation)](https://www.irs.gov/businesses/small-businesses-self-employed/independent-contractor-self-employed-or-employee)
- [IRS About Schedule C (Form 1040)](https://www.irs.gov/forms-pubs/about-schedule-c-form-1040)
- [SBA: Manage your finances](https://www.sba.gov/business-guide/manage-your-business/manage-your-finances)
- [QuickBooks Online: fix issues at the end of a reconciliation (vendor help)](https://quickbooks.intuit.com/learn-support/en-us/help-article/statement-reconciliation/fix-issues-end-reconciliation-quickbooks-online/L3mZimyAb_US_en_US)
- [Xero: What is bank reconciliation? (vendor glossary)](https://www.xero.com/us/glossary/bank-reconciliation/)
- [Streamlined Sales Tax Governing Board (orientation; rates are ask-not-invent)](https://www.streamlinedsalestax.org/)
- [IRS About Form 1099-K](https://www.irs.gov/businesses/understanding-your-form-1099-k)
- [IRS Publication 946, How to Depreciate Property (orientation)](https://www.irs.gov/publications/p946)

---

## 2026-11-08: Subscriptions and SaaS
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/subscriptions.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role software and SaaS charges hit the card or bank every month, or once a year. Monthly software usually hits expense. Annual prepay may be prepaid or expense-when-paid. Personal or family subscriptions on the business card are an ask (draw versus business). The list exists so recurring charges are coded the same way each month. Next files are the card-coding pack and their software list if they keep one. Typical fields are vendor, amount, cadence, account name, and personal-or-business question if unclear. Files are the card CSV and invoices in email. Cadence is monthly coding. The bookkeeper codes; the owner cancels or confirms personal. Shops vary. Ask this shop's software list and prepaid habit. A starter guess until they teach: monthly to software expense on their chart; annual small amounts expense-when-paid unless they already prepaid; personal-looking names as questions. Common mistakes are inventing a prepaid schedule for a small app, hiding a personal streaming charge in office, and creating a new account per app. Never invent prepaid, never log into the app, never cancel or buy software, and never treat a subscription as deductible as a tax opinion.

---

## 2026-11-08: This is a starter
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/THIS-IS-A-STARTER.md
**Status:** active

These facts, rules, and tools are **typical for this kind of role in many US small and mid-size shops**, summarized from public professional practice. They are still not how *your* shop works.

Until you correct them, treat them as guesses. After you correct the Expert, it must save *your* version (remember) and use that next time.

Run **define-role** (or correct `MyRole.txt`) so the title, tools, and “must never” match this business.

---

## 2026-11-08: Transfers are not income
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/transfers-not-income.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role a transfer is money moving between the shop's own accounts: operating to savings, a card payment from checking, or an owner contribution they already labeled. It is not sales. Bank descriptions like "transfer" or "online banking" still need their word. The distinction exists so income is not inflated before tax time. Next files are the bank-questions pack and both accounts' recs. Typical fields are date, amount, from account, to account, and their label (transfer, contribution, card payment). Files are both bank or card exports. Cadence is every coding batch. The bookkeeper matches both sides; they confirm odd memos. Shops vary. Ask. A starter guess until they teach: same-amount out of one shop account and into another is a transfer question, not sales. Common mistakes are coding transfers as sales, missing one side so cash is double-counted, and treating an owner contribution as a customer deposit. Never invent the other side, never move the money, never treat a transfer as taxable sales as an opinion, and never store full account numbers.

---

## 2026-11-08: Unapplied customer payments
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/unapplied-payments.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role an unapplied payment is customer money sitting on AR without an invoice, or a leftover credit after a short pay. Software often shows it as a credit on aging. It exists so cash application stays honest and so deposits are not income twice. Next files are the AR aging, the undeposited-funds match, and the AR questions pack. Typical fields are customer, payment date, amount, method, and invoices they said it applies to if any. Files are the AR open-credits export and the bank or processor line. Cadence is weekly cash application and month-end. The bookkeeper proposes application; they confirm odd leftovers. Shops vary on oldest-open versus invoice number in the memo. Ask their rule. A starter guess until they teach: do not apply a payment just because the amount matches an invoice. Common mistakes are applying to the wrong invoice, writing off a leftover, and income-coding an unapplied payment a second time when it deposits. Never write off, never invent the invoice, never email the customer unless they asked, and never store card numbers from the payment.

---

## 2026-11-08: Undeposited funds / payments to deposit
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/undeposited-funds.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role undeposited funds (or payments to deposit) is the holding account for checks and card batches that are recorded as received but not yet matched to a bank deposit. Software defaults often land here. It exists so a Tuesday deposit that includes three invoices plus card batches can match one bank line. Next files are the deposit worksheet and the bank rec. Typical fields are payment date, customer or batch id, amount, and deposit date when matched. Files are the undeposited-funds detail export and the bank deposit line. Cadence is every deposit day and at month-end if a leftover remains. The bookkeeper matches batches; they make the physical or processor deposit. Shops vary on whether they use this account or deposit each payment straight to the bank account in software. Ask this shop's batch process. A starter guess until they teach: leftover balance is a question, not a plug. Common mistakes are recording the invoice payment and the bank deposit as two income events, leaving old batches uncleared, and clearing leftover with an income plug. Never invent a batch, never log into the processor, never treat undeposited funds as petty cash, and never force the account to zero without their word.

---

## 2026-11-08: Vehicle costs
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/vehicle-ask.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role vehicle costs are fuel, repairs, insurance, and loan payments on a shop truck or car they already treat as business. Loan principal is not fuel. Mixed personal use is an ask. The pile exists so auto is not mixed with owner draws and so the loan split stays correct. Next files are the card coding, the loan statement, and the mileage log if they keep one. Typical fields are date, payee, amount, vehicle label if they have more than one, and personal-use question if mixed. Files are card lines, fuel receipts, and the loan file. Cadence is monthly. The bookkeeper codes; they assign vehicles. Shops vary. Do not apply a standard mileage rate unless they taught that as their book method. A starter guess until they teach: code fuel and repairs to their auto accounts; leave mixed use and mileage method as questions. Common mistakes are putting a personal car loan on the business balance sheet without their word, expensing loan principal as fuel, and applying a cents-per-mile rate they did not teach. Never invent personal-use percent, never pick the tax method, never compute a deduction, and never store a VIN in a public write-up unless their file already uses it as a label.

---

## 2026-11-08: Vendor credits
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/vendor-credits.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role a vendor credit is money the supplier owes the shop: a return, a pricing error, or a rebate sitting on AP as a credit memo, not as a random negative bill if they use credit memos. It exists so returns reduce what they pay and so aging is not a mystery credit in 90-plus. Next files are the AP aging, the pay list (net of credits), and the vendor-bills pack. Typical fields are vendor, credit date, original bill if any, amount, and whether it is applied or still open. Files are the credit PDF and the AP export. Cadence is when credits arrive and at each pay run. The bookkeeper applies if that is their job; the owner decides which open bill to net. Shops vary. Some take credits as a check; some only net on the next payment. Ask. A starter guess until they teach: list open credits on the pay list and ask before applying. Common mistakes are expensing a vendor credit as income, leaving credits unapplied, and entering a negative bill when they use credit memos. Never invent a credit, never take a rebate as owner cash, never treat a credit as taxable income as an opinion, and never pay a net amount from this folder.

---

## 2026-11-08: Voids, duplicates, and reversed entries
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/voids-and-duplicates.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role voids and reverses happen because a bank feed plus a manual bill created two of the same spend, or someone entered the same PDF twice. Typical fix is void or reverse with a trail, not a silent delete after the period was reviewed. The trail exists so the CPA can see what changed. Next files are the duplicate-flag list and the close questions. Typical fields are transaction dates, vendor, amount, source (feed versus manual), and proposed action (void, reverse, ask). Files are the register export. Cadence is during coding and at rec. The bookkeeper flags; they approve a void in a closed period. Shops vary on closed-period rules. Ask. A starter guess until they teach: flag possible duplicates (same vendor, date, amount) instead of deleting. Common mistakes are deleting both sides and hoping, "fixing" a prior month already sent to the CPA, and voiding a customer invoice that was already paid. Never silently delete after review, never invent which one is real without their file, never edit a locked month without asking, and never hide a duplicate inside miscellaneous.

---

## 2026-11-08: W-9 on file
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/w9-on-file.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role a W-9 is the vendor's taxpayer-ID form collected before paying a new service vendor. This role only notes path-to-file and missing or present. IRS requester instructions exist for electronic W-9s and TIN matching. Those are orientation. The note exists so the 1099 tracker is honest and so missing forms are a question list, not a surprise in January. Next files are the W-9 status CSV and the tracker pack. Typical fields are payee label, received date if they store it, file path or "missing," and who asked the vendor. Files are PDFs in a folder they name, not in docs/ as recopied IDs. Cadence is at vendor setup and at year-end gap review. The bookkeeper flags; they collect. Shops vary on where PDFs live (email, a drive, software attachments). Ask. Backup withholding is a tax decision. Flag missing W-9; do not withhold. A starter guess until they teach: present or missing only; no IDs in the write-up. Common mistakes are transcribing Social Security numbers or EINs into chats and CSVs, storing a signed W-9 in a public write-up, and deciding backup withholding. Never copy SSN or EIN into docs/ or work CSVs, never withhold, never file, and never treat a missing W-9 as "they are exempt."

---

## 2026-11-08: Write-offs and allowances
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/write-off-ask.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role writing off accounts receivable is an owner or CPA decision with a date and a reason in their file. Cash-basis shops may have little AR to write off. An allowance for doubtful accounts is even less common on small books. The rule exists so aging is not "cleaned" for looks. Next files are their written instruction and a journal only if they already use one. Typical fields are customer, invoice, amount, date they authorized, and reason as they wrote. Files are an email or a close-checklist tick. Cadence is rare, often year-end. The bookkeeper does not write off; they list and ask. Shops vary. Do not write off to make aging pretty. A starter guess until they teach: 90-plus is a question list, not a write-off. Common mistakes are dumping write-offs into miscellaneous expense, writing off a credit balance, and treating a write-off as a tax bad-debt opinion. Never write off without their word, never invent an allowance, never decide tax deductibility, and never threaten the customer.

---

## 2026-11-08: Year-end handoff to their CPA
**Scope:** expert-role
**Workflows:** all
**Captured:** 2026-11-08
**Source:** seeds/bookkeeping/docs/facts/year-end-handoff.md
**Status:** active

**Starter / guess until they teach.**

On a typical US role the year-end handoff is a prepared-by-client pack: trial balance, bank recs, AP and AR, loan statements, payroll reports, 1099 tracker, sales-tax filings they already made, and open questions. This role assembles files. It does not sign the return or say books are audit ready. The pack exists so their CPA can work. Next files are out/ year-end notes and the work CSVs the checks can see. Typical fields are a checklist of files attached, period, and labeled questions. Files are exports they provide plus your write-up. Cadence is once after the last month of their year, plus follow-up. The bookkeeper assembles; their CPA files. Shops vary. Ask their CPA's list. A starter guess until they teach: gather recs, aging, payroll, 1099 tracker, and questions; do not hide questions in a clean-looking P&L. Common mistakes are presenting a clean P&L with silent plugs, saying the books are audit ready, and filing anything. Never sign a return, never claim CPA status, never invent missing statements, never say filed, and never hide questions.

---
