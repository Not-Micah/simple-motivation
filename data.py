def read_quotes():
    quotes = []
    with open("saved.txt", "r") as f:
        for line in f:
            quote, author = line.strip().rsplit('" ', 1)
            quotes.append([quote.strip('"'), author.strip()])
    return quotes

def write_quote(quote, author):
    with open("saved.txt", "a") as f:
        f.write(f'"{quote}" {author}\n')

def read_theme():
    with open('theme.txt', 'r') as f:
        theme = f.read().strip()
    return theme

def write_theme(theme):
    with open('theme.txt', 'w') as f:
        f.write(theme)

# quotes_list = read_quotes()
# print("Quotes from the file:")
# print(quotes_list)

# # Adding a new quote
# new_quote = "The only way to do great work is to love what you do."
# new_author = "Steve Jobs"
# write_quote(new_quote, new_author)
