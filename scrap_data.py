import json
import time

import requests
import tqdm
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from database import connect_to_database


def scrap_ton_contracts():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        data_list = []

        # Navigate to the page
        page.goto("https://ton.app/jettons")

        # Scroll to the bottom of the page to load all content
        previous_height = 0
        while True:
            # Scroll to the bottom
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            # Wait for new content to load
            page.wait_for_timeout(1000)  # Adjust timeout if needed

            # Check if scrolling is complete
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == previous_height:
                break
            previous_height = new_height

        # Extract all hrefs starting with "https://ton.app/jettons/"
        links = page.query_selector_all("div a[href^='/jettons/']")
        for link in links:
            href = link.get_attribute("href")
            if href:
                data_list.append(href)

        # Save the scraped links into a JSON file
        with open("jettons_links.json", "w", encoding="utf-8") as json_file:
            json.dump(data_list, json_file, ensure_ascii=False, indent=4)

        # Print or return the scraped links
        print(f"Total links scraped: {len(data_list)}")

        # Close the browser
        browser.close()

    return data_list


def jettons_contract(file_path):
    # Load the JSON file
    with open(file_path, "r", encoding="utf-8") as json_file:
        links = json.load(json_file)

    # Prepare the API base URL
    base_url = "https://tonapi.io/v2/jettons/"

    # List to store extracted data
    extracted_data = []

    # Iterate through each link with a loading bar
    for link in tqdm.tqdm(links, desc="Processing jettons"):
        # Extract the end part of the URL (e.g., "/jettons/{token}")
        end_url = link.replace("https://ton.app", "")

        # Construct the full API URL
        url = f"{base_url}{end_url}"

        # Make the API request
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error if the request fails
            data = response.json()  # Parse the JSON response
            # Extract the required fields
            contract_address = end_url
            symbol = data["metadata"]["symbol"]
            decimal = data["metadata"]["decimals"]

            # Add the extracted data to the list
            extracted_data.append(
                {
                    "contract_address": contract_address,
                    "symbol": symbol,
                    "decimal": decimal,
                }
            )

        except requests.exceptions.RequestException as e:
            print(f"Error with {link}: {e}")

        # Rate limit: 1 API call per second
        time.sleep(1)

    # Save the extracted data to a JSON file
    with open("jettons_data.json", "w", encoding="utf-8") as output_file:
        json.dump(extracted_data, output_file, ensure_ascii=False, indent=4)

    print(f"Data saved to jettons_data.json")


def jettons_contract_to_db(file_path):
    # Load the JSON file
    with open(file_path, "r", encoding="utf-8") as json_file:
        jettons_data = json.load(json_file)

    supabase = connect_to_database()

    # Iterate through each token with a progress bar
    for token in tqdm.tqdm(jettons_data, desc="Inserting into database"):
        # Extract token details
        contract_address = token.get("token_address")
        print(contract_address)
        symbol = token.get("token_symbol")
        print(symbol)
        decimal = token.get("decimal")

        # Insert into Supabase
        try:
            # Check if the contract_address already exists
            existing_contracts = (
                supabase.table("Contracts")
                .select("contract_address")
                .eq("contract_address", contract_address)
                .execute()
            )

            if existing_contracts.data:
                print(
                    f"{symbol} {contract_address} already exists in the table. Skipping."
                )
                continue  # Skip this entry if it already exists

            data = (
                supabase.table("Contracts")
                .insert(
                    {
                        "blockchain": "SOL",
                        "contract_address": contract_address,
                        "token_symbol": symbol,
                        "decimal": decimal,
                    }
                )
                .execute()
            )
            print(f"{symbol} {contract_address} added to the table.")

        except Exception as e:
            print("An error occurred:", e)
            return None  # Return None in case of any errors

        except Exception as e:
            print(f"Error inserting {contract_address}: {e}")

        # Rate limit: 1 insertion per second
        time.sleep(0.1)


def scrape_bsc_contracts():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        data_list = []

        # Iterate over pages
        for page_number in range(1, 27):  # Assuming you want to scrape 5 pages
            page.goto(f"https://etherscan.com/tokens/?p={page_number}")

            # Wait for the content to load
            page.wait_for_selector("tr")

            # Extracting tr elements
            tr_elements = page.query_selector_all("tr")

            # Extracting data from each tr element
            for tr_element in tr_elements:
                # Extracting data from the tr element
                td_elements = tr_element.query_selector_all("td")
                if len(td_elements) >= 7:  # Ensure there are enough td elements
                    href = td_elements[1].query_selector("a").get_attribute("href")
                    token_name = td_elements[1].query_selector(".hash-tag").inner_text()
                    token_symbol = (
                        td_elements[1]
                        .query_selector("span")
                        .inner_text()
                        .replace("(", "")
                        .replace(")", "")
                    )
                    # Extracting token ID from href
                    token_address = href.split("/token/")[-1]

                    # Adding data to the list
                    data_list.append(
                        {
                            "contract_address": token_address,
                            "token_name": token_name,
                            "token_symbol": token_symbol,
                        }
                    )

    # Save the data to a JSON file
    with open("eth_contracts.json", "w") as json_file:
        json.dump(data_list, json_file)

    return data_list


def scrape_bsc():
    with open("eth_contracts_organized.json", "r") as json_file:
        data_dict = json.load(json_file)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        supabase = connect_to_database()
        progress_bar = tqdm.tqdm(total=len(data_dict), desc="Processing to the table")
        for contract_address, item in data_dict.items():
            # Check if the contract address already exists in the database for the blockchain
            existing_contract = (
                supabase.table("Contracts")
                .select("contract_address")
                .eq("blockchain", "ETH")
                .eq("contract_address", contract_address)
                .execute()
            )

            if existing_contract and len(existing_contract.data) > 0:
                print(
                    f"Contract address {contract_address} already exists in the database for BSC blockchain. Skipping..."
                )
                progress_bar.update(1)
                continue  # Skip to the next iteration

            # Navigate to the specific address for each item
            page.goto(f"https://etherscan.com/token/{contract_address}")

            # Wait for the content to load
            # You may need to adjust the selector and wait condition based on your specific page
            page.wait_for_selector("h4.text-cap.mb-1 b")

            # Extract the decimal value
            decimal_value = page.query_selector("h4.text-cap.mb-1 b").inner_text()

            # Extract the text from the span with class "text-muted"
            token_symbol = (
                page.query_selector("span.fs-base.fw-medium .text-muted")
                .inner_text()
                .replace("(", "")
                .replace(")", "")
            )

            try:
                data = (
                    supabase.table("Contracts")
                    .insert(
                        {
                            "blockchain": "ETH",
                            "contract_address": contract_address,
                            "token_symbol": token_symbol,
                            "decimal": decimal_value,
                        }
                    )
                    .execute()
                )
                progress_bar.update(1)
                print(f"{contract_address} added to the table.")

            except Exception as e:
                print("An error occurred:", e)
                return None  # Return None in case of any errors

            time.sleep(1.3)

    browser.close()


def scrape_tokens():
    token_data = {}
    url = "https://thetascan.io/tokens/"

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all div elements with the specified style for token names
        token_name_divs = soup.find_all(
            "div",
            style=[
                "width: 100px; float:left; padding: 9px 5px; white-space: nowrap;overflow: hidden;"
            ],
        )
        for div in token_name_divs:
            token_name = div.text.strip()
            if token_name not in token_data:
                token_data[token_name] = None

        # Find all div elements with the specified style for token addresses
        token_address_divs = soup.find_all(
            "div",
            style=["width: 380px; float:left; padding: 9px 5px;"],
        )
        for index, div in enumerate(token_address_divs):
            token_address = div.text.strip()
            token_name = token_name_divs[index].text.strip()
            if token_name in token_data:
                token_data[token_name] = token_address

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

        # Write data to JSON file
    with open("theta_contracts.json", "w") as json_file:
        json.dump(token_data, json_file)

    return token_data


def scrape_bsc_single_contract():
    with sync_playwright() as p:
        contract_address: str = 0x58538E6A46E07434D7E7375BC268D3CB839C0133
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(
            f"https://bscscan.com/token/0x58538E6A46E07434D7E7375BC268D3CB839C0133"
        )
        content = page.content()

        # Extracting values using JavaScript evaluation
        net = page.evaluate("() => window.net")
        litAssetType = page.evaluate("() => window.litAssetType")
        litAssetAddress = page.evaluate("() => window.litAssetAddress")
        litAssetSymbol = page.evaluate("() => window.litAssetSymbol")
        litAssetDecimal = page.evaluate("() => window.litAssetDecimal")

        time.sleep(0.5)
        browser.close()

        # Printing extracted values
        print("Network:", net)
        print("Asset Type:", litAssetType)
        print("Asset Address:", litAssetAddress)
        print("Asset Symbol:", litAssetSymbol)
        print("Asset Decimal:", litAssetDecimal)


def add_theta_contracts_to_db():

    supabase = connect_to_database()
    token_data = scrape_tokens()

    contract_addresses = [
        address for address in token_data.values() if address is not None
    ]

    # Initialize tqdm progress bar
    progress_bar = tqdm.tqdm(
        total=len(contract_addresses), desc="Processing to the table"
    )

    for contract_address in contract_addresses:
        url = f"https://www.thetascan.io/api/contract/?contract={contract_address}"
        try:
            # Send a GET request to the URL
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                data = response.json()

                symbol = data["symbol"]
                decimal = data["decimal"]

                try:
                    data = (
                        supabase.table("Contracts")
                        .insert(
                            {
                                "blockchain": "THETA",
                                "contract_address": contract_address,
                                "token_symbol": symbol,
                                "decimal": decimal,
                            }
                        )
                        .execute()
                    )
                    progress_bar.update(1)

                except Exception as e:
                    print("An error occurred:", e)
                    return None  # Return None in case of any errors

            else:
                print(f"Failed to retrieve data. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


def organize_json(json_file_path):
    # Read data from the input JSON file
    with open(json_file_path, "r") as json_file:
        data_list = json.load(json_file)

    # Organize data into a dictionary
    organized_data = {}
    for data in data_list:
        token_address = data["contract_address"]
        if token_address not in organized_data:
            organized_data[token_address] = {
                "token_name": data["token_name"],
                "token_symbol": data["token_symbol"],
            }

    # Write organized data to a new JSON file
    output_json_file_path = json_file_path.replace(".json", "_organized.json")
    with open(output_json_file_path, "w") as output_json_file:
        json.dump(organized_data, output_json_file, indent=4)

    return organized_data, len(organized_data)


def scrape_sol_contracts():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        data_list = []

        # Iterate over pages
        for page_number in range(1, 20):  # Assuming you want to scrape 5 pages
            page.goto(f"https://solscan.io/leaderboard/token?page={page_number}")

            # Wait for the specific <td> element to load
            page.wait_for_selector(
                "td.h-12.px-2.py-\\[10px\\].align-middle.text-\\[14px\\].leading-\\[24px\\].font-normal.text-neutral7.\\[\\&\\:has\\(\\[role\\=checkbox\\]\\)\\]\\:pr-0.border-b.first\\:pl-4.last\\:pr-4 a"
            )

            # Extract all hrefs from <a> tags inside <td> with the specified class
            links = page.query_selector_all(
                "td.h-12.px-2.py-\\[10px\\].align-middle.text-\\[14px\\].leading-\\[24px\\].font-normal.text-neutral7.\\[\\&\\:has\\(\\[role\\=checkbox\\]\\)\\]\\:pr-0.border-b.first\\:pl-4.last\\:pr-4 a"
            )
            print(links)
            for link in links:
                href = link.get_attribute("href")
                if href:
                    data_list.append(href)

        # Save the scraped links into a JSON file
        with open("tokens_links.json", "w", encoding="utf-8") as json_file:
            json.dump(data_list, json_file, ensure_ascii=False, indent=4)

        # Print or return the scraped links
        print(f"Total links scraped: {len(data_list)}")

        # Close the browser
        browser.close()

    return data_list


def extract_token_info(token_address):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the token page
        page.goto(f"https://solscan.io/token/{token_address}")

        # Wait for the page to load fully
        page.wait_for_load_state("networkidle")

        # Extract the token name and symbol
        token_name_element = page.query_selector(
            "div.not-italic.font-normal.text-neutral7.text-\\[14px\\].leading-\\[24px\\].autoTruncate.block"
        )
        if token_name_element:
            token_name = token_name_element.inner_text().strip()
            # Extract the symbol from parentheses
            if "(" in token_name and ")" in token_name:
                token_symbol = token_name.split("(")[1].split(")")[0]
            else:
                token_symbol = None
        else:
            token_name = None
            token_symbol = None

        # Extract the decimal
        decimal_element = page.query_selector("div:has-text('Decimals') + div")
        if decimal_element:
            decimal = decimal_element.inner_text().strip()
        else:
            decimal = None

        # Close the browser
        browser.close()

        return {
            "token_address": token_address,
            "token_symbol": token_symbol,
            "decimal": decimal,
        }


def main():
    # # Load token addresses from the JSON file
    # with open("tokens_links.json", "r", encoding="utf-8") as json_file:
    #     token_addresses = json.load(json_file)

    # # Scrape token info for each address
    # all_token_info = []
    # for token_address in tqdm.tqdm(
    #     token_addresses, desc="Scraping tokens", unit="token"
    # ):
    #     print(f"Scraping data for token: {token_address}")
    #     try:
    #         token_info = extract_token_info(token_address)
    #         all_token_info.append(token_info)
    #         print(f"Scraped data: {token_info}")
    #     except Exception as e:
    #         print(f"Failed to scrape data for token {token_address}: {e}")

    # # Save all token info to a new JSON file
    # with open("all_token_info.json", "w", encoding="utf-8") as json_file:
    #     json.dump(all_token_info, json_file, ensure_ascii=False, indent=4)

    # print("Scraping completed. Data saved to all_token_info.json.")
    # jettons_contract_to_db("all_token_info.json")
    print("scrapping")
    scrape_bsc_single_contract()


if __name__ == "__main__":
    main()
