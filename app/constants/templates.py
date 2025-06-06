class Templates:
    """
    Class to store all templates
    """
    
    summary_template = (
        "Gives the information about the person {information}. From this, I want you to create:"
        "1. A short summary"
        "2. Some interesting facts about them"
    )

    summarise_content = (
        "Summarize the following Wikipedia content in a clear and concise manner for a general audience:\n\n"
        "{content}"
    )
