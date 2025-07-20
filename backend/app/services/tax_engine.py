"""
Tax calculation engine with basic tax rules.
In production, this would integrate with IRS tax tables and complex rules.
"""
from typing import Dict, Any


def calculate_tax(income: float, deductions: float = 0, filing_status: str = "single") -> Dict[str, Any]:
    """
    Simplified tax calculation based on 2023 tax brackets.
    """
    # Standard deduction for 2023
    standard_deductions = {
        "single": 13850,
        "married_filing_jointly": 27700,
        "married_filing_separately": 13850,
        "head_of_household": 20800
    }

    # Tax brackets for 2023 (single filers)
    tax_brackets = [
        (10275, 0.10),
        (41775, 0.12),
        (89450, 0.22),
        (190750, 0.24),
        (364200, 0.32),
        (462550, 0.35),
        (float('inf'), 0.37)
    ]

    # Use standard deduction if higher than itemized
    standard_ded = standard_deductions.get(filing_status, 13850)
    total_deductions = max(deductions, standard_ded)

    # Calculate taxable income
    taxable_income = max(income - total_deductions, 0)

    # Calculate tax using brackets
    tax_owed = 0
    previous_bracket = 0

    for bracket_limit, rate in tax_brackets:
        if taxable_income <= previous_bracket:
            break

        taxable_in_bracket = min(taxable_income, bracket_limit) - previous_bracket
        tax_owed += taxable_in_bracket * rate
        previous_bracket = bracket_limit

        if taxable_income <= bracket_limit:
            break

    # Calculate effective tax rate
    effective_rate = (tax_owed / income * 100) if income > 0 else 0
    marginal_rate = next((rate * 100 for limit, rate in tax_brackets if taxable_income <= limit), 37)

    return {
        "gross_income": income,
        "total_deductions": total_deductions,
        "taxable_income": taxable_income,
        "tax_owed": round(tax_owed, 2),
        "effective_tax_rate": round(effective_rate, 2),
        "marginal_tax_rate": marginal_rate,
        "filing_status": filing_status
    }


def calculate_quarterly_payments(annual_tax: float) -> Dict[str, float]:
    """Calculate quarterly estimated tax payments"""
    quarterly_amount = annual_tax / 4
    return {
        "quarterly_payment": round(quarterly_amount, 2),
        "q1_due": "April 15",
        "q2_due": "June 15", 
        "q3_due": "September 15",
        "q4_due": "January 15"
    }


def validate_tax_form_data(form_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and clean tax form data"""
    errors = []
    warnings = []

    # Basic validation
    if not form_data.get("income") or form_data["income"] <= 0:
        errors.append("Income must be greater than 0")

    if form_data.get("deductions", 0) < 0:
        errors.append("Deductions cannot be negative")

    # Warnings for common issues
    if form_data.get("income", 0) > 1000000:
        warnings.append("High income detected - consider additional tax planning")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }