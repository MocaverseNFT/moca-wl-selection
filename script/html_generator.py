from jinja2 import Environment, FileSystemLoader
import os

'''
This script generates an summary.html file that lists all the details of a WL selection.
Then it generates an index.html file that lists all the summary pages
in the summaries directory.

The resulting index.html file contains a list of links to each summary page.
'''


def generate_html(wl_name, wallets, max_wins_per_wallet, num_winners, seed_phrase, winners, timestamp):
    # Load the HTML template
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template_summary.html")
    template_index = env.get_template("template_index.html")

    # Render the template with the selection data
    html1 = template.render(
        wl_name=wl_name,
        wallets=wallets,
        max_wins_per_wallet=max_wins_per_wallet,
        #stake_at_week=stake_at_week,
        num_winners=num_winners,
        seed_phrase=seed_phrase,
        winners=winners,
        timestamp=timestamp
    )

    # Define HTML file name
    summary_filename = wl_name+"_winner_summary"

    # Write the HTML file to folder
    with open(f"../docs/summaries/{summary_filename}.html", "w") as f:
        f.write(html1)

    
    path = "../docs/summaries"

    # Get a list of all files in the summaries directory with a .html extension
    html_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith(".html")]

    # Extract the base filename without the extension from each file
    summary_filenames = [os.path.splitext(f)[0] for f in html_files]

    # Render the template with the dynamic data
    html = template_index.render(
    timestamp=timestamp, summary_filenames=summary_filenames)

    # Write the HTML file to disk
    with open("../docs/index.html", "w") as f:
             f.write(html)

    # # Check if the HTML files were created successfully
    # if not os.path.isfile("../docs/summaries/"+summary_filename+".html") or not os.path.isfile("../docs/"+"index.html"):
    #     print("Error: HTML files not created.")
