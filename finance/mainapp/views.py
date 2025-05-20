from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse,JsonResponse
from .forms import ContactForm
from .models import Contact,Boxes
import math
from django.views.generic import DetailView,UpdateView,DeleteView,ListView,CreateView
# Create your views here.
def homeView(request):
    context = {
    }
    return render(request, 'home.html', context)
def aboutView(request):
    context = {
    }
    return render(request, 'about.html', context)
def servicesView(request):
    context = {
        'Boxes' : Boxes.objects.all()
    }
    return render(request, 'services.html', context)
def calculatorView(request):
    context = {
    }
    return render(request, 'calculator.html', context)
def contactView(request):
    context = {
    }
    return render(request, 'contact.html', context)
def DisclaimerView(request):
    context = {
    }
    return render(request, 'disclaimer.html', context)
def PolicyView(request):
    context = {
    }
    return render(request, 'policy.html', context)
def TermView(request):
    context = {
    }
    return render(request, 'term.html', context)

class Contact(CreateView):
    model = Contact
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/'

def calculate_emi(request):
    emi = total_payment = total_interest = None
    if request.method == 'POST':
        principal = float(request.POST['principal'])
        rate = float(request.POST['rate'])
        tenure = int(request.POST['tenure'])

        monthly_rate = rate / 12 / 100
        months = tenure * 12

        emi = (principal * monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
        emi = round(emi, 2)
        total_payment = round(emi * months, 2)
        total_interest = round(total_payment - principal, 2)

    return render(request, 'loan_calx/loan_cal.html', {
        'emi': emi,
        'total_payment': total_payment,
        'total_interest': total_interest
    })

def calculate_extra_emi(request):
    result = {}
    if request.method == 'POST':
        principal = float(request.POST['principal'])
        annual_rate = float(request.POST['rate'])
        tenure_years = int(request.POST['tenure'])
        extra_payment = float(request.POST.get('extra', 0))

        monthly_rate = annual_rate / 12 / 100
        months = tenure_years * 12

        # Normal EMI
        emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
        total_payment = emi * months
        total_interest = total_payment - principal

        # With extra payments
        balance = principal
        new_months = 0
        new_total_interest = 0

        while balance > 0:
            interest = balance * monthly_rate
            principal_payment = emi + extra_payment - interest
            if principal_payment <= 0:
                break  # prevents infinite loop if payment is too low
            balance -= principal_payment
            new_total_interest += interest
            new_months += 1

        result = {
            'emi': round(emi, 2),
            'normal_months': months,
            'new_months': new_months,
            'months_saved': months - new_months,
            'interest_saved': round(total_interest - new_total_interest, 2),
            'total_interest': round(total_interest, 2),
            'new_interest': round(new_total_interest, 2),
        }

    return render(request, 'loan_calx/extra_cal.html', result)

def stamp_duty_calculator(request):
    context = {}
    if request.method == 'POST':
        property_value = float(request.POST['property_value'])
        location = request.POST['location']

        # Example rates (can be updated based on real location data)
        rates = {
            'Tamil Nadu': 7.0,
            'Karnataka': 5.0,
            'Maharashtra': 6.0,
            'Delhi': 4.0,
        }

        rate = rates.get(location, 7.0)  # default 7%
        stamp_duty = (property_value * rate) / 100

        context = {
            'property_value': property_value,
            'location': location,
            'rate': rate,
            'stamp_duty': round(stamp_duty, 2),
        }

    return render(request, 'loan_calx/stamp_cal.html', context)

def borrowing_calculator(request):
    context = {}
    if request.method == 'POST':
        income = float(request.POST['income'])
        expenses = float(request.POST['expenses'])
        interest_rate = float(request.POST['interest_rate'])
        tenure_years = int(request.POST['tenure'])

        net_income = income - expenses
        monthly_net_income = net_income * 0.6  # 60% used for EMI assumption

        r = (interest_rate / 12) / 100
        n = tenure_years * 12

        if r > 0:
            loan_amount = (monthly_net_income * ((1 + r) ** n - 1)) / (r * ((1 + r) ** n))
        else:
            loan_amount = monthly_net_income * n

        context = {
            'income': income,
            'expenses': expenses,
            'interest_rate': interest_rate,
            'tenure': tenure_years,
            'monthly_emi_afford': round(monthly_net_income, 2),
            'borrow_power': round(loan_amount, 2),
        }

    return render(request, 'loan_calx/borrow_cal.html', context)

def home_calculator(request):
    context = {}
    if request.method == 'POST':
        loan_amount = float(request.POST['loan_amount'])
        interest_rate = float(request.POST['interest_rate'])
        loan_term = int(request.POST['loan_term'])
        offset_amount = float(request.POST['offset_amount'])

        r = (interest_rate / 100)
        years = loan_term

        # Without offset
        total_interest_no_offset = loan_amount * r * years

        # With offset
        adjusted_loan = loan_amount - offset_amount
        total_interest_with_offset = adjusted_loan * r * years

        # Savings
        interest_saved = total_interest_no_offset - total_interest_with_offset

        context = {
            'loan_amount': loan_amount,
            'interest_rate': interest_rate,
            'loan_term': loan_term,
            'offset_amount': offset_amount,
            'interest_no_offset': round(total_interest_no_offset, 2),
            'interest_with_offset': round(total_interest_with_offset, 2),
            'interest_saved': round(interest_saved, 2),
        }

    return render(request, 'loan_calx/home_cal.html', context)


def lump_calculator(request):
    context = {}
    if request.method == 'POST':
        principal = float(request.POST['principal'])
        annual_rate = float(request.POST['rate'])
        tenure_years = int(request.POST['tenure'])
        lump_sum = float(request.POST['lump_sum'])
        lump_month = int(request.POST['lump_month'])

        monthly_rate = annual_rate / 12 / 100
        tenure_months = tenure_years * 12

        # EMI before lump sum
        emi = principal * monthly_rate * (1 + monthly_rate) ** tenure_months / ((1 + monthly_rate) ** tenure_months - 1)

        balance = principal
        total_interest = 0

        for month in range(1, tenure_months + 1):
            interest = balance * monthly_rate
            principal_payment = emi - interest
            balance -= principal_payment
            total_interest += interest

            if month == lump_month:
                balance -= lump_sum
                if balance < 0:
                    balance = 0

            if balance <= 0:
                tenure_months_actual = month
                break

        new_interest = total_interest
        interest_saved = (emi * tenure_years * 12) - (emi * tenure_months_actual + lump_sum)

        context = {
            'emi': round(emi, 2),
            'lump_sum': lump_sum,
            'lump_month': lump_month,
            'new_interest': round(new_interest, 2),
            'interest_saved': round(interest_saved, 2),
            'original_term': tenure_years * 12,
            'new_term': tenure_months_actual,
            'months_saved': tenure_years * 12 - tenure_months_actual,
        }

    return render(request, 'loan_calx/lump_cal.html', context)

def mort_calculator(request):
    context = {}
    if request.method == 'POST':
        principal = float(request.POST['principal'])
        annual_rate = float(request.POST['rate'])
        tenure_years = int(request.POST['tenure'])

        monthly_rate = annual_rate / 12 / 100
        tenure_months = tenure_years * 12

        # Interest-only monthly payment
        interest_only_payment = principal * monthly_rate

        # Normal EMI with principal and interest
        emi = principal * monthly_rate * (1 + monthly_rate) ** tenure_months / ((1 + monthly_rate) ** tenure_months - 1)
        total_interest = (emi * tenure_months) - principal

        context = {
            'principal': principal,
            'interest_only_payment': round(interest_only_payment, 2),
            'emi': round(emi, 2),
            'total_interest': round(total_interest, 2),
        }

    return render(request, 'loan_calx/mort_cal.html', context)

def saving_calculator(request):
    context = {}
    if request.method == 'POST':
        monthly_saving = float(request.POST['monthly_saving'])
        annual_rate = float(request.POST['rate'])
        years = int(request.POST['years'])

        months = years * 12
        monthly_rate = annual_rate / 12 / 100

        future_value = 0
        for i in range(months):
            future_value += monthly_saving * ((1 + monthly_rate) ** (months - i - 1))

        total_deposits = monthly_saving * months
        interest_earned = future_value - total_deposits

        context = {
            'monthly_saving': monthly_saving,
            'annual_rate': annual_rate,
            'years': years,
            'future_value': round(future_value, 2),
            'total_deposits': round(total_deposits, 2),
            'interest_earned': round(interest_earned, 2),
        }

    return render(request, 'loan_calx/saving_cal.html', context)

def goal_calculator(request):
    context = {}
    if request.method == 'POST':
        goal_amount = float(request.POST['goal'])
        annual_rate = float(request.POST['rate'])
        years = int(request.POST['years'])

        months = years * 12
        monthly_rate = annual_rate / 12 / 100

        # Formula to calculate monthly deposit:
        # P = FV * r / ((1 + r)^n - 1)
        if monthly_rate == 0:
            monthly_saving = goal_amount / months
        else:
            monthly_saving = goal_amount * monthly_rate / ((1 + monthly_rate) ** months - 1)

        total_deposit = monthly_saving * months
        interest_earned = goal_amount - total_deposit

        context = {
            'goal_amount': goal_amount,
            'annual_rate': annual_rate,
            'years': years,
            'monthly_saving': round(monthly_saving, 2),
            'total_deposit': round(total_deposit, 2),
            'interest_earned': round(interest_earned, 2),
        }

    return render(request, 'loan_calx/goal_cal.html', context)

def compound_calculator(request):
    context = {}
    if request.method == 'POST':
        principal = float(request.POST['principal'])
        rate = float(request.POST['rate'])
        years = float(request.POST['years'])
        frequency = int(request.POST['frequency'])

        # Compound Interest Formula: A = P * (1 + r/n)^(nt)
        amount = principal * (1 + (rate / 100) / frequency) ** (frequency * years)
        interest = amount - principal

        context = {
            'principal': principal,
            'rate': rate,
            'years': years,
            'frequency': frequency,
            'amount': round(amount, 2),
            'interest': round(interest, 2),
        }

    return render(request, 'loan_calx/compound_cal.html', context)

def rent_calculator(request):
    context = {}
    if request.method == 'POST':
        home_price = float(request.POST['home_price'])
        loan_years = int(request.POST['loan_years'])
        interest_rate = float(request.POST['interest_rate'])
        property_tax_rate = float(request.POST['property_tax_rate'])
        maintenance_cost = float(request.POST['maintenance_cost'])
        rent_per_month = float(request.POST['rent_per_month'])
        rent_increase_rate = float(request.POST['rent_increase_rate'])

        # Buy Calculations
        loan_term_months = loan_years * 12
        monthly_interest_rate = (interest_rate / 100) / 12
        emi = (home_price * monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) / ((1 + monthly_interest_rate) ** loan_term_months - 1)
        total_emi = emi * loan_term_months
        total_tax = (property_tax_rate / 100) * home_price * loan_years
        total_maintenance = maintenance_cost * loan_years
        total_buy_cost = total_emi + total_tax + total_maintenance

        # Rent Calculations
        total_rent = 0
        current_rent = rent_per_month
        for _ in range(loan_years):
            total_rent += current_rent * 12
            current_rent *= (1 + rent_increase_rate / 100)

        difference = abs(total_buy_cost - total_rent)
        context = {
            'emi': emi,
            'total_buy_cost': total_buy_cost,
            'total_rent': total_rent,
            'loan_years': loan_years,
            'difference': difference,
        }


    return render(request, 'loan_calx/rent_cal.html', context)

def income_calculator(request):
    tax_amount = 0
    regime = ''
    
    if request.method == 'POST':
        income = float(request.POST.get('income', 0))
        regime = request.POST.get('regime')

        if regime == 'old':
            slabs = [
                (250000, 0.0),
                (500000, 0.05),
                (1000000, 0.2),
                (float('inf'), 0.3),
            ]
        else:  # new regime
            slabs = [
                (300000, 0.0),
                (600000, 0.05),
                (900000, 0.1),
                (1200000, 0.15),
                (1500000, 0.2),
                (float('inf'), 0.3),
            ]

        last_limit = 0
        for limit, rate in slabs:
            if income > limit:
                tax_amount += (limit - last_limit) * rate
                last_limit = limit
            else:
                tax_amount += (income - last_limit) * rate
                break

    return render(request, 'loan_calx/income_cal.html', {
        'tax_amount': tax_amount,
        'regime': regime,
    })

def budget_calculator(request):
    total_income = 0
    total_expenses = 0
    balance = 0
    details = {}

    if request.method == 'POST':
        try:
            total_income = float(request.POST.get('income', 0))
            expenses = {
                'Housing': float(request.POST.get('housing', 0)),
                'Food': float(request.POST.get('food', 0)),
                'Transportation': float(request.POST.get('transportation', 0)),
                'Utilities': float(request.POST.get('utilities', 0)),
                'Entertainment': float(request.POST.get('entertainment', 0)),
                'Others': float(request.POST.get('others', 0)),
            }
            total_expenses = sum(expenses.values())
            balance = total_income - total_expenses
            details = expenses
        except ValueError:
            pass

    return render(request, 'loan_calx/budget_cal.html', {
        'income': total_income,
        'expenses': total_expenses,
        'balance': balance,
        'details': details
    })

def credit_calculator(request):
    result = None

    if request.method == 'POST':
        try:
            balance = float(request.POST.get('balance'))
            interest_rate = float(request.POST.get('interest_rate')) / 100
            monthly_payment = float(request.POST.get('monthly_payment'))

            monthly_interest = interest_rate / 12
            months = 0
            total_interest = 0
            original_balance = balance

            while balance > 0 and months < 1000:
                interest = balance * monthly_interest
                balance = balance + interest - monthly_payment
                total_interest += interest
                months += 1
                if balance < 0:
                    balance = 0

            if months >= 1000:
                message = "Your monthly payment is too low to ever repay the debt."
            else:
                message = f"You will pay off the balance in {months} months with a total interest of ₹{total_interest:.2f}."

            result = {
                'original_balance': original_balance,
                'interest_rate': interest_rate * 100,
                'monthly_payment': monthly_payment,
                'months': months,
                'total_interest': total_interest,
                'message': message,
            }
        except ValueError:
            result = {'error': 'Invalid input'}

    return render(request, 'loan_calx/credit_cal.html', {'result': result})

def intro_calculator(request):
    result = None

    if request.method == 'POST':
        try:
            principal = float(request.POST.get('principal'))
            intro_rate = float(request.POST.get('intro_rate')) / 100
            intro_period = int(request.POST.get('intro_period'))
            regular_rate = float(request.POST.get('regular_rate')) / 100
            total_years = int(request.POST.get('loan_term'))

            total_months = total_years * 12
            intro_months = intro_period * 12
            regular_months = total_months - intro_months

            # Monthly EMI for intro period
            intro_monthly_rate = intro_rate / 12
            regular_monthly_rate = regular_rate / 12

            if intro_monthly_rate > 0:
                intro_emi = principal * intro_monthly_rate * ((1 + intro_monthly_rate) ** total_months) / (((1 + intro_monthly_rate) ** total_months) - 1)
            else:
                intro_emi = principal / total_months

            # After intro period, recalculate EMI based on new balance
            balance_after_intro = principal
            for _ in range(intro_months):
                interest = balance_after_intro * intro_monthly_rate
                principal_paid = intro_emi - interest
                balance_after_intro -= principal_paid

            if regular_monthly_rate > 0:
                regular_emi = balance_after_intro * regular_monthly_rate * ((1 + regular_monthly_rate) ** regular_months) / (((1 + regular_monthly_rate) ** regular_months) - 1)
            else:
                regular_emi = balance_after_intro / regular_months

            total_payment = (intro_emi * intro_months) + (regular_emi * regular_months)
            total_interest = total_payment - principal

            result = {
                'principal': principal,
                'intro_emi': intro_emi,
                'regular_emi': regular_emi,
                'total_payment': total_payment,
                'total_interest': total_interest,
                'intro_period': intro_period,
                'loan_term': total_years
            }

        except Exception as e:
            result = {'error': f'Error in calculation: {str(e)}'}

    return render(request, 'loan_calx/intro_cal.html', {'result': result})

def fortnight_calculator(request):
    result = None

    if request.method == 'POST':
        try:
            principal = float(request.POST.get('principal'))
            annual_rate = float(request.POST.get('annual_rate')) / 100
            loan_term_years = int(request.POST.get('loan_term'))

            # Fortnightly details
            total_fortnights = loan_term_years * 26  # 26 fortnights per year
            fortnightly_rate = annual_rate / 26  # Fortnightly interest rate

            if fortnightly_rate > 0:
                repayment = principal * fortnightly_rate * ((1 + fortnightly_rate) ** total_fortnights) / (((1 + fortnightly_rate) ** total_fortnights) - 1)
            else:
                repayment = principal / total_fortnights

            total_payment = repayment * total_fortnights
            total_interest = total_payment - principal

            result = {
                'principal': principal,
                'repayment': repayment,
                'total_payment': total_payment,
                'total_interest': total_interest,
                'loan_term': loan_term_years
            }

        except Exception as e:
            result = {'error': f'Error: {str(e)}'}

    return render(request, 'loan_calx/fortnight_cal.html', {'result': result})

