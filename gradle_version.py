import os
import requests

def main():
    # Figure out which Gradle version to upgrade.
    # See https://developer.github.com/v3/repos/releases/#get-the-latest-release.
    response = requests.get("https://api.github.com/repos/gradle/gradle/releases/latest")
    json = response.json()
    latestGradleVersion = json["name"]
    print("Latest Gradle version: " + latestGradleVersion)

# ---------- main -------------
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)