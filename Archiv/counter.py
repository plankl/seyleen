import csv

def count_dishes(csv_file):
    dish_counts = {}
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                vorspeisen = row['Vorspeisen'].split(', ')
                hauptspeisen = row['Hauptspeisen'].split(', ')
                nachspeisen = row['Nachspeisen'].split(', ')
            except KeyError:
                continue
            for dish in vorspeisen + hauptspeisen + nachspeisen:
                if dish:
                    dish_counts[dish] = dish_counts.get(dish, 0) + 1
    return dish_counts

def write_dish_counts_to_txt(dish_counts, txt_file):
    with open(txt_file, 'w', encoding='utf-8') as txtfile:
        for dish, count in dish_counts.items():
            txtfile.write(f"{dish}: {count}\n")

def main():
    csv_file = 'survey_results.csv'
    txt_file = 'dish_counts.txt'
    dish_counts = count_dishes(csv_file)
    write_dish_counts_to_txt(dish_counts, txt_file)

if __name__ == "__main__":
    main()
