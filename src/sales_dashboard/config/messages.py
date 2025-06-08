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

# System errors
ERROR_APP_INITIALIZATION: Final[str] = (
    "❌ **Gagal menginisialisasi aplikasi**\n\nSilakan hubungi administrator atau restart aplikasi."
)
ERROR_BCRYPT_NOT_AVAILABLE: Final[str] = "bcrypt not available"
ERROR_LOGGING_SETUP_FAILED: Final[str] = "Logging setup failed: {error}"

# Logging status messages
LOG_DEBUG_ENABLED: Final[str] = "Debug logging enabled (console output via Loguru)"
LOG_PRODUCTION_ENABLED: Final[str] = (
    "Production logging enabled (file output via Loguru)"
)
LOG_SETUP_COMPLETE: Final[str] = (
    "Centralized logging setup complete - all logs route through Loguru"
)
LOG_ALREADY_INITIALIZED: Final[str] = (
    "Logging already initialized this session - skipping"
)
LOG_STARTING_INITIALIZATION: Final[str] = "Starting logging initialization..."

# =============================================================================
# ✅ SUCCESS MESSAGES
# =============================================================================

# Authentication success
SUCCESS_LOGIN: Final[str] = "✅ Login successful!"
SUCCESS_LOGOUT: Final[str] = "👋 Logged out successfully"
SUCCESS_PASSWORD_CHANGED: Final[str] = "✅ Password updated successfully!"

# Session management
WARNING_SESSION_EXPIRED: Final[str] = (
    "⏰ Sesi telah berakhir setelah 8 jam. Silakan login kembali."
)

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

# Role display text (short form for UI)
ROLE_ADMIN_SHORT: Final[str] = "Admin"
ROLE_USER_SHORT: Final[str] = "User"

# User interface icons
ICON_ADMIN_FANCY: Final[str] = "😎"
ICON_USER_FANCY: Final[str] = "🤓"
ICON_ADMIN_SIMPLE: Final[str] = "😎"
ICON_USER_SIMPLE: Final[str] = "👤"

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

# =============================================================================
# 📄 PAGE-SPECIFIC MESSAGES
# =============================================================================

# Authentication page
AUTH_WELCOME_TITLE: Final[str] = "Welcome"
AUTH_LOGIN_SUCCESS: Final[str] = "✅ Login successful! Redirecting to dashboard..."
AUTH_LOGIN_REDIRECT_INFO: Final[str] = (
    "If you're not redirected automatically, please refresh the page."
)
AUTH_SIGNING_IN: Final[str] = "🔐 Signing in..."
AUTH_PLEASE_WAIT: Final[str] = "Please wait while we log you in..."
AUTH_ENTER_CREDENTIALS: Final[str] = "Please enter both username and password"
AUTH_WELCOME_USER: Final[str] = "Welcome, {nama}!"
AUTH_LOGIN_ERROR: Final[str] = (
    "❌ Gagal masuk. Silakan coba lagi atau hubungi administrator."
)

# System settings page
SYS_HEADER_SYSTEM_SETTINGS: Final[str] = "⚙️ System Settings"
SYS_HEADER_DATABASE_SETTINGS: Final[str] = "🏠 Database Settings"
SYS_HEADER_USER_SYSTEM_SETTINGS: Final[str] = "👥 User System Settings"
SYS_HEADER_APPLICATION_SETTINGS: Final[str] = "📝 Application Settings"
SYS_HEADER_MAINTENANCE: Final[str] = "🔧 System Maintenance"
SYS_HEADER_DANGER_ZONE: Final[str] = "⚠️ Danger Zone"

# Database status messages
SYS_DB_STATUS_CONNECTION: Final[str] = "✅ Connection: Active"
SYS_DB_STATUS_TABLES: Final[str] = "✅ Tables: Initialized"
SYS_DB_STATUS_MIGRATIONS: Final[str] = "✅ Migrations: Up to date"
SYS_DB_TEST_SUCCESS: Final[str] = "Database connection test successful!"
SYS_DB_STATS_COMING_SOON: Final[str] = "Coming soon - database statistics"

# System info messages
SYS_INFO_RUNNING_NORMAL: Final[str] = "System running normally"
SYS_INFO_CURRENT_ADMIN: Final[str] = "Current Admin:"
SYS_INFO_SYSTEM_VERSION: Final[str] = "System Version:"
SYS_INFO_DATABASE_TYPE: Final[str] = "Database:"

# Coming soon messages
SYS_COMING_SOON_BACKUP: Final[str] = "Backup functionality coming soon"
SYS_COMING_SOON_RESTORE: Final[str] = "Restore functionality coming soon"
SYS_COMING_SOON_LOGS: Final[str] = "Log viewer coming soon"
SYS_COMING_SOON_PERFORMANCE: Final[str] = "Performance monitoring coming soon"
SYS_COMING_SOON_GENERAL: Final[str] = "Coming soon"

# Settings captions
SYS_CAPTION_PASSWORD_LENGTH: Final[str] = "Currently fixed at 6 characters"
SYS_CAPTION_SPECIAL_CHARS: Final[str] = "Coming soon"
SYS_CAPTION_SESSION_TIMEOUT: Final[str] = "Coming soon"
SYS_CAPTION_AUTO_LOGOUT: Final[str] = "Currently enabled by default"
SYS_CAPTION_APP_TITLE: Final[str] = "Coming soon"
SYS_CAPTION_THEME: Final[str] = "Coming soon"
SYS_CAPTION_REPORTS: Final[str] = "Coming soon"
SYS_CAPTION_EXPORTS: Final[str] = "Coming soon"
SYS_CAPTION_CLEAR_SESSIONS: Final[str] = "Coming soon"
SYS_CAPTION_RESET_DB: Final[str] = "Coming soon - requires confirmation"

# Danger zone messages
SYS_DANGER_WARNING: Final[str] = (
    "These operations cannot be undone. Proceed with extreme caution."
)
SYS_DANGER_CLEAR_SESSIONS: Final[str] = "This would log out all users"
SYS_DANGER_RESET_DATABASE: Final[str] = "This would delete all data"

# User management page
USER_MGMT_HEADER: Final[str] = "👥 User Management"
USER_MGMT_CREATE_HEADER: Final[str] = "➕ Create New User"
USER_MGMT_EXISTING_HEADER: Final[str] = "👥 Existing Users"
USER_MGMT_ACTIVITY_HEADER: Final[str] = "📊 User Activity Logs"

USER_MGMT_CREATE_EXPAND: Final[str] = "Create New User Account"
USER_MGMT_NO_USERS: Final[str] = "No users found in the system."
USER_MGMT_RESET_PASSWORD_FOR: Final[str] = "🔄 Reset Password for {nama}"

# User management form labels
USER_MGMT_FULL_NAME: Final[str] = "Full Name"
USER_MGMT_USERNAME: Final[str] = "Username"
USER_MGMT_EMAIL: Final[str] = "Email"
USER_MGMT_INITIAL_PASSWORD: Final[str] = "Initial Password"
USER_MGMT_GRANT_ADMIN: Final[str] = "Grant Administrator Privileges"
USER_MGMT_NEW_TEMP_PASSWORD: Final[str] = "New temporary password"

# User management placeholders
USER_MGMT_PLACEHOLDER_NAME: Final[str] = "Enter full name"
USER_MGMT_PLACEHOLDER_USERNAME: Final[str] = "Enter username"
USER_MGMT_PLACEHOLDER_EMAIL: Final[str] = "Enter email address"
USER_MGMT_PLACEHOLDER_PASSWORD: Final[str] = "Set initial password"
USER_MGMT_PLACEHOLDER_TEMP_PASSWORD: Final[str] = (
    "Enter new password (min 6 characters)"
)

# User management success messages
USER_MGMT_LOGIN_INFO: Final[str] = "ℹ️ The user can now log in with their credentials"

# User management activity info
USER_MGMT_ACTIVITY_INFO: Final[str] = """**Activity Logging**

Coming soon - user login/logout history, password changes, and administrative actions."""
USER_MGMT_ACTIVITY_RECENT: Final[str] = "Recent Activity:"
USER_MGMT_ACTIVITY_AUTH: Final[str] = "- User authentication events"
USER_MGMT_ACTIVITY_PASSWORD: Final[str] = "- Password change requests"
USER_MGMT_ACTIVITY_ADMIN: Final[str] = "- Administrative actions"
USER_MGMT_ACTIVITY_STATUS: Final[str] = "- Account status changes"

# User status labels
USER_STATUS_YOU: Final[str] = "(You)"
