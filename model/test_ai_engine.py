from model.ai_engine import solve_ticket

test_cases = [

    # Printer Tests
    "Printer login issue",
    "Printer Login issue",
    "Printer not working",
    "Install printer",

    # Software Error
    "Getting unexpected error in dashboard",
    "Software crash",
    "Application not responding",

    # Account Issues
    "User account locked",
    "Unable to login",
    "Password reset required",

    # Database
    "Bring database to latest version",
    "Database version outdated",
    "Upgrade PostgreSQL",

    # Negative Cases
    "What is the weather today",
    "Random text testing model",
    "hello how are you",

    # Short Queries
    "install",
    "vpn",
    "error",

    # Installation
    "Install Docker on development machine",
    "Request installation of Visual Studio Code",

    # Outlook
    "Unable to launch Outlook",

    # Long Query
    "I am currently experiencing an issue where the PostgreSQL database is running on an older version and we need to upgrade to the latest version",

    # Typo Tests
    "softwere crash",
    "softwere crush",

    # New Domain
    "Kubernetes pod crashing",

]


print("\n================ TEST RESULTS ================\n")

for i, ticket in enumerate(test_cases, 1):

    print(f"\n---------------- Test {i} ----------------")
    print(f"Ticket: {ticket}")

    result = solve_ticket(ticket)

    print("Result:")
    print(result)

print("\n============== TEST COMPLETE ==============\n")