def run():
    """
    Example two-day task that saves output to the data folder.
    """
    import datetime
    import os

    data_dir = os.path.dirname(os.path.dirname(__file__))
    output_file = os.path.join(data_dir, "two_day_output.txt")

    with open(output_file, "w") as f:
        f.write(f"Two-day task ran at {datetime.datetime.now()}\n")
        f.write("Processed some data...\n")

    print("Two-day task completed.")