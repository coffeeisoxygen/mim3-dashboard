"""User-facing messages and text for MIM3 Dashboard.

Centralized location for all UI text, error messages, and labels.
Future: Database-driven i18n support for multiple languages.
"""

from __future__ import annotations

from typing import Final

# =============================================================================
# 🚨 ERROR MESSAGES
# =============================================================================

# Authentication errors
ERROR_SESSION_EXPIRED: Final[str] = "🔒 Session expired. Please log in again."
ERROR_ACCESS_DENIED: Final[str] = (
    "❌ Anda tidak memiliki akses administrator untuk halaman ini."
)
ERROR_ACCOUNT_INACTIVE: Final[str] = "🚫 Account tidak aktif. Hubungi administrator."
ERROR_PAGE_NOT_FOUND: Final[str] = "❌ Halaman tidak ditemukan."

# Login errors
ERROR_INVALID_CREDENTIALS: Final[str] = "❌ Username atau password salah"
ERROR_ACCOUNT_LOCKED: Final[str] = "🔒 Account terkunci. Coba lagi nanti"
ERROR_LOGIN_REQUIRED: Final[str] = (
    "🔒 Silakan login terlebih dahulu untuk mengakses halaman ini."
)

# Form validation errors
ERROR_REQUIRED_FIELDS: Final[str] = "❌ Please fill in all required fields"
ERROR_PASSWORD_TOO_SHORT: Final[str] = (
    "❌ Password must be at least {min_length} characters long"
)
ERROR_PASSWORDS_DONT_MATCH: Final[str] = "❌ New passwords don't match"
ERROR_SAME_PASSWORD: Final[str] = (
    "⚠️ New password must be different from current password"
)

# Data operation errors
ERROR_USER_EXISTS: Final[str] = (
    "❌ Failed to create user. Username or email may already exist."
)
ERROR_USER_NOT_FOUND: Final[str] = "❌ User not found"
ERROR_OPERATION_FAILED: Final[str] = "❌ Operation failed. Please try again."

# =============================================================================
# ✅ SUCCESS MESSAGES
# =============================================================================

# Authentication success
SUCCESS_LOGIN: Final[str] = "✅ Login successful!"
SUCCESS_LOGOUT: Final[str] = "👋 Logged out successfully"
SUCCESS_PASSWORD_CHANGED: Final[str] = "✅ Password updated successfully!"

# User management success
SUCCESS_USER_CREATED: Final[str] = "✅ User '{username}' created successfully!"
SUCCESS_USER_ACTIVATED: Final[str] = "✅ User {username} activated"
SUCCESS_USER_DEACTIVATED: Final[str] = "✅ User {username} deactivated"
SUCCESS_PASSWORD_RESET: Final[str] = "✅ Password reset for {username}"

# =============================================================================
# ℹ️ INFO MESSAGES
# =============================================================================

# General info
INFO_PLEASE_LOGIN: Final[str] = "ℹ️ Please use your new password for future logins"
INFO_CONTACT_ADMIN: Final[str] = (
    "Contact your system administrator if you need additional help or account changes."
)
INFO_COMING_SOON: Final[str] = "Coming soon"

# Development placeholders
INFO_FEATURE_DISABLED: Final[str] = "This feature is currently disabled"
INFO_UNDER_DEVELOPMENT: Final[str] = "Feature under development"

# =============================================================================
# 🏷️ UI LABELS
# =============================================================================

# Navigation labels
LABEL_DASHBOARD: Final[str] = "Dashboard"
LABEL_PROFILE: Final[str] = "Profile"
LABEL_LOGIN: Final[str] = "Log in"
LABEL_LOGOUT: Final[str] = "Log out"
LABEL_USER_MANAGEMENT: Final[str] = "User Management"
LABEL_SYSTEM_SETTINGS: Final[str] = "System Settings"
LABEL_HPP_CALCULATOR: Final[str] = "HPP Calculator"

# Form labels
LABEL_USERNAME: Final[str] = "Username"
LABEL_PASSWORD: Final[str] = "Password"
LABEL_EMAIL: Final[str] = "Email"
LABEL_FULL_NAME: Final[str] = "Full Name"
LABEL_CURRENT_PASSWORD: Final[str] = "Current Password"
LABEL_NEW_PASSWORD: Final[str] = "New Password"
LABEL_CONFIRM_PASSWORD: Final[str] = "Confirm New Password"

# Button labels
BUTTON_LOGIN: Final[str] = "🚀 Login"
BUTTON_UPDATE_PASSWORD: Final[str] = "🔄 Update Password"
BUTTON_CREATE_USER: Final[str] = "✨ Create User"
BUTTON_RESET_PASSWORD: Final[str] = "🔄 Reset Password"
BUTTON_ACTIVATE: Final[str] = "✅ Activate"
BUTTON_DEACTIVATE: Final[str] = "❌ Deactivate"
BUTTON_CANCEL: Final[str] = "❌ Cancel"

# Status labels
STATUS_ACTIVE: Final[str] = "Active"
STATUS_INACTIVE: Final[str] = "Inactive"
STATUS_ADMIN: Final[str] = "Administrator"
STATUS_USER: Final[str] = "Regular User"

# =============================================================================
# 📊 DASHBOARD MESSAGES
# =============================================================================

# Welcome messages
WELCOME_ADMIN: Final[str] = "🔐 **Admin View** - Full system access"
WELCOME_USER: Final[str] = "👤 **User View** - Standard access"

# Metric labels
METRIC_TOTAL_SALES: Final[str] = "Total Sales"
METRIC_ACTIVE_TERRITORIES: Final[str] = "Active Territories"
METRIC_MONTHLY_GROWTH: Final[str] = "Monthly Growth"
METRIC_ACTIVE_USERS: Final[str] = "Active Users"

# Section headers
HEADER_KEY_METRICS: Final[str] = "📈 Key Metrics"
HEADER_QUICK_ACTIONS: Final[str] = "📋 Quick Actions"
HEADER_ACCOUNT_INFO: Final[str] = "📋 Account Information"
HEADER_PASSWORD_MANAGEMENT: Final[str] = "🔐 Change Password"
HEADER_USER_OVERVIEW: Final[str] = "📊 User Overview"

# =============================================================================
# 🔧 ADMIN INTERFACE MESSAGES
# =============================================================================

# Admin warnings
WARNING_ADMIN_PRIVILEGES: Final[str] = (
    "⚠️ Administrator accounts have full system access"
)
WARNING_DESTRUCTIVE_OPERATION: Final[str] = (
    "⚠️ This operation cannot be undone. Proceed with extreme caution."
)
WARNING_DANGER_ZONE: Final[str] = "**⚠️ Destructive Operations**"

# Admin help text
HELP_PASSWORD_REQUIREMENTS: Final[str] = """**Password Requirements:**
- Minimum {min_length} characters
- Must be different from current password
- Cannot be empty"""

HELP_CONTACT_SUPPORT: Final[str] = "**Contact Support:**"
HELP_SECURITY_TIPS: Final[str] = """**Security Tips:**
- Change your password regularly
- Don't share your login credentials
- Log out when finished"""

# =============================================================================
# 🌐 FUTURE I18N PREPARATION
# =============================================================================

# Language codes (Future: Database-driven)
LANG_ID: Final[str] = "id_ID"  # Indonesian
LANG_EN: Final[str] = "en_US"  # English

# Currency and formatting (Future: Admin-configurable)
CURRENCY_SYMBOL: Final[str] = "Rp"
DATE_FORMAT: Final[str] = "DD/MM/YYYY"
NUMBER_FORMAT: Final[str] = "id_ID"
