import os, sys, time, json, threading
from operagxdriver import start_opera_driver
from selenium.webdriver.common.by import By
from win32com.shell import shell, shellcon
from colorama import init, Fore

init(autoreset=True)  # Initialize colorama for colored output


def print_debug(symbol_type_and_colour: int, message, thread_id):
    colour = Fore.RESET  # Initialize colour to a default value
    symbol = "!!"  # Default value for symbol

    if symbol_type_and_colour == 1:
        symbol = "+"
        colour = Fore.GREEN
    elif symbol_type_and_colour == 2:
        symbol = "/"
        colour = Fore.YELLOW
    elif symbol_type_and_colour == 3:
        symbol = "!"
        colour = Fore.RED

    print(
        f"[{colour}{symbol}{Fore.RESET}] {colour}{message}{Fore.RESET} | {Fore.CYAN}(TID: {thread_id}){Fore.RESET}"
    )


def load_config():
    config_path = "config.json"
    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            return json.load(file)


def find_opera_gx_directory():
    app_data_local = shell.SHGetFolderPath(0, shellcon.CSIDL_LOCAL_APPDATA, None, 0)
    default_opera_gx_path = os.path.join(app_data_local, "Programs", "Opera GX")
    default_opera_exe_path = os.path.join(default_opera_gx_path, "opera.exe")

    if os.path.exists(default_opera_exe_path):
        print_debug(1, f"Found Opera GX path: {default_opera_exe_path}", thread_id=None)
        config = load_config() or {"opera_browser_exe": "", "opera_driver_exe": ""}

        if not config["opera_browser_exe"]:
            config["opera_browser_exe"] = default_opera_exe_path
            with open("config.json", "w") as file:
                json.dump(config, file, indent=4)

            print(
                "Default Opera GX path saved to config.json. Please restart the script."
            )
            sys.exit()

        return True

    print_debug(3, "Opera GX path not found", thread_id=None)
    return False


def process_thread(thread_id):
    config = load_config()

    if not config["opera_browser_exe"] and not config["opera_driver_exe"]:
        default_opera_path = find_opera_gx_directory()
        custom_browser_path = input(f"Enter the path to Opera browser executable: ")
        custom_driver_path = input("Enter the path to Opera WebDriver executable: ")

        config["opera_browser_exe"] = custom_browser_path or default_opera_path
        config["opera_driver_exe"] = custom_driver_path

    elif not config["opera_browser_exe"]:
        default_opera_path = find_opera_gx_directory()
        custom_browser_path = input(f"Enter the path to Opera browser executable: ")
        config["opera_browser_exe"] = custom_browser_path or config["opera_browser_exe"]

        with open("config.json", "w") as file:
            json.dump(config, file, indent=4)

    elif not config["opera_driver_exe"]:
        custom_driver_path = input("Enter the path to Opera WebDriver executable: ")
        config["opera_driver_exe"] = custom_driver_path

    with open("config.json", "w") as file:
        json.dump(config, file, indent=4)

    opera_driver_exe = config["opera_driver_exe"]
    opera_browser_exe = config["opera_browser_exe"]

    driver = None

    try:
        driver = start_opera_driver(
            opera_browser_exe=opera_browser_exe,
            opera_driver_exe=opera_driver_exe,
            arguments=(
                "--no-sandbox",
                "--test-type",
                "--no-default-browser-check",
                "--no-first-run",
                "--incognito",
                "--start-maximized",
                # "--headless",
            ),
        )

        initial_url = "https://www.opera.com/gx/discord-nitro"
        driver.get(initial_url)
        print_debug(2, f"Opening: {initial_url}", thread_id)

        time.sleep(3)
        driver.execute_script("document.getElementById('claim-button').click()")
        print_debug(2, "Clicking claim button", thread_id)
        time.sleep(3)

        time.sleep(5)

        for tab_index, tab_handle in enumerate(driver.window_handles):
            driver.switch_to.window(tab_handle)
            current_tab_url = driver.current_url

            if "discord.com" in current_tab_url:
                print_debug(1, f"Received URL: {current_tab_url}", thread_id)

                with open("output.txt", "a") as file:
                    file.write(current_tab_url + "\n\n")
                    print_debug(2, "Writing to output.txt", thread_id)
                break

    except Exception as e:
        print_debug(3, f"Thread {thread_id} - Error: {e}", Fore.RED, thread_id)

    finally:
        if driver:
            try:
                driver.quit()
                time.sleep(5)
                print_debug(1, "Successfully saved URL, closing...", thread_id)
            except Exception as close_error:
                print_debug(
                    3,
                    f"Thread {thread_id} - Error closing driver: {close_error}",
                    Fore.RED,
                    thread_id,
                )


def main():
    try:
        num_threads = int(
            input("Enter the number of threads to open (default is 1): ") or 1
        )

        while True:
            threads = []
            for i in range(num_threads):
                thread = threading.Thread(
                    target=process_thread, args=(i + 1,), daemon=True
                )
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

    except KeyboardInterrupt:
        print("Script terminated by the user.")


if __name__ == "__main__":
    main()
