from django.shortcuts import render, redirect
from .models import RegisteredUser
from django.core.files.storage import FileSystemStorage


import matplotlib
matplotlib.use('Agg')

def register_view(request):
    msg = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        image = request.FILES.get('image')

        # Basic validation
        if not (name and email and mobile and password and image):
            msg = "All fields are required."
        else:
            # Save image manually
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            img_url = fs.url(filename)

            # Save user with is_active=False
            RegisteredUser.objects.create(
                name=name,
                email=email,
                mobile=mobile,
                password=password,
                image=filename,
                is_active=False
            )
            msg = "Registered successfully! Wait for admin approval."

    return render(request, 'register.html', {'msg': msg})

from django.utils import timezone

from django.utils import timezone
import pytz

def user_login(request):
    msg = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            user = RegisteredUser.objects.get(name=name, password=password)
            if user.is_active:
                # Convert current time to IST
                ist = pytz.timezone('Asia/Kolkata')
                local_time = timezone.now().astimezone(ist)

                # Save user info in session
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['user_image'] = user.image.url  # image URL
                request.session['login_time'] = local_time.strftime('%I:%M:%S %p')

                return redirect('user_homepage')
            else:
                msg = "Your account is not activated yet."
        except RegisteredUser.DoesNotExist:
            msg = "Invalid credentials."

    return render(request, 'user_login.html', {'msg': msg})

def admin_login(request):
    msg = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        if name == 'admin' and password == 'admin':
            request.session['is_admin'] = True   # ✅ ADD THIS
            request.session['user_name'] = 'Admin'  # optional
            return redirect('admin_home')
        else:
            msg = "Invalid admin credentials."

    return render(request, 'admin_login.html', {'msg': msg})

def admin_home(request):
    return render(request, 'admin_home.html')
    
def admin_dashboard(request):
    users = RegisteredUser.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users})

def activate_user(request, user_id):
    user = RegisteredUser.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('admin_dashboard')

def deactivate_user(request, user_id):
    user = RegisteredUser.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('admin_dashboard')

def delete_user(request, user_id):
    user = RegisteredUser.objects.get(id=user_id)
    user.delete()
    return redirect('admin_dashboard')



def home(request):
    return render(request, 'home.html')

def user_homepage(request):
    # ✅ Allow both user OR admin
    if 'user_id' not in request.session and not request.session.get('is_admin'):
        return redirect('user_login')

    user_name = request.session.get('user_name', 'Admin')
    user_image = request.session.get('user_image', '')  # admin may not have image
    login_time = request.session.get('login_time', '')

    context = {
        'user_name': user_name,
        'user_image': user_image,
        'login_time': login_time,
    }
    return render(request, 'users/user_homepage.html', context)

def user_logout(request):
    request.session.flush()  # Clears all session data
    return redirect('user_login')



import random
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import RegisteredUser

otp_storage = {}  # Temporary dictionary to store OTPs


def send_otp(email):
    otp = random.randint(100000, 999999)  # Generate 6 digit OTP
    otp_storage[email] = otp

    subject = "Password Reset OTP"
    message = f"Your OTP for password reset is: {otp}"
    from_email = "lakkulakshmidurga777@gmail.com"

    send_mail(subject, message, from_email, [email])

    return otp
from django.conf import settings

# def send_otp(email):
#     otp = random.randint(100000, 999999)  # Generate 6 digit OTP
#     otp_storage[email] = otp

#     subject = "Password Reset OTP"
#     message = f"Your OTP for password reset is: {otp}"
#     from_email = settings.EMAIL_HOST_USER  # Use configured email

#     send_mail(subject, message, from_email, [email], fail_silently=False)

#     return otp

   
import random
from django.core.mail import send_mail
from django.conf import settings

otp_storage = {}


def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        print("User email entered:", email)

        if RegisteredUser.objects.filter(email=email).exists():

            send_otp(email)

            request.session["reset_email"] = email

            return redirect("verify_otp")

        else:
            messages.error(request, "Email not registered!")

    return render(request, "forgot_password.html")


def verify_otp(request):
    if request.method == "POST":
        otp_entered = request.POST.get("otp")
        email = request.session.get("reset_email")

        if otp_storage.get(email) and str(otp_storage[email]) == otp_entered:
            return redirect("reset_password")
        else:
            messages.error(request, "Invalid OTP!")

    return render(request, "verify_otp.html")

def reset_password(request):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        email = request.session.get("reset_email")

        if RegisteredUser.objects.filter(email=email).exists():
            user = RegisteredUser.objects.get(email=email)
            user.password = new_password  # Updating password
            user.save()
            messages.success(request, "Password reset successful! Please log in.")
            return redirect("user_login")

    return render(request, "reset_password.html")

# Ml code
import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from django.shortcuts import render
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix
)
from xgboost import XGBClassifier
from .forms import PredictionForm

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'media', 'aluminum_casting_quality_balanced_dataset.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'media', 'models')
GRAPH_DIR = os.path.join(BASE_DIR, 'media', 'graphs')

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(GRAPH_DIR, exist_ok=True)

def train_models(request):
    df = pd.read_csv(DATA_PATH)
    X = df.drop("Quality_Label", axis=1)
    y = df["Quality_Label"]

    # Save correlation matrix plot
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR, "correlation_matrix.png"))
    plt.close()

    # Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, stratify=y, random_state=42)

    results = {}

    # SVM
    svm = SVC(kernel='rbf', probability=True, random_state=42)
    svm.fit(X_train, y_train)
    joblib.dump(svm, os.path.join(MODEL_DIR, "SVM_model.pkl"))
    y_pred_svm = svm.predict(X_test)
    y_prob_svm = svm.predict_proba(X_test)[:, 1]

    results['SVM'] = {
        "accuracy": round(accuracy_score(y_test, y_pred_svm), 4),
        "precision": round(precision_score(y_test, y_pred_svm), 4),
        "recall": round(recall_score(y_test, y_pred_svm), 4),
        "f1": round(f1_score(y_test, y_pred_svm), 4),
        "roc_auc": round(roc_auc_score(y_test, y_prob_svm), 4),
    }

    # Confusion matrix - SVM
    conf_svm = confusion_matrix(y_test, y_pred_svm)
    plt.figure(figsize=(5, 4))
    sns.heatmap(conf_svm, annot=True, fmt='d', cmap='Blues')
    plt.title("Confusion Matrix - SVM")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR, "confusion_matrix_SVM.png"))
    plt.close()

    # ROC Curve - SVM
    fpr_svm, tpr_svm, _ = roc_curve(y_test, y_prob_svm)
    plt.figure()
    plt.plot(fpr_svm, tpr_svm, label=f"SVM (AUC = {results['SVM']['roc_auc']})")
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve - SVM")
    plt.legend()
    plt.savefig(os.path.join(GRAPH_DIR, "roc_curve_SVM.png"))
    plt.close()

    # XGBoost
    xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    xgb.fit(X_train, y_train)
    joblib.dump(xgb, os.path.join(MODEL_DIR, "XGB_model.pkl"))
    y_pred_xgb = xgb.predict(X_test)
    y_prob_xgb = xgb.predict_proba(X_test)[:, 1]

    results['XGBoost'] = {
        "accuracy": round(accuracy_score(y_test, y_pred_xgb), 4),
        "precision": round(precision_score(y_test, y_pred_xgb), 4),
        "recall": round(recall_score(y_test, y_pred_xgb), 4),
        "f1": round(f1_score(y_test, y_pred_xgb), 4),
        "roc_auc": round(roc_auc_score(y_test, y_prob_xgb), 4),
    }

    # Confusion matrix - XGBoost
    conf_xgb = confusion_matrix(y_test, y_pred_xgb)
    plt.figure(figsize=(5, 4))
    sns.heatmap(conf_xgb, annot=True, fmt='d', cmap='Greens')
    plt.title("Confusion Matrix - XGBoost")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR, "confusion_matrix_XGB.png"))
    plt.close()

    # ROC Curve - XGBoost
    fpr_xgb, tpr_xgb, _ = roc_curve(y_test, y_prob_xgb)
    plt.figure()
    plt.plot(fpr_xgb, tpr_xgb, label=f"XGBoost (AUC = {results['XGBoost']['roc_auc']})", color='darkorange')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve - XGBoost")
    plt.legend()
    plt.savefig(os.path.join(GRAPH_DIR, "roc_curve_XGB.png"))
    plt.close()

    return render(request, "users/train_result.html", {
        "results": results,
        "roc_svm": "/media/graphs/roc_curve_SVM.png",
        "roc_xgb": "/media/graphs/roc_curve_XGB.png",
        "conf_svm": "/media/graphs/confusion_matrix_SVM.png",
        "conf_xgb": "/media/graphs/confusion_matrix_XGB.png",
        "corr_image": "/media/graphs/correlation_matrix.png"
    })
def predict_quality(request):
    if request.method == "POST":
        form = PredictionForm(request.POST)
        if form.is_valid():
            data = [form.cleaned_data[field] for field in form.fields]
            model = joblib.load(os.path.join(MODEL_DIR, "SVM_model.pkl"))
            scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
            scaled_data = scaler.transform([data])
            pred = model.predict(scaled_data)[0]
            prob = model.predict_proba(scaled_data)[0][1]
            return render(request, "users/predict_result.html", {"prediction": pred, "probability": round(prob, 4)})
    else:
        form = PredictionForm()
    return render(request, "users/predict_form.html", {"form": form})