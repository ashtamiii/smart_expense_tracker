from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
import csv
from django.http import HttpResponse


#  Smart Category Prediction
def predict_category(description):
    description = description.lower()

    keywords = {
        'food': ['pizza', 'burger', 'coffee', 'restaurant'],
        'travel': ['uber', 'bus', 'train', 'taxi'],
        'shopping': ['amazon', 'flipkart', 'clothes'],
        'entertainment': ['movie', 'netflix', 'game']
    }

    for category, words in keywords.items():
        for word in words:
            if word in description:
                return category

    return 'others'


#  Home page - show all expenses
def home(request):
    expenses = Expense.objects.filter(user=request.user)

    # Prepare data for chart
    category_data = {}

    for expense in expenses:
        if expense.category in category_data:
            category_data[expense.category] += expense.amount
        else:
            category_data[expense.category] = expense.amount

    labels = list(category_data.keys())
    values = list(category_data.values())

    return render(request, 'expenses/home.html', {
        'expenses': expenses,
        'labels': labels,
        'values': values
    })


#  Add expense
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.category = predict_category(expense.description)  # ⭐ smart logic
            expense.save()
            return redirect('home')
    else:
        form = ExpenseForm()

    return render(request, 'expenses/add_expense.html', {'form': form})


#  Delete expense
def delete_expense(request, id):
    expense = Expense.objects.get(id=id)
    expense.delete()
    return redirect('home')


#  Edit expense
def edit_expense(request, id):
    expense = Expense.objects.get(id=id)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            updated_expense = form.save(commit=False)
            updated_expense.category = predict_category(updated_expense.description)  # ⭐ smart logic again
            updated_expense.save()
            return redirect('home')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'expenses/edit_expense.html', {'form': form})

def download_csv(request):
    expenses = Expense.objects.filter(user=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)
    writer.writerow(['Description', 'Category', 'Amount', 'Date'])

    for expense in expenses:
        writer.writerow([
            expense.description,
            expense.category,
            expense.amount,
            expense.date
        ])

    return response