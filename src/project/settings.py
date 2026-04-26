"""
AUTHOR: Rohan Joseph
PURPOSE: Repository-wide settings, schema definitions, and taxonomy templates.
DATE CREATED: 2026-04-25
DATE MODIFIED: 2026-04-25
MODIFIED BY: Rohan Joseph
"""



"""
Settings
"""

DEFAULT_MAX_IOS_ROWS = 1000
DEFAULT_MAX_ANDROID_ROWS = 1000
UNMAPPED_COMMON_LABEL = "UNMAPPED"

IOS_BASE_COLUMNS = [
    "app_id",
    "Platform",
    "App_Name",
    "Seller",
    "Category",
    "Price",
    "Languages",
    "App_Information",
    "Version_History",
    "Privacy_Labels",
    "URL",
]

IOS_STATUS_COLUMNS = [
    "NoDetailsProvided",
    "DataNotCollected",
]

ANDROID_BASE_COLUMNS = [
    "app_id",
    "Platform",
    "App_Name",
    "Seller",
    "Safety_Forms",
    "URL",
]

ANDROID_STATUS_COLUMNS = [
    "Nodatacollected",
    "Nodatasharedwiththirdparties",
]

IOS_PRIVACY_LABELS_TEMPLATE = {
    "Data Used to Track You": {},
    "Data Linked to You": {
        "App Functionality": {},
        "Third-Party Advertising": {},
        "Developer's Advertising or Marketing": {},
        "Product Personalization": {},
        "Analytics": {},
        "Other Purposes": {},
    },
    "Data Not Linked to You": {
        "App Functionality": {},
        "Third-Party Advertising": {},
        "Developer's Advertising or Marketing": {},
        "Product Personalization": {},
        "Analytics": {},
        "Other Purposes": {},
    },
}

IOS_DATA_TYPES = [
    "Identifiers",
    "Contact Info",
    "Location",
    "Contacts",
    "Browsing History",
    "Search History",
    "User Content",
    "Purchases",
    "Financial Info",
    "Sensitive Info",
    "Health & Fitness",
    "Diagnostics",
    "Usage Data",
    "Other Data",
]

IOS_DATA_ITEMS = {
    "Identifiers": ["User ID", "Device ID"],
    "Contact Info": ["Name", "Phone Number", "Email Address", "Physical Address", "Other User Contact Info"],
    "Location": ["Coarse Location", "Precise Location"],
    "Contacts": ["Contacts"],
    "Browsing History": ["Browsing History"],
    "Search History": ["Search History"],
    "User Content": [
        "Audio Data",
        "Emails or Text Messages",
        "Photos or Videos",
        "Gameplay Content",
        "Customer Support",
        "Other User Content",
    ],
    "Purchases": ["Purchases"],
    "Financial Info": ["Payment Info", "Credit Info", "Other Financial Info"],
    "Sensitive Info": ["Sensitive Info"],
    "Health & Fitness": ["Health", "Fitness"],
    "Diagnostics": ["Crash Data", "Performance Data", "Other Diagnostic Data"],
    "Usage Data": ["Advertising Data", "Product Interaction", "Other Usage Data"],
    "Other Data": ["Other Data Types"],
}

ANDROID_SAFETY_FORMS_TEMPLATE = {
    "Data shared": {},
    "Data collected": {},
    "Security practices": [
        "Data is encrypted in transit",
        "Data isn't encrypted",
        "You can request that data be deleted",
        "Data can't be deleted",
        "Independent security review",
        "Committed to follow the Play Families Policy",
    ],
}

ANDROID_DATA_CATEGORIES = [
    "Location",
    "Personal info",
    "Financial info",
    "Health and fitness",
    "Messages",
    "Photos and videos",
    "Audio files",
    "Files and docs",
    "Calendar",
    "Contacts",
    "App activity",
    "Web browsing",
    "App info and performance",
    "Device or other IDs",
]

ANDROID_DATA_TYPES = {
    "Location": {
        "Approximate location": {},
        "Precise location": {},
    },
    "Personal info": {
        "Name": {},
        "Email address": {},
        "User IDs": {},
        "Address": {},
        "Phone number": {},
        "Race and ethnicity": {},
        "Political or religious beliefs": {},
        "Sexual orientation": {},
        "Other info": {},
    },
    "Financial info": {
        "User payment info": {},
        "Purchase history": {},
        "Credit score": {},
        "Other financial info": {},
    },
    "Health and fitness": {
        "Health info": {},
        "Fitness info": {},
    },
    "Messages": {
        "Emails": {},
        "SMS or MMS": {},
        "Other in-app messages": {},
    },
    "Photos and videos": {
        "Photos": {},
        "Videos": {},
    },
    "Audio files": {
        "Voice or sound recordings": {},
        "Music files": {},
        "Other audio files": {},
    },
    "Files and docs": {
        "Files and docs": {},
    },
    "Calendar": {
        "Calendar": {},
    },
    "Contacts": {
        "Contacts": {},
    },
    "App activity": {
        "App interactions": {},
        "In-app search history": {},
        "Installed apps": {},
        "Other user-generated content": {},
        "Other actions": {},
    },
    "Web browsing": {
        "Web browsing history": {},
    },
    "App info and performance": {
        "Crash logs": {},
        "Diagnostics": {},
        "Other app performance data": {},
    },
    "Device or other IDs": {
        "Device or other IDs": {},
    },
}

ANDROID_DATA_PURPOSES = [
    "Account management",
    "Advertising or marketing",
    "App functionality",
    "Analytics",
    "Developer communications",
    "Fraud prevention, security, and compliance",
    "Personalization",
]
