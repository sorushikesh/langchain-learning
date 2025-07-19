from langchain.tools import Tool


def calculate_sip(monthly_investment, annual_rate, years):
    r = annual_rate / 100 / 12
    n = years * 12
    amount = monthly_investment * (((1 + r) ** n - 1) * (1 + r)) / r
    return f"The estimated SIP return is ₹{round(amount, 2)}"


def calculate_emi(principal, rate, tenure_years):
    r = rate / 100 / 12
    n = tenure_years * 12
    emi = principal * r * ((1 + r) ** n) / ((1 + r) ** n - 1)
    return f"The EMI is ₹{round(emi, 2)} per month"


def convert_usd_to_inr(usd_amount):
    rate = 83.2
    return f"${usd_amount} ≈ ₹{round(float(usd_amount) * rate, 2)} at {rate} INR/USD"


tools = [
    Tool(
        name="SIPCalculator",
        func=lambda q: calculate_sip(*map(float, q.strip().split())),
        description="Calculate SIP returns. Input format: monthly_investment rate years (e.g., '5000 12 10')"
    ),
    Tool(
        name="EMICalculator",
        func=lambda q: calculate_emi(*map(float, q.strip().split())),
        description="Calculate EMI. Input: principal rate years (e.g., '1000000 7.5 15')"
    ),
    Tool(
        name="CurrencyConverter",
        func=lambda q: convert_usd_to_inr(q.strip()),
        description="Convert USD to INR. Input: USD amount (e.g., '2500')"
    )
]
